import folium
from folium import plugins
from utils.district_data import get_district_boundaries, get_council_member, get_district_info
from utils.geocoding import geocode_address
import pandas as pd
from pathlib import Path
import streamlit as st

def create_base_district_map():
    """Creates a base map showing all district boundaries"""
    # Initialize the map centered on Chattanooga
    m = folium.Map(
        location=[35.0456, -85.3097],
        zoom_start=12,
        tiles='cartodbpositron'
    )

    # Get district boundaries
    district_boundaries = get_district_boundaries()

    # Add district polygons to map
    for district_num, geometry in district_boundaries.items():
        council_info = get_council_member(f"District {district_num}")
        folium.GeoJson(
            geometry,
            style_function=lambda x: {
                'fillColor': '#1B4E5D',
                'color': '#ffffff',
                'weight': 2,
                'fillOpacity': 0.3
            },
            tooltip=f"District {district_num}<br>{council_info['name']}"
        ).add_to(m)

    return m

@st.cache_data(ttl=3600)
def create_district_map(lat, lon, district_info):
    """Creates a map showing specific district with marker"""
    m = create_base_district_map()

    # Add marker for searched address
    folium.Marker(
        [lat, lon],
        popup='Your Location',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    return m