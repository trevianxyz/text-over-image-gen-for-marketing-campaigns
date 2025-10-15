import os
import httpx
import base64
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
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

# Brand overlay settings
BRAND_IMAGE_PATH = Path("frontend/images/werkr_brand_image.png")
BRAND_OVERLAY_SIZE = (200, 200)  # Size of brand overlay
BRAND_POSITION = "bottom_right"  # Position of brand overlay


def translate_message_with_llm(message: str, region: str) -> str:
    """
    Use LLM to translate the message into the native language of the region.
    """
    # Map regions to their primary languages
    region_languages = {
        "California": "Spanish",
        "Texas": "Spanish", 
        "Nevada": "Spanish",
        "New York": "English",
        "Florida": "Spanish",
        "Costa Rica": "Spanish",
        "Mexico": "Spanish",
        "Canada": "French",
        "UK": "English",
        "Germany": "German",
        "France": "French",
        "Japan": "Japanese",
        "Australia": "English",
        "Brazil": "Portuguese",
        "Italy": "Italian",
        "Spain": "Spanish",
        "China": "Chinese",
        "India": "Hindi",
        "South Korea": "Korean",
        "Russia": "Russian"
    }
    
    target_language = region_languages.get(region, "English")
    
    if target_language == "English":
        return message
    
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": f"Translate the following marketing message into {target_language}. Keep it concise and impactful for advertising. Return only the translation, no explanations."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=100,
            temperature=0.3
        )
        
        translated_message = response.choices[0].message.content.strip()
        print(f"🌍 Translated '{message}' to {target_language}: '{translated_message}'")
        return translated_message
        
    except Exception as e:
        print(f"⚠️ Translation failed for {region}: {e}")
        return message  # Fallback to original message


def localize_prompt(prompt: str, region: str) -> str:
    """
    Localize the prompt based on region for better cultural relevance.
    """
    localization_map = {
        "California": "California lifestyle, West Coast vibes, sunny weather",
        "Texas": "Texas pride, Southern hospitality, big sky country",
        "Nevada": "Nevada desert, Las Vegas energy, outdoor adventure",
        "New York": "New York City energy, urban sophistication, fast-paced",
        "Florida": "Florida sunshine, tropical vibes, beach lifestyle",
        "Costa Rica": "Costa Rica eco-friendly, tropical paradise, Pura Vida lifestyle",
        "Mexico": "Mexican culture, vibrant colors, traditional craftsmanship",
        "Canada": "Canadian wilderness, friendly people, outdoor adventure",
        "UK": "British heritage, classic style, urban sophistication",
        "Germany": "German precision, engineering excellence, quality craftsmanship",
        "France": "French elegance, artisanal quality, sophisticated style",
        "Japan": "Japanese minimalism, attention to detail, quality craftsmanship",
        "Australia": "Australian outback, laid-back lifestyle, outdoor adventure"
    }
    
    localized_context = localization_map.get(region, f"{region} culture and lifestyle")
    return f"{prompt}, {localized_context}"


def add_brand_overlay(image_path: str, product: str, region: str, message: str) -> str:
    """
    Add brand overlay, localized text, and translated message to the image.
    """
    # Translate the message to the region's native language
    translated_message = translate_message_with_llm(message, region)
    
    # Load the main image
    with Image.open(image_path) as img:
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Load brand image
        if BRAND_IMAGE_PATH.exists():
            brand_img = Image.open(BRAND_IMAGE_PATH)
            brand_img = brand_img.resize(BRAND_OVERLAY_SIZE, Image.Resampling.LANCZOS)
            
            # Calculate position based on BRAND_POSITION
            if BRAND_POSITION == "bottom_right":
                x = img.width - brand_img.width - 20
                y = img.height - brand_img.height - 20
            elif BRAND_POSITION == "bottom_left":
                x = 20
                y = img.height - brand_img.height - 20
            elif BRAND_POSITION == "top_right":
                x = img.width - brand_img.width - 20
                y = 20
            else:  # top_left
                x = 20
                y = 20
            
            # Paste brand overlay
            img.paste(brand_img, (x, y), brand_img)
        
        # Add text overlays
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fallback to default if not available
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            try:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            except:
                font_large = None
                font_small = None
        
        # 1. Add translated message (main text) in bottom right
        if translated_message:
            # Calculate position for translated message (bottom right, above brand)
            if font_large:
                bbox = draw.textbbox((0, 0), translated_message, font=font_large)
                msg_width = bbox[2] - bbox[0]
                msg_height = bbox[3] - bbox[1]
            else:
                msg_width = len(translated_message) * 12
                msg_height = 24
            
            # Position message in bottom right, above brand logo
            msg_x = img.width - msg_width - 30
            msg_y = img.height - msg_height - 80 if BRAND_IMAGE_PATH.exists() else img.height - msg_height - 30
            
            # Add message with outline for visibility
            outline_color = (0, 0, 0, 255)
            text_color = (255, 255, 255, 255)
            
            # Draw outline
            for adj in range(-2, 3):
                for adj2 in range(-2, 3):
                    if adj != 0 or adj2 != 0:
                        draw.text((msg_x + adj, msg_y + adj2), translated_message, font=font_large, fill=outline_color)
            
            # Draw main text
            draw.text((msg_x, msg_y), translated_message, font=font_large, fill=text_color)
        
        # 2. Add region branding text (smaller, above brand logo)
        region_text = {
            "California": "Made in California",
            "Texas": "Texas Strong",
            "Nevada": "Nevada Proud",
            "New York": "NYC Quality",
            "Florida": "Florida Fresh",
            "Costa Rica": "Pura Vida",
            "Mexico": "Hecho en México",
            "Canada": "Made in Canada",
            "UK": "British Quality",
            "Germany": "Made in Germany",
            "France": "Fabriqué en France",
            "Japan": "日本製",
            "Australia": "Made in Australia"
        }
        
        region_label = region_text.get(region, f"Made in {region}")
        
        # Calculate position for region label (above brand logo)
        if font_small:
            bbox = draw.textbbox((0, 0), region_label, font=font_small)
            region_width = bbox[2] - bbox[0]
            region_height = bbox[3] - bbox[1]
        else:
            region_width = len(region_label) * 8
            region_height = 16
        
        region_x = x + (brand_img.width - region_width) // 2 if BRAND_IMAGE_PATH.exists() else 20
        region_y = y - region_height - 10 if BRAND_IMAGE_PATH.exists() else img.height - 50
        
        # Add region label with outline
        for adj in range(-1, 2):
            for adj2 in range(-1, 2):
                if adj != 0 or adj2 != 0:
                    draw.text((region_x + adj, region_y + adj2), region_label, font=font_small, fill=outline_color)
        
        # Draw main region text
        draw.text((region_x, region_y), region_label, font=font_small, fill=text_color)
        
        # Save the modified image
        img.save(image_path, "PNG", quality=95)
        print(f"🏷️ Added brand overlay, translated message, and localization for {product} in {region}")
    
    return image_path


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


