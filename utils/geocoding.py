import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import streamlit as st
from time import sleep
from typing import Optional, Tuple

def validate_address(address: str) -> bool:
    """
    Validate if the input address contains a street address and ZIP code
    More lenient pattern to accept various address formats
    """
    # More lenient pattern that accepts various address formats
    address_pattern = r'.*\b\d{5}\b'
    if not re.search(address_pattern, address, re.IGNORECASE):
        return False
    return True

def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert address to coordinates with retry mechanism and improved address handling
    Returns tuple of (latitude, longitude) or None if geocoding fails
    """
    # Clean and format the address
    address = address.strip()

    # Add state if not present
    if "tn" not in address.lower() and "tennessee" not in address.lower():
        address = f"{address}, TN"

    # Add city if not present
    if "chattanooga" not in address.lower():
        address = f"{address}, Chattanooga"

    max_retries = 3
    timeout = 15  # Increased timeout

    geolocator = Nominatim(user_agent="chattanooga_voting_info")

    for attempt in range(max_retries):
        try:
            # Try with the full address first
            location = geolocator.geocode(
                address,
                timeout=timeout,
                exactly_one=True,
                country_codes=['us']
            )

            if location:
                # Verify coordinates are roughly in Chattanooga area
                if 34.9 <= location.latitude <= 35.2 and -85.4 <= location.longitude <= -85.1:
                    return location.latitude, location.longitude
                else:
                    if attempt == max_retries - 1:
                        st.error("The address appears to be outside of Chattanooga city limits.")
                    return None

            if attempt == max_retries - 1:
                st.error(
                    "Could not find this address. Please ensure you've entered a valid Chattanooga address "
                    "including street number, street name, and ZIP code."
                )
            return None

        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt == max_retries - 1:
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
            st.error(
                "There was an error processing your address. Please make sure you've entered "
                "a valid Chattanooga address with a street number, name, and ZIP code."
            )
            return None

    return None