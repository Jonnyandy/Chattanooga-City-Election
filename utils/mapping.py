import folium
from folium import plugins
from utils.district_data import get_district_boundaries, get_council_member, get_district_info
from utils.geocoding import geocode_address
import pandas as pd
from pathlib import Path
import streamlit as st

def get_district_style(color: str, feature):
    """Style function for normal state"""
    return {
        'fillColor': color,
        'color': 'white',
        'weight': 1,
        'fillOpacity': 0.5,
        'opacity': 1,
        'dashArray': None
    }

def get_district_highlight_style(color: str, feature):
    """Style function for hover state"""
    return {
        'fillColor': color,
        'color': 'white',
        'weight': 2,
        'fillOpacity': 0.7,
        'opacity': 1
    }

@st.cache_data(ttl=3600)  # Cache base map for 1 hour
def create_base_district_map() -> folium.Map:
    """Create a base map showing all Chattanooga districts with animated transitions"""
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

    # Create feature groups for layers
    districts_group = folium.FeatureGroup(name='Districts', show=True)

    # Get all district boundaries
    district_boundaries = get_district_boundaries()

    # Color palette
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45']

    # Add districts with different colors and animations
    for i, (district_name, district_geojson) in enumerate(district_boundaries.items()):
        color = colors[i % len(colors)]
        council_info = get_council_member(district_name)

        # Get candidates for this district
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

        # Enhanced popup with candidate information
        popup_html = f"""
        <div style="
            min-width: 200px;
            max-width: 300px;
            padding: 15px;
            font-family: Arial;
            font-size: 14px;
        ">
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

        # Create GeoJson layer with enhanced interactivity
        def style_fn(x):
            return get_district_style(color, x)
            
        def highlight_fn(x):
            return get_district_highlight_style(color, x)
            
        g = folium.GeoJson(
            district_geojson,
            style_function=style_fn,
            highlight_function=highlight_fn,
            popup=folium.Popup(popup_html, max_width=300),
            name=f'District {district_name}'
        )

        # Add click event for zooming
        g.add_child(folium.Element("""
            <script>
                (function() {
                    var districtLayer = document.querySelector('path:last-child');
                    if (districtLayer) {
                        districtLayer.addEventListener('click', function(e) {
                            var map = document.querySelector('#map');
                            if (map && map._leaflet_map) {
                                var tooltip = document.querySelector('.district-tooltip');
                                if (tooltip) {
                                    tooltip.style.display = 'none';
                                }
                                var bounds = e.target.getBounds();
                                map._leaflet_map.fitBounds(bounds, {
                                    padding: [50, 50],
                                    maxZoom: 14,
                                    duration: 1
                                });
                            }
                        });
                    }
                })();
            </script>
        """))

        g.add_to(districts_group)

    # Add districts group to map
    districts_group.add_to(m)

    # Add custom CSS for animations
    custom_css = """
    <style>
        .district-tooltip {
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s ease-in-out;
        }
        .district-tooltip:hover {
            opacity: 1;
            transform: translateY(0);
        }
        path {
            transition: all 0.3s ease-in-out;
            cursor: pointer;
        }
        path:hover {
            transform: scale(1.01);
        }
        .leaflet-popup-content-wrapper {
            border-radius: 8px;
            box-shadow: 0 3px 14px rgba(0,0,0,0.2);
        }
        .leaflet-popup-content {
            margin: 0;
            padding: 0;
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    return m

@st.cache_data(ttl=300)  # Cache district map for 5 minutes
def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
    """Create an interactive map highlighting the user's district"""
    # Start with the base map
    m = create_base_district_map()

    # Add marker for the entered address
    marker = folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="green", icon="home", prefix='fa')
    )
    marker.add_to(m)

    # Center the map on the entered address with closer zoom
    m.location = [lat, lon]
    m.zoom_start = 15

    # Add JavaScript to zoom to marker after the map loads
    m.get_root().html.add_child(folium.Element(f"""
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                setTimeout(function() {{
                    var map = document.querySelector('#map')._leaflet_map;
                    map.setView([{lat}, {lon}], 17, {{
                        animate: true,
                        duration: 1
                    }});
                }}, 1000);
            }});
        </script>
    """))

    return m