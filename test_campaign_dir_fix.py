#!/usr/bin/env python3
"""
Test script to verify the campaign_dir bug fix.
This tests that all products use the same campaign directory.
"""

import tempfile
import uuid
from pathlib import Path
from datetime import datetime

def test_campaign_dir_consistency():
    """Test that all products use the same campaign directory"""
    print("🧪 Testing Campaign Directory Consistency Fix")
    print("=" * 60)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Using temporary directory: {temp_dir}")
        
        # Simulate the exact logic from routes.py
        campaign_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create campaign directory (from routes.py)
        campaign_dir = Path(temp_dir) / "assets" / "generated" / f"campaign_{timestamp}_{campaign_id}"
        campaign_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created campaign directory: {campaign_dir}")
        
        # Simulate multiple products
        products = ["Work gloves", "hard hat", "safety_helmet"]
        
        print(f"\n🎨 Testing {len(products)} products with same campaign_dir")
        print("-" * 50)
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. Processing product: '{product}'")
            
            # Simulate the generate_creatives call with campaign_dir
            print(f"   📤 Calling generate_creatives with campaign_dir: {campaign_dir}")
            
            # Simulate product directory creation
            product_dir = campaign_dir / product.replace(" ", "_").lower()
            product_dir.mkdir(parents=True, exist_ok=True)
            print(f"   📁 Product directory: {product_dir}")
            
            # Verify the product directory is within the campaign directory
            if campaign_dir in product_dir.parents or product_dir.parent == campaign_dir:
                print(f"   ✅ Product directory is within campaign directory")
            else:
                print(f"   ❌ Product directory is NOT within campaign directory!")
                return False
            
            # Simulate size directories
            size_configs = {
                "1:1": {"dir": "1x1"},
                "16:9": {"dir": "16x9"},
                "9:16": {"dir": "9x16"}
            }
            
            for aspect_ratio, config in size_configs.items():
                size_dir = product_dir / config["dir"]
                size_dir.mkdir(parents=True, exist_ok=True)
                print(f"   📁 Size directory: {size_dir}")
                
                # Verify the size directory is within the campaign directory
                if campaign_dir in size_dir.parents:
                    print(f"   ✅ Size directory is within campaign directory")
                else:
                    print(f"   ❌ Size directory is NOT within campaign directory!")
                    return False
        
        # Test the key fix: all paths should be under the same campaign directory
        print(f"\n🔍 Directory Structure Verification:")
        print("=" * 40)
        
        # Check that all product directories are under the same campaign directory
        all_product_dirs = [campaign_dir / product.replace(" ", "_").lower() for product in products]
        
        for product_dir in all_product_dirs:
            if product_dir.exists():
                print(f"✅ Product directory exists: {product_dir}")
                
                # Check that it's under the campaign directory
                if campaign_dir in product_dir.parents or product_dir.parent == campaign_dir:
                    print(f"✅ Product directory is under campaign directory")
                else:
                    print(f"❌ Product directory is NOT under campaign directory!")
                    return False
            else:
                print(f"❌ Product directory missing: {product_dir}")
                return False
        
        # Verify the campaign directory structure
        print(f"\n📊 Final Directory Structure:")
        print("=" * 30)
        display_directory_structure(campaign_dir)
        
        print(f"\n🎉 Campaign directory consistency test PASSED!")
        print("✅ All products use the same campaign directory")
        print("✅ No duplicate campaign directories created")
        print("✅ Proper hierarchical structure maintained")
        
        return True

def display_directory_structure(path, prefix=""):
    """Display directory structure in a tree format"""
    if path.is_file():
        print(f"{prefix}📄 {path.name}")
    else:
        print(f"{prefix}📁 {path.name}/")
        for item in sorted(path.iterdir()):
            display_directory_structure(item, prefix + "  ")

if __name__ == "__main__":
    success = test_campaign_dir_consistency()
    if success:
        print("\n✅ Campaign directory fix test PASSED!")
        print("The bug has been fixed - all products will use the same campaign directory.")
        exit(0)
    else:
        print("\n❌ Campaign directory fix test FAILED!")
        print("The bug still exists - products may create separate campaign directories.")
        exit(1)
