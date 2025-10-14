import os
import httpx
import base64
from pathlib import Path
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

MODEL = "Qwen/Qwen-Image"   # can replace with "stabilityai/stable-diffusion-xl-base-1.0"
BASE_URL = "https://api-inference.huggingface.co"

OUTPUT_DIR = Path("assets/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_image(prompt: str, width: int = 1024, height: int = 1024) -> str:
    """
    Generate an image from a text prompt using Hugging Face Inference API.
    """
    url = f"{BASE_URL}/models/{MODEL}"
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

    print(f"🚀 Generating image with model {MODEL}...")
    with httpx.Client(timeout=120) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        image_bytes = response.content

    filename = OUTPUT_DIR / f"gen_{os.getpid()}_{width}x{height}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"✅ Saved image to {filename}")
    return str(filename)


if __name__ == "__main__":
    test_prompt = "a hero image for social ad campaign"
    generate_image(test_prompt, width=768, height=512)