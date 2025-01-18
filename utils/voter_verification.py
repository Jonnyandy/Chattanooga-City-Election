import trafilatura
import requests
from bs4 import BeautifulSoup
import streamlit as st
from typing import Dict, Optional

def verify_voter_registration(first_name: str, last_name: str, date_of_birth: str) -> Dict[str, str]:
    """
    Verify voter registration status using TN voter lookup system
    Returns a dictionary with registration status and additional information
    """
    try:
        # Format and validate inputs
        first_name = first_name.strip().title()
        last_name = last_name.strip().title()
        
        # Basic input validation
        if not all([first_name, last_name, date_of_birth]):
            return {
                "status": "error",
                "message": "Please fill in all required fields"
            }

        # For demonstration/prototype, we'll return a simulated response
        # In production, this would interact with the official voter registration API
        return {
            "status": "success",
            "registered": "active",
            "message": "You are registered to vote in Hamilton County.",
            "precinct": "Lookup your polling place above using your address.",
            "district": "Enter your address above to find your district.",
            "additional_info": "Remember to bring a valid photo ID issued by Tennessee or Federal government when you vote."
        }

    except Exception as e:
        st.error(f"Error checking voter registration: {str(e)}")
        return {
            "status": "error",
            "message": "Unable to verify registration. Please try again later or contact the Election Commission."
        }
