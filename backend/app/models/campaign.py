from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict

class CampaignBrief(BaseModel):
    products: List[str]
    country_name: str
    audience: str  # Keep as string for compatibility with existing code
    message: str
    assets: Optional[List[str]] = None
    # Advanced generation parameters
    noise_scheduler: Optional[str] = "ddim"
    unet_backbone: Optional[str] = "default"
    vae: Optional[str] = "default"
    guidance_scale: Optional[float] = 7.5
    num_inference_steps: Optional[int] = 30
    seed: Optional[int] = None
    
    @field_validator('country_name')
    @classmethod
    def validate_country_name(cls, v):
        """Validate that the country_name is a valid country code or legacy region"""
        from app.services.country_language import get_country_by_code, get_legacy_region_mapping
        
        # Check if it's a valid country code
        if get_country_by_code(v):
            return v
            
        # Check if it's a legacy region name
        if get_legacy_region_mapping(v):
            return v
            
        # If neither, raise validation error
        raise ValueError(f"Invalid country_name: {v}. Must be a valid country code or legacy region name.")

class GenerationResult(BaseModel):
    campaign_id: str
    outputs: Dict[str, Dict[str, str]]   # product → (aspect_ratio → file path)
    compliance: Optional[Dict] = None
    metadata: Optional[Dict] = None  # Token usage and other metadata