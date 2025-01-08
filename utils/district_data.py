import pandas as pd
import json
from typing import Dict, Any

def get_district_boundaries() -> Dict[str, Any]:
    """
    Get GeoJSON boundaries for Chattanooga city council districts
    """
    # Define boundaries for all districts
    districts = {}

    # District 1 - Downtown/North Shore
    districts["District 1"] = {
        "type": "Feature",
        "properties": {
            "district": "District 1",
            "style": {
                "fillColor": "#1E88E5",
                "color": "#1E88E5",
                "weight": 2,
                "fillOpacity": 0.3
            }
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-85.3125, 35.0625],  # Downtown area
                [-85.3000, 35.0625],  # North Shore
                [-85.3000, 35.0750],  # UTC area
                [-85.3125, 35.0750],  # Riverfront
                [-85.3125, 35.0625]
            ]]
        }
    }

    # Add other districts with their specific boundaries
    districts["District 2"] = {
        "type": "Feature",
        "properties": {
            "district": "District 2",
            "style": {"fillColor": "#1E88E5", "color": "#1E88E5", "weight": 2, "fillOpacity": 0.3}
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-85.2900, 35.0800],  # North Chattanooga
                [-85.2750, 35.0800],  # Red Bank border
                [-85.2750, 35.0900],  # Signal Mountain Rd
                [-85.2900, 35.0900],  # Cherokee Blvd
                [-85.2900, 35.0800]
            ]]
        }
    }

    # District 5 (Brainerd area) - more precise boundary
    districts["District 5"] = {
        "type": "Feature",
        "properties": {
            "district": "District 5",
            "style": {"fillColor": "#1E88E5", "color": "#1E88E5", "weight": 2, "fillOpacity": 0.3}
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-85.2375, 35.0815],  # Eastgate Town Center
                [-85.2220, 35.0815],  # East Brainerd Road
                [-85.2220, 35.0925],  # Brainerd Road
                [-85.2375, 35.0925],  # Lee Highway
                [-85.2375, 35.0815]
            ]]
        }
    }

    # We would typically load this data from a GeoJSON file or database
    # For now, returning our hardcoded district boundaries
    return districts

def get_district_info(lat: float, lon: float) -> dict:
    """
    Get district information based on coordinates
    """
    # This would typically use spatial queries to determine the district
    # For now, using polling_places.csv for basic info
    df = pd.read_csv('assets/polling_places.csv')

    # In a real implementation, we would use spatial operations to find the correct district
    # For demo, returning Precinct 54 info
    polling_place = df[df['precinct'] == 'Precinct 54'].iloc[0]

    return {
        "district_number": "District 5",
        "precinct": "Precinct 54",
        "polling_place": polling_place['location_name'],
        "polling_address": f"{polling_place['address']}, {polling_place['city']}, {polling_place['state']} {polling_place['zip']}"
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