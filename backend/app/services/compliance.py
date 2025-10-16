"""Compliance checking for campaign content"""
from typing import Dict, Optional
import re


# List of inappropriate words and phrases (expandable)
INAPPROPRIATE_CONTENT = [
    'fuck', 'shit', 'damn', 'hell', 'ass', 'bitch', 'bastard',
    'crap'
]


def check_compliance(message: str) -> Optional[Dict]:
    """
    Check if the campaign message complies with regulations
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

