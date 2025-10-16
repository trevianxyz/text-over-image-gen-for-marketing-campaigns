"""
Audience selector service for standardized target audience selection.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel

class AudienceOption(BaseModel):
    """Represents an audience option for the selector"""
    id: str
    label: str
    description: str
    age_group: Optional[str] = None
    gender: Optional[str] = None
    interests: List[str] = []
    category: str  # e.g., "Demographics", "Professions", "Interests"

# Predefined audience options
AUDIENCE_OPTIONS: List[AudienceOption] = [
    # Demographics
    AudienceOption(
        id="young_adults",
        label="Young Adults (18-24)",
        description="College students and young professionals",
        age_group="18-24",
        interests=["technology", "social media", "entertainment"],
        category="Demographics"
    ),
    AudienceOption(
        id="millennials",
        label="Millennials (25-34)",
        description="Early career professionals",
        age_group="25-34",
        interests=["technology", "career", "travel", "fitness"],
        category="Demographics"
    ),
    AudienceOption(
        id="gen_x",
        label="Gen X (35-44)",
        description="Established professionals and parents",
        age_group="35-44",
        interests=["family", "career", "home improvement", "health"],
        category="Demographics"
    ),
    AudienceOption(
        id="boomers",
        label="Baby Boomers (45-64)",
        description="Experienced professionals and empty nesters",
        age_group="45-54",
        interests=["retirement planning", "health", "travel", "hobbies"],
        category="Demographics"
    ),
    
    # Professions
    AudienceOption(
        id="construction_workers",
        label="Construction Workers",
        description="Skilled tradespeople in construction industry",
        interests=["safety", "tools", "construction", "workplace safety"],
        category="Professions"
    ),
    AudienceOption(
        id="healthcare_workers",
        label="Healthcare Workers",
        description="Medical professionals and healthcare staff",
        interests=["health", "medical", "patient care", "safety"],
        category="Professions"
    ),
    AudienceOption(
        id="office_workers",
        label="Office Workers",
        description="Corporate and administrative professionals",
        interests=["productivity", "technology", "career", "workplace"],
        category="Professions"
    ),
    AudienceOption(
        id="retail_workers",
        label="Retail Workers",
        description="Sales associates and retail staff",
        interests=["customer service", "sales", "fashion", "retail"],
        category="Professions"
    ),
    AudienceOption(
        id="manufacturing_workers",
        label="Manufacturing Workers",
        description="Industrial and production workers",
        interests=["safety", "tools", "manufacturing", "quality"],
        category="Professions"
    ),
    AudienceOption(
        id="transportation_workers",
        label="Transportation Workers",
        description="Drivers, logistics, and transportation staff",
        interests=["safety", "logistics", "transportation", "fleet management"],
        category="Professions"
    ),
    
    # Interest-based
    AudienceOption(
        id="safety_conscious",
        label="Safety-Conscious Individuals",
        description="People who prioritize safety in their work and daily life",
        interests=["safety", "protection", "workplace safety", "personal safety"],
        category="Interests"
    ),
    AudienceOption(
        id="tech_enthusiasts",
        label="Tech Enthusiasts",
        description="Early adopters of technology and innovation",
        interests=["technology", "innovation", "gadgets", "digital tools"],
        category="Interests"
    ),
    AudienceOption(
        id="fitness_enthusiasts",
        label="Fitness Enthusiasts",
        description="People focused on health and physical fitness",
        interests=["fitness", "health", "exercise", "wellness"],
        category="Interests"
    ),
    AudienceOption(
        id="environmental_conscious",
        label="Environmentally Conscious",
        description="People who care about sustainability and environmental impact",
        interests=["sustainability", "environment", "green living", "eco-friendly"],
        category="Interests"
    ),
    
    # Gender-specific
    AudienceOption(
        id="male_professionals",
        label="Male Professionals",
        description="Working men across various industries",
        gender="male",
        interests=["career", "technology", "sports", "tools"],
        category="Demographics"
    ),
    AudienceOption(
        id="female_professionals",
        label="Female Professionals",
        description="Working women across various industries",
        gender="female",
        interests=["career", "workplace equality", "health", "work-life balance"],
        category="Demographics"
    ),
    
    # Industry-specific
    AudienceOption(
        id="warehouse_workers",
        label="Warehouse Workers",
        description="Logistics and warehouse operations staff",
        interests=["logistics", "inventory", "safety", "efficiency"],
        category="Professions"
    ),
    AudienceOption(
        id="maintenance_workers",
        label="Maintenance Workers",
        description="Facilities and equipment maintenance staff",
        interests=["tools", "repair", "maintenance", "safety"],
        category="Professions"
    ),
    AudienceOption(
        id="security_personnel",
        label="Security Personnel",
        description="Security guards and safety officers",
        interests=["safety", "security", "protection", "emergency response"],
        category="Professions"
    ),
]

def get_audience_selector_data() -> Dict:
    """Get audience selector data for the frontend"""
    categories = {}
    
    # Group by category
    for option in AUDIENCE_OPTIONS:
        if option.category not in categories:
            categories[option.category] = []
        categories[option.category].append({
            "id": option.id,
            "label": option.label,
            "description": option.description,
            "age_group": option.age_group,
            "gender": option.gender,
            "interests": option.interests,
            "category": option.category
        })
    
    # Convert AUDIENCE_OPTIONS to dict format for JSON serialization
    audiences_list = [option.model_dump() for option in AUDIENCE_OPTIONS]
    
    return {
        "audiences": audiences_list,
        "categories": categories,
        "total_count": len(AUDIENCE_OPTIONS)
    }

def get_audience_by_id(audience_id: str) -> Optional[AudienceOption]:
    """Get an audience option by its ID"""
    for option in AUDIENCE_OPTIONS:
        if option.id == audience_id:
            return option
    return None

def validate_audience(audience_id: str) -> bool:
    """Validate that an audience ID is valid"""
    return get_audience_by_id(audience_id) is not None
