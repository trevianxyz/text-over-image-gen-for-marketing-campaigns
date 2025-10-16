#!/usr/bin/env python3
"""
Master Manifest Generator

This script creates a master_manifest.json that concatenates all response_artifact.json files
from the assets/generated directory, providing a comprehensive overview of all campaigns.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

def find_response_artifacts() -> List[Path]:
    """Find all response_artifact.json files in the generated campaigns directory"""
    generated_dir = Path("assets/generated")
    if not generated_dir.exists():
        print("❌ No assets/generated directory found")
        return []
    
    artifacts = []
    for campaign_dir in generated_dir.iterdir():
        if campaign_dir.is_dir():
            artifact_path = campaign_dir / "response_artifact.json"
            if artifact_path.exists():
                artifacts.append(artifact_path)
    
    return sorted(artifacts, key=lambda x: x.stat().st_mtime, reverse=True)  # Most recent first

def load_artifact(artifact_path: Path) -> Dict[str, Any]:
    """Load and parse a response artifact JSON file"""
    try:
        with open(artifact_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add metadata about the file
        data['_manifest_metadata'] = {
            'file_path': str(artifact_path),
            'file_size': artifact_path.stat().st_size,
            'last_modified': datetime.fromtimestamp(artifact_path.stat().st_mtime).isoformat(),
            'campaign_directory': str(artifact_path.parent)
        }
        
        return data
    except Exception as e:
        print(f"⚠️ Error loading {artifact_path}: {e}")
        return {
            'error': str(e),
            'file_path': str(artifact_path),
            '_manifest_metadata': {
                'file_path': str(artifact_path),
                'error': True,
                'last_modified': datetime.fromtimestamp(artifact_path.stat().st_mtime).isoformat()
            }
        }

def generate_master_manifest() -> Dict[str, Any]:
    """Generate the master manifest by concatenating all response artifacts"""
    print("🔍 Scanning for response artifacts...")
    artifacts = find_response_artifacts()
    
    if not artifacts:
        print("❌ No response artifacts found")
        return {
            'error': 'No response artifacts found',
            'generated_at': datetime.now().isoformat(),
            'total_campaigns': 0,
            'campaigns': []
        }
    
    print(f"📁 Found {len(artifacts)} response artifacts")
    
    # Load all artifacts
    campaigns = []
    total_images = 0
    total_products = 0
    regions = set()
    audiences = set()
    
    for artifact_path in artifacts:
        print(f"📄 Loading {artifact_path.name} from {artifact_path.parent.name}")
        campaign_data = load_artifact(artifact_path)
        
        if 'error' not in campaign_data:
            campaigns.append(campaign_data)
            
            # Aggregate statistics
            if 'response' in campaign_data and 'outputs' in campaign_data['response']:
                for product, sizes in campaign_data['response']['outputs'].items():
                    total_products += 1
                    total_images += len(sizes)
            
            if 'request' in campaign_data:
                if 'region' in campaign_data['request']:
                    regions.add(campaign_data['request']['region'])
                if 'audience' in campaign_data['request']:
                    audiences.add(campaign_data['request']['audience'])
        else:
            campaigns.append(campaign_data)
    
    # Create master manifest
    master_manifest = {
        'manifest_info': {
            'generated_at': datetime.now().isoformat(),
            'total_campaigns': len(campaigns),
            'total_images': total_images,
            'total_products': total_products,
            'unique_regions': sorted(list(regions)),
            'unique_audiences': sorted(list(audiences)),
            'generator_version': '1.0.0',
            'description': 'Master manifest concatenating all campaign response artifacts'
        },
        'campaigns': campaigns
    }
    
    return master_manifest

def main():
    """Main function to generate and save the master manifest"""
    print("🚀 Generating Master Manifest...")
    
    # Generate the manifest
    manifest = generate_master_manifest()
    
    # Save to file
    output_path = Path("assets/generated/master_manifest.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Master manifest saved to: {output_path}")
        print(f"📊 Summary:")
        print(f"   - Total campaigns: {manifest['manifest_info']['total_campaigns']}")
        print(f"   - Total images: {manifest['manifest_info']['total_images']}")
        print(f"   - Total products: {manifest['manifest_info']['total_products']}")
        print(f"   - Regions: {', '.join(manifest['manifest_info']['unique_regions'])}")
        print(f"   - Audiences: {', '.join(manifest['manifest_info']['unique_audiences'])}")
        
        # Show file size
        file_size = output_path.stat().st_size
        print(f"   - File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
    except Exception as e:
        print(f"❌ Error saving master manifest: {e}")

if __name__ == "__main__":
    main()
