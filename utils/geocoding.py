import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import streamlit as st
from time import sleep
from typing import Optional, Tuple

def validate_address(address: str) -> bool:
    """
    Validate if the input address contains a street address and ZIP code
    """
    # Enhanced pattern matching for address format
    address_pattern = r'^[\w\s\.-]+.*\b\d{5}\b'
    if not re.search(address_pattern, address, re.IGNORECASE):
        return False
    return True

def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert address to coordinates with retry mechanism
    Returns tuple of (latitude, longitude) or None if geocoding fails
    """
    # Append Chattanooga, TN if not present
    if "chattanooga" not in address.lower():
        address = f"{address}, Chattanooga, TN"

    max_retries = 3
    timeout = 10

    geolocator = Nominatim(user_agent="chattanooga_voting_info")

    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address, timeout=timeout)
            if location:
                return location.latitude, location.longitude

            if attempt == max_retries - 1:  # Only show error on last attempt
                st.error(f"Could not find the address: {address}")
            return None

        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt == max_retries - 1:  # Last attempt
                st.error("""
                Unable to connect to the geocoding service. Please try again in a few moments.
                If the problem persists, you can:
                1. Verify your internet connection
                2. Try a different address format
                3. Contact support if the issue continues
                """)
                return None

            # Wait before retrying with exponential backoff
            sleep(min(2 ** attempt, 8))  # Cap maximum wait time at 8 seconds
            continue

        except Exception as e:
            st.error(f"An unexpected error occurred while looking up the address: {str(e)}")
            return None

    return None