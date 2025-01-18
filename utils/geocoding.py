import re
from functools import lru_cache
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import streamlit as st
from typing import List, Optional, Tuple
from time import sleep

def get_address_suggestions(partial_address: str) -> List[str]:
    """Get address suggestions for Hamilton County addresses"""
    if not partial_address or len(partial_address.strip()) < 3:
        return []

    try:
        # Add Hamilton County, TN if not present
        if 'hamilton' not in partial_address.lower():
            partial_address += ' Hamilton County TN'

        geolocator = Nominatim(user_agent="chattanooga_voting_info")
        locations = geolocator.geocode(
            partial_address,
            exactly_one=False,
            country_codes=['us'],
            viewbox=(-85.4, 34.9, -85.1, 35.2),  # Chattanooga area bounding box
            bounded=True
        )

        if not locations:
            return []

        suggestions = []
        for location in locations:
            if location.address:
                # Only include addresses in Chattanooga area
                if 'Chattanooga' in location.address:
                    suggestions.append(location.address)

        return suggestions[:5]  # Limit to 5 suggestions
    except Exception as e:
        st.error(f"Error getting address suggestions: {str(e)}")
        return []

def validate_address(address: str) -> bool:
    """
    Validate if the input address follows the expected format for Chattanooga
    Returns True if the address is valid, False otherwise
    """
    # Check for empty or None input
    if not address or not isinstance(address, str):
        return False

    # Extract components from the address
    # Look for 5-digit ZIP code anywhere in the address
    zip_match = re.search(r'\b\d{5}\b', address)
    if not zip_match:
        return False

    zip_code = zip_match.group()

    # Check for street number at the start of any part
    has_street_number = bool(re.search(r'\b\d+\s+[A-Za-z]', address))
    if not has_street_number:
        return False

    # Verify it's a Chattanooga ZIP
    chattanooga_zips = {'37401', '37402', '37403', '37404', '37405', '37406', 
                       '37407', '37408', '37409', '37410', '37411', '37412', 
                       '37415', '37416', '37419', '37421', '37450', '37351'}

    if zip_code not in chattanooga_zips:
        return False

    return True

def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert address to coordinates with retry mechanism and improved error handling
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