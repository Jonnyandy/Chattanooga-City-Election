import streamlit as st
from typing import Dict
from datetime import datetime, date
import re

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
        return 18 <= age <= 120
    except ValueError:
        return False

def verify_voter_registration(first_name: str, last_name: str, date_of_birth: str) -> Dict[str, str]:
    """
    Redirect users to the official TN voter registration verification system
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

        return {
            "status": "redirect",
            "message": """
            To check your voter registration status, please visit the official Tennessee voter lookup tool:

            [Click here to verify your registration](https://tnmap.tn.gov/voterlookup/)

            This official tool provides the most accurate and up-to-date information about your voter registration status.

            If you need assistance, you can:
            1. Contact the Hamilton County Election Commission at (423) 493-5100
            2. Visit their office at 700 River Terminal Rd, Chattanooga, TN 37406
            3. Email them at vote@hamiltontn.gov
            """
        }

    except Exception as e:
        st.error(f"Error in voter verification process: {str(e)}")
        return {
            "status": "error",
            "message": "Unable to process your request. Please try again later or contact the Election Commission directly."
        }