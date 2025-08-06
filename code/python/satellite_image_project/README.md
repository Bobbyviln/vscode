# Satellite Image Retrieval Tool

A Python tool that converts street addresses to GPS coordinates and retrieves satellite imagery from public APIs.

##  Project Overview

This tool demonstrates several key programming concepts:
- **API Integration**: Working with external geocoding and satellite image services
- **Error Handling**: Graceful handling of network failures and invalid data
- **Caching**: Using `@lru_cache` to avoid repeated API calls
- **Type Hints**: Clear function signatures with type annotations
- **Logging**: Comprehensive logging for debugging and monitoring

##  Architecture Breakdown

### 1. **Geocoding Component** (`get_coordinates`)
- **Purpose**: Converts human-readable addresses to GPS coordinates
- **API Used**: OpenStreetMap's Nominatim (free, no API key required)
- **Input**: Street address (e.g., "1600 Amphitheatre Parkway, Mountain View, CA")
- **Output**: Tuple of (latitude, longitude)

### 2. **Satellite Image Component** (`get_nasa_satellite_image`)
- **Purpose**: Retrieves satellite imagery for given coordinates
- **API Used**: NASA's GIBS (Global Imagery Browse Services)
- **Input**: Latitude, longitude, zoom level
- **Output**: Raw image bytes (JPEG format)

### 3. **Integration Component** (`get_satellite_image`)
- **Purpose**: Orchestrates the entire process
- **Features**: 
  - Caching with `@lru_cache`
  - Error handling and fallbacks
  - Mock image generation for testing

##  Quick Start

### Installation

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from satellite_image import get_satellite_image

# Get satellite image for an address
coords, image_bytes = get_satellite_image("Statue of Liberty, New York, NY")

print(f"Coordinates: {coords}")
print(f"Image size: {len(image_bytes)} bytes")

# Save the image
with open("satellite_image.jpg", "wb") as f:
    f.write(image_bytes)
```

### Testing with Mock Images

```python
# Use mock images for testing (no internet required)
coords, image_bytes = get_satellite_image("Test Address", use_mock=True)
```

##  Educational Breakdown

### Understanding the Code Structure

#### 1. **Imports and Setup**
```python
import requests          # For HTTP requests to APIs
from geopy.geocoders import Nominatim  # For address-to-coordinates conversion
from functools import lru_cache       # For caching results
from PIL import Image                 # For image manipulation
import logging                        # For debugging and monitoring
```

#### 2. **Custom Exceptions**
```python
class SatelliteImageError(Exception):
    """Custom exception for satellite image retrieval errors."""
    pass

class GeocodingError(Exception):
    """Custom exception for geocoding errors."""
    pass
```
**Why Custom Exceptions?** They make error handling more specific and informative.

#### 3. **Geocoding Function**
```python
def get_coordinates(address: str) -> Tuple[float, float]:
    geolocator = Nominatim(user_agent="satellite_image_tool/1.0")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)
```
**Key Concepts:**
- **Type Hints**: `-> Tuple[float, float]` tells us the return type
- **User Agent**: Required by Nominatim to identify your application
- **Error Handling**: Catches network timeouts and service unavailability

#### 4. **Caching with Decorators**
```python
@lru_cache(maxsize=100)
def get_satellite_image(address: str, use_mock: bool = False):
    # Function implementation
```
**What `@lru_cache` does:**
- Stores the last 100 function calls
- If you call the same address again, it returns the cached result
- Saves API calls and improves performance

### API Deep Dive

#### OpenStreetMap Nominatim API
- **URL**: `https://nominatim.openstreetmap.org/`
- **Rate Limit**: 1 request per second (free tier)
- **No API Key Required**: Perfect for learning and small projects
- **Example Response**:
```json
{
  "lat": "40.6892",
  "lon": "-74.0445",
  "display_name": "Statue of Liberty, New York, NY, USA"
}
```

#### NASA GIBS API
- **URL**: `https://gibs.earthdata.nasa.gov/`
- **Free**: No API key required
- **Data**: MODIS satellite imagery (updated daily)
- **Format**: Web Map Tile Service (WMTS)

##  Advanced Features

### 1. **Error Handling Strategy**
```python
try:
    coordinates = get_coordinates(address)
except GeocodingError as e:
    logger.error(f"Geocoding failed: {e}")
    raise  # Re-raise the exception for the caller to handle
```

### 2. **Fallback Mechanisms**
```python
# Try NASA GIBS first, fall back to mock if it fails
try:
    image_bytes = get_nasa_satellite_image(lat, lon)
except SatelliteImageError:
    logger.warning("NASA GIBS API failed, using mock image")
    image_bytes = create_mock_image(lat, lon)
```

### 3. **Mock Image Generation**
```python
def create_mock_image(lat: float, lon: float) -> bytes:
    img = Image.new('RGB', (800, 600), color='green')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    return img_bytes.getvalue()
```

##  Testing the Tool

Run the included test script:
```bash
python satellite_image.py
```

This will test three addresses:
1. Statue of Liberty, New York, NY
2. 1600 Amphitheatre Parkway, Mountain View, CA (Google HQ)
3. Eiffel Tower, Paris, France

##  Learning Objectives

After studying this code, you should understand:

1. **API Integration**: How to work with external services
2. **Error Handling**: Graceful failure management
3. **Caching**: Performance optimization techniques
4. **Type Safety**: Using type hints for better code
5. **Logging**: Debugging and monitoring practices
6. **Modular Design**: Separating concerns into functions

##  Potential Enhancements

1. **Add More APIs**: Google Maps, Mapbox (requires API keys)
2. **Image Processing**: Add filters, annotations, or overlays
3. **Batch Processing**: Handle multiple addresses at once
4. **Web Interface**: Create a Flask/FastAPI web app
5. **Database Storage**: Save results to SQLite/PostgreSQL
6. **Scheduling**: Automatically update images periodically

##  Troubleshooting

### Common Issues

1. **Geocoding Fails**: Check internet connection and address format
2. **NASA API Fails**: Service might be down, falls back to mock images
3. **Import Errors**: Make sure all dependencies are installed
4. **Rate Limiting**: Nominatim limits to 1 request/second

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

##  Further Reading

- [Nominatim Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)
- [NASA GIBS Documentation](https://wiki.earthdata.nasa.gov/display/GIBS)
- [Python Requests Library](https://requests.readthedocs.io/)
- [Pillow (PIL) Documentation](https://pillow.readthedocs.io/)

##  Contributing

Feel free to:
- Add more satellite image providers
- Improve error handling
- Add unit tests
- Create a web interface
- Optimize performance

---

**Happy Coding!** 
