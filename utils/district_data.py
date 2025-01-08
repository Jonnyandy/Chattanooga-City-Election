import pandas as pd

def get_district_info(lat: float, lon: float) -> dict:
    """
    Get district information based on coordinates
    """
    # In a real implementation, this would query a spatial database
    # For demo purposes, returning mock data
    return {
        "district_number": "District 5",
        "precinct": "Precinct 54",
        "polling_place": "Brainerd Recreation Center",
        "polling_address": "1010 N Moore Rd, Chattanooga, TN 37411"
    }

def get_council_member(district: str) -> dict:
    """
    Get council member information for a district
    """
    # Load council member data
    df = pd.read_csv('assets/council_members.csv')
    member = df[df['district'] == district].iloc[0]
    
    return {
        "name": member['name'],
        "email": member['email'],
        "phone": member['phone']
    }
