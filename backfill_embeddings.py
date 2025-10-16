"""
Backfill embeddings from existing campaigns in master_manifest.json
"""
import json
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.services.embeddings import embed_and_store

def backfill_embeddings():
    """Load existing campaigns and create embeddings"""
    manifest_path = Path("assets/generated/master_manifest.json")
    
    if not manifest_path.exists():
        print("❌ master_manifest.json not found")
        return
    
    print("📚 Loading master manifest...")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    campaigns = manifest.get("campaigns", [])
    print(f"📊 Found {len(campaigns)} campaigns")
    
    success_count = 0
    error_count = 0
    
    for campaign in campaigns:
        try:
            campaign_id = campaign.get("campaign_id")
            request = campaign.get("request", {})
            message = request.get("message", "")
            
            if not campaign_id or not message:
                print(f"⚠️  Skipping campaign {campaign_id}: missing data")
                continue
            
            # Prepare metadata for embedding
            metadata = {
                "products": request.get("products", []),
                "country_name": request.get("country_name") or request.get("region", ""),
                "audience": request.get("audience", ""),
                "message": message
            }
            
            # Store embedding
            embed_and_store(campaign_id, message, metadata)
            success_count += 1
            print(f"✅ Embedded campaign {campaign_id[:8]}... - '{message[:50]}...'")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Error embedding campaign {campaign_id[:8] if campaign_id else 'unknown'}: {e}")
    
    print(f"\n🎉 Backfill complete!")
    print(f"   ✅ Successfully embedded: {success_count}")
    print(f"   ❌ Errors: {error_count}")

if __name__ == "__main__":
    backfill_embeddings()

