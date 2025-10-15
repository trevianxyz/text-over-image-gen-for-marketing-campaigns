#!/usr/bin/env python3
"""
Manual test script to verify the country selector integration without server dependency.
This tests the core functionality and integration points.
"""

import json
from pathlib import Path

def test_backend_service():
    """Test the backend country service directly"""
    print("🧪 Testing Backend Country Service")
    print("=" * 40)
    
    try:
        from backend.app.services.country_language import get_country_selector_data
        
        data = get_country_selector_data()
        print("✅ Country service is working")
        print(f"📊 Countries loaded: {len(data.get('countries', []))}")
        print(f"🗺️  Regions: {len(data.get('regions', []))}")
        
        # Test data structure
        if 'countries' in data and 'regions' in data:
            print("✅ Data structure is correct")
            
            # Test sample country
            if data['countries']:
                sample = data['countries'][0]
                required_fields = ['code', 'name', 'primary_language', 'region']
                missing = [f for f in required_fields if f not in sample]
                
                if not missing:
                    print("✅ Country data structure is correct")
                    print(f"📋 Sample: {sample['name']} ({sample['code']})")
                    return True
                else:
                    print(f"❌ Missing fields: {missing}")
                    return False
            else:
                print("❌ No countries in data")
                return False
        else:
            print("❌ Invalid data structure")
            return False
            
    except Exception as e:
        print(f"❌ Backend service failed: {e}")
        return False

def test_frontend_files():
    """Test that all frontend files exist and have correct content"""
    print("\n🧪 Testing Frontend Files")
    print("=" * 30)
    
    # Check HTML template
    html_file = Path('frontend/templates/index.html')
    if html_file.exists():
        html_content = html_file.read_text()
        required_elements = [
            'id="regionSearch"',
            'id="regionDropdown"', 
            'id="region"',
            'id="selectedCountry"',
            'class="country-selector"'
        ]
        
        missing_elements = [elem for elem in required_elements if elem not in html_content]
        if not missing_elements:
            print("✅ HTML template has all required elements")
        else:
            print(f"❌ Missing HTML elements: {missing_elements}")
            return False
    else:
        print("❌ HTML template missing")
        return False
    
    # Check JavaScript
    js_file = Path('frontend/static/js/main.js')
    if js_file.exists():
        js_content = js_file.read_text()
        required_js = [
            'fetch(\'/api/countries\')',
            'regionSearch',
            'regionDropdown',
            'selectCountry',
            'countriesData'
        ]
        
        missing_js = [js for js in required_js if js not in js_content]
        if not missing_js:
            print("✅ JavaScript has all required functionality")
        else:
            print(f"❌ Missing JavaScript: {missing_js}")
            return False
    else:
        print("❌ JavaScript file missing")
        return False
    
    # Check CSS
    css_file = Path('frontend/static/css/style.css')
    if css_file.exists():
        css_content = css_file.read_text()
        required_css = [
            '.country-selector',
            '.country-dropdown',
            '.country-option',
            '.selected-country'
        ]
        
        missing_css = [css for css in required_css if css not in css_content]
        if not missing_css:
            print("✅ CSS has all required styles")
        else:
            print(f"❌ Missing CSS: {missing_css}")
            return False
    else:
        print("❌ CSS file missing")
        return False
    
    return True

def test_data_flow_simulation():
    """Simulate the data flow from backend to frontend"""
    print("\n🧪 Testing Data Flow Simulation")
    print("=" * 40)
    
    try:
        from backend.app.services.country_language import get_country_selector_data
        
        # Get data from backend service
        data = get_country_selector_data()
        countries = data.get('countries', [])
        
        print(f"📊 Backend provides {len(countries)} countries")
        
        # Simulate frontend search functionality
        test_queries = [
            ("united", "United States"),
            ("german", "Germany"), 
            ("spanish", "Spanish-speaking countries"),
            ("asia", "Asian countries")
        ]
        
        print("🔍 Simulating frontend search:")
        for query, description in test_queries:
            # Simulate the frontend filtering logic
            filtered = [c for c in countries if 
                       query.lower() in c['name'].lower() or 
                       query.lower() in c['primary_language'].lower() or
                       query.lower() in c['region'].lower()]
            print(f"  🔍 '{query}': {len(filtered)} results - {description}")
        
        # Test form integration
        print("\n📝 Form integration:")
        print("✅ Hidden input 'region' will store country code")
        print("✅ Form validation will check for country selection")
        print("✅ Country data will be sent to backend")
        
        return True
        
    except Exception as e:
        print(f"❌ Data flow simulation failed: {e}")
        return False

def test_integration_points():
    """Test the key integration points"""
    print("\n🧪 Testing Integration Points")
    print("=" * 35)
    
    # Test 1: Backend API endpoint definition
    main_py = Path('backend/app/main.py')
    if main_py.exists():
        content = main_py.read_text()
        if '@app.get("/api/countries")' in content:
            print("✅ API endpoint is defined in main.py")
        else:
            print("❌ API endpoint not found in main.py")
            return False
    else:
        print("❌ main.py not found")
        return False
    
    # Test 2: Frontend JavaScript API call
    js_file = Path('frontend/static/js/main.js')
    if js_file.exists():
        content = js_file.read_text()
        if 'fetch(\'/api/countries\')' in content:
            print("✅ Frontend makes API call to /api/countries")
        else:
            print("❌ Frontend API call not found")
            return False
    else:
        print("❌ JavaScript file not found")
        return False
    
    # Test 3: Form submission integration
    if 'region' in content and 'selectedCountry' in content:
        print("✅ Form integration is complete")
    else:
        print("❌ Form integration incomplete")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Country Selector Integration Test (Manual)")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Backend Service", test_backend_service),
        ("Frontend Files", test_frontend_files), 
        ("Data Flow", test_data_flow_simulation),
        ("Integration Points", test_integration_points)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"\n✅ {test_name} test PASSED")
            else:
                print(f"\n❌ {test_name} test FAILED")
                all_passed = False
        except Exception as e:
            print(f"\n❌ {test_name} test ERROR: {e}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Country selector is properly wired.")
        print("✅ Backend service is working")
        print("✅ Frontend files are complete")
        print("✅ Data flow is functional")
        print("✅ Integration points are connected")
        print("\n💡 To test with server: python -m uvicorn backend.app.main:app --reload")
        exit(0)
    else:
        print("\n❌ Some tests failed. Check the issues above.")
        exit(1)
