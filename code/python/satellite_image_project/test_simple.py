#!/usr/bin/env python3
"""
Simple test script for the Satellite Image Retrieval Tool

This script tests the basic functionality using mock images
to ensure everything works without requiring internet access.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from satellite_image import get_satellite_image, GeocodingError, SatelliteImageError

def test_basic_functionality():
    """Test the basic functionality with mock images."""
    print("🧪 Testing Basic Functionality")
    print("=" * 40)
    
    # Test with a simple address
    test_address = "Test Location"
    
    try:
        print(f"Testing address: '{test_address}'")
        coords, image_data = get_satellite_image(test_address, use_mock=True)
        
        print(f"✅ Success!")
        print(f"   Coordinates: {coords}")
        print(f"   Image size: {len(image_data)} bytes")
        
        # Verify we got reasonable data
        assert len(coords) == 2, "Coordinates should be a tuple of 2 values"
        assert isinstance(coords[0], (int, float)), "Latitude should be a number"
        assert isinstance(coords[1], (int, float)), "Longitude should be a number"
        assert len(image_data) > 1000, "Image should be at least 1KB"
        
        print("   ✅ All assertions passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid input."""
    print("\n🧪 Testing Error Handling")
    print("=" * 40)
    
    # Test with empty string
    try:
        print("Testing empty string...")
        coords, image_data = get_satellite_image("", use_mock=True)
        print("❌ Should have raised an error for empty string")
        return False
    except GeocodingError:
        print("✅ Correctly handled empty string")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

def test_caching():
    """Test that caching works correctly."""
    print("\n🧪 Testing Caching")
    print("=" * 40)
    
    address = "Cache Test Location"
    
    # First call
    print("First call...")
    coords1, image1 = get_satellite_image(address, use_mock=True)
    
    # Second call (should use cache)
    print("Second call (should use cache)...")
    coords2, image2 = get_satellite_image(address, use_mock=True)
    
    # Verify results are identical
    if coords1 == coords2 and image1 == image2:
        print("✅ Caching works correctly!")
        return True
    else:
        print("❌ Caching failed - results are different")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Satellite Image Tool Tests\n")
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Error Handling", test_error_handling),
        ("Caching", test_caching),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print(f"{'='*60}")
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*60}")
    print(f"Test Results: {passed}/{total} tests passed")
    print(f"{'='*60}")
    
    if passed == total:
        print("🎉 All tests passed! The tool is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 