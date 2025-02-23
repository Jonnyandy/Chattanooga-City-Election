import pandas as pd
import json
from typing import Dict, Any, Tuple, List, Optional
from shapely.geometry import Point, Polygon, mapping, shape
import math
from pathlib import Path
from utils.geocoding import geocode_address
import streamlit as st

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
        boundaries_path = Path('assets') / 'district_boundaries.json'
        if not boundaries_path.exists():
            st.error("District boundaries data file not found.")
            return {}

        with boundaries_path.open() as f:
            try:
                geojson = json.load(f)
                if not isinstance(geojson, dict) or 'features' not in geojson:
                    st.error("Invalid GeoJSON structure")
                    return {}
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON in district boundaries file: {str(e)}")
                return {}

        districts = {}
        for feature in geojson.get('features', []):
            try:
                if not isinstance(feature, dict) or 'properties' not in feature:
                    continue

                properties = feature.get('properties', {})
                district = str(properties.get('district', ''))

                if not district:
                    continue

                geometry = feature.get('geometry', {})
                if not isinstance(geometry, dict) or 'type' not in geometry or 'coordinates' not in geometry:
                    continue

                districts[district] = {
                    "type": "Feature",
                    "properties": {
                        "district": district,
                        "description": str(properties.get('description', '')),
                        "demographics": properties.get('demographics', {})
                    },
                    "geometry": geometry
                }
            except Exception as e:
                st.error(f"Error processing district {district}: {str(e)}")
                continue

        if not districts:
            st.error("No valid district data found in the file")
            return {}

        return districts

    except Exception as e:
        st.error(f"Error loading district boundaries: {str(e)}")
        return {}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def point_in_polygon(point: Point, polygon_coords: List[List[float]], buffer_distance: float = 0.0001) -> bool:
    """
    Check if a point is within a polygon with a small buffer zone for boundary cases
    """
    try:
        polygon = Polygon(polygon_coords[0])
        buffered_polygon = polygon.buffer(buffer_distance)
        return buffered_polygon.contains(point)
    except Exception as e:
        st.error(f"Error checking point in polygon: {str(e)}")
        return False

@st.cache_data(ttl=3600)  # Cache polling place data for 1 hour
def find_nearest_polling_place(lat: float, lon: float, df: pd.DataFrame) -> Optional[Tuple[str, str, str]]:
    """
    Find the nearest polling place to the given coordinates using haversine distance
    """
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
        except Exception as e:
            st.error(f"Error processing polling place {place['location_name']}: {str(e)}")
            continue

    if nearest_place is not None:
        return (
            nearest_place['precinct'],
            nearest_place['location_name'],
            f"{nearest_place['address']}, {nearest_place['city']}, {nearest_place['state']} {nearest_place['zip']}"
        )
    return None

@st.cache_data(ttl=300)  # Cache district results for 5 minutes
def get_district_for_coordinates(lat: float, lon: float) -> str:
    """
    Determine which district a point falls within using GIS boundaries
    """
    try:
        point = Point(lon, lat)

        if not (34.9 <= lat <= 35.2 and -85.4 <= lon <= -85.1):
            st.warning("Coordinates appear to be outside the expected Chattanooga area")
            return "District not found"

        district_boundaries = get_district_boundaries()
        if not district_boundaries:
            st.error("Failed to load district boundaries")
            return "District not found"

        for district, geojson in district_boundaries.items():
            try:
                if 'geometry' not in geojson:
                    continue

                district_shape = shape(geojson['geometry'])

                if district_shape.contains(point):
                    return district

                if district_shape.buffer(0.001).contains(point):
                    return district

            except Exception as e:
                st.error(f"Error checking district {district}: {str(e)}")
                continue

        st.warning("Location not matched to any district. Please verify the address.")
        return "District not found"

    except Exception as e:
        st.error(f"Error in district matching: {str(e)}")
        return "District not found"

@st.cache_data(ttl=3600)  # Cache candidate data for 1 hour
def get_district_candidates(district: str) -> list:
    """
    Get list of candidates running in the March 4th, 2025 election for a given district
    """
    try:
        from utils.candidate_scraper import get_candidate_info

        candidates_info = get_candidate_info()
        district_info = candidates_info.get(district, {})

        formatted_candidates = []
        for candidate_name, info in district_info.items():
            candidate_str = candidate_name

            # Add contact info if available
            if 'contact' in info:
                candidate_str = f"{candidate_str}\n*Contact: {info['contact']}*"

            formatted_candidates.append(candidate_str)

        return formatted_candidates if formatted_candidates else []

    except Exception as e:
        st.error(f"Error getting candidate information: {str(e)}")
        # Fallback to basic candidate list if scraping fails
        candidates_2025 = {
            "1": ["James \"Skip\" Burnette", "Chip Henderson"],
            "2": ["Jenny Hill"],
            "3": [
                "Jeff Davis",
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
            "distance": "N/A",
            "error": "Location outside city limits",
            "candidates": []
        }

    boundaries = get_district_boundaries()
    district_data = boundaries.get(district, {}).get('properties', {})
    candidates = get_district_candidates(district)

    try:
        polling_places_path = Path('assets/polling_places.csv')
        if not polling_places_path.exists():
            raise FileNotFoundError("Polling places data file not found")

        df = pd.read_csv(polling_places_path)
        polling_info = find_nearest_polling_place(lat, lon, df)

        if polling_info:
            precinct, location_name, address = polling_info
            return {
                "district_number": district,
                "district_description": district_data.get('description', ''),
                "precinct": precinct,
                "polling_place": location_name,
                "polling_address": address,
                "distance": "Based on your location",
                "candidates": candidates
            }
    except Exception as e:
        st.error(f"Error retrieving polling place information: {str(e)}")

    return {
        "district_number": district,
        "district_description": district_data.get('description', ''),
        "precinct": "Not found",
        "polling_place": "Not found",
        "polling_address": "Not found",
        "distance": "N/A",
        "candidates": candidates
    }

@st.cache_data(ttl=3600)  # Cache council member data for 1 hour
def get_council_member(district: str) -> dict:
    """
    Get council member information for a district
    """
    try:
        council_members_path = Path('attached_assets/City_Council__old__20250115.csv')
        if not council_members_path.exists():
            raise FileNotFoundError("Council members data file not found")

        df = pd.read_csv(council_members_path)
        member = df[df['District'] == int(district)]
        if member.empty:
            raise ValueError(f"No council member found for district {district}")

        return {
            "name": member.iloc[0]['City Rep'],
            "district": str(district)
        }
    except FileNotFoundError:
        st.error("Council members data file not found")
    except (ValueError, IndexError) as e:
        st.error(f"Error retrieving council member: {str(e)}")
    except Exception as e:
        st.error(f"Error retrieving council member information: {str(e)}")

    return {
        "name": "Information unavailable",
        "district": str(district)
    }