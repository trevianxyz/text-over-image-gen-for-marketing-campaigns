from fastapi import APIRouter
import uuid
import json
from pathlib import Path
from datetime import datetime
from app.models import CampaignBrief, GenerationResult
from app.services.embeddings import embed_and_store, search_similar
from app.services.generator import generate_creatives, get_last_translation_metadata
from app.services.logging_db import log_campaign
from app.services.compliance import check_compliance

router = APIRouter()

@router.post("/generate", response_model=GenerationResult)
def generate_campaign(brief: CampaignBrief):
    campaign_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Check compliance FIRST before any processing
    compliance = check_compliance(brief.message)
    print(f"🔍 Compliance check result: {compliance['status']}")
    
    if compliance['status'] == 'failed':
        print(f"❌ Compliance check failed: {compliance['message']}")
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail={
            "error": "Compliance check failed",
            "compliance": compliance
        })
    
    # Create campaign directory
    campaign_dir = Path("assets/generated") / f"campaign_{timestamp}_{campaign_id}"
    campaign_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created campaign directory: {campaign_dir}")

    # Store embeddings
    embed_and_store(campaign_id, brief.message, brief.model_dump())

    # Generate images for each product
    prompt = f"{brief.message} for {brief.audience} in {brief.region}"
    all_outputs = {}
    
    for product in brief.products:
        print(f"🎨 Generating creatives for product: {product}")
        product_outputs = generate_creatives(prompt, campaign_id=campaign_id, product=product, region=brief.region, message=brief.message, campaign_dir=campaign_dir, audience=brief.audience)
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

    # Collect metadata (token usage from translations)
    translation_metadata = get_last_translation_metadata()
    
    # Calculate cost based on model and token usage
    def calculate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost in USD based on OpenAI pricing (as of October 2024)"""
        # Pricing per 1M tokens - https://openai.com/api/pricing/
        pricing = {
            "gpt-5": {"prompt": 1.250, "completion": 10.00},  # $1.250 input, $10.00 output per 1M tokens
            "gpt-4.1": {"prompt": 3.00, "completion": 12.00},  # $3.00 input, $12.00 output per 1M tokens
            "gpt-4": {"prompt": 30.00, "completion": 60.00},  # $30.00 input, $60.00 output per 1M tokens
            "gpt-3.5-turbo": {"prompt": 0.50, "completion": 1.50}  # $0.50 input, $1.50 output per 1M tokens
        }
        
        # Get model pricing (default to gpt-4 if not found)
        model_pricing = pricing.get(model, pricing["gpt-4"])
        
        # Calculate cost: (tokens / 1,000,000) * price_per_million
        prompt_cost = (prompt_tokens / 1_000_000) * model_pricing["prompt"]
        completion_cost = (completion_tokens / 1_000_000) * model_pricing["completion"]
        total_cost = prompt_cost + completion_cost
        
        return round(total_cost, 6)  # Round to 6 decimal places for micro-cents
    
    if translation_metadata:
        cost = calculate_cost(
            translation_metadata.get("model", "gpt-4"),
            translation_metadata.get("prompt_tokens", 0),
            translation_metadata.get("completion_tokens", 0)
        )
    else:
        cost = 0.0
    
    metadata = {
        "generated_at": datetime.now().isoformat(),
        "total_products": len(brief.products),
        "total_images": sum(len(outputs) for outputs in all_outputs.values()),
        "llm_usage": translation_metadata if translation_metadata else {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "model": "none"
        },
        "cost_usd": cost
    }

    print(f"📁 Campaign artifacts saved to: {campaign_dir}")
    print(f"📊 LLM Token usage: {metadata['llm_usage']}")
    return GenerationResult(campaign_id=campaign_id, outputs=all_outputs, compliance=compliance, metadata=metadata)


@router.get("/master-manifest")
def get_master_manifest():
    """
    Returns the master manifest containing all campaign history
    """
    master_manifest_path = Path("assets/generated/master_manifest.json")
    
    if not master_manifest_path.exists():
        return {
            "campaigns": [],
            "total_count": 0,
            "last_updated": None
        }
    
    try:
        with open(master_manifest_path, "r") as f:
            manifest = json.load(f)
        return manifest
    except Exception as e:
        print(f"❌ Error reading master manifest: {e}")
        return {
            "campaigns": [],
            "total_count": 0,
            "last_updated": None,
            "error": str(e)
        }
