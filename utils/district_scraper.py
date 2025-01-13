import requests
import json
from pathlib import Path
import streamlit as st

def fetch_district_boundaries():
    """
    Fetch district boundaries from Chattanooga GIS server
    """
    # GIS Server endpoint for district boundaries
    url = "https://pwgis.chattanooga.gov/server/rest/services/Administrative_Areas/CouncilDistricts/MapServer/0/query"

    # Parameters for the query
    params = {
        'f': 'json',  # Request JSON format
        'where': '1=1',  # Get all districts
        'outFields': 'DISTRICT,COUNCIL_MEMBER,DESCRIPTION',
        'returnGeometry': 'true',
        'spatialRel': 'esriSpatialRelIntersects',
        'geometryType': 'esriGeometryEnvelope',
        'inSR': '102100',  # Web Mercator projection used by the map viewer
        'outSR': '4326',   # Convert to WGS84 for our use
        'geometry': json.dumps({  # Chattanooga extent in Web Mercator
            "xmin": -9509333.352331966,
            "ymin": 4082084.7143734153,
            "xmax": -9472643.578755133,
            "ymax": 4272412.914803248,
            "spatialReference": {"wkid": 102100}
        })
    }

    headers = {
        'User-Agent': 'ChattanoogaVotingApp/1.0',
        'Accept': 'application/json',
        'Referer': 'https://pwgis.chattanooga.gov/portal/apps/webappviewer/'
    }

    try:
        print("Fetching district boundaries from GIS server...")
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()

        # Process the GeoJSON data
        data = response.json()
        print("Response received:", json.dumps(data)[:200])  # Print first 200 chars for debugging

        if 'error' in data:
            print(f"GIS server returned an error: {data['error']}")
            return False

        if 'features' not in data:
            print("No features found in the response")
            return False

        print(f"Found {len(data['features'])} districts")

        # Transform the data into GeoJSON format
        features = []
        for feature in data['features']:
            try:
                attributes = feature.get('attributes', {})
                district_num = str(attributes.get('DISTRICT', ''))
                if not district_num:
                    print(f"Skipping feature without district number: {attributes}")
                    continue

                # Convert ESRI geometry to GeoJSON format
                geometry = feature.get('geometry', {})
                if 'rings' in geometry:
                    geometry = {
                        'type': 'Polygon',
                        'coordinates': geometry['rings']
                    }
                    print(f"Converted geometry for District {district_num}")
                else:
                    print(f"No rings found in geometry for District {district_num}")
                    continue

                # Create GeoJSON feature
                features.append({
                    'type': 'Feature',
                    'properties': {
                        'district': f'District {district_num}',
                        'description': f'City Council District {district_num}',
                        'council_member': attributes.get('COUNCIL_MEMBER', 'Information not available'),
                        'area_description': attributes.get('DESCRIPTION', '')
                    },
                    'geometry': geometry
                })
                print(f"Processed District {district_num}")

            except (KeyError, TypeError) as e:
                print(f"Error processing district feature: {str(e)}")
                continue

        if not features:
            print("No valid district features found")
            return False

        # Create the final GeoJSON structure
        district_geojson = {
            'type': 'FeatureCollection',
            'features': features
        }

        # Save to file
        output_path = Path('assets') / 'district_boundaries.json'
        output_path.parent.mkdir(exist_ok=True)

        with output_path.open('w') as f:
            json.dump(district_geojson, f, indent=2)

        print(f"Successfully saved {len(features)} district boundaries")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error fetching district data: {str(e)}")
        return False
    except Exception as e:
        print(f"Error processing district data: {str(e)}")
        return False

if __name__ == '__main__':
    # Create assets directory if it doesn't exist
    Path('assets').mkdir(exist_ok=True)

    # Add debug info about the request
    print("Debugging GIS request...")
    url = "https://pwgis.chattanooga.gov/server/rest/services/Administrative_Areas/CouncilDistricts/MapServer/0/query"
    params = {
        'f': 'json',
        'where': '1=1',
        'outFields': 'DISTRICT,COUNCIL_MEMBER,DESCRIPTION',
        'returnGeometry': 'true',
        'spatialRel': 'esriSpatialRelIntersects',
        'geometryType': 'esriGeometryEnvelope',
        'inSR': '102100',
        'outSR': '4326',
        'geometry': json.dumps({
            "xmin": -9509333.352331966,
            "ymin": 4082084.7143734153,
            "xmax": -9472643.578755133,
            "ymax": 4272412.914803248,
            "spatialReference": {"wkid": 102100}
        })
    }
    print(f"Request URL: {url}")
    print(f"Request params: {json.dumps(params, indent=2)}")

    # Fetch and save district boundaries
    success = fetch_district_boundaries()
    if success:
        print("District boundaries updated successfully")
    else:
        print("Failed to update district boundaries")