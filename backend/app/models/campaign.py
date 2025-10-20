from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict

class CampaignBrief(BaseModel):
    products: List[str]
    country_name: str
    audience: str  # Keep as string for compatibility with existing code
    message: str
    assets: Optional[List[str]] = None
    hf_model: Optional[str] = "Qwen/Qwen-Image"  # Default HF model
    image_quality: Optional[str] = "standard"  # Default quality setting
    
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