#!/usr/bin/env python3
"""
Test script for enhanced text styling functionality.
"""

import requests
import json
import time

def test_text_styling():
    """Test the enhanced text styling with different message lengths and languages."""
    
    base_url = "http://localhost:8080"
    
    # Test cases with different message lengths and languages
    test_cases = [
        {
            "name": "Short message - English",
            "data": {
                "products": ["safety helmet"],
                "country_name": "US",
                "audience": "construction workers",
                "message": "Safety first!",
                "noise_scheduler": "ddim",
                "unet_backbone": "default",
                "vae": "default",
                "guidance_scale": 7.5,
                "num_inference_steps": 20,
                "seed": 42
            }
        },
        {
            "name": "Long message - English",
            "data": {
                "products": ["safety helmet"],
                "country_name": "US",
                "audience": "construction workers",
                "message": "Professional safety equipment for modern construction sites with advanced protection technology and comfort features designed for maximum worker safety and productivity",
                "noise_scheduler": "ddim",
                "unet_backbone": "default",
                "vae": "default",
                "guidance_scale": 7.5,
                "num_inference_steps": 20,
                "seed": 42
            }
        },
        {
            "name": "Medium message - German",
            "data": {
                "products": ["safety helmet"],
                "country_name": "Germany",
                "audience": "construction workers",
                "message": "Professionelle Sicherheitsausrüstung für moderne Baustellen mit fortschrittlicher Schutztechnologie",
                "noise_scheduler": "ddim",
                "unet_backbone": "default",
                "vae": "default",
                "guidance_scale": 7.5,
                "num_inference_steps": 20,
                "seed": 42
            }
        }
    ]
    
    print("🧪 Testing Enhanced Text Styling")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 30)
        
        try:
            # Test API health first
            health_response = requests.get(f"{base_url}/api/health", timeout=5)
            if health_response.status_code != 200:
                print(f"❌ API health check failed: {health_response.status_code}")
                continue
                
            print("✅ API is healthy")
            
            # Make the request
            print(f"📤 Sending request for: {test_case['data']['message'][:50]}...")
            response = requests.post(
                f"{base_url}/campaigns/generate",
                headers={"Content-Type": "application/json"},
                json=test_case['data'],
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success! Campaign ID: {result.get('campaign_id', 'N/A')}")
                
                # Check if images were generated
                if 'outputs' in result:
                    for product, sizes in result['outputs'].items():
                        print(f"   📸 {product}: {len(sizes)} size variants generated")
                        for size, path in sizes.items():
                            print(f"      - {size}: {path}")
                else:
                    print("   ⚠️ No outputs found in response")
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out")
        except requests.exceptions.ConnectionError:
            print("🔌 Connection error - is the container running?")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Wait between tests
        if i < len(test_cases):
            print("⏳ Waiting 3 seconds before next test...")
            time.sleep(3)
    
    print("\n🏁 Text styling tests completed!")

if __name__ == "__main__":
    test_text_styling()
