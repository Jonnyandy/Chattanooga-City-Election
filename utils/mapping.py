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
        zoom_start=11,  # Adjusted zoom to show all districts
        tiles="cartodbpositron",
        zoom_control=True
    )

    # Add fullscreen option
    plugins.Fullscreen().add_to(m)

    # Get all district boundaries
    district_boundaries = get_district_boundaries()

    # Color palette matching the reference code
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45']

    # Add districts with different colors
    for i, (district_name, district_geojson) in enumerate(district_boundaries.items()):
        color = colors[i % len(colors)]  # Cycle through colors if more districts than colors

        style_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 1,
            'fillOpacity': 0.5,
            'opacity': 1,
            'dashArray': None,
            'interactive': True
        }

        highlight_function = lambda x, color=color: {
            'fillColor': color,
            'color': '#000000',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 1,
            'dashArray': None
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
            highlight_function=highlight_function,
            tooltip=tooltip_html,
            popup=folium.Popup(tooltip_html, max_width=300),
            control=False,  # Prevents selection rectangle
            overlay=True,   # Ensures proper layering
            show=True      # Always visible
        ).add_to(m)

        # Add district label at the center of each district
        if 'geometry' in district_geojson:
            try:
                # Calculate centroid for label placement
                coordinates = district_geojson['geometry']['coordinates'][0]
                center_lat = sum(coord[1] for coord in coordinates) / len(coordinates)
                center_lon = sum(coord[0] for coord in coordinates) / len(coordinates)

                # Add district number label
                folium.Popup(
                    f"District {district_name}",
                    permanent=True
                ).add_to(folium.CircleMarker(
                    location=[center_lat, center_lon],
                    radius=0,
                    popup=f"District {district_name}",
                    tooltip=f"District {district_name}",
                    color="none",
                    fill=False
                ).add_to(m))
            except Exception as e:
                print(f"Error adding label for district {district_name}: {str(e)}")

    return m

def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
    """
    Create an interactive map highlighting the user's district
    """
    # Start with the base map
    m = create_base_district_map()

    # Add marker for the entered address
    folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    # Center the map on the entered address
    m.location = [lat, lon]
    m.zoom_start = 13

    return m