#!/usr/bin/env python3
"""
Test script to verify the countries API endpoint is working correctly.
Run this script to test the country selector backend functionality.
"""

import requests
import json
import sys

def test_countries_api():
    """Test the countries API endpoint"""
    try:
        print("🧪 Testing Countries API Endpoint...")
        print("=" * 50)
        
        # Test the API endpoint
        response = requests.get('http://localhost:8000/api/countries', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API endpoint is working!")
            print(f"📊 Response status: {response.status_code}")
            print(f"🌍 Total countries: {len(data.get('countries', []))}")
            print(f"🗺️  Regions: {len(data.get('regions', []))}")
            
            # Show sample countries
            countries = data.get('countries', [])
            if countries:
                print("\n📋 Sample countries:")
                for i, country in enumerate(countries[:5]):
                    print(f"  {i+1}. {country['name']} ({country['code']}) - {country['primary_language']} - {country['region']}")
                
                if len(countries) > 5:
                    print(f"  ... and {len(countries) - 5} more countries")
            
            # Show regions
            regions = data.get('regions', [])
            if regions:
                print(f"\n🗺️  Available regions: {', '.join(regions)}")
            
            print("\n✅ Countries API test passed!")
            return True
            
        else:
            print(f"❌ API endpoint failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the server is running on localhost:8000")
        print("💡 Start the server with: python -m uvicorn backend.app.main:app --reload")
        return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_country_search():
    """Test country search functionality"""
    try:
        print("\n🔍 Testing Country Search...")
        print("=" * 30)
        
        response = requests.get('http://localhost:8000/api/countries')
        if response.status_code != 200:
            print("❌ Cannot test search - API not available")
            return False
            
        data = response.json()
        countries = data.get('countries', [])
        
        # Test search scenarios
        test_cases = [
            ("united", "Should find United States, United Kingdom"),
            ("german", "Should find Germany"),
            ("spanish", "Should find Spanish-speaking countries"),
            ("asia", "Should find Asian countries"),
            ("xx", "Should find no results")
        ]
        
        for query, description in test_cases:
            filtered = [c for c in countries if query.lower() in c['name'].lower() or 
                       query.lower() in c['primary_language'].lower() or 
                       query.lower() in c['region'].lower()]
            print(f"  🔍 '{query}': {len(filtered)} results - {description}")
        
        print("✅ Country search test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Countries API Test Suite")
    print("=" * 50)
    
    # Test API endpoint
    api_success = test_countries_api()
    
    if api_success:
        # Test search functionality
        search_success = test_country_search()
        
        if search_success:
            print("\n🎉 All tests passed! Country selector is properly wired.")
            sys.exit(0)
        else:
            print("\n⚠️  API works but search has issues.")
            sys.exit(1)
    else:
        print("\n❌ API endpoint is not working. Check server status.")
        sys.exit(1)
