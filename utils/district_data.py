import pandas as pd
import json
from typing import Dict, Any, Tuple, List, Optional
from shapely.geometry import Point, Polygon, mapping
import math
from pathlib import Path
from utils.geocoding import geocode_address
import streamlit as st

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers
    r = 6371
    return c * r

def get_district_boundaries() -> Dict[str, Any]:
    """
    Load GeoJSON boundaries for Chattanooga city council districts
    """
    try:
        with open(Path('assets') / 'district_boundaries.json') as f:
            geojson = json.load(f)

        districts = {}
        for feature in geojson['features']:
            district = feature['properties']['district']
            districts[district] = {
                "type": "Feature",
                "properties": {
                    "district": district,
                    "description": feature['properties'].get('description', ''),
                    "style": {
                        "fillColor": "#1E88E5",
                        "color": "#1E88E5",
                        "weight": 2,
                        "fillOpacity": 0.3
                    }
                },
                "geometry": feature['geometry']
            }
        return districts
    except FileNotFoundError:
        st.error("District boundaries data not found.")
        return {}
    except json.JSONDecodeError:
        st.error("Error reading district boundaries data.")
        return {}

def point_in_polygon(point: Point, polygon_coords: List[List[float]], buffer_distance: float = 0.0001) -> bool:
    """
    Check if a point is within a polygon with a very small buffer zone for boundary cases
    """
    try:
        polygon = Polygon(polygon_coords)
        # Reduced buffer distance for more precise boundary detection
        buffered_polygon = polygon.buffer(buffer_distance)
        return buffered_polygon.contains(point)
    except Exception as e:
        st.write(f"Notice: Point-in-polygon check: {str(e)}")
        return False

def find_nearest_polling_place(lat: float, lon: float, df: pd.DataFrame) -> Optional[Tuple[str, str, str]]:
    """
    Find the nearest polling place to the given coordinates using haversine distance
    """
    min_dist = float('inf')
    nearest_place = None

    for _, place in df.iterrows():
        try:
            # Get polling place coordinates
            polling_address = f"{place['address']}, {place['city']}, {place['state']} {place['zip']}"
            place_coords = geocode_address(polling_address)

            if place_coords:
                place_lat, place_lon = place_coords
                dist = haversine_distance(lat, lon, place_lat, place_lon)
                if dist < min_dist:
                    min_dist = dist
                    nearest_place = place
                    # Replace st.debug with st.write for development feedback
                    st.write(f"Found polling place: {place['location_name']} ({dist:.2f} km away)")
        except Exception as e:
            st.warning(f"Notice: Error processing polling place {place['location_name']}")
            continue

    if nearest_place is not None:
        return (
            nearest_place['precinct'],
            nearest_place['location_name'],
            f"{nearest_place['address']}, {nearest_place['city']}, {nearest_place['state']} {nearest_place['zip']}"
        )
    return None

def get_district_for_coordinates(lat: float, lon: float) -> str:
    """
    Determine which district a point falls within using GIS boundaries with improved accuracy
    """
    point = Point(lon, lat)  # GeoJSON uses (lon, lat) order
    district_boundaries = get_district_boundaries()
    
    if not district_boundaries:
        st.error("No district boundaries loaded. Please check the data file.")
        return "District not found"

    st.write(f"Debug - Checking coordinates: ({lat}, {lon})")
    
    # Try multiple buffer distances
    buffer_distances = [0.0001, 0.001, 0.002, 0.003]  # Increasing buffer sizes
    
    for buffer_distance in buffer_distances:
        for district, geojson in district_boundaries.items():
            try:
                if 'geometry' not in geojson or 'coordinates' not in geojson['geometry']:
                    st.warning(f"Invalid geometry data for {district}")
                    continue
                    
                coords = geojson["geometry"]["coordinates"][0]
                if point_in_polygon(point, coords, buffer_distance):
                    st.success(f"Found match in {district} with buffer distance {buffer_distance}")
                    return district
            except Exception as e:
                st.write(f"Notice: District check for {district}: {str(e)}")
                continue
    
    # If still not found, check coordinates are within reasonable bounds
    if not (34.9 <= lat <= 35.2 and -85.4 <= lon <= -85.1):
        st.warning("Coordinates appear to be outside the expected Chattanooga area.")
    else:
        st.warning("Location not matched to any district. Please verify the address.")
    
    return "District not found"

def get_district_info(lat: float, lon: float) -> dict:
    """
    Get comprehensive district information based on coordinates
    """
    # Determine district based on coordinates
    district = get_district_for_coordinates(lat, lon)

    if district == "District not found":
        return {
            "district_number": district,
            "precinct": "Not found",
            "polling_place": "Not found",
            "polling_address": "Not found",
            "distance": "N/A",
            "error": "Location outside city limits"
        }

    # Get district boundaries for additional info
    boundaries = get_district_boundaries()
    district_data = boundaries.get(district, {}).get('properties', {})

    # Get nearest polling place
    try:
        df = pd.read_csv('assets/polling_places.csv')
        polling_info = find_nearest_polling_place(lat, lon, df)

        if polling_info:
            precinct, location_name, address = polling_info
            return {
                "district_number": district,
                "district_description": district_data.get('description', ''),
                "precinct": precinct,
                "polling_place": location_name,
                "polling_address": address,
                "distance": "Based on your location"
            }
    except Exception as e:
        st.error(f"Error retrieving polling place information: {str(e)}")

    return {
        "district_number": district,
        "district_description": district_data.get('description', ''),
        "precinct": "Not found",
        "polling_place": "Not found",
        "polling_address": "Not found",
        "distance": "N/A"
    }

def get_council_member(district: str) -> dict:
    """
    Get council member information for a district
    """
    try:
        df = pd.read_csv('assets/council_members.csv')
        member = df[df['district'] == district].iloc[0]

        return {
            "name": member['name'],
            "email": member['email'],
            "phone": member['phone']
        }
    except Exception as e:
        st.error(f"Error retrieving council member information: {str(e)}")
        return {
            "name": "Information unavailable",
            "email": "Please contact the City Council office",
            "phone": "(423) 643-7170"
        }