from pydantic import BaseModel
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

class GenerationResult(BaseModel):
    campaign_id: str
    outputs: Dict[str, str]   # aspect_ratio → file path
    compliance: Optional[Dict] = None