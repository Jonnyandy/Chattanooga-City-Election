import pandas as pd
import json
from pathlib import Path
import streamlit as st
from ast import literal_eval
from shapely.geometry import Polygon, mapping
import math

def calculate_distance(coord1, coord2):
    """Calculate distance between two coordinates"""
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    return math.sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)

def is_valid_coordinate_sequence(coords):
    """
    Validate if the coordinate sequence forms a valid polygon without extreme jumps
    """
    if len(coords) < 3:
        return False

    # Maximum allowed distance between consecutive points (in degrees)
    MAX_DISTANCE = 0.05  # approximately 5.5km - reduced for better accuracy

    for i in range(len(coords) - 1):
        distance = calculate_distance(coords[i], coords[i + 1])
        if distance > MAX_DISTANCE:
            print(f"Invalid distance ({distance:.4f}) between points: {coords[i]} and {coords[i + 1]}")
            return False

    # Check if the polygon is closed (first and last points match)
    if coords[0] != coords[-1]:
        print("Polygon is not closed - first and last points don't match")
        return False

    return True

def convert_polygon_string_to_coords(polygon_str: str, district_name: str) -> list:
    """
    Convert polygon string from CSV to coordinate list with enhanced validation
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
                    # Red Bank area exclusion (approximate boundaries)
                    if not (-85.3 <= lon <= -85.28 and 35.09 <= lat <= 35.12):
                        # Additional validation for District 1
                        if district_name == "District 1":
                            # Check for obviously invalid coordinates that would create obtuse triangles
                            if len(coords) >= 2:
                                prev_coord = coords[-1]
                                distance = calculate_distance([lon, lat], prev_coord)
                                if distance > 0.05:  # About 5.5km
                                    print(f"Skipping likely invalid coordinate in District 1: {lon}, {lat}")
                                    continue
                        coords.append([lon, lat])
                    else:
                        print(f"Excluding Red Bank coordinate pair: {lon}, {lat}")
                else:
                    print(f"Skipping invalid coordinate pair: {lon}, {lat}")
            except ValueError as e:
                print(f"Error parsing coordinate pair '{pair}': {str(e)}")
                continue

        # Additional validation for the sequence of coordinates
        if not is_valid_coordinate_sequence(coords):
            print("Invalid coordinate sequence detected - possible anomalous points")
            return []

        # Verify we have enough coordinates to form a valid polygon
        if len(coords) >= 3:
            # Create a test polygon to verify validity
            try:
                poly = Polygon(coords)
                if not poly.is_valid:
                    print("Invalid polygon shape detected")
                    return []

                # Additional check for District 1 to prevent obtuse triangles
                if district_name == "District 1":
                    # Calculate area and verify it's reasonable
                    area = poly.area
                    if area > 0.1:  # Arbitrary threshold for obviously wrong shapes
                        print(f"District 1 area too large: {area}")
                        return []

                return coords
            except Exception as e:
                print(f"Error creating polygon: {str(e)}")
                return []
        else:
            print(f"Not enough valid coordinates: {len(coords)}")
            return []

    except Exception as e:
        print(f"Error processing polygon string: {str(e)}")
        return []

def fetch_district_boundaries():
    """
    Create district boundaries from CSV data with enhanced validation
    """
    try:
        # Create assets directory if it doesn't exist
        Path('assets').mkdir(exist_ok=True)

        # Read the CSV file
        csv_path = Path('attached_assets') / 'Chattanooga_Redistricting_-_New_Districts_20250113 (1).csv'
        if not csv_path.exists():
            print("District data CSV file not found")
            return False

        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} districts in CSV")

        features = []
        for _, row in df.iterrows():
            try:
                district_name = row['District Name']
                district_num = district_name.replace('District ', '')
                print(f"\nProcessing {district_name}...")
                polygon_coords = convert_polygon_string_to_coords(row['polygon'], district_name)

                if not polygon_coords:
                    print(f"Failed to process coordinates for {district_name}")
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