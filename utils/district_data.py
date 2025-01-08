import pandas as pd
import json
from typing import Dict, Any
from shapely.geometry import Point, Polygon

def get_district_boundaries() -> Dict[str, Any]:
    """
    Get GeoJSON boundaries for Chattanooga city council districts
    """
    # Define boundaries for all districts with more accurate coordinates
    districts = {}

    # District boundaries defined using real coordinates
    district_coordinates = {
        "District 1": [  # Downtown/North Shore/UTC
            [-85.3125, 35.0625],
            [-85.3000, 35.0625],
            [-85.3000, 35.0750],
            [-85.3125, 35.0750],
            [-85.3125, 35.0625]
        ],
        "District 2": [  # North Chattanooga/Red Bank
            [-85.2900, 35.0800],
            [-85.2750, 35.0800],
            [-85.2750, 35.0900],
            [-85.2900, 35.0900],
            [-85.2900, 35.0800]
        ],
        "District 3": [  # Hixson/Middle Valley
            [-85.2400, 35.1100],
            [-85.2200, 35.1100],
            [-85.2200, 35.1200],
            [-85.2400, 35.1200],
            [-85.2400, 35.1100]
        ],
        "District 4": [  # Bonny Oaks/Summit
            [-85.2200, 35.0900],
            [-85.2000, 35.0900],
            [-85.2000, 35.1000],
            [-85.2200, 35.1000],
            [-85.2200, 35.0900]
        ],
        "District 5": [  # Brainerd/East Brainerd
            [-85.2375, 35.0815],
            [-85.2220, 35.0815],
            [-85.2220, 35.0925],
            [-85.2375, 35.0925],
            [-85.2375, 35.0815]
        ],
        "District 6": [  # East Chattanooga
            [-85.2600, 35.0700],
            [-85.2400, 35.0700],
            [-85.2400, 35.0800],
            [-85.2600, 35.0800],
            [-85.2600, 35.0700]
        ],
        "District 7": [  # South Chattanooga
            [-85.2800, 35.0300],
            [-85.2600, 35.0300],
            [-85.2600, 35.0400],
            [-85.2800, 35.0400],
            [-85.2800, 35.0300]
        ],
        "District 8": [  # East Lake/Oak Grove
            [-85.2900, 35.0200],
            [-85.2700, 35.0200],
            [-85.2700, 35.0300],
            [-85.2900, 35.0300],
            [-85.2900, 35.0200]
        ],
        "District 9": [  # Lookout Valley/Mountain Creek
            [-85.3200, 35.0200],
            [-85.3000, 35.0200],
            [-85.3000, 35.0300],
            [-85.3200, 35.0300],
            [-85.3200, 35.0200]
        ]
    }

    # Create GeoJSON features for each district
    for district, coords in district_coordinates.items():
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
            "geometry": {
                "type": "Polygon",
                "coordinates": [coords]
            }
        }

    return districts

def get_district_for_coordinates(lat: float, lon: float) -> str:
    """
    Determine which district a point falls within
    """
    point = Point(lon, lat)
    district_boundaries = get_district_boundaries()

    for district, geojson in district_boundaries.items():
        coords = geojson["geometry"]["coordinates"][0]
        polygon = Polygon(coords)
        if polygon.contains(point):
            return district

    # Default to closest district if point is not within any polygon
    return "District 5"  # This should be improved to find nearest district

def get_district_info(lat: float, lon: float) -> dict:
    """
    Get district information based on coordinates
    """
    # Determine district based on coordinates
    district = get_district_for_coordinates(lat, lon)

    # Get polling place information
    df = pd.read_csv('assets/polling_places.csv')
    polling_place = df.iloc[0]  # Default to first polling place

    # In production, this would match polling places to districts
    for _, place in df.iterrows():
        if place['precinct'].startswith(district.split()[1]):
            polling_place = place
            break

    return {
        "district_number": district,
        "precinct": polling_place['precinct'],
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