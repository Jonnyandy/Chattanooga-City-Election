import pandas as pd
import json
from typing import Dict, Any, Tuple, List, Optional
from shapely.geometry import Point, Polygon, mapping, shape
import math
from pathlib import Path
from utils.geocoding import geocode_address
import streamlit as st

def validate_geojson(geojson: Dict) -> bool:
    """
    Validate GeoJSON structure
    """
    try:
        if not isinstance(geojson, dict) or 'features' not in geojson:
            return False
        return True
    except Exception:
        return False

@st.cache_data(ttl=3600)  # Cache for 1 hour
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

@st.cache_data(ttl=3600)  # Cache district boundaries for 1 hour
def get_district_boundaries() -> Dict[str, Any]:
    """
    Load GeoJSON boundaries for Chattanooga city council districts
    """
    try:
        boundaries_path = Path('assets/district_boundaries.json')
        if not boundaries_path.exists():
            st.warning("District boundaries data file not found.")
            return {}

        with boundaries_path.open() as f:
            try:
                geojson = json.load(f)
                if not validate_geojson(geojson):
                    st.warning("Invalid GeoJSON structure")
                    return {}
            except json.JSONDecodeError:
                st.warning("Invalid JSON in district boundaries file")
                return {}

        districts = {}
        for feature in geojson.get('features', []):
            try:
                properties = feature.get('properties', {})
                district = str(properties.get('district', ''))

                if not district:
                    continue

                districts[district] = {
                    "type": "Feature",
                    "properties": {
                        "district": district,
                        "description": str(properties.get('description', '')),
                        "demographics": properties.get('demographics', {})
                    },
                    "geometry": feature.get('geometry', {})
                }
            except Exception:
                continue

        return districts

    except Exception:
        st.warning("Error loading district boundaries")
        return {}

@st.cache_data(ttl=300)  # Cache district results for 5 minutes
def get_district_for_coordinates(lat: float, lon: float) -> str:
    """
    Determine which district a point falls within using GIS boundaries
    """
    try:
        point = Point(lon, lat)

        if not (34.9 <= lat <= 35.2 and -85.4 <= lon <= -85.1):
            return "District not found"

        district_boundaries = get_district_boundaries()
        if not district_boundaries:
            return "District not found"

        for district, geojson in district_boundaries.items():
            try:
                district_shape = shape(geojson['geometry'])
                if district_shape.contains(point):
                    return district
            except Exception:
                continue

        return "District not found"

    except Exception:
        return "District not found"

@st.cache_data(ttl=3600)  # Cache council member data for 1 hour
def get_council_member(district: str) -> dict:
    """
    Get council member information for a district
    """
    try:
        council_members_path = Path('assets/City_Council.csv')
        if not council_members_path.exists():
            return {"name": "Information unavailable", "district": str(district)}

        df = pd.read_csv(council_members_path)
        member = df[df['District'] == int(district)]

        if member.empty:
            return {"name": "Information unavailable", "district": str(district)}

        return {
            "name": member.iloc[0]['City Rep'],
            "district": str(district)
        }
    except Exception:
        return {"name": "Information unavailable", "district": str(district)}

@st.cache_data(ttl=3600)  # Cache candidate data for 1 hour
def get_district_candidates(district: str) -> list:
    """
    Get list of candidates running in the March 4th, 2025 election for a given district
    """
    candidates_2025 = {
        "1": ["James \"Skip\" Burnette", "Chip Henderson"],
        "2": ["Jenny Hill"],
        "3": [
            "Jeff Davis ([Campaign Website](https://votejeffdavis.com/))",
            "Tom Marshall"
        ],
        "4": ["Cody Harvey"],
        "5": ["Dennis Clark", "Cory Hall", "Isiah (Ike) Hester", "Samantha Reid-Hawkins"],
        "6": ["Jenni Berz", "Jennifer Gregory", "Mark Holland", "Christian Siler", "Robert C Wilson"],
        "7": ["Raquetta Dotley"],
        "8": ["Anna Golladay", "Marvene Noel", "Doll Sandridge", "Kelvin Scott"],
        "9": ["Ron Elliott", "Letechia Ellis", "Evelina Irén Kertay"]
    }
    return candidates_2025.get(district, [])

@st.cache_data(ttl=300)  # Cache district info for 5 minutes
def get_district_info(lat: float, lon: float) -> dict:
    """
    Get comprehensive district information based on coordinates
    """
    district = get_district_for_coordinates(lat, lon)
    if district == "District not found":
        return {
            "district_number": district,
            "precinct": "Not found",
            "polling_place": "Not found",
            "polling_address": "Not found",
            "candidates": []
        }

    boundaries = get_district_boundaries()
    district_data = boundaries.get(district, {}).get('properties', {})
    candidates = get_district_candidates(district)

    try:
        polling_places_path = Path('assets/polling_places.csv')
        if not polling_places_path.exists():
            return {
                "district_number": district,
                "district_description": district_data.get('description', ''),
                "precinct": "Information unavailable",
                "polling_place": "Information unavailable",
                "polling_address": "Information unavailable",
                "candidates": candidates
            }

        df = pd.read_csv(polling_places_path)
        polling_info = find_nearest_polling_place(lat, lon, df) if not df.empty else None

        if polling_info:
            precinct, location_name, address = polling_info
            return {
                "district_number": district,
                "district_description": district_data.get('description', ''),
                "precinct": precinct,
                "polling_place": location_name,
                "polling_address": address,
                "candidates": candidates
            }
    except Exception:
        pass

    return {
        "district_number": district,
        "district_description": district_data.get('description', ''),
        "precinct": "Information unavailable",
        "polling_place": "Information unavailable",
        "polling_address": "Information unavailable",
        "candidates": candidates
    }

@st.cache_data(ttl=3600)  # Cache polling place data for 1 hour
def find_nearest_polling_place(lat: float, lon: float, df: pd.DataFrame) -> Optional[Tuple[str, str, str]]:
    """
    Find the nearest polling place to the given coordinates using haversine distance
    """
    try:
        min_dist = float('inf')
        nearest_place = None

        for _, place in df.iterrows():
            try:
                polling_address = f"{place['address']}, {place['city']}, {place['state']} {place['zip']}"
                place_coords = geocode_address(polling_address)

                if place_coords:
                    place_lat, place_lon = place_coords
                    dist = haversine_distance(lat, lon, place_lat, place_lon)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_place = place
            except Exception:
                continue

        if nearest_place is not None:
            return (
                nearest_place['precinct'],
                nearest_place['location_name'],
                f"{nearest_place['address']}, {nearest_place['city']}, {nearest_place['state']} {nearest_place['zip']}"
            )
    except Exception:
        pass

    return None