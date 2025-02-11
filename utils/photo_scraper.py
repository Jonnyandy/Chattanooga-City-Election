import os
from pathlib import Path
import streamlit as st
from PIL import Image
import shutil
from typing import Optional, Union
import subprocess

def create_photo_directory() -> Path:
    """Create directory for storing candidate photos if it doesn't exist"""
    photo_dir = Path('assets/candidate_photos')
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
            st.error(f"Source photo not found: {source_path}")
            return None

        # For AVIF files, first convert to PNG
        if source_path.suffix.lower() == '.avif':
            png_path = convert_avif_to_png(source_path)
            if png_path:
                source_path = png_path

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

            # Clean up temporary PNG if it was created
            if source_path.suffix.lower() == '.png' and source_path.stem.endswith('_temp'):
                source_path.unlink(missing_ok=True)

            return str(target_path)

        except Exception as e:
            st.error(f"Error processing image for {candidate_name}: {str(e)}")
            # If source is already a JPEG, try direct copy
            if source_path.suffix.lower() in ['.jpg', '.jpeg']:
                shutil.copy2(source_path, target_path)
                return str(target_path)
            return None

    except Exception as e:
        st.error(f"Error processing photo for {candidate_name}: {str(e)}")
        return None

def get_candidate_photo(candidate_name: str, district: str = None) -> Optional[str]:
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
                f"{name}-District-{district}{ext}" if district else None,
                f"{name}-D{district}{ext}" if district else None
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