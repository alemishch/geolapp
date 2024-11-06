import os
import requests
from PIL import Image
from io import BytesIO
from typing import List
import streamlit as st

# Configuration
API_BASE_URL = "http://localhost:8000"  
IMAGE_STATIC_URL = f"{API_BASE_URL}/images"  # Endpoint where images are served
PLACEHOLDER_URL = "https://via.placeholder.com/150?text=Image+Not+Found"  # Placeholder image

def get_full_image_url(photo_path):
    """
    Constructs the full URL to access the image based on its relative path.
    
    Args:
        photo_path (str): Relative path to the image stored in the 'photos' table.
        
    Returns:
        str: Full URL to access the image.
    """
    return f"{IMAGE_STATIC_URL}/{photo_path}"

def image_exists(photo_path):
    """
    Checks if the image exists by making a HEAD request.
    
    Args:
        photo_path (str): Relative path to the image.
        
    Returns:
        bool: True if the image exists, False otherwise.
    """
    url = get_full_image_url(photo_path)
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def load_image(photo_path):
    if photo_path and image_exists(photo_path):
        try:
            url = get_full_image_url(photo_path)
            response = requests.get(url)
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except Exception as e:
            st.error(f"Error loading image at {photo_path}: {e}")
            return load_placeholder()
    else:
        return load_placeholder()

def load_placeholder():
    try:
        placeholder_path = "img/placeholder.jpg"  # Path to your local placeholder image
        return Image.open(placeholder_path)
    except Exception as e:
        st.error(f"Error loading placeholder image: {e}")
        return None

def map_photos(photos_data, expected_types):
    """
    Maps each expected photo type to its corresponding path.
    
    Args:
        photos_data (List[dict]): List of photo records fetched from the API.
        expected_types (List[str]): List of expected photo types.
        
    Returns:
        dict: Mapping of photo types to their paths.
    """
    photos_map = {ptype: None for ptype in expected_types}
    for record in photos_data:
        for ptype in expected_types:
            path = record.get(ptype)
            if path:
                # Remove 'img/' prefix if present
                if path.startswith("img/"):
                    path = path[4:]
                photos_map[ptype] = path
    return photos_map

def display_photos(photo_records):
    """
    Displays images based on their types. Shows placeholder if an image is missing.
    
    Args:
        photo_records (List[dict]): List of photo records fetched from the API.
    """
    # Define expected photo types
    EXPECTED_PHOTO_TYPES = ["macro", "straight_light", "reflected_light"]
    
    # Map photo types to their paths
    photo_map = map_photos(photo_records, EXPECTED_PHOTO_TYPES)
    
    # Define layout: columns for each photo type
    cols = st.columns(len(EXPECTED_PHOTO_TYPES))
    
    for idx, ptype in enumerate(EXPECTED_PHOTO_TYPES):
        with cols[idx]:
            st.write(f"**{ptype.replace('_', ' ').title()}**")
            photo_path = photo_map.get(ptype)
            if photo_path:
                image = load_image(photo_path)
                if image is not None:
                    st.image(image, use_column_width=True)
                else:
                    st.write("Image not found.")
            else:
                image = load_placeholder()
                if image:
                    st.image(image, use_column_width=True)
                else:
                    st.write("Image not found.")
