import trafilatura
import requests
from bs4 import BeautifulSoup
import streamlit as st
from typing import Dict, Optional
import re
from datetime import datetime, date

def validate_name(name: str) -> bool:
    """Validate name format"""
    if not name:
        return False
    # Check for valid name format (letters, spaces, hyphens, and apostrophes only)
    return bool(re.match(r"^[A-Za-z\s\-']+$", name.strip()))

def validate_dob(dob_str: str) -> bool:
    """Validate date of birth"""
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Check if person is at least 18 years old and not unreasonably old
        return 18 <= age <= 120
    except ValueError:
        return False

def verify_voter_registration(first_name: str, last_name: str, date_of_birth: str) -> Dict[str, str]:
    """
    Verify voter registration status using validation checks
    Returns a dictionary with registration status and additional information
    """
    try:
        # Input validation
        if not all([first_name, last_name, date_of_birth]):
            return {
                "status": "error",
                "message": "Please fill in all required fields"
            }

        # Validate names
        if not validate_name(first_name) or not validate_name(last_name):
            return {
                "status": "error",
                "message": "Please enter valid names using only letters, spaces, hyphens, and apostrophes"
            }

        # Validate date of birth
        if not validate_dob(date_of_birth):
            return {
                "status": "error",
                "message": "Invalid date of birth. You must be at least 18 years old to register to vote"
            }

        # Format names for consistency
        first_name = first_name.strip().title()
        last_name = last_name.strip().title()

        # In a real implementation, this would make an API call to the voter registration system
        # For this prototype, we'll implement some basic checks

        # Example validation: Names shouldn't be too short
        if len(first_name) < 2 or len(last_name) < 2:
            return {
                "status": "error",
                "message": "Please enter your complete legal name"
            }

        # Example: Detect test/dummy data
        test_names = {"test", "john", "jane", "doe", "smith"}
        if first_name.lower() in test_names and last_name.lower() in test_names:
            return {
                "status": "error",
                "message": "Unable to verify registration. Please ensure you're entering your legal name as it appears on your ID"
            }

        # For demonstration, we'll return a "not found" response
        # In production, this would be replaced with actual API verification
        return {
            "status": "success",
            "registered": "not_found",
            "message": "We couldn't find a voter registration matching this information.",
            "additional_info": """
            If you believe this is an error, you can:
            1. Verify your information is entered exactly as it appears on your ID
            2. Contact the Hamilton County Election Commission at (423) 493-5100
            3. Visit GoVoteTN.gov to check your registration status or register to vote
            """
        }

    except Exception as e:
        st.error(f"Error checking voter registration: {str(e)}")
        return {
            "status": "error",
            "message": "Unable to verify registration. Please try again later or contact the Election Commission."
        }