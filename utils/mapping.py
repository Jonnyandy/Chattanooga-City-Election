import folium
from folium import plugins
from utils.district_data import get_district_boundaries
from utils.geocoding import geocode_address

def create_base_district_map() -> folium.Map:
    """
    Create a base map showing all Chattanooga districts
    """
    # Create base map centered on Chattanooga
    m = folium.Map(
        location=[35.0456, -85.2672],  # Chattanooga center coordinates
        zoom_start=12,
        tiles="cartodbpositron",
        zoom_control=True
    )

    # Add fullscreen option
    plugins.Fullscreen().add_to(m)

    # Get all district boundaries
    district_boundaries = get_district_boundaries()

    # Color palette for districts
    colors = ['#1E88E5', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB', 
              '#0D47A1', '#1565C0', '#1976D2', '#1E88E5']

    # Add districts with different colors
    for i, (district_name, district_geojson) in enumerate(district_boundaries.items()):
        color = colors[i % len(colors)]

        style_function = lambda x, color=color: {
            'fillColor': color,
            'color': '#1565C0',
            'weight': 2,
            'fillOpacity': 0.4,
            'opacity': 0.8,
            'dashArray': '5, 5'
        }

        # Create tooltip with district information
        tooltip_html = f"""
        <div style="
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            font-family: Arial;
            font-size: 12px;
            min-width: 150px;
        ">
            <strong>District {district_name}</strong><br>
            {district_geojson['properties'].get('description', '')}
        </div>
        """

        # Add district boundary with interactive features
        folium.GeoJson(
            district_geojson,
            style_function=style_function,
            tooltip=folium.GeoJsonTooltip(
                fields=['district', 'description'],
                aliases=['District:', 'Area:'],
                style="""
                    background-color: white;
                    color: #333333;
                    font-family: arial;
                    font-size: 12px;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                """
            )
        ).add_to(m)

    return m

def create_district_map(lat: float, lon: float, district_info: dict, opacity: float = 1.0) -> folium.Map:
    """
    Create an interactive map with district boundaries and markers
    """
    # Create base map centered on location with zoom controls
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles="cartodbpositron",
        zoom_control=True
    )

    # Add fullscreen option
    plugins.Fullscreen().add_to(m)

    # Add custom home button using JavaScript
    home_button_js = """
        function goHome() {
            var map = document.querySelector('#map');
            map.setView([%s, %s], 13);
        }

        // Create custom home button
        var homeButton = L.control({position: 'topleft'});
        homeButton.onAdd = function (map) {
            var div = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
            div.innerHTML = '<a href="#" onclick="goHome(); return false;" title="Return to starting view">🏠</a>';
            return div;
        };
        homeButton.addTo(map);
    """ % (lat, lon)

    # Add the JavaScript to the map
    m.get_root().script.add_child(folium.Element(home_button_js))

    # Create feature groups for better organization
    markers_group = folium.FeatureGroup(name="Locations")
    district_group = folium.FeatureGroup(name="District Boundaries")

    # Add user location marker
    folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(markers_group)

    # Get polling place coordinates
    polling_coords = geocode_address(district_info['polling_address'])
    if polling_coords:
        polling_lat, polling_lon = polling_coords
        folium.Marker(
            [polling_lat, polling_lon],
            popup=f"""
            <div style='width: 200px'>
                <b>Polling Place:</b><br>
                {district_info['polling_place']}<br>
                {district_info['polling_address']}<br>
                <b>Hours:</b> 7:00 AM - 7:00 PM
            </div>
            """,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(markers_group)

    # Get all district boundaries for visualization
    district_boundaries = get_district_boundaries()

    # Add all districts with interactive styling and opacity control
    for district_name, district_geojson in district_boundaries.items():
        # Enhanced styling for the user's district
        is_user_district = district_name == district_info['district_number']

        style_function = lambda x, is_user_district=is_user_district, opacity=opacity: {
            'fillColor': '#1E88E5' if is_user_district else '#64B5F6',
            'color': '#1565C0' if is_user_district else '#2196F3',
            'weight': 3 if is_user_district else 2,
            'fillOpacity': (0.5 if is_user_district else 0.3) * opacity,
            'opacity': opacity,
            'dashArray': None if is_user_district else '5, 5'
        }

        highlight_function = lambda x: {
            'fillColor': '#3949AB',
            'color': '#283593',
            'weight': 4,
            'fillOpacity': 0.7
        }

        # Create tooltip with district information
        tooltip_html = f"""
        <div style="
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            font-family: Arial;
            font-size: 12px;
            min-width: 150px;
        ">
            <strong>{district_name}</strong><br>
            {district_geojson['properties'].get('description', '')}
        </div>
        """

        # Add district boundary with interactive features
        folium.GeoJson(
            district_geojson,
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=folium.GeoJsonTooltip(
                fields=['district', 'description'],
                aliases=['District:', 'Area:'],
                style="""
                    background-color: white;
                    color: #333333;
                    font-family: arial;
                    font-size: 12px;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                """
            ),
            popup=folium.GeoJsonPopup(
                fields=['district', 'description'],
                aliases=['District:', 'Area:'],
                style="""
                    background-color: white;
                    color: #333333;
                    font-family: arial;
                    font-size: 12px;
                    padding: 10px;
                    border-radius: 5px;
                    max-width: 200px;
                """
            )
        ).add_to(district_group)

    # Add all feature groups to the map
    markers_group.add_to(m)
    district_group.add_to(m)

    # Add layer control with collapsed option
    folium.LayerControl(collapsed=False).add_to(m)

    return m