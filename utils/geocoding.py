import re
from functools import lru_cache
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import streamlit as st
from typing import List, Optional, Tuple
from time import sleep

def validate_address(address: str) -> bool:
    """
    Validate if the input address follows the expected format for Chattanooga
    """
    if not address:
        return False

    # Check for ZIP code
    zip_match = re.search(r'\b\d{5}\b', address)
    if not zip_match:
        return False

    zip_code = zip_match.group()

    # Verify it's a Chattanooga ZIP
    chattanooga_zips = {'37401', '37402', '37403', '37404', '37405', '37406', 
                       '37407', '37408', '37409', '37410', '37411', '37412', 
                       '37415', '37416', '37419', '37421', '37450', '37351'}

    return zip_code in chattanooga_zips

def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert address to coordinates
    """
    try:
        # Clean address
        address = ' '.join(address.split())

        # Add location context if missing
        if "chattanooga" not in address.lower():
            address = f"{address}, Chattanooga, TN"
        elif "tn" not in address.lower() and "tennessee" not in address.lower():
            address = f"{address}, TN"

        # Initialize geocoder
        geolocator = Nominatim(user_agent="chattanooga_voting_info")

        # Try geocoding
        location = geolocator.geocode(
            address,
            timeout=10,
            exactly_one=True,
            country_codes=['us']
        )

        if location:
            # Verify coordinates are in Chattanooga area
            if 34.9 <= location.latitude <= 35.2 and -85.4 <= location.longitude <= -85.1:
                return location.latitude, location.longitude

        return None

    except Exception as e:
        st.error("Unable to process address. Please try again.")
        return None