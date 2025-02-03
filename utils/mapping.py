import folium
from folium import plugins
from utils.district_data import get_district_boundaries, get_council_member, get_district_info
from utils.geocoding import geocode_address
import pandas as pd
from pathlib import Path
import streamlit as st

class DistrictStyle:
    def __init__(self, color: str):
        self.color = color

    def style(self, feature):
        return {
            'fillColor': self.color,
            'color': 'white',
            'weight': 1,
            'fillOpacity': 0.5,
            'opacity': 1,
            'dashArray': None
        }

    def highlight(self, feature):
        return {
            'fillColor': self.color,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 1
        }

def create_base_district_map() -> folium.Map:
    """Create a base map showing all Chattanooga districts"""
    # Create base map centered on Chattanooga
    m = folium.Map(
        location=[35.0456, -85.2672],
        zoom_start=11,
        tiles="cartodbpositron",
        zoom_control=True,
        smooth_factor=3.0
    )

    # Add fullscreen option
    plugins.Fullscreen().add_to(m)

    # Add mouse position coordinates
    plugins.MousePosition().add_to(m)

    # Create feature group for districts
    districts_group = folium.FeatureGroup(name='Districts', show=True)

    # Get all district boundaries
    district_boundaries = get_district_boundaries()

    # Color palette
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45']

    # Add districts with different colors
    for i, (district_name, district_geojson) in enumerate(district_boundaries.items()):
        color = colors[i % len(colors)]
        council_info = get_council_member(district_name)

        # Get candidates
        from utils.district_data import get_district_candidates
        candidates = get_district_candidates(district_name)

        # Create candidate information HTML
        candidates_html = ""
        if candidates:
            clean_candidates = [candidate.split('[')[0].strip() for candidate in candidates]
            if len(clean_candidates) == 1:
                candidates_html = f"<strong>{clean_candidates[0]}</strong> (running unopposed)"
            else:
                candidates_html = "<br>".join([f"• {candidate}" for candidate in clean_candidates])

        # Enhanced popup
        popup_html = f"""
        <div style="min-width: 200px; max-width: 300px; padding: 15px; font-family: Arial; font-size: 14px;">
            <h3 style="margin: 0 0 10px 0; color: #1976D2;">District {district_name}</h3>
            <div style="margin-bottom: 10px;">
                <strong>Current Council Member:</strong> {council_info['name']}<br>
            </div>
            <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
            <div style="margin-bottom: 10px;">
                <strong>March 4th, 2025 Election Candidates:</strong><br>
                {candidates_html}
            </div>
        </div>
        """

        # Create district style
        district_style = DistrictStyle(color)

        # Create GeoJson layer
        g = folium.GeoJson(
            district_geojson,
            style_function=district_style.style,
            highlight_function=district_style.highlight,
            popup=folium.Popup(popup_html, max_width=300),
            name=f'District {district_name}'
        )

        g.add_to(districts_group)

    # Add districts group to map
    districts_group.add_to(m)

    # Add custom CSS for animations
    custom_css = """
    <style>
        .leaflet-popup-content-wrapper {
            border-radius: 8px;
            box-shadow: 0 3px 14px rgba(0,0,0,0.2);
        }
        .leaflet-popup-content {
            margin: 0;
            padding: 0;
        }
        path {
            transition: all 0.3s ease-in-out;
        }
        path:hover {
            transform: scale(1.01);
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    return m

def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
    """Create a map highlighting the user's district"""
    m = folium.Map(
        location=[lat, lon],
        zoom_start=15,
        tiles="cartodbpositron",
        zoom_control=True
    )

    # Add marker for the entered address
    marker = folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="green", icon="home", prefix='fa')
    )
    marker.add_to(m)

    return m