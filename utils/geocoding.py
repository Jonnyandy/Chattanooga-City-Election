import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import streamlit as st
from time import sleep

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
    Convert address to coordinates with retry mechanism
    """
    # Append Chattanooga, TN if not present
    if not "chattanooga" in address.lower():
        address = f"{address}, Chattanooga, TN"

    max_retries = 3
    timeout = 10  # Increased timeout to 10 seconds

    geolocator = Nominatim(user_agent="chattanooga_voting_info")

    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address, timeout=timeout)
            if location:
                return location.latitude, location.longitude

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

            # Wait before retrying (exponential backoff)
            sleep(2 ** attempt)
            continue

        except Exception as e:
            st.error(f"An unexpected error occurred while looking up the address: {str(e)}")
            return None

    return None