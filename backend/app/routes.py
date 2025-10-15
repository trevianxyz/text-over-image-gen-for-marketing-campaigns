from fastapi import APIRouter
import uuid
import json
from pathlib import Path
from datetime import datetime
from app.models import CampaignBrief, GenerationResult
from app.services.embeddings import embed_and_store, search_similar
from app.services.generator import generate_creatives
from app.services.logging_db import log_campaign
from app.services.compliance import check_compliance

router = APIRouter()

@router.post("/generate", response_model=GenerationResult)
def generate_campaign(brief: CampaignBrief):
    campaign_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create campaign directory
    campaign_dir = Path("assets/generated") / f"campaign_{timestamp}_{campaign_id}"
    campaign_dir.mkdir(parents=True, exist_ok=True)

    # Store embeddings
    embed_and_store(campaign_id, brief.message, brief.model_dump())

    # Generate images for each product
    prompt = f"{brief.message} for {brief.audience} in {brief.region}"
    all_outputs = {}
    
    for product in brief.products:
        print(f"🎨 Generating creatives for product: {product}")
        product_outputs = generate_creatives(prompt, campaign_id=campaign_id, product=product, region=brief.region, message=brief.message)
        all_outputs[product] = product_outputs
        
        # Create individual artifacts for each size variant
        for aspect_ratio, image_path in product_outputs.items():
            size_artifact = {
                "campaign_id": campaign_id,
                "timestamp": timestamp,
                "product": product,
                "aspect_ratio": aspect_ratio,
                "request": {
                    "products": brief.products,
                    "region": brief.region,
                    "audience": brief.audience,
                    "message": brief.message,
                    "assets": brief.assets
                },
                "response": {
                    "campaign_id": campaign_id,
                    "product": product,
                    "aspect_ratio": aspect_ratio,
                    "image_path": image_path,
                    "compliance": check_compliance(brief.message)
                },
                "metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "campaign_directory": str(campaign_dir),
                    "product_directory": str(Path(image_path).parent.parent),
                    "size_directory": str(Path(image_path).parent)
                }
            }
            
            # Save size-specific artifact
            size_dir = Path(image_path).parent
            artifact_path = size_dir / f"response_artifact_{aspect_ratio.replace(':', 'x')}.json"
            with open(artifact_path, "w") as f:
                json.dump(size_artifact, f, indent=2)
            
            print(f"📄 Saved artifact for {product} {aspect_ratio}: {artifact_path}")

    # Compliance
    compliance = check_compliance(brief.message)

    # Create main response artifact
    main_artifact = {
        "campaign_id": campaign_id,
        "timestamp": timestamp,
        "request": {
            "products": brief.products,
            "region": brief.region,
            "audience": brief.audience,
            "message": brief.message,
            "assets": brief.assets
        },
        "response": {
            "campaign_id": campaign_id,
            "outputs": all_outputs,
            "compliance": compliance
        },
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "campaign_directory": str(campaign_dir),
            "total_products": len(brief.products),
            "total_images": sum(len(outputs) for outputs in all_outputs.values())
        }
    }

    # Save main response artifact
    main_artifact_path = campaign_dir / "response_artifact.json"
    with open(main_artifact_path, "w") as f:
        json.dump(main_artifact, f, indent=2)

    # Log to DuckDB (using first product's outputs for compatibility)
    first_product_outputs = list(all_outputs.values())[0] if all_outputs else {}
    log_campaign(campaign_id, brief, first_product_outputs, compliance)

    print(f"📁 Campaign artifacts saved to: {campaign_dir}")
    return GenerationResult(campaign_id=campaign_id, outputs=first_product_outputs, compliance=compliance)