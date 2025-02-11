import os
from pathlib import Path
import streamlit as st
from PIL import Image
import shutil
from typing import Optional, Union
import requests
from bs4 import BeautifulSoup

def create_photo_directory() -> Path:
    """Create directory for storing candidate photos if it doesn't exist"""
    photo_dir = Path('assets/candidate_photos')
    photo_dir.mkdir(parents=True, exist_ok=True)
    return photo_dir

def process_candidate_photo(source_path: Union[str, Path], candidate_name: str) -> Optional[str]:
    """Process and save candidate photo from source path"""
    try:
        photo_dir = create_photo_directory()
        file_name = f"{candidate_name.replace(' ', '_')}.jpg"
        target_path = photo_dir / file_name

        # Check if photo already exists
        if target_path.exists():
            return str(target_path)

        source_path = Path(source_path)
        if not source_path.exists():
            st.error(f"Source photo not found: {source_path}")
            return None

        # Copy and convert if needed
        if source_path.suffix.lower() in ['.jpg', '.jpeg']:
            shutil.copy2(source_path, target_path)
        else:
            # For AVIF or other formats, convert to JPEG
            try:
                img = Image.open(source_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Resize if too large while maintaining aspect ratio
                max_size = (800, 800)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save as optimized JPEG
                img.save(target_path, 'JPEG', quality=85, optimize=True)
            except Exception as e:
                st.error(f"Error converting image for {candidate_name}: {str(e)}")
                return None

        return str(target_path)

    except Exception as e:
        st.error(f"Error processing photo for {candidate_name}: {str(e)}")
        return None

def get_candidate_photo(candidate_name: str) -> Optional[str]:
    """Get candidate photo path, checking attached_assets first"""
    # Check for photo in attached_assets
    possible_extensions = ['.avif', '.jpg', '.jpeg', '.png']
    name_variants = [
        candidate_name.replace(' ', '-'),
        candidate_name.replace(' ', '_'),
        candidate_name.lower().replace(' ', '-'),
        candidate_name.lower().replace(' ', '_')
    ]

    for name in name_variants:
        for ext in possible_extensions:
            # Check different name patterns
            patterns = [
                f"{name}{ext}",
                f"{name}-District-{candidate_district}{ext}" if 'candidate_district' in locals() else None,
                f"{name}-D{candidate_district}{ext}" if 'candidate_district' in locals() else None
            ]

            for pattern in patterns:
                if not pattern:
                    continue

                source_path = Path('attached_assets') / pattern
                if source_path.exists():
                    return process_candidate_photo(source_path, candidate_name)

    # If no photo found in attached_assets, check assets/candidate_photos
    photo_dir = create_photo_directory()
    file_name = f"{candidate_name.replace(' ', '_')}.jpg"
    photo_path = photo_dir / file_name

    if photo_path.exists():
        return str(photo_path)

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
                                photo_path = process_candidate_photo(src, candidate_name)
                                if photo_path:
                                    return photo_path

            except Exception as e:
                st.error(f"Error scraping from {url}: {str(e)}")
                continue

        return None

    except Exception as e:
        st.error(f"Error in photo scraping for {candidate_name}: {str(e)}")
        return None

def get_candidate_photo_old(candidate_name: str, social_links: list) -> str:
    """Get candidate photo path, attempting to scrape if not already available"""
    photo_dir = create_photo_directory()
    file_path = photo_dir / f"{candidate_name.replace(' ', '_')}.jpg"

    if file_path.exists():
        return str(file_path)

    return scrape_candidate_photo(candidate_name, social_links)