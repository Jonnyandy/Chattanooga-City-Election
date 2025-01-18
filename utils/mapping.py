import folium
from folium import plugins
from utils.district_data import get_district_boundaries, get_council_member, get_district_info
from utils.geocoding import geocode_address
import pandas as pd
from pathlib import Path

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

        # Style function for normal state
        style_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 1,
            'fillOpacity': 0.5,
            'opacity': 1,
            'dashArray': None
        }

        # Style function for hover state
        highlight_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 1
        }

        # Enhanced tooltip with more information
        tooltip_html = f"""
        <div class="district-tooltip" style="
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            font-family: Arial;
            font-size: 12px;
            min-width: 250px;
        ">
            <h4 style="margin: 0 0 8px 0; color: #1976D2;">District {district_name}</h4>
            <strong>Council Member:</strong> {council_info['name']}<br>
            <div style="margin-top: 5px; font-size: 11px; color: #666;">
                <em>Click for more information</em>
            </div>
        </div>
        """

        # Enhanced popup with detailed information
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
                <strong>Council Member:</strong> {council_info['name']}<br>
                <strong>Area Description:</strong><br>
                {district_geojson['properties'].get('description', '')}
            </div>
            <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
            <div style="font-size: 13px; color: #666;">
                <strong>District Information:</strong><br>
                • Use mouse wheel to zoom in/out<br>
                • Drag to pan the map<br>
                • Click 'Reset View' to see all districts
            </div>
        </div>
        """

        # Create GeoJson layer with enhanced interactivity
        g = folium.GeoJson(
            district_geojson,
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=folium.Tooltip(tooltip_html),
            popup=folium.Popup(popup_html, max_width=300),
            name=f'District {district_name}'
        )

        # Add click event for zooming to district and hiding tooltip
        g.add_child(folium.Element(f"""
            <script>
                (function() {{
                    var districtLayer = document.querySelector('path:last-child');
                    if (districtLayer) {{
                        districtLayer.addEventListener('click', function(e) {{
                            var map = document.querySelector('#map');
                            if (map && map._leaflet_map) {{
                                // Hide tooltip after click
                                var tooltip = document.querySelector('.district-tooltip');
                                if (tooltip) {{
                                    tooltip.style.display = 'none';
                                }}

                                // Zoom to district bounds
                                var bounds = e.target.getBounds();
                                map._leaflet_map.fitBounds(bounds, {{
                                    padding: [50, 50],
                                    maxZoom: 14,
                                    duration: 1
                                }});
                            }}
                        }});
                    }}
                }})();
            </script>
        """))

        g.add_to(districts_group)

    # Add districts group to map
    districts_group.add_to(m)

    # Add reset view button
    reset_button_html = '''
        <button 
            onclick="document.querySelector('#map')._leaflet_map.setView([35.0456, -85.2672], 11);"
            style="
                position: absolute;
                top: 80px;
                left: 10px;
                z-index: 1000;
                background: white;
                border: 2px solid rgba(0,0,0,0.2);
                border-radius: 4px;
                padding: 5px 10px;
                cursor: pointer;
            "
            title="Reset view"
        >
            <i class="fa fa-home"></i>
        </button>
    '''
    m.get_root().html.add_child(folium.Element(reset_button_html))

    # Add custom layer control
    folium.LayerControl(
        position='topright',
        collapsed=False
    ).add_to(m)

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

    # Center the map on the entered address
    m.location = [lat, lon]
    m.zoom_start = 13

    return m