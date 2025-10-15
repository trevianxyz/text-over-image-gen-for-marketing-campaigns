import os
import httpx
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional
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
    from .country_language import get_legacy_region_mapping, get_primary_language
    
    # Handle both legacy region names and country codes
    country_code = get_legacy_region_mapping(region) or region
    target_language = get_primary_language(country_code)

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
    from .country_language import get_legacy_region_mapping, get_country_by_code
    
    # Handle both legacy region names and country codes
    country_code = get_legacy_region_mapping(region) or region
    country_info = get_country_by_code(country_code)
    
    if country_info:
        # Use country-specific localization
        localized_context = f"{country_info.name} culture, {country_info.region} lifestyle"
    else:
        # Fallback to generic localization
        localized_context = f"{region} culture and lifestyle"
    
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
        from .country_language import get_legacy_region_mapping, get_country_by_code
        
        # Handle both legacy region names and country codes
        country_code = get_legacy_region_mapping(region) or region
        country_info = get_country_by_code(country_code)
        
        if country_info:
            # Use country-specific branding
            region_label = f"Made in {country_info.name}"
        else:
            # Fallback to generic branding
            region_label = f"Made in {region}"

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


def generate_single_image(prompt: str, campaign_id: str, product: str, region: str, campaign_dir: Optional[Path] = None) -> str:
    """
    Generate a single base image using Hugging Face or OpenAI fallback.
    Returns the path to the base image.
    """
    # Use provided campaign directory or create a new one
    if campaign_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        campaign_dir = OUTPUT_DIR / f"campaign_{timestamp}_{campaign_id}"
        print(f"⚠️ No campaign_dir provided, creating new one: {campaign_dir}")
    else:
        print(f"✅ Using provided campaign_dir: {campaign_dir}")
    
    product_dir = campaign_dir / product.replace(" ", "_").lower()
    product_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created product directory: {product_dir}")

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


def create_size_variants(base_image_path: str, campaign_id: str, product: str, region: str, message: str, campaign_dir: Optional[Path] = None) -> dict:
    """
    Create 3 size variants (1:1, 16:9, 9:16) from a base image.
    Uses smart cropping to maintain aspect ratio and image quality.
    """
    base_path = Path(base_image_path)
    
    # Use provided campaign_dir to determine product_dir, or fall back to base_path.parent
    if campaign_dir is not None:
        product_dir = campaign_dir / product.replace(" ", "_").lower()
        print(f"✅ Using campaign_dir for product_dir: {product_dir}")
    else:
        product_dir = base_path.parent
        print(f"⚠️ No campaign_dir provided, using base_path.parent: {product_dir}")

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
            print(f"📁 Created size directory: {size_dir}")

            # Smart resize with cropping to maintain aspect ratio
            resized_img = smart_resize_and_crop(img, config["size"])

            # Include size in filename
            size_filename = f"image_{aspect_ratio.replace(':', 'x')}.png"
            image_path = size_dir / size_filename
            resized_img.save(image_path, "PNG", quality=95)

            # Add brand overlay, localization, and translated message
            final_image_path = add_brand_overlay(str(image_path), product, region, message)
            outputs[aspect_ratio] = final_image_path
            print(f"📐 Created {aspect_ratio} variant for {product}: {final_image_path}")

    return outputs


def smart_resize_and_crop(img: Image.Image, target_size: tuple) -> Image.Image:
    """
    Smart resize and crop to maintain aspect ratio and image quality.
    """
    target_width, target_height = target_size
    target_ratio = target_width / target_height

    # Get current dimensions
    current_width, current_height = img.size
    current_ratio = current_width / current_height

    if current_ratio > target_ratio:
        # Image is too wide - crop width
        new_width = int(current_height * target_ratio)
        left = (current_width - new_width) // 2
        right = left + new_width
        img = img.crop((left, 0, right, current_height))
    elif current_ratio < target_ratio:
        # Image is too tall - crop height
        new_height = int(current_width / target_ratio)
        top = (current_height - new_height) // 2
        bottom = top + new_height
        img = img.crop((0, top, current_width, bottom))

    # Now resize to exact target size
    return img.resize(target_size, Image.Resampling.LANCZOS)


def generate_creatives(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    campaign_id: Optional[str] = None,
    product: Optional[str] = None,
    region: Optional[str] = None,
    message: Optional[str] = None,
    campaign_dir: Optional[Path] = None,
) -> dict:
    """
    Generate one image and create 3 size variants for a specific product.
    Returns dict with aspect ratios as keys and file paths as values.
    """
    # Validate required parameters
    if not campaign_id or not product or not region:
        raise ValueError("campaign_id, product, and region are required")
    
    # Ensure campaign_dir is provided
    if campaign_dir is None:
        raise ValueError("campaign_dir is required for proper directory structure")
    
    print(f"🎨 Generating creatives for product '{product}' in campaign_dir: {campaign_dir}")
    
    # Generate the base image for this product
    base_image_path = generate_single_image(prompt, campaign_id, product, region, campaign_dir)

    # Create size variants for this product
    outputs = create_size_variants(base_image_path, campaign_id, product, region, message, campaign_dir)

    return outputs


if __name__ == "__main__":
    test_prompt = "a hero image for social ad campaign"
    generate_creatives(test_prompt, width=768, height=512)