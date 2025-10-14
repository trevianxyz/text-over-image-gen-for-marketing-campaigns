from pydantic import BaseModel
from typing import Optional, List, Dict


class CampaignBrief(BaseModel):
    products: List[str]
    region: str
    audience: str
    message: str
    assets: Optional[List[str]] = None


class GenerationResult(BaseModel):
    campaign_id: str
    outputs: Dict[str, str]   # aspect_ratio → file path
    compliance: Optional[Dict] = None