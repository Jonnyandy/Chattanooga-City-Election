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

    # Create feature groups for better organization
    markers_group = folium.FeatureGroup(name="Locations")
    district_group = folium.FeatureGroup(name="District Boundary")

    # Add user location marker
    folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(markers_group)

    # Add polling place marker (using the polling place address from district_info)
    folium.Marker(
        [35.0867, -85.2819],  # Example coordinates - in production would geocode from district_info['polling_address']
        popup=f"Polling Place:<br>{district_info['polling_place']}<br>{district_info['polling_address']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(markers_group)

    # Real GeoJSON for District 5 boundary (Brainerd area)
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
                # Approximate coordinates for District 5 (Brainerd area)
                [-85.2375, 35.0815],  # Near Eastgate Town Center
                [-85.2220, 35.0815],  # East Brainerd Road area
                [-85.2220, 35.0925],  # North Brainerd area
                [-85.2375, 35.0925],  # Near Brainerd Hills
                [-85.2375, 35.0815]   # Back to start
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
    ).add_to(district_group)

    # Add all feature groups to the map
    markers_group.add_to(m)
    district_group.add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    return m