from fastapi import APIRouter, HTTPException
import uuid
import json
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel
from app.models import CampaignBrief, GenerationResult
from app.services.embeddings import embed_and_store, search_similar
from app.services.generator import generate_creatives, get_last_translation_metadata
from app.services.logging_db import log_campaign
from app.services.compliance import check_compliance

router = APIRouter()

class SearchQuery(BaseModel):
    query: str
    top_k: int = 3

@router.post("/generate", response_model=GenerationResult)
def generate_campaign(brief: CampaignBrief):
    campaign_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    campaign_dir = None
    
    try:
        # Create campaign directory
        campaign_dir = Path("assets/generated") / f"campaign_{timestamp}_{campaign_id}"
        campaign_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created campaign directory: {campaign_dir}")

        # Store embeddings
        embed_and_store(campaign_id, brief.message, brief.model_dump())

        # Generate images for each product with comprehensive prompts
        all_outputs = {}

        for product in brief.products:
            print(f"🎨 Generating creatives for product: {product}")
            
            # Get country and language information
            from app.services.country_language import get_legacy_region_mapping, get_primary_language, get_country_by_code
            country_code = get_legacy_region_mapping(brief.country_name) or brief.country_name
            target_language = get_primary_language(country_code)
            country_info = get_country_by_code(country_code)
            country_full_name = country_info.name if country_info else brief.country_name
            
            # Parse audience into profession and demographic
            audience_parts = brief.audience.split('_') if brief.audience else []
            profession = audience_parts[0] if len(audience_parts) > 0 else brief.audience
            demographic = audience_parts[1] if len(audience_parts) > 1 else ""
            
            # Craft comprehensive prompt with all context
            prompt_parts = [
                brief.message,
                f"Product: {product}",
                f"Target audience: {profession}",
            ]
            
            if demographic:
                prompt_parts.append(f"Demographic: {demographic}")
            
            prompt_parts.extend([
                f"Location: {country_full_name}",
                f"Language: {target_language}",
                f"Style: professional marketing photography for work apparel brand"
            ])
            
            prompt = ". ".join(prompt_parts)
            print(f"📝 Generated prompt: {prompt[:150]}...")
            
            product_outputs = generate_creatives(
                prompt,
                campaign_id=campaign_id,
                product=product,
                country_name=brief.country_name,
                message=brief.message,
                campaign_dir=campaign_dir,
                audience=brief.audience
            )
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
                        "country_name": brief.country_name,
                        "audience": brief.audience,
                        "message": brief.message,
                        "assets": brief.assets
                    },
                    "response": {
                        "campaign_id": campaign_id,
                        "product": product,
                        "aspect_ratio": aspect_ratio,
                        "image_path": image_path
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

        # Check compliance LAST - after all images are generated but before finalization
        print(f"🔍 Running compliance check on generated content...")
        
        # Collect all generated image paths for brand overlay verification
        all_image_paths = []
        for product_name, product_outputs in all_outputs.items():
            for aspect_ratio, image_path in product_outputs.items():
                all_image_paths.append(image_path)
        
        print(f"📸 Verifying brand overlay on {len(all_image_paths)} images...")
        compliance = check_compliance(brief.message, image_paths=all_image_paths)
        print(f"📋 Compliance check result: {compliance['status']}")
        
        # If compliance fails, raise an error
        if compliance['status'] == 'failed':
            print(f"❌ Compliance check failed: {compliance['message']}")
            # Clean up the campaign directory since it failed compliance
            import shutil
            if campaign_dir.exists():
                shutil.rmtree(campaign_dir)
                print(f"🗑️  Removed campaign directory due to compliance failure")
            
            raise HTTPException(status_code=400, detail={
                "error": "Compliance check failed",
                "compliance": compliance
            })

        # Create main response artifact
        main_artifact = {
            "campaign_id": campaign_id,
            "timestamp": timestamp,
            "request": {
                "products": brief.products,
                "country_name": brief.country_name,
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
                "gpt-4o": {"prompt": 30.00, "completion": 60.00},  # $30.00 input, $60.00 output per 1M tokens
                "gpt-3.5-turbo": {"prompt": 0.50, "completion": 1.50}  # $0.50 input, $1.50 output per 1M tokens
            }
            
            # Get model pricing (default to gpt-4 if not found)
            model_pricing = pricing.get(model, pricing["gpt-4.1"])
            
            # Calculate cost: (tokens / 1,000,000) * price_per_million
            prompt_cost = (prompt_tokens / 1_000_000) * model_pricing["prompt"]
            completion_cost = (completion_tokens / 1_000_000) * model_pricing["completion"]
            total_cost = prompt_cost + completion_cost
            
            return round(total_cost, 6)  # Round to 6 decimal places for micro-cents
        
        if translation_metadata:
            cost = calculate_cost(
                translation_metadata.get("model", "gpt-4.1"),
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
    
    except HTTPException:
        # Re-raise HTTP exceptions (like compliance failures)
        raise
    except Exception as e:
        # Handle unexpected errors
        print(f"❌ Unexpected error during campaign generation: {e}")
        import traceback
        traceback.print_exc()
        
        # Clean up campaign directory if it was created
        if campaign_dir and campaign_dir.exists():
            import shutil
            shutil.rmtree(campaign_dir)
            print(f"🗑️  Cleaned up failed campaign directory: {campaign_dir}")
        
        raise HTTPException(status_code=500, detail={
            "error": "Campaign generation failed",
            "message": str(e),
            "campaign_id": campaign_id
        })


@router.post("/search")
def search_campaigns(search_query: SearchQuery):
    """
    Search for similar campaigns using natural language query.
    Searches across campaign messages, countries, audiences, and products.
    """
    try:
        # Validate input
        if not search_query.query or not search_query.query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        if search_query.top_k < 1 or search_query.top_k > 20:
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 20")
        
        print(f"🔍 Searching for similar campaigns: '{search_query.query}'")
        
        # Search the vector database
        results = search_similar(search_query.query, top_k=search_query.top_k)
        
        # Load master manifest to get full campaign details
        master_manifest_path = Path("assets/generated/master_manifest.json")
        campaigns_lookup = {}
        
        if master_manifest_path.exists():
            with open(master_manifest_path, "r") as f:
                manifest = json.load(f)
                campaigns_lookup = {c["campaign_id"]: c for c in manifest.get("campaigns", [])}
        
        # Enrich results with full campaign data
        enriched_results = []
        if results and results.get("ids") and len(results["ids"]) > 0:
            for i, campaign_id in enumerate(results["ids"][0]):
                distance = results["distances"][0][i] if "distances" in results else None
                metadata = results["metadatas"][0][i] if "metadatas" in results else {}
                document = results["documents"][0][i] if "documents" in results else ""
                
                # Get full campaign data from manifest
                campaign_data = campaigns_lookup.get(campaign_id, {})
                
                # Convert cosine distance (0-2) to similarity percentage (0-100)
                # Cosine distance: 0 = identical, 2 = opposite
                # Cosine similarity = 1 - (distance / 2) -> ranges from 0 to 1
                similarity = (1 - (distance / 2)) if distance is not None else None
                
                enriched_results.append({
                    "campaign_id": campaign_id,
                    "similarity_score": similarity,
                    "distance": distance,
                    "message": document,
                    "metadata": metadata,
                    "full_campaign": campaign_data
                })
        
        print(f"✅ Found {len(enriched_results)} similar campaigns")
        return {
            "results": enriched_results,
            "query": search_query.query,
            "total_results": len(enriched_results)
        }
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


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
