
import trafilatura
import requests
from typing import Dict, Optional
import re
from bs4 import BeautifulSoup
import streamlit as st

def get_candidate_info() -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Get information about all candidates including their verified websites
    """
    candidates = {
        "1": {
            "Chip Henderson": {},
            "James \"Skip\" Burnette": {}
        },
        "2": {
            "Jenny Hill": {}
        },
        "3": {
            "Jeff Davis": {},
            "Tom Marshall": {}
        },
        "4": {
            "Cody Harvey": {}
        },
        "5": {
            "Isiah (Ike) Hester": {},
            "Dennis Clark": {},
            "Cory Hall": {},
            "Samantha Reid-Hawkins": {}
        },
        "6": {
            "Jenni Berz": {},
            "Jennifer Gregory": {},
            "Mark Holland": {},
            "Christian Siler": {},
            "Robert C Wilson": {}
        },
        "7": {
            "Raquetta Dotley": {}
        },
        "8": {
            "Marvene Noel": {},
            "Anna Golladay": {},
            "Doll Sandridge": {},
            "Kelvin Scott": {}
        },
        "9": {
            
            "Ron Elliott": {},
            "Letechia Ellis": {},
            "Evelina Irén Kertay": {}
        }
    }

    return candidates

if __name__ == "__main__":
    # Test the candidate info
    candidate_info = get_candidate_info()
    print("Found candidate information:")
    for district, candidates in candidate_info.items():
        print(f"\nDistrict {district}:")
        for name, info in candidates.items():
            print(f"  {name}: {info.get('website', 'No website found')}")
