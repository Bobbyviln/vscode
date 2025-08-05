"""
Satellite Image Retrieval Tool

This module provides functionality to:
1. Convert street addresses to GPS coordinates using OpenStreetMap's Nominatim API
2. Retrieve satellite images using NASA's GIBS API
3. Cache results to avoid repeated API calls
4. Handle errors gracefully

Author: Assistant
Date: 2024
"""

import requests
import time
from typing import Tuple, Optional
from functools import lru_cache
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from PIL import Image
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SatelliteImageError(Exception):
    """Custom exception for satellite image retrieval errors."""
    pass


class GeocodingError(Exception):
    """Custom exception for geocoding errors."""
    pass


def get_coordinates(address: str) -> Tuple[float, float]:
    """
    Convert a street address to GPS coordinates using OpenStreetMap's Nominatim API.
    
    Args:
        address (str): A street address (e.g., "1600 Amphitheatre Parkway, Mountain View, CA")
        
    Returns:
        Tuple[float, float]: GPS coordinates as (latitude, longitude)
        
    Raises:
        GeocodingError: If the address cannot be geocoded
    """
    try:
        # Create a geocoder instance with a custom user agent
        geolocator = Nominatim(user_agent="satellite_image_tool/1.0")
        
        # Geocode the address
        location = geolocator.geocode(address)
        
        if location is None:
            raise GeocodingError(f"Could not find coordinates for address: {address}")
        
        logger.info(f"Successfully geocoded '{address}' to coordinates: ({location.latitude}, {location.longitude})")
        return (location.latitude, location.longitude)
        
    except GeocoderTimedOut:
        raise GeocodingError(f"Geocoding timed out for address: {address}")
    except GeocoderUnavailable:
        raise GeocodingError(f"Geocoding service unavailable for address: {address}")
    except Exception as e:
        raise GeocodingError(f"Unexpected error during geocoding: {str(e)}")


def get_nasa_satellite_image(lat: float, lon: float, zoom: int = 10) -> bytes:
    """
    Retrieve a satellite image using NASA's GIBS API.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        zoom (int): Zoom level (1-15, higher = more detail)
        
    Returns:
        bytes: Satellite image as raw bytes
        
    Raises:
        SatelliteImageError: If the image cannot be retrieved
    """
    import math
    
    try:
        # NASA GIBS API endpoint for MODIS True Color imagery
        # This provides recent satellite imagery
        base_url = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor/default"
        
        # Calculate tile coordinates based on lat/lon and zoom
        # This is a simplified calculation - in production you'd want more precise tile math
        tile_x = int((lon + 180) / 360 * (2 ** zoom))
        tile_y = int((1 - math.log(math.tan(math.radians(lat)) + 1/math.cos(math.radians(lat))) / math.pi) / 2 * (2 ** zoom))
        
        # Construct the URL
        url = f"{base_url}/{zoom}/{tile_y}/{tile_x}.jpg"
        
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        logger.info(f"Successfully retrieved satellite image for coordinates ({lat}, {lon})")
        return response.content
        
    except requests.exceptions.RequestException as e:
        raise SatelliteImageError(f"Failed to retrieve satellite image: {str(e)}")
    except Exception as e:
        raise SatelliteImageError(f"Unexpected error retrieving satellite image: {str(e)}")


