"""Compliance checking for campaign content"""
from typing import Dict, Optional, List
import re
from pathlib import Path
# from PIL import Image  # For future brand overlay verification
# import numpy as np  # For future brand overlay verification


# List of inappropriate words and phrases (expandable)
INAPPROPRIATE_CONTENT = [
    'shit', 'damn', 'hell', 'ass', 'bastard',
    'crap'
]


def verify_brand_overlay(image_path: str, brand_reference_path: str = "frontend/images/werkr_brand_image.png") -> bool:
    """
    Verify that the brand overlay was successfully applied to the image.
    
    PLACEHOLDER: Currently always returns True.
    TODO: Implement computer vision-based verification when needed.
    
    Returns True if brand overlay is detected, False otherwise.
    """
    # Placeholder implementation - assumes brand overlay is applied correctly
    # The add_brand_overlay() function in generator.py handles the actual overlay
    print(f"✅ Brand overlay check (placeholder) passed for {Path(image_path).name}")
    return True
    
    # Future implementation would use image comparison:
    # try:
    #     img_path = Path(image_path)
    #     if not img_path.exists():
    #         return False
    #     
    #     brand_path = Path(brand_reference_path)
    #     if not brand_path.exists():
    #         return False
    #     
    #     with Image.open(img_path) as img, Image.open(brand_path) as brand:
    #         # Extract top-left region (20, 20) where brand should be
    #         # Compare with expected brand image
    #         # Calculate similarity metric (MSE, SSIM, etc.)
    #         # Return True if similarity above threshold
    #         pass
    # except Exception as e:
    #     print(f"❌ Error verifying brand overlay: {e}")
    #     return False


def check_compliance(message: str, image_paths: Optional[List[str]] = None) -> Optional[Dict]:
    """
    Check if the campaign message and generated images comply with regulations.
    
    Args:
        message: Campaign message text
        image_paths: Optional list of image paths to verify brand overlay
    
    Returns compliance report
    """
    issues = []
    message_lower = message.lower()
    
    # Check for inappropriate language
    for word in INAPPROPRIATE_CONTENT:
        # Use word boundaries to match whole words
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, message_lower):
            issues.append(f"Inappropriate language detected: '{word}'")
    
    # Check for excessive caps (yelling)
    if len(message) > 10 and sum(1 for c in message if c.isupper()) / len(message) > 0.7:
        issues.append("Excessive use of capital letters detected")
    
    # Check for minimum length
    if len(message.strip()) < 10:
        issues.append("Message too short (minimum 10 characters required)")
    
    # Check brand overlay on images if provided
    if image_paths:
        images_without_overlay = []
        for img_path in image_paths:
            if not verify_brand_overlay(img_path):
                images_without_overlay.append(Path(img_path).name)
        
        if images_without_overlay:
            issues.append(f"Brand overlay missing or not detected in {len(images_without_overlay)} image(s): {', '.join(images_without_overlay[:3])}")
    
    # Determine status based on issues
    if len(issues) > 0:
        return {
            "status": "failed",
            "issues": issues,
            "message": f"Compliance check failed: {', '.join(issues)}"
        }
    else:
        return {
            "status": "approved",
            "issues": [],
            "message": "No compliance issues detected"
        }

