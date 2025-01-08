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

def point_in_polygon(point: Point, polygon_coords: List[List[float]], buffer_distance: float = 0.001) -> bool:
    """
    Check if a point is within a polygon with a small buffer zone for better accuracy
    """
    try:
        polygon = Polygon(polygon_coords)
        # Add a small buffer around the polygon to handle edge cases
        buffered_polygon = polygon.buffer(buffer_distance)
        return buffered_polygon.contains(point)
    except Exception as e:
        st.debug(f"Error in point_in_polygon check: {str(e)}")
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
                    st.debug(f"Found polling place {place['location_name']} at distance {dist:.2f} km")
            else:
                st.debug(f"Could not geocode address for polling place: {polling_address}")

        except Exception as e:
            st.warning(f"Error processing polling place {place['location_name']}: {str(e)}")
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

    # First, check exact matches with a small buffer
    for district, geojson in district_boundaries.items():
        try:
            coords = geojson["geometry"]["coordinates"][0]
            if point_in_polygon(point, coords):
                st.debug(f"Found exact district match: {district}")
                return district
        except Exception as e:
            st.debug(f"Error checking district {district}: {str(e)}")
            continue

    # If no exact match, find nearest district with distance calculation
    min_dist = float('inf')
    nearest_district = None
    nearest_distance_km = None

    for district, geojson in district_boundaries.items():
        try:
            coords = geojson["geometry"]["coordinates"][0]
            polygon = Polygon(coords)
            dist = point.distance(polygon)
            dist_km = dist * 111  # Rough conversion to kilometers

            if dist_km < min_dist:
                min_dist = dist_km
                nearest_district = district
                nearest_distance_km = dist_km

        except Exception as e:
            st.debug(f"Error calculating distance to district {district}: {str(e)}")
            continue

    # Only return nearest district if it's within reasonable distance (5km)
    if nearest_district and nearest_distance_km <= 5:
        st.info(
            f"Your location appears to be near the boundary of {nearest_district}. "
            "Distance to district boundary: {:.2f} km".format(nearest_distance_km)
        )
        return nearest_district

    st.warning("Your location appears to be outside Chattanooga city limits.")
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