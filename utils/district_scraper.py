import pandas as pd
import json
from pathlib import Path
import streamlit as st
from shapely.geometry import Polygon, mapping
from shapely import wkt
from shapely.validation import make_valid
import math

def fetch_district_boundaries():
    """Create district boundaries from CSV data using WKT parsing"""
    try:
        # Create assets directory if it doesn't exist
        Path('assets').mkdir(exist_ok=True)

        # Read the CSV file with current districts (valid until April 13th, 2025)
        csv_path = Path('attached_assets') / 'Current_City_Council_Districts_20250115.csv'
        if not csv_path.exists():
            print("District data CSV file not found")
            return False

        # Read CSV and convert WKT strings to geometry objects
        df = pd.read_csv(csv_path)
        features = []

        for _, row in df.iterrows():
            try:
                district_num = str(row['citydst'])  # Use citydst column for district number

                # Parse polygon using WKT from the_geom column
                geometry = wkt.loads(row['the_geom'])

                # If geometry is not valid, try to fix it
                if not geometry.is_valid:
                    try:
                        geometry = make_valid(geometry)
                        if not geometry.is_valid:
                            print(f"Could not fix invalid geometry for District {district_num}")
                            continue
                    except Exception as e:
                        print(f"Error fixing geometry for District {district_num}: {str(e)}")
                        continue

                # Create GeoJSON feature
                feature = {
                    'type': 'Feature',
                    'properties': {
                        'district': district_num,
                        'description': f'City Council District {district_num}',
                        'representative': row.get('cityrep', 'Information not available')
                    },
                    'geometry': mapping(geometry)
                }

                features.append(feature)
                print(f"Successfully processed District {district_num}")

            except Exception as e:
                print(f"Error processing district: {str(e)}")
                continue

        if not features:
            print("No valid district features created")
            return False

        # Create the final GeoJSON structure
        district_geojson = {
            'type': 'FeatureCollection',
            'features': features
        }

        # Save to file
        output_path = Path('assets') / 'district_boundaries.json'
        with output_path.open('w') as f:
            json.dump(district_geojson, f, indent=2)

        print(f"Successfully saved {len(features)} district boundaries")
        return True

    except Exception as e:
        print(f"Error in district data processing: {str(e)}")
        return False

if __name__ == '__main__':
    # Create assets directory if it doesn't exist
    Path('assets').mkdir(exist_ok=True)

    # Fetch and save district boundaries
    success = fetch_district_boundaries()
    if success:
        print("District boundaries updated successfully")
    else:
        print("Failed to update district boundaries")