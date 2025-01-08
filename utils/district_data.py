import pandas as pd
import json
from typing import Dict, Any, Tuple, List
from shapely.geometry import Point, Polygon
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
    Load real GeoJSON boundaries for Chattanooga city council districts
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

def find_nearest_polling_place(lat: float, lon: float, df: pd.DataFrame) -> Tuple[str, str, str]:
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
    Determine which district a point falls within using real boundaries
    """
    point = Point(lon, lat)
    district_boundaries = get_district_boundaries()

    for district, geojson in district_boundaries.items():
        coords = geojson["geometry"]["coordinates"][0]
        polygon = Polygon(coords)
        if polygon.contains(point):
            return district

    # If point isn't in any polygon, find nearest district
    min_dist = float('inf')
    nearest_district = None

    for district, geojson in district_boundaries.items():
        coords = geojson["geometry"]["coordinates"][0]
        polygon = Polygon(coords)
        dist = point.distance(polygon)
        if dist < min_dist:
            min_dist = dist
            nearest_district = district

    return nearest_district if nearest_district else "District not found"

def get_district_info(lat: float, lon: float) -> dict:
    """
    Get district information based on coordinates
    """
    # Determine district based on coordinates
    district = get_district_for_coordinates(lat, lon)

    # Get nearest polling place
    df = pd.read_csv('assets/polling_places.csv')
    polling_info = find_nearest_polling_place(lat, lon, df)

    if polling_info:
        precinct, location_name, address = polling_info
        return {
            "district_number": district,
            "precinct": precinct,
            "polling_place": location_name,
            "polling_address": address,
            "distance": "Based on your location" # This could be enhanced with actual distance
        }
    else:
        st.warning("Unable to find the nearest polling place. Please contact the Election Commission for assistance.")
        return {
            "district_number": district,
            "precinct": "Not found",
            "polling_place": "Not found",
            "polling_address": "Not found",
            "distance": "N/A"
        }

def get_council_member(district: str) -> dict:
    """
    Get council member information for a district
    """
    df = pd.read_csv('assets/council_members.csv')
    member = df[df['district'] == district].iloc[0]

    return {
        "name": member['name'],
        "email": member['email'],
        "phone": member['phone']
    }