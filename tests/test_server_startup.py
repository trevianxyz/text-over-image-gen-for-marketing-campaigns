#!/usr/bin/env python3
"""
Test script to verify the server startup and route registration.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def test_server_import():
    """Test if the server can be imported correctly"""
    print("🧪 Testing Server Import")
    print("=" * 30)
    
    try:
        from app.main import app
        print("✅ Server app imported successfully")
        
        # Check if the app has routes
        routes = [route for route in app.routes if hasattr(route, 'path')]
        print(f"📊 Found {len(routes)} routes")
        
        for route in routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"  📍 {route.path} - {list(route.methods)}")
        
        # Check specifically for the countries endpoint
        countries_routes = [route for route in routes if hasattr(route, 'path') and '/api/countries' in route.path]
        if countries_routes:
            print("✅ /api/countries endpoint found")
        else:
            print("❌ /api/countries endpoint not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        return False

def test_countries_service():
    """Test the countries service directly"""
    print("\n🧪 Testing Countries Service")
    print("=" * 35)
    
    try:
        from app.services.country_language import get_country_selector_data
        
        data = get_country_selector_data()
        print("✅ Countries service imported successfully")
        print(f"📊 Countries: {len(data.get('countries', []))}")
        print(f"🗺️  Regions: {len(data.get('regions', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Countries service failed: {e}")
        return False

def test_static_files():
    """Test if static files exist"""
    print("\n🧪 Testing Static Files")
    print("=" * 25)
    
    project_root = Path(__file__).parent
    frontend_static = project_root / "frontend" / "static"
    frontend_templates = project_root / "frontend" / "templates"
    assets_dir = project_root / "assets"
    
    paths_to_check = [
        (frontend_static, "Frontend static"),
        (frontend_templates, "Frontend templates"),
        (assets_dir, "Assets directory")
    ]
    
    all_exist = True
    for path, name in paths_to_check:
        if path.exists():
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (missing)")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("🚀 Server Startup Test Suite")
    print("=" * 50)
    
    tests = [
        ("Server Import", test_server_import),
        ("Countries Service", test_countries_service),
        ("Static Files", test_static_files)
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
        print("\n🎉 All tests passed! Server should start correctly.")
        print("💡 Try: cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        exit(0)
    else:
        print("\n❌ Some tests failed. Check the issues above.")
        exit(1)
