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

    # TODO: find base image (mock: just use a placeholder)
    base_image = "assets/input/sample.png"

    outputs = generate_creatives(base_image, brief.message, f"assets/output/{campaign_id}")

    # Compliance
    compliance = check_compliance(brief.message)

    # Log to DuckDB
    log_campaign(campaign_id, brief, outputs, compliance)

    return GenerationResult(campaign_id=campaign_id, outputs=outputs, compliance=compliance)