def generate_single_image(prompt: str, campaign_id: str, product: str, region: str) -> str:
    """
    Generate a single base image using Hugging Face or OpenAI fallback.
    Returns the path to the base image.
    """
    # Create timestamped campaign directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    campaign_dir = OUTPUT_DIR / f"campaign_{timestamp}_{campaign_id}"
    product_dir = campaign_dir / product.replace(" ", "_").lower()
    product_dir.mkdir(parents=True, exist_ok=True)
    
    # Localize the prompt for better cultural relevance
    localized_prompt = localize_prompt(prompt, region)
    print(f"🌍 Localized prompt for {region}: {localized_prompt}")
    
    # Generate base image (use square format for best quality)
    try:
        # Try Hugging Face first
        image_bytes = generate_with_huggingface(localized_prompt, width=1024, height=1024)
        print(f"✅ Hugging Face generation successful for {product}")
        
    except Exception as e:
        print(f"⚠️ Hugging Face failed for {product}: {e}")
        
        if not OPENAI_API_KEY:
            raise Exception("Hugging Face failed and no OpenAI API key provided")
        
        try:
            # Fallback to OpenAI
            image_bytes = generate_with_openai(localized_prompt, width=1024, height=1024)
            print(f"✅ OpenAI fallback successful for {product}")
            
        except Exception as openai_error:
            raise Exception(f"Both Hugging Face and OpenAI failed for {product}. HF: {e}, OpenAI: {openai_error}")

    # Save the base image
    base_image_path = product_dir / "base_image.png"
    with open(base_image_path, "wb") as f:
        f.write(image_bytes)

    print(f"💾 Saved base image for {product} to {base_image_path}")
    return str(base_image_path)


def create_size_variants(base_image_path: str, campaign_id: str, product: str, region: str, message: str) -> dict:
    """
    Create 3 size variants (1:1, 16:9, 9:16) from a base image.
    Each size gets its own subdirectory with image and artifact.
    Returns dict with aspect ratios as keys and file paths as values.
    """
    base_path = Path(base_image_path)
    product_dir = base_path.parent
    
    # Load the base image
    with Image.open(base_image_path) as img:
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        outputs = {}
        size_configs = {
            "1:1": {"size": (1024, 1024), "dir": "1x1"},
            "16:9": {"size": (1024, 576), "dir": "16x9"},
            "9:16": {"size": (576, 1024), "dir": "9x16"}
        }
        
        for aspect_ratio, config in size_configs.items():
            # Create size subdirectory
            size_dir = product_dir / config["dir"]
            size_dir.mkdir(parents=True, exist_ok=True)
            
            # Resize image
            resized_img = img.resize(config["size"], Image.Resampling.LANCZOS)
            # Include size in filename
            size_filename = f"image_{aspect_ratio.replace(':', 'x')}.png"
            image_path = size_dir / size_filename
            resized_img.save(image_path, "PNG", quality=95)
            
            # Add brand overlay, localization, and translated message
            final_image_path = add_brand_overlay(str(image_path), product, region, message)
            outputs[aspect_ratio] = final_image_path
            print(f"📐 Created {aspect_ratio} variant for {product}: {final_image_path}")
    
    return outputs


def generate_creatives(prompt: str, width: int = 1024, height: int = 1024, campaign_id: str = None, product: str = None, region: str = None, message: str = None) -> dict:
    """
    Generate one image and create 3 size variants for a specific product.
    Returns dict with aspect ratios as keys and file paths as values.
    """
    # Generate the base image for this product
    base_image_path = generate_single_image(prompt, campaign_id, product, region)
    
    # Create size variants for this product
    outputs = create_size_variants(base_image_path, campaign_id, product, region, message)
    
    return outputs


if __name__ == "__main__":
    test_prompt = "a hero image for social ad campaign"
    generate_creatives(test_prompt, width=768, height=512)