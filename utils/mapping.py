import folium
from folium import plugins
from utils.district_data import get_district_boundaries
from utils.geocoding import geocode_address

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

    # Get polling place coordinates
    polling_coords = geocode_address(district_info['polling_address'])
    if polling_coords:
        polling_lat, polling_lon = polling_coords
        folium.Marker(
            [polling_lat, polling_lon],
            popup=f"Polling Place:<br>{district_info['polling_place']}<br>{district_info['polling_address']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(markers_group)

    # Get district boundaries
    district_boundaries = get_district_boundaries()
    district_geojson = district_boundaries.get(district_info['district_number'])

    if district_geojson:
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