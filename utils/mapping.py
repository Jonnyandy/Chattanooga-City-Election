import folium
from folium import plugins
from utils.district_data import get_district_boundaries, get_council_member
from utils.geocoding import geocode_address

def create_base_district_map() -> folium.Map:
    """
    Create a base map showing all Chattanooga districts with animated transitions
    """
    # Create base map centered on Chattanooga
    m = folium.Map(
        location=[35.0456, -85.2672],  # Chattanooga center coordinates
        zoom_start=11,  # Adjusted zoom to show all districts
        tiles="cartodbpositron",
        zoom_control=True,
        smooth_factor=3.0  # Add native smooth factor for better animations
    )

    # Add fullscreen option
    plugins.Fullscreen().add_to(m)

    # Get all district boundaries
    district_boundaries = get_district_boundaries()

    # Color palette matching the reference code
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', 
              '#911eb4', '#42d4f4', '#f032e6', '#bfef45']

    # Add districts with different colors and animations
    for i, (district_name, district_geojson) in enumerate(district_boundaries.items()):
        color = colors[i % len(colors)]  # Cycle through colors if more districts than colors

        # Get council member information
        council_info = get_council_member(district_name)

        # Enhanced style function with transition animations
        style_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 1,
            'fillOpacity': 0.5,
            'opacity': 1,
            'dashArray': None,
            'className': 'district-polygon',  # Add class for CSS animations
            'transition': 'all 0.3s ease-in-out'  # Add transition property
        }

        # Enhanced highlight function with smooth transitions
        highlight_function = lambda x, color=color: {
            'fillColor': color,
            'color': 'white',
            'weight': 2,
            'fillOpacity': 0.7,
            'opacity': 1,
            'className': 'district-polygon-highlight'
        }

        # Create tooltip with district and council member information
        tooltip_html = f"""
        <div class="district-tooltip" style="
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            font-family: Arial;
            font-size: 12px;
            min-width: 200px;
            transition: opacity 0.3s ease-in-out;
        ">
            <strong>District {district_name}</strong><br>
            <strong>Council Member:</strong> {council_info['name']}<br>
            {district_geojson['properties'].get('description', '')}
        </div>
        """

        # Add district boundary with interactive features
        g = folium.GeoJson(
            district_geojson,
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=folium.Tooltip(tooltip_html),
            popup=folium.Popup(tooltip_html, max_width=300),
            control=False,
            overlay=True,
            show=True
        )
        g.add_to(m)

    # Add custom CSS for animations
    custom_css = """
    <style>
        .district-polygon {
            transition: all 0.3s ease-in-out !important;
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
    </style>
    """
    m.get_root().html.add_child(folium.Element(custom_css))

    return m

def create_district_map(lat: float, lon: float, district_info: dict) -> folium.Map:
    """
    Create an interactive map highlighting the user's district with animations
    """
    # Start with the base map
    m = create_base_district_map()

    # Add marker for the entered address with bounce animation
    marker = folium.Marker(
        [lat, lon],
        popup="Your Location",
        icon=folium.Icon(color="red", icon="info-sign")
    )
    marker.add_to(m)

    # Add smooth zoom animation to marker
    plugins.MarkerCluster(markers=[marker], options={
        'showCoverageOnHover': False,
        'zoomToBoundsOnClick': True,
        'spiderfyOnMaxZoom': False,
        'animate': True
    }).add_to(m)

    # Center the map on the entered address with smooth animation
    m.location = [lat, lon]
    m.zoom_start = 13

    return m