import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def validate_address(address: str) -> bool:
    """
    Validate if the input address is in Chattanooga
    """
    # Basic pattern matching for address format
    address_pattern = r'^[\w\s\.-]+,?\s*Chattanooga,?\s*TN'
    if not re.search(address_pattern, address, re.IGNORECASE):
        return False
    
    return True

def geocode_address(address: str) -> tuple:
    """
    Convert address to coordinates
    """
    geolocator = Nominatim(user_agent="chattanooga_voting_info")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        return None
