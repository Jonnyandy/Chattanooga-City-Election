import os
from pathlib import Path
import streamlit as st
from PIL import Image
import shutil
from typing import Optional, Union
import subprocess

def create_photo_directory() -> Path:
    """Create directory for storing candidate photos if it doesn't exist"""
    photo_dir = Path('candidate_photos')
    photo_dir.mkdir(parents=True, exist_ok=True)
    return photo_dir

def convert_avif_to_png(avif_path: Path) -> Optional[Path]:
    """Convert AVIF to PNG using system tools"""
    try:
        png_path = avif_path.with_suffix('.png')
        result = subprocess.run(
            ['convert', str(avif_path), str(png_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and png_path.exists():
            return png_path
    except Exception as e:
        st.error(f"Error converting AVIF to PNG: {str(e)}")
    return None

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
            return None

        try:
            # Open and process the image
            img = Image.open(str(source_path))

            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize if too large while maintaining aspect ratio
            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Save as optimized JPEG
            img.save(target_path, 'JPEG', quality=85, optimize=True)
            return str(target_path)

        except Exception as e:
            st.error(f"Error processing image for {candidate_name}: {str(e)}")
            return None

    except Exception as e:
        st.error(f"Error processing photo for {candidate_name}: {str(e)}")
        return None

def get_candidate_photo(candidate_name: str, district: str) -> Optional[str]:
    """Get candidate photo path from various sources"""
    # Clean the candidate name for file matching
    clean_name = candidate_name.replace(' ', '_').replace('"', '').replace("'", "")

    # Check in candidate_photos directory first
    photo_dir = create_photo_directory()
    jpg_path = photo_dir / f"{clean_name}.jpg"
    if jpg_path.exists():
        return str(jpg_path)

    # Check in attached_assets directory
    assets_dir = Path('attached_assets')
    if assets_dir.exists():
        # Try different possible file names and formats
        possible_names = [
            f"{clean_name}.jpg",
            f"{clean_name}.avif",
            f"{clean_name}-District-{district}.jpg",
            f"{clean_name}-District-{district}.avif",
            f"{clean_name}-D{district}.jpg",
            f"{clean_name}-D{district}.avif"
        ]

        for name in possible_names:
            asset_path = assets_dir / name
            if asset_path.exists():
                if asset_path.suffix == '.avif':
                    # Convert AVIF to PNG
                    png_path = convert_avif_to_png(asset_path)
                    if png_path:
                        # Process and store in candidate_photos
                        processed_path = process_candidate_photo(png_path, candidate_name)
                        if processed_path:
                            return processed_path
                else:
                    # Process and store regular image
                    processed_path = process_candidate_photo(asset_path, candidate_name)
                    if processed_path:
                        return processed_path

    return None