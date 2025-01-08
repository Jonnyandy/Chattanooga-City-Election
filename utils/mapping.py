import folium

def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
    """
    Create an interactive map with district boundaries and markers
    """
    # Create base map centered on location
    m = folium.Map(
        location=[lat, lon],
        zoom_start=13,
        tiles="cartodbpositron"
    )
    
    # Add marker for user location
    folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)
    
    # Add marker for polling place
    # In real implementation, would geocode polling place address
    folium.Marker(
        [35.0867, -85.2819],
        popup=f"Polling Place:<br>{district_info['polling_place']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    
    # Add district boundary
    # In real implementation, would load GeoJSON for district boundaries
    
    return m
