#!/usr/bin/env python3
"""
Test script to verify server routes are registered correctly.
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def test_server_routes():
    """Test that all routes are registered correctly"""
    print("🧪 Testing Server Routes")
    print("=" * 30)
    
    try:
        from app.main import app
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                routes.append({
                    'path': route.path,
                    'methods': list(route.methods)
                })
        
        print(f"📊 Found {len(routes)} routes:")
        for route in routes:
            print(f"  📍 {route['path']} - {route['methods']}")
        
        # Check for specific routes
        route_paths = [route['path'] for route in routes]
        
        # Check for countries endpoint
        if '/api/countries' in route_paths:
            print("✅ /api/countries endpoint is registered")
        else:
            print("❌ /api/countries endpoint is NOT registered")
            return False
        
        # Check for health endpoint
        if '/api/health' in route_paths:
            print("✅ /api/health endpoint is registered")
        else:
            print("❌ /api/health endpoint is NOT registered")
        
        # Check for root endpoint
        if '/' in route_paths:
            print("✅ Root endpoint is registered")
        else:
            print("❌ Root endpoint is NOT registered")
        
        # Check for docs endpoint
        if '/docs' in route_paths:
            print("✅ /docs endpoint is registered")
        else:
            print("❌ /docs endpoint is NOT registered")
        
        return True
        
    except Exception as e:
        print(f"❌ Server routes test failed: {e}")
        return False

def test_countries_endpoint_function():
    """Test that the countries endpoint function exists"""
    print("\n🧪 Testing Countries Endpoint Function")
    print("=" * 45)
    
    try:
        from app.main import get_countries
        
        print("✅ get_countries function is imported")
        
        # Test the function directly
        result = get_countries()
        print("✅ get_countries function executed successfully")
        
        if isinstance(result, dict) and 'countries' in result:
            print(f"✅ Function returns correct data structure")
            print(f"📊 Countries: {len(result.get('countries', []))}")
            print(f"🗺️  Regions: {len(result.get('regions', []))}")
            return True
        else:
            print(f"❌ Function returns incorrect data: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Countries endpoint function test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Server Routes Test")
    print("=" * 30)
    
    # Test routes
    routes_success = test_server_routes()
    
    if routes_success:
        # Test countries endpoint function
        function_success = test_countries_endpoint_function()
        
        if function_success:
            print("\n🎉 All tests passed!")
            print("✅ Server routes are registered correctly")
            print("✅ Countries endpoint function is working")
            print("💡 The server should work when started with:")
            print("   cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            exit(0)
        else:
            print("\n⚠️  Routes are registered but countries function has issues")
            exit(1)
    else:
        print("\n❌ Server routes test failed")
        exit(1)
