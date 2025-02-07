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
            'dashArray': None,
            'className': 'district-polygon'
        }

    def highlight(self, feature):
        return {
            'fillColor': self.color,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 1,
            'className': 'district-polygon-highlight'
        }

def create_base_district_map() -> folium.Map:
    """Create a base map showing all Chattanooga districts with smooth transitions"""
    # Create base map centered on Chattanooga
    m = folium.Map(
        location=[35.0456, -85.2672],
        zoom_start=11,
        tiles="cartodbpositron",
        zoom_control=True,
        smooth_factor=3.0,
        prefer_canvas=True,
        zoom_animation_threshold=4
    )

    # Add fullscreen option with smooth transitions
    plugins.Fullscreen(
        position='topright',
        title='Expand map',
        title_cancel='Exit full screen',
        force_separate_button=True
    ).add_to(m)

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

        # Enhanced popup with smooth transitions and view candidates button
        popup_html = f"""
        <div class="district-popup">
            <h3>District {district_name}</h3>
            <div>
                <strong>Current Council Member:</strong> {council_info['name']}<br>
            </div>
            <hr>
            <div>
                <strong>March 4th, 2025 Election Candidates:</strong><br>
                {candidates_html}
            </div>
            <div class="view-candidates-button">
                <a href="/candidates?district={district_name}" 
                   class="btn-view-candidates"
                   target="_self">
                   👥 View Candidate Details
                </a>
            </div>
        </div>
        """

        # Create district style
        district_style = DistrictStyle(color)

        # Create GeoJson layer with smooth transitions
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

    # Add custom CSS for animations and button styling
    custom_css = """
    <style>
        .leaflet-popup-content-wrapper {
            border-radius: 8px;
            box-shadow: 0 3px 14px rgba(0,0,0,0.2);
            transition: all 0.3s ease-in-out;
        }
        .leaflet-popup-content {
            margin: 0;
            padding: 0;
        }
        .district-popup {
            min-width: 200px;
            max-width: 300px;
            padding: 15px;
            font-family: Arial;
            font-size: 14px;
        }
        .district-popup h3 {
            margin: 0 0 10px 0;
            color: #1976D2;
        }
        .district-polygon {
            transition: all 0.3s ease-in-out;
        }
        .district-polygon-highlight {
            transition: all 0.3s ease-in-out;
            transform: scale(1.01);
        }
        .leaflet-marker-icon {
            transition: all 0.3s ease-in-out;
        }
        .leaflet-tile {
            transition: opacity 0.2s ease-in-out;
        }
        .leaflet-zoom-animated {
            transition: transform 0.25s cubic-bezier(0,0,0.25,1);
        }
        .view-candidates-button {
            margin-top: 15px;
            text-align: center;
        }
        .btn-view-candidates {
            display: inline-block;
            padding: 8px 16px;
            background-color: #1976D2;
            color: white !important;
            text-decoration: none;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        .btn-view-candidates:hover {
            background-color: #1565C0;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    return m

def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
    """Create a map highlighting the user's district with smooth transitions"""
    # Create base map centered on Chattanooga
    m = folium.Map(
        location=[lat, lon],
        zoom_start=15,
        tiles="cartodbpositron",
        zoom_control=True,
        prefer_canvas=True,
        smooth_factor=3.0,
        zoom_animation_threshold=4
    )

    # Add district boundaries first
    district_boundaries = get_district_boundaries()
    districts_group = folium.FeatureGroup(name='Districts', show=True)

    # Color palette
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45']

    # Add districts with different colors
    for i, (district_name, district_geojson) in enumerate(district_boundaries.items()):
        color = colors[i % len(colors)]
        style_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 1,
            'fillOpacity': 0.5,
            'opacity': 1
        }

        highlight_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 1
        }

        g = folium.GeoJson(
            district_geojson,
            style_function=style_function,
            highlight_function=highlight_function,
            popup=folium.Popup(
                f"District {district_name}",
                max_width=300
            ),
            name=f'District {district_name}'
        )
        g.add_to(districts_group)

    # Add districts group to map
    districts_group.add_to(m)

    # Add marker for the entered address with animation
    icon_html = """
    <div class="marker-pin" style="animation: dropIn 0.5s ease-out;">
        <i class="fa fa-home"></i>
    </div>
    """

    marker = folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.DivIcon(
            html=icon_html,
            class_name="custom-marker"
        )
    )
    marker.add_to(m)

    # Add custom CSS for marker animation
    custom_css = """
    <style>
        .marker-pin {
            width: 30px;
            height: 30px;
            border-radius: 50% 50% 50% 0;
            background: #00796b;
            position: absolute;
            transform: rotate(-45deg);
            left: 50%;
            top: 50%;
            margin: -15px 0 0 -15px;
        }
        .marker-pin i {
            color: #fff;
            transform: rotate(45deg);
            margin: 7px 0 0 7px;
            font-size: 16px;
        }
        @keyframes dropIn {
            from {
                opacity: 0;
                transform: translateY(-20px) rotate(-45deg);
            }
            to {
                opacity: 1;
                transform: translateY(0) rotate(-45deg);
            }
        }
        .leaflet-tile {
            transition: opacity 0.2s ease-in-out;
        }
        .leaflet-zoom-animated {
            transition: transform 0.25s cubic-bezier(0,0,0.25,1);
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    return m