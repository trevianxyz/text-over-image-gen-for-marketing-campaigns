from pydantic import BaseModel, validator
from typing import Optional, List, Dict

from enum import Enum

class AgeGroup(str, Enum):
    group_18_24 = "18-24"
    group_25_34 = "25-34"
    group_35_44 = "35-44"
    group_45_54 = "45-54"
    group_55_64 = "55-64"
    group_65_plus = "65+"

class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "transgender"
    not_specified = "not specified"

class Audience(BaseModel):
    age_group: Optional[AgeGroup] = None
    gender: Optional[Gender] = None
    interests: Optional[List[str]] = None # e.g. ["tech", "sports"]
   

class CampaignBrief(BaseModel):
    products: List[str]
    region: str
    audience: str  # Keep as string for compatibility with existing code
    message: str
    assets: Optional[List[str]] = None
    
    @validator('region')
    def validate_region(cls, v):
        """Validate that the region is a valid country code or legacy region"""
        from app.services.country_language import get_country_by_code, get_legacy_region_mapping
        
        # Check if it's a valid country code
        if get_country_by_code(v):
            return v
            
        # Check if it's a legacy region name
        if get_legacy_region_mapping(v):
            return v
            
        # If neither, raise validation error
        raise ValueError(f"Invalid region: {v}. Must be a valid country code or legacy region name.")

class GenerationResult(BaseModel):
    campaign_id: str
    outputs: Dict[str, Dict[str, str]]   # product → (aspect_ratio → file path)
    compliance: Optional[Dict] = None
    metadata: Optional[Dict] = None  # Token usage and other metadata