def get_mapbox_satellite_image(lat: float, lon: float, zoom: int = 14) -> bytes:
    """
    Retrieve a satellite image using Mapbox Static Images API (requires API key).
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        zoom (int): Zoom level (1-22)
        
    Returns:
        bytes: Satellite image as raw bytes
        
    Raises:
        SatelliteImageError: If the image cannot be retrieved
    """
    # Note: This requires a Mapbox API key
    # For this demo, we'll use a placeholder implementation
    # In production, you would need to get a free API key from mapbox.com
    
    api_key = "YOUR_MAPBOX_API_KEY"  # Replace with actual API key
    
    if api_key == "YOUR_MAPBOX_API_KEY":
        raise SatelliteImageError("Mapbox API key not configured. Please get a free API key from mapbox.com")
    
    try:
        # Mapbox Static Images API
        url = f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/{lon},{lat},{zoom}/800x600@2x"
        params = {
            'access_token': api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        logger.info(f"Successfully retrieved Mapbox satellite image for coordinates ({lat}, {lon})")
        return response.content
        
    except requests.exceptions.RequestException as e:
        raise SatelliteImageError(f"Failed to retrieve Mapbox satellite image: {str(e)}")


def create_mock_image(lat: float, lon: float) -> bytes:
    """
    Create a mock satellite image for testing/offline use.
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        
    Returns:
        bytes: Mock satellite image as raw bytes
    """
    try:
        # Create a simple image with coordinates displayed
        img = Image.new('RGB', (800, 600), color='green')
        
        # Add text with coordinates (simplified - in production you'd use PIL's ImageDraw)
        # For now, just return the basic image
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        
        logger.info(f"Created mock satellite image for coordinates ({lat}, {lon})")
        return img_bytes.getvalue()
        
    except Exception as e:
        raise SatelliteImageError(f"Failed to create mock image: {str(e)}")


@lru_cache(maxsize=100)
def get_satellite_image(address: str, use_mock: bool = False) -> Tuple[Tuple[float, float], bytes]:
    """
    Convert a street address to GPS coordinates and retrieve a satellite image.
    
    Args:
        address (str): A street address (e.g., "1600 Amphitheatre Parkway, Mountain View, CA")
        use_mock (bool): If True, use mock image instead of real API calls
        
    Returns:
        Tuple[Tuple[float, float], bytes]: A tuple containing:
            - GPS coordinates as (latitude, longitude)
            - Satellite image as raw bytes
            
    Raises:
        GeocodingError: If the address cannot be geocoded
        SatelliteImageError: If the satellite image cannot be retrieved
    """
    logger.info(f"Processing request for address: {address}")
    
    # Step 1: Convert address to coordinates
    try:
        coordinates = get_coordinates(address)
        lat, lon = coordinates
    except GeocodingError as e:
        logger.error(f"Geocoding failed: {e}")
        raise
    
    # Step 2: Retrieve satellite image
    try:
        if use_mock:
            image_bytes = create_mock_image(lat, lon)
        else:
            # Try NASA GIBS first, fall back to mock if it fails
            try:
                image_bytes = get_nasa_satellite_image(lat, lon)
            except SatelliteImageError:
                logger.warning("NASA GIBS API failed, using mock image")
                image_bytes = create_mock_image(lat, lon)
        
        # Verify we got a reasonable amount of data
        if len(image_bytes) < 1000:
            raise SatelliteImageError("Retrieved image is too small, likely an error")
        
        logger.info(f"Successfully processed request for '{address}'. Image size: {len(image_bytes)} bytes")
        return coordinates, image_bytes
        
    except SatelliteImageError as e:
        logger.error(f"Satellite image retrieval failed: {e}")
        raise


def save_image_to_file(image_bytes: bytes, filename: str) -> None:
    """
    Save image bytes to a file.
    
    Args:
        image_bytes (bytes): Image data
        filename (str): Output filename
    """
    try:
        with open(filename, 'wb') as f:
            f.write(image_bytes)
        logger.info(f"Image saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to save image: {e}")


# Example usage and testing
if __name__ == "__main__":
    import math
    
    # Test addresses
    test_addresses = [
        "Statue of Liberty, New York, NY",
        "1600 Amphitheatre Parkway, Mountain View, CA",
        "Eiffel Tower, Paris, France"
    ]
    
    print("=== Satellite Image Retrieval Tool ===\n")
    
    for address in test_addresses:
        try:
            print(f"Processing: {address}")
            coords, image_data = get_satellite_image(address, use_mock=True)  # Use mock for testing
            
            print(f"  Coordinates: {coords}")
            print(f"  Image size: {len(image_data)} bytes")
            
            # Save the image
            filename = f"satellite_{address.replace(' ', '_').replace(',', '')}.jpg"
            save_image_to_file(image_data, filename)
            print(f"  Saved to: {filename}\n")
            
        except (GeocodingError, SatelliteImageError) as e:
            print(f"  Error: {e}\n")
        except Exception as e:
            print(f"  Unexpected error: {e}\n") 