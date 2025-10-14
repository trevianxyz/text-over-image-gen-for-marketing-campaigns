from fastapi import APIRouter
import uuid
from app.models.campaign import CampaignBrief
from app.services.embeddings import upsert_asset, search_assets
from app.services.logging_db import log_campaign
from app.services.generator import generate_creative

router = APIRouter(prefix="/campaigns")

@router.post("/generate")
def generate_campaign(brief: CampaignBrief):
    campaign_id = str(uuid.uuid4())

    # index in Chroma
    upsert_asset(campaign_id, brief.message, brief.dict())

    # optional: search existing assets
    similar = search_assets(brief.message, top_k=2)

    # generate creatives
    base_img = "assets/input/sample.png"
    outputs = generate_creative(base_img, brief.message, f"assets/output/{campaign_id}")

    # log in DuckDB
    log_campaign(campaign_id, brief, outputs, {"similar": similar})

    return {"id": campaign_id, "outputs": outputs, "similar_assets": similar}