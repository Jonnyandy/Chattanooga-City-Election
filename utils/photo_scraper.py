import requests
from bs4 import BeautifulSoup
from pathlib import Path
import streamlit as st
from PIL import Image
from io import BytesIO
import os

def create_photo_directory():
    """Create directory for storing candidate photos if it doesn't exist"""
    photo_dir = Path('assets/candidate_photos')
    photo_dir.mkdir(parents=True, exist_ok=True)
    return photo_dir

def save_photo(image_url: str, candidate_name: str) -> str:
    """Download and save candidate photo"""
    try:
        photo_dir = create_photo_directory()
        file_name = f"{candidate_name.replace(' ', '_')}.jpg"
        file_path = photo_dir / file_name

        # Check if photo already exists
        if file_path.exists():
            return str(file_path)

        # Download image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Open and process image
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if too large while maintaining aspect ratio
            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(file_path, 'JPEG', quality=85, optimize=True)
            return str(file_path)
        
        return None

    except Exception as e:
        st.error(f"Error saving photo for {candidate_name}: {str(e)}")
        return None

def scrape_candidate_photo(candidate_name: str, social_links: list) -> str:
    """
    Attempt to scrape candidate photo from their social media profiles
    Returns the path to the saved photo or None if unsuccessful
    """
    try:
        # Check if photo already exists
        photo_dir = create_photo_directory()
        file_path = photo_dir / f"{candidate_name.replace(' ', '_')}.jpg"
        
        if file_path.exists():
            return str(file_path)

        # Try each social media link
        for url in social_links:
            if not url:
                continue

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Look for profile images
                    img_selectors = [
                        'img[class*="profile"]',
                        'img[class*="avatar"]',
                        'img[class*="photo"]',
                        'img[alt*="profile"]',
                        'img[alt*="' + candidate_name + '"]'
                    ]
                    
                    for selector in img_selectors:
                        images = soup.select(selector)
                        for img in images:
                            src = img.get('src', '')
                            if src and (src.startswith('http') or src.startswith('//')):
                                if src.startswith('//'):
                                    src = 'https:' + src
                                photo_path = save_photo(src, candidate_name)
                                if photo_path:
                                    return photo_path
            
            except Exception as e:
                st.error(f"Error scraping from {url}: {str(e)}")
                continue

        return None

    except Exception as e:
        st.error(f"Error in photo scraping for {candidate_name}: {str(e)}")
        return None

def get_candidate_photo(candidate_name: str, social_links: list) -> str:
    """Get candidate photo path, attempting to scrape if not already available"""
    photo_dir = create_photo_directory()
    file_path = photo_dir / f"{candidate_name.replace(' ', '_')}.jpg"
    
    if file_path.exists():
        return str(file_path)
    
    return scrape_candidate_photo(candidate_name, social_links)
