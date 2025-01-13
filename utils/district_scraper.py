import pandas as pd
import json
from pathlib import Path
import streamlit as st
from ast import literal_eval
from shapely.geometry import Polygon, mapping

def convert_polygon_string_to_coords(polygon_str: str) -> list:
    """
    Convert polygon string from CSV to coordinate list
    """
    try:
        # Remove POLYGON keyword and both sets of parentheses
        coords_str = polygon_str.replace('POLYGON ((', '').replace('))', '')
        # Split into coordinate pairs
        coord_pairs = coords_str.split(', ')
        # Convert to float pairs
        coords = []
        for pair in coord_pairs:
            # Clean up any remaining parentheses and split
            pair = pair.strip('() ')
            try:
                lon, lat = map(float, pair.split())
                # Validate coordinates are in reasonable range for Chattanooga
                if (-85.5 <= lon <= -85.0) and (34.9 <= lat <= 35.3):
                    coords.append([lon, lat])
                else:
                    print(f"Skipping invalid coordinate pair: {lon}, {lat}")
            except ValueError as e:
                print(f"Error parsing coordinate pair '{pair}': {str(e)}")
                continue

        # Verify we have enough coordinates to form a valid polygon
        if len(coords) >= 3:
            return coords
        else:
            print(f"Not enough valid coordinates: {len(coords)}")
            return []

    except Exception as e:
        print(f"Error processing polygon string: {str(e)}")
        return []

def fetch_district_boundaries():
    """
    Create district boundaries from CSV data
    """
    try:
        # Read the CSV file
        csv_path = Path('attached_assets') / 'Chattanooga_Redistricting_-_New_Districts_20250113.csv'
        if not csv_path.exists():
            print("District data CSV file not found")
            return False

        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} districts in CSV")

        features = []
        for _, row in df.iterrows():
            try:
                district_num = row['District Name'].replace('District ', '')
                print(f"\nProcessing {row['District Name']}...")
                polygon_coords = convert_polygon_string_to_coords(row['polygon'])

                if not polygon_coords:
                    print(f"Failed to process coordinates for {row['District Name']}")
                    continue

                # Create GeoJSON feature
                features.append({
                    'type': 'Feature',
                    'properties': {
                        'district': district_num,  # Store just the number
                        'description': f'City Council District {district_num}',
                        'demographics': {
                            'total_population': int(row['Total Population']),
                            'percent_white': float(row['Percent White']),
                            'percent_black': float(row['Percent Black']),
                            'percent_hispanic': float(row['Percent Hispanic']),
                            'percent_other': float(row['Percent Other'])
                        }
                    },
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [polygon_coords]  # GeoJSON requires nested array
                    }
                })
                print(f"Successfully processed District {district_num} with {len(polygon_coords)} coordinates")

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
        output_path.parent.mkdir(exist_ok=True)

        with output_path.open('w') as f:
            json.dump(district_geojson, f, indent=2)

        print(f"\nSuccessfully saved {len(features)} district boundaries")
        return True

    except Exception as e:
        print(f"Error processing district data: {str(e)}")
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