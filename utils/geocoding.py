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
    Returns True if the address is valid, False otherwise
    """
    # Check for empty or None input
    if not address or not isinstance(address, str):
        return False

    # Convert multiple spaces to single space and strip
    address = ' '.join(address.split())

    # Extract components from the address
    # Look for 5-digit ZIP code anywhere in the address
    zip_match = re.search(r'\b\d{5}\b', address)
    if not zip_match:
        st.error("Please include a valid 5-digit ZIP code")
        return False

    zip_code = zip_match.group()

    # Check for street number at the start of any part
    has_street_number = bool(re.search(r'\b\d+\s+[A-Za-z]', address))
    if not has_street_number:
        st.error("Please include a street number at the start of your address")
        return False

    # Verify it's a Chattanooga ZIP
    chattanooga_zips = {'37401', '37402', '37403', '37404', '37405', '37406', 
                       '37407', '37408', '37409', '37410', '37411', '37412', 
                       '37415', '37416', '37419', '37421', '37450', '37351'}

    if zip_code not in chattanooga_zips:
        st.error(f"ZIP code {zip_code} is not a valid Chattanooga ZIP code")
        return False

    return True

def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert address to coordinates with retry mechanism and improved error handling
    Returns tuple of (latitude, longitude) or None if geocoding fails
    """
    try:
        # Clean and format the address
        address = ' '.join(address.split())  # Normalize whitespace

        # Add state if not present
        if "tn" not in address.lower() and "tennessee" not in address.lower():
            address = f"{address}, TN"

        # Add city if not present
        if "chattanooga" not in address.lower():
            address = f"{address}, Chattanooga"

        # Print debug information
        st.debug(f"Attempting to geocode address: {address}")

        max_retries = 3
        timeout = 20  # Increased timeout
        delay_between_retries = 2  # seconds

        geolocator = Nominatim(user_agent="chattanooga_voting_info")

        for attempt in range(max_retries):
            try:
                # Try with the full address
                location = geolocator.geocode(
                    address,
                    timeout=timeout,
                    exactly_one=True,
                    country_codes=['us']
                )

                if location:
                    # Verify coordinates are roughly in Chattanooga area
                    if 34.9 <= location.latitude <= 35.2 and -85.4 <= location.longitude <= -85.1:
                        st.success("Address found successfully!")
                        return location.latitude, location.longitude
                    else:
                        st.error("The provided address appears to be outside of Chattanooga city limits.")
                        return None

                # If we get here, the address wasn't found
                if attempt == max_retries - 1:
                    st.error(
                        "Could not find this address. Please verify:\n"
                        "1. Street number is correct\n"
                        "2. Street name is spelled correctly\n"
                        "3. ZIP code is valid for Chattanooga"
                    )
                else:
                    # Wait before retry
                    sleep(delay_between_retries)

            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                if attempt == max_retries - 1:
                    st.error(
                        "Unable to connect to the geocoding service. Please try again in a few moments.\n"
                        "If the problem persists:\n"
                        "1. Check your internet connection\n"
                        "2. Try a different address format\n"
                        "3. Contact support if the issue continues"
                    )
                    return None

                sleep(min(2 ** attempt, 8))  # Exponential backoff
                continue

        return None

    except Exception as e:
        st.error(
            f"Error processing address: {str(e)}\n"
            "Please make sure you've entered a valid Chattanooga address with:\n"
            "1. Street number\n"
            "2. Street name\n"
            "3. ZIP code"
        )
        return None