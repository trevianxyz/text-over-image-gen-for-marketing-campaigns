from fastapi import APIRouter
import uuid
from app.models import CampaignBrief, GenerationResult
from app.services.embeddings import embed_and_store, search_similar
from app.services.generator import generate_creatives
from app.services.logging_db import log_campaign
from app.services.compliance import check_compliance

router = APIRouter()

@router.post("/generate", response_model=GenerationResult)
def generate_campaign(brief: CampaignBrief):
    campaign_id = str(uuid.uuid4())

    # Store embeddings
    embed_and_store(campaign_id, brief.message, brief.model_dump())

    # Generate creatives for different aspect ratios
    prompt = f"{brief.message} for {brief.audience} in {brief.region}"
    outputs = {
        "1:1": generate_creatives(prompt, width=1024, height=1024),    # Square
        "16:9": generate_creatives(prompt, width=1024, height=576),    # Landscape
        "9:16": generate_creatives(prompt, width=576, height=1024),    # Portrait
    }

    # Compliance
    compliance = check_compliance(brief.message)

    # Log to DuckDB
    log_campaign(campaign_id, brief, outputs, compliance)

    return GenerationResult(campaign_id=campaign_id, outputs=outputs, compliance=compliance)