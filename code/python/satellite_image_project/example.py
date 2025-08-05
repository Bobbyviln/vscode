#!/usr/bin/env python3
"""
Example usage of the Satellite Image Retrieval Tool

This script demonstrates how to use the tool with different addresses
and shows various features like error handling and caching.
"""

from satellite_image import get_satellite_image, save_image_to_file
from satellite_image import GeocodingError, SatelliteImageError
import time

def main():
    print("🌍 Satellite Image Retrieval Tool - Examples\n")
    
    # List of interesting addresses to test
    test_addresses = [
        "Statue of Liberty, New York, NY",
        "1600 Amphitheatre Parkway, Mountain View, CA",  # Google HQ
        "Eiffel Tower, Paris, France",
        "Sydney Opera House, Sydney, Australia",
        "Taj Mahal, Agra, India"
    ]
    
    print("Testing with mock images (no internet required for satellite images):")
    print("=" * 60)
    
    for i, address in enumerate(test_addresses, 1):
        print(f"\n{i}. Processing: {address}")
        print("-" * 40)
        
        try:
            # Use mock images for this example (faster and no API limits)
            start_time = time.time()
            coords, image_data = get_satellite_image(address, use_mock=True)
            end_time = time.time()
            
            print(f"✅ Success!")
            print(f"   📍 Coordinates: {coords}")
            print(f"   📊 Image size: {len(image_data):,} bytes")
            print(f"   ⏱️  Time taken: {end_time - start_time:.2f} seconds")
            
            # Save the image with a clean filename
            filename = f"satellite_{i:02d}_{address.replace(' ', '_').replace(',', '').replace(' ', '')}.jpg"
            save_image_to_file(image_data, filename)
            print(f"   💾 Saved as: {filename}")
            
        except GeocodingError as e:
            print(f"❌ Geocoding Error: {e}")
        except SatelliteImageError as e:
            print(f"❌ Satellite Image Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Example completed!")
    print("\nTo try with real satellite images, change use_mock=True to use_mock=False")
    print("Note: Real satellite images require internet connection and may have API rate limits.")

def demonstrate_caching():
    """Demonstrate the caching feature of the tool."""
    print("\n🔄 Caching Demonstration")
    print("=" * 40)
    
    address = "Times Square, New York, NY"
    
    print(f"Testing caching with address: {address}")
    
    # First call (will hit the API)
    print("\n1st call (API hit):")
    start_time = time.time()
    coords1, image1 = get_satellite_image(address, use_mock=True)
    time1 = time.time() - start_time
    print(f"   Time: {time1:.3f} seconds")
    
    # Second call (will use cache)
    print("\n2nd call (cached):")
    start_time = time.time()
    coords2, image2 = get_satellite_image(address, use_mock=True)
    time2 = time.time() - start_time
    print(f"   Time: {time2:.3f} seconds")
    
    # Verify results are identical
    print(f"\nResults identical: {coords1 == coords2 and image1 == image2}")
    print(f"Speed improvement: {time1/time2:.1f}x faster")

def demonstrate_error_handling():
    """Demonstrate error handling with invalid addresses."""
    print("\n⚠️  Error Handling Demonstration")
    print("=" * 40)
    
    invalid_addresses = [
        "This is not a real address",
        "",  # Empty string
        "1234567890" * 100,  # Very long string
    ]
    
    for address in invalid_addresses:
        print(f"\nTesting: '{address}'")
        try:
            coords, image_data = get_satellite_image(address, use_mock=True)
            print(f"   ✅ Unexpected success!")
        except GeocodingError as e:
            print(f"   ❌ Expected geocoding error: {e}")
        except Exception as e:
            print(f"   ❌ Other error: {e}")

if __name__ == "__main__":
    main()
    demonstrate_caching()
    demonstrate_error_handling() 