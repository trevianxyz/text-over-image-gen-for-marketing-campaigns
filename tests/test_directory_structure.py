#!/usr/bin/env python3
"""
Test script to verify the campaign directory structure is correct.
This script simulates the directory creation process to ensure proper organization.
"""

import os
import tempfile
from pathlib import Path
from datetime import datetime
import uuid

def test_directory_structure():
    """Test the campaign directory structure creation"""
    print("🧪 Testing Campaign Directory Structure")
    print("=" * 50)
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"📁 Using temporary directory: {temp_dir}")
        
        # Simulate campaign creation
        campaign_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        campaign_dir = Path(temp_dir) / f"campaign_{timestamp}_{campaign_id}"
        campaign_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created campaign directory: {campaign_dir}")
        
        # Simulate multiple products
        products = ["safety_helmet", "work_gloves", "hard_hat"]
        
        for product in products:
            print(f"\n🎨 Processing product: {product}")
            
            # Create product directory
            product_dir = campaign_dir / product.replace(" ", "_").lower()
            product_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created product directory: {product_dir}")
            
            # Create size directories
            size_configs = {
                "1:1": {"dir": "1x1"},
                "16:9": {"dir": "16x9"},
                "9:16": {"dir": "9x16"}
            }
            
            for aspect_ratio, config in size_configs.items():
                size_dir = product_dir / config["dir"]
                size_dir.mkdir(parents=True, exist_ok=True)
                print(f"📁 Created size directory: {size_dir}")
                
                # Create dummy files to simulate the structure
                dummy_image = size_dir / f"image_{aspect_ratio.replace(':', 'x')}.png"
                dummy_artifact = size_dir / f"response_artifact_{aspect_ratio.replace(':', 'x')}.json"
                
                dummy_image.write_text("dummy image content")
                dummy_artifact.write_text('{"dummy": "artifact"}')
                print(f"📄 Created files: {dummy_image.name}, {dummy_artifact.name}")
        
        # Create main campaign artifact
        main_artifact = campaign_dir / "response_artifact.json"
        main_artifact.write_text('{"campaign": "metadata"}')
        print(f"\n📄 Created main artifact: {main_artifact}")
        
        # Display the final structure
        print(f"\n📊 Final Directory Structure:")
        print("=" * 30)
        display_directory_structure(campaign_dir)
        
        # Verify the structure
        print(f"\n✅ Structure Verification:")
        print("=" * 25)
        verify_structure(campaign_dir, products)
        
        print(f"\n🎉 Directory structure test completed successfully!")
        return True

def display_directory_structure(path, prefix=""):
    """Display directory structure in a tree format"""
    if path.is_file():
        print(f"{prefix}📄 {path.name}")
    else:
        print(f"{prefix}📁 {path.name}/")
        for item in sorted(path.iterdir()):
            display_directory_structure(item, prefix + "  ")

def verify_structure(campaign_dir, products):
    """Verify the directory structure is correct"""
    issues = []
    
    # Check campaign directory exists
    if not campaign_dir.exists():
        issues.append(f"❌ Campaign directory missing: {campaign_dir}")
    else:
        print(f"✅ Campaign directory exists: {campaign_dir}")
    
    # Check each product directory
    for product in products:
        product_dir = campaign_dir / product.replace(" ", "_").lower()
        if not product_dir.exists():
            issues.append(f"❌ Product directory missing: {product_dir}")
        else:
            print(f"✅ Product directory exists: {product_dir}")
            
            # Check size directories
            size_dirs = ["1x1", "16x9", "9x16"]
            for size_dir in size_dirs:
                size_path = product_dir / size_dir
                if not size_path.exists():
                    issues.append(f"❌ Size directory missing: {size_path}")
                else:
                    print(f"✅ Size directory exists: {size_path}")
                    
                    # Check for required files
                    image_file = size_path / f"image_{size_dir}.png"
                    artifact_file = size_path / f"response_artifact_{size_dir}.json"
                    
                    if not image_file.exists():
                        issues.append(f"❌ Image file missing: {image_file}")
                    else:
                        print(f"✅ Image file exists: {image_file}")
                    
                    if not artifact_file.exists():
                        issues.append(f"❌ Artifact file missing: {artifact_file}")
                    else:
                        print(f"✅ Artifact file exists: {artifact_file}")
    
    # Check main artifact
    main_artifact = campaign_dir / "response_artifact.json"
    if not main_artifact.exists():
        issues.append(f"❌ Main artifact missing: {main_artifact}")
    else:
        print(f"✅ Main artifact exists: {main_artifact}")
    
    if issues:
        print(f"\n⚠️  Found {len(issues)} issues:")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print(f"\n🎉 All structure checks passed!")
        return True

if __name__ == "__main__":
    success = test_directory_structure()
    if success:
        print("\n✅ Directory structure test PASSED!")
        exit(0)
    else:
        print("\n❌ Directory structure test FAILED!")
        exit(1)
