import folium
from folium import plugins

def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
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

    # Add layer control
    folium.LayerControl().add_to(m)

    # Add user location marker
    folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Add polling place marker
    polling_coords = [35.0867, -85.2819]  # Example coordinates
    folium.Marker(
        polling_coords,
        popup=f"Polling Place:<br>{district_info['polling_place']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

    # Mock GeoJSON for district boundary (replace with actual data)
    district_geojson = {
        "type": "Feature",
        "properties": {
            "district": district_info['district_number'],
            "style": {
                "fillColor": "#1E88E5",
                "color": "#1E88E5",
                "weight": 2,
                "fillOpacity": 0.3
            }
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-85.27, 35.08],
                [-85.26, 35.08],
                [-85.26, 35.09],
                [-85.27, 35.09],
                [-85.27, 35.08]
            ]]
        }
    }

    # Add district boundary with hover effect
    folium.GeoJson(
        district_geojson,
        style_function=lambda x: x['properties']['style'],
        highlight_function=lambda x: {
            'fillColor': '#3949AB',
            'color': '#3949AB',
            'fillOpacity': 0.5,
            'weight': 3
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['district'],
            aliases=['District:'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        )
    ).add_to(m)

    return m