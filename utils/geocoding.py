import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def validate_address(address: str) -> bool:
    """
    Validate if the input address contains a street address and ZIP code
    """
    # Basic pattern matching for address format: street address + ZIP code
    address_pattern = r'^[\w\s\.-]+.*\b\d{5}\b'
    if not re.search(address_pattern, address, re.IGNORECASE):
        return False

    return True

def geocode_address(address: str) -> tuple:
    """
    Convert address to coordinates
    """
    # Append Chattanooga, TN if not present
    if not "chattanooga" in address.lower():
        address = f"{address}, Chattanooga, TN"

    geolocator = Nominatim(user_agent="chattanooga_voting_info")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None
    except GeocoderTimedOut:
        return None