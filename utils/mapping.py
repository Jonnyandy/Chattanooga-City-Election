import folium
from folium import plugins
from utils.district_data import get_district_boundaries, get_council_member, get_district_info
from utils.geocoding import geocode_address
import pandas as pd
from pathlib import Path

def create_polling_markers(m: folium.Map):
    """Add polling location markers to the map with interactive tooltips"""
    try:
        polling_places_path = Path('assets/polling_places.csv')
        if not polling_places_path.exists():
            return

        df = pd.read_csv(polling_places_path)

        # Create a marker cluster group for polling locations
        marker_cluster = plugins.MarkerCluster(
            name='Polling Locations',
            overlay=True,
            control=True,
            icon_create_function='''
                function(cluster) {
                    return L.divIcon({
                        html: '<div class="polling-cluster">' + cluster.getChildCount() + '</div>',
                        className: 'marker-cluster marker-cluster-large',
                        iconSize: new L.Point(40, 40)
                    });
                }
            '''
        )

        # Add markers for each polling location
        for _, place in df.iterrows():
            address = f"{place['address']}, {place['city']}, {place['state']} {place['zip']}"
            coords = geocode_address(address)

            if coords:
                lat, lon = coords

                # Create detailed HTML for the tooltip
                tooltip_html = f"""
                <div class="polling-tooltip" style="
                    background-color: white;
                    padding: 12px;
                    border-radius: 6px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    font-family: Arial, sans-serif;
                    font-size: 13px;
                    min-width: 200px;
                ">
                    <h4 style="margin: 0 0 8px 0; color: #1976D2;">{place['location_name']}</h4>
                    <strong>Address:</strong><br>
                    {place['address']}<br>
                    {place['city']}, {place['state']} {place['zip']}<br>
                    <strong>Precinct:</strong> {place['precinct']}<br>
                    <div style="margin-top: 8px; font-size: 12px; color: #666;">
                        Click for more information
                    </div>
                </div>
                """

                # Create detailed HTML for the popup
                popup_html = f"""
                <div style="
                    min-width: 200px;
                    max-width: 300px;
                    padding: 15px;
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                ">
                    <h3 style="margin: 0 0 10px 0; color: #1976D2;">{place['location_name']}</h3>
                    <div style="margin-bottom: 10px;">
                        <strong>Address:</strong><br>
                        {place['address']}<br>
                        {place['city']}, {place['state']} {place['zip']}
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>Precinct:</strong> {place['precinct']}<br>
                        <strong>Hours:</strong> See early voting section for details
                    </div>
                    <hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;">
                    <div style="font-size: 13px; color: #666;">
                        <strong>Important:</strong><br>
                        • Bring valid PHOTO ID<br>
                        • Check eligibility requirements<br>
                        • Confirm your registration status
                    </div>
                </div>
                """

                # Create marker with custom icon
                icon = folium.Icon(
                    color='red',
                    icon='info-sign',
                    prefix='fa'
                )

                marker = folium.Marker(
                    location=[lat, lon],
                    tooltip=folium.Tooltip(tooltip_html),
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=icon
                )
                marker.add_to(marker_cluster)

        marker_cluster.add_to(m)

        # Add custom CSS for marker clusters
        custom_css = """
        <style>
            .polling-cluster {
                background-color: #1976D2;
                color: white;
                border-radius: 50%;
                text-align: center;
                line-height: 40px;
                font-weight: bold;
                font-family: Arial, sans-serif;
            }
            .polling-tooltip {
                opacity: 0;
                transform: translateY(10px);
                transition: all 0.3s ease-in-out;
            }
            .polling-tooltip:hover {
                opacity: 1;
                transform: translateY(0);
            }
        </style>
        """
        m.get_root().html.add_child(folium.Element(custom_css))

    except Exception as e:
        print(f"Error adding polling markers: {str(e)}")

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

    # Add zoom home button
    plugins.Home(
        position='topleft',
        home_coordinates=[35.0456, -85.2672],
        home_zoom=11
    ).add_to(m)

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

        style_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 1,
            'fillOpacity': 0.5,
            'opacity': 1,
            'dashArray': None,
            'className': 'district-polygon'
        }

        highlight_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 1,
            'className': 'district-polygon-highlight'
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
            transition: opacity 0.3s ease-in-out;
        ">
            <h4 style="margin: 0 0 8px 0; color: #1976D2;">District {district_name}</h4>
            <strong>Council Member:</strong> {council_info['name']}<br>
            {district_geojson['properties'].get('description', '')}<br>
            <div style="margin-top: 5px; font-size: 11px; color: #666;">
                <em>Click to zoom to district</em>
            </div>
        </div>
        """

        # Enhanced popup with more detailed information
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
                • Click anywhere to return to full map<br>
                • Use mouse wheel to zoom in/out<br>
                • Drag to pan the map
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

        # Add click event for zooming to district
        g.add_child(folium.Element(f"""
            <script>
                var layer = document.querySelector('path.district-polygon:last-child');
                layer.addEventListener('click', function (e) {{
                    var bounds = e.target._bounds;
                    map.fitBounds(bounds, {{
                        padding: [50, 50],
                        maxZoom: 14,
                        animation: true,
                        duration: 1
                    }});
                }});
            </script>
        """))

        g.add_to(districts_group)

    # Add districts group to map
    districts_group.add_to(m)

    # Add polling location markers
    create_polling_markers(m)

    # Add custom layer control
    folium.LayerControl(
        position='topright',
        collapsed=False
    ).add_to(m)

    # Add custom CSS for animations and interactivity
    custom_css = """
    <style>
        .district-polygon {
            transition: all 0.3s ease-in-out !important;
            cursor: pointer;
        }
        .district-polygon:hover {
            transform: scale(1.01);
            transition: all 0.3s ease-in-out !important;
        }
        .district-tooltip {
            opacity: 0;
            transform: translateY(10px);
            transition: all 0.3s ease-in-out !important;
        }
        .district-tooltip:hover {
            opacity: 1;
            transform: translateY(0);
        }
        .leaflet-popup-content-wrapper {
            border-radius: 8px;
            box-shadow: 0 3px 14px rgba(0,0,0,0.2);
        }
        .leaflet-popup-content {
            margin: 0;
            padding: 0;
        }
        .home {
            background-color: white;
            border: 2px solid rgba(0,0,0,0.2);
            border-radius: 4px;
            padding: 5px;
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    return m

def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
    """Create an interactive map highlighting the user's district with animations"""
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