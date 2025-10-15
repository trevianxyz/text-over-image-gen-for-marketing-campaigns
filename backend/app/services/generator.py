import os
import httpx
import base64
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load API keys from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Models
HF_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"  # Primary: Hugging Face
OPENAI_MODEL = "dall-e-3"  # Fallback: OpenAI DALL-E 3

HF_BASE_URL = "https://api-inference.huggingface.co"

OUTPUT_DIR = Path("assets/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_with_huggingface(prompt: str, width: int, height: int) -> bytes:
    """Generate image using Hugging Face API"""
    url = f"{HF_BASE_URL}/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": width,
            "height": height,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        }
    }

    print(f"🚀 Trying Hugging Face model {HF_MODEL}...")
    with httpx.Client(timeout=30) as client:  # Shorter timeout for faster fallback
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.content


def generate_with_openai(prompt: str, width: int, height: int) -> bytes:
    """Generate image using OpenAI DALL-E 3"""
    print(f"🔄 Falling back to OpenAI {OPENAI_MODEL}...")
    
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # DALL-E 3 has fixed sizes, map to closest
    if width == height:  # Square
        size = "1024x1024"
    elif width > height:  # Landscape
        size = "1792x1024"
    else:  # Portrait
        size = "1024x1792"
    
    response = client.images.generate(
        model=OPENAI_MODEL,
        prompt=prompt,
        size=size,
        quality="standard",
        n=1,
    )
    
    # Download the image
    image_url = response.data[0].url
    with httpx.Client() as client:
        response = client.get(image_url)
        response.raise_for_status()
        return response.content


def generate_creatives(prompt: str, width: int = 1024, height: int = 1024) -> str:
    """
    Generate an image with Hugging Face primary, OpenAI fallback.
    """
    try:
        # Try Hugging Face first
        image_bytes = generate_with_huggingface(prompt, width, height)
        print(f"✅ Hugging Face generation successful")
        
    except Exception as e:
        print(f"⚠️ Hugging Face failed: {e}")
        
        if not OPENAI_API_KEY:
            raise Exception("Hugging Face failed and no OpenAI API key provided")
        
        try:
            # Fallback to OpenAI
            image_bytes = generate_with_openai(prompt, width, height)
            print(f"✅ OpenAI fallback successful")
            
        except Exception as openai_error:
            raise Exception(f"Both Hugging Face and OpenAI failed. HF: {e}, OpenAI: {openai_error}")

    # Save the image
    filename = OUTPUT_DIR / f"gen_{os.getpid()}_{width}x{height}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"💾 Saved image to {filename}")
    return str(filename)


if __name__ == "__main__":
    test_prompt = "a hero image for social ad campaign"
    generate_creatives(test_prompt, width=768, height=512)