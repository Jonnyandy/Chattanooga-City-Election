import trafilatura
import requests
from typing import Dict, Optional
import re
from bs4 import BeautifulSoup
import streamlit as st

def search_candidate_website(candidate_name: str, district: str) -> Optional[str]:
    """
    Search for a candidate's official campaign website or social media profile
    Returns the most relevant URL found
    """
    try:
        # Clean the candidate name for search
        clean_name = candidate_name.replace('"', '').replace('(', '').replace(')', '')
        search_query = f"{clean_name} chattanooga city council district {district} 2025"

        # Use DuckDuckGo as search engine
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        search_url = f"https://duckduckgo.com/html/?q={search_query}"

        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for results
        results = soup.find_all('a', {'class': 'result__url'}, limit=5)

        # Social media profiles we want to include
        valid_domains = [
            'facebook.com', 
            'twitter.com',
            'instagram.com',
            'linkedin.com',
            'vote411.org',
            'ballotpedia.org'
        ]

        for result in results:
            url = result.get('href', '')

            # Accept campaign websites or valid social media profiles
            if any(domain in url.lower() for domain in valid_domains) or verify_campaign_website(url, clean_name):
                return url

        return None

    except Exception as e:
        st.error(f"Error searching for {candidate_name}'s website: {str(e)}")
        return None

def verify_campaign_website(url: str, candidate_name: str) -> bool:
    """
    Verify if a URL is likely to be a campaign website
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return False

        text = trafilatura.extract(downloaded)
        if not text:
            return False

        # Check if it's a campaign website
        campaign_keywords = [
            'campaign', 'elect', 'vote', 'city council', 
            'district', 'chattanooga', 'platform', 'candidate',
            'election', '2025', 'leadership'
        ]

        text_lower = text.lower()
        name_parts = candidate_name.lower().split()

        # Count how many keywords are present
        keyword_matches = sum(1 for keyword in campaign_keywords if keyword in text_lower)
        name_matches = sum(1 for part in name_parts if part in text_lower)

        # Return True if we find enough matches
        return keyword_matches >= 2 and name_matches >= 1

    except Exception:
        return False

def get_candidate_info() -> Dict[str, Dict[str, Dict[str, str]]]:
    """
    Get information about all candidates including their websites
    """
    candidates = {
        "1": {
            "James \"Skip\" Burnette": {},
            "Chip Henderson": {}
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
            "Dennis Clark": {},
            "Cory Hall": {},
            "Isiah (Ike) Hester": {},
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
            "Anna Golladay": {},
            "Marvene Noel": {},
            "Doll Sandridge": {},
            "Kelvin Scott": {}
        },
        "9": {
            "Ron Elliott": {},
            "Letechia Ellis": {},
            "Evelina Irén Kertay": {}
        }
    }

    # Search for websites for each candidate
    for district, district_candidates in candidates.items():
        for candidate_name in district_candidates.keys():
            try:
                website = search_candidate_website(candidate_name, district)
                if website:
                    candidates[district][candidate_name]['website'] = website
                    st.info(f"Found website for {candidate_name}: {website}")
            except Exception as e:
                st.error(f"Error processing candidate {candidate_name}: {str(e)}")
                continue

    return candidates

if __name__ == "__main__":
    # Test the scraper
    candidate_info = get_candidate_info()
    print("Found candidate information:")
    for district, candidates in candidate_info.items():
        print(f"\nDistrict {district}:")
        for name, info in candidates.items():
            print(f"  {name}: {info.get('website', 'No website found')}")