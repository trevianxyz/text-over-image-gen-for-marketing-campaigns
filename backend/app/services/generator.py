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
# QWEN_MODEL = "Qwen/Qwen-Image"  # Qwen-Image (requires Diffusers) - COMMENTED OUT
OPENAI_MODEL = "dall-e-3"  # Fallback: OpenAI DALL-E 3

HF_BASE_URL = "https://api-inference.huggingface.co"

OUTPUT_DIR = Path("assets/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Brand overlay settings
BRAND_IMAGE_PATH = Path("frontend/images/werkr_brand_image.png")
BRAND_OVERLAY_SIZE = (350, 350)  # Size of brand overlay (increased from 200x200)
BRAND_POSITION = "top_left"  # Position of brand overlay

# RTL (Right-to-Left) language codes
RTL_LANGUAGES = {
    'ar', 'he', 'fa', 'ur', 'ps', 'sd', 'ku', 'dv'  # Arabic, Hebrew, Persian, Urdu, Pashto, Sindhi, Kurdish, Dhivehi
}

# Global variables to store metadata
_last_translation_metadata = None
_last_image_generation_metadata = None

def is_rtl_language(language_code: str) -> bool:
    """Check if a language code represents an RTL language"""
    return language_code.lower() in RTL_LANGUAGES

def get_text_direction(language_code: str) -> str:
    """Get text direction for a language"""
    return 'rtl' if is_rtl_language(language_code) else 'ltr'

def get_last_translation_metadata():
    """Get the metadata from the last translation operation"""
    global _last_translation_metadata
    return _last_translation_metadata

def get_last_image_generation_metadata():
    """Get the metadata from the last image generation operation"""
    global _last_image_generation_metadata
    return _last_image_generation_metadata


def translate_message_with_llm(message: str, country_name: str, audience: str = None) -> str:
    """
    Use LLM to translate the message into the native language of the country,
    considering the target audience for better cultural adaptation.
    """
    from .country_language import get_legacy_region_mapping, get_primary_language, get_country_by_code, get_country_by_name
    
    # Handle both legacy region names and country codes
    country_code = get_legacy_region_mapping(country_name) or country_name
    target_language = get_primary_language(country_code)
    
    # Try to get country info by code first, then by name as fallback
    country_info = get_country_by_code(country_code) or get_country_by_name(country_name)
    country_full_name = country_info.name if country_info else country_name

    if target_language == "English":
        return message

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Build audience context for better translation
        audience_context = ""
        if audience:
            # Get audience details from the audience selector service
            from .audience_selector import get_audience_by_id
            audience_info = get_audience_by_id(audience)
            if audience_info:
                audience_context = f"Target audience: {audience_info.label} - {audience_info.description}. "
                if audience_info.interests:
                    audience_context += f"Key interests: {', '.join(audience_info.interests)}. "
                if audience_info.age_group:
                    audience_context += f"Age group: {audience_info.age_group.value}. "
                if audience_info.gender:
                    audience_context += f"Gender: {audience_info.gender.value}. "

        system_prompt = f"""
You are an integrated marketing AI professional working on the global construction work apparel brand WERKR. 
Your role is to receive an English seed copy and generate a new, creative, and localized, culturally resonant marketing message in {target_language} for the target audience. 

TASK:
- Generate a new, different, compelling creative marketing message for a {target_language}-speaking audience.
- Consider cultural nuances and social preferences of audiences in {country_full_name}.
- The target audience is: {audience_context}.

OUTPUT RULES:
- Write the final message directly, with no explanations, prefixes, or commentary.
- If the target language is not English:
  - First line: the localized message in {target_language}.
  - Second line: the English translation of that localized message.
- If the target language is English:
  - Output only the English message.

The new, creative, generated copy must be production-ready, in {target_language} and suitable for use in an advertising campaign in {country_full_name}.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
        except Exception as gpt41_error:
            print(f"⚠️ GPT-4.1 model failed: {gpt41_error}. Falling back to gpt-4o")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )

        translated_message = response.choices[0].message.content.strip()
        
        # Extract token usage metadata
        usage = response.usage
        token_metadata = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
            "model": response.model if hasattr(response, 'model') else "unknown"
        }
        
        print(f"🌍 Translated '{message}' to {target_language} for audience '{audience}': '{translated_message}'")
        print(f"📊 Token usage: {token_metadata['total_tokens']} tokens (prompt: {token_metadata['prompt_tokens']}, completion: {token_metadata['completion_tokens']})")
        
        # Store metadata globally for later retrieval
        global _last_translation_metadata
        _last_translation_metadata = token_metadata
        
        return translated_message

    except Exception as e:
        print(f"⚠️ Translation failed for {country_name}: {e}")
        return message  # Fallback to original message


def localize_prompt(prompt: str, country_name: str) -> str:
    """
    Localize the prompt based on country for better cultural relevance.
    """
    from .country_language import get_legacy_region_mapping, get_country_by_code
    
    # Handle both legacy region names and country codes
    country_code = get_legacy_region_mapping(country_name) or country_name
    country_info = get_country_by_code(country_code)
    
    if country_info:
        # Use country-specific localization
        localized_context = f"{country_info.name} culture, {country_info.region} lifestyle"
    else:
        # Fallback to generic localization
        localized_context = f"{country_name} culture and lifestyle"
    
    return f"{prompt}, {localized_context}"


def add_brand_overlay(image_path: str, product: str, country_name: str, message: str, audience: str = None) -> str:
    """
    Add brand overlay, localized text, and translated message to the image.
    """
    # Translate the message to the country's native language
    translated_message = translate_message_with_llm(message, country_name, audience)

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

        # Try to load fonts that support international text (RTL, non-Latin scripts)
        font_large = None
        font_small = None
        
        # Determine language and select appropriate font
        from .country_language import get_legacy_region_mapping, get_primary_language
        country_code = get_legacy_region_mapping(country_name) or country_name
        language_code = get_primary_language(country_code)
        
        # List of fonts to try in order of preference (international support)
        # Prioritize script-specific fonts for better rendering
        if language_code.lower() in ['japanese', 'chinese', 'korean']:
            # CJK-specific fonts
            font_paths = [
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf",
                "/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf",
                "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
                "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
                "/System/Library/Fonts/Hiragino Sans GB.ttc",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            ]
        elif language_code.lower() in ['arabic', 'persian', 'urdu', 'hebrew']:
            # Arabic/Hebrew RTL script fonts
            font_paths = [
                "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf",
                "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
                "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf",
                "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Has Arabic support
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
                "/System/Library/Fonts/GeezaPro.ttc",  # macOS Arabic
            ]
        elif language_code.lower() in ['russian', 'ukrainian', 'bulgarian', 'serbian', 'kazakh', 'georgian', 'armenian']:
            # Cyrillic and other non-Latin scripts
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Excellent Cyrillic support
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",  # Good Cyrillic support
                "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
                "/usr/share/fonts/truetype/noto/NotoSansCyrillic-Bold.ttf",
                "/usr/share/fonts/truetype/noto/NotoSansGeorgian-Bold.ttf",
                "/usr/share/fonts/truetype/noto/NotoSansArmenian-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
        else:
            # General Unicode fonts for Latin and other scripts
            font_paths = [
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",  # Fallback for mixed content
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "/System/Library/Fonts/Arial.ttf",  # macOS
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]
        
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    # For .ttc files (TrueType Collections), try index 0
                    if font_path.endswith('.ttc'):
                        font_large = ImageFont.truetype(font_path, 48, index=0)
                        font_small = ImageFont.truetype(font_path, 32, index=0)
                    else:
                        font_large = ImageFont.truetype(font_path, 48)
                        font_small = ImageFont.truetype(font_path, 32)
                    print(f"✅ Using font for {language_code}: {font_path}")
                    break
            except Exception as e:
                print(f"⚠️ Font {font_path} failed: {e}")
                continue
        
        # Final fallback to default font
        if not font_large:
            try:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
                print("⚠️ Using default font (limited international support)")
            except:
                font_large = None
                font_small = None
                print("❌ No fonts available")

        # 1. Add translated message (main text) in bottom right
        if translated_message:
            # Get language direction for proper positioning
            from .country_language import get_legacy_region_mapping, get_primary_language
            country_code = get_legacy_region_mapping(country_name) or country_name
            language_code = get_primary_language(country_code)
            is_rtl = is_rtl_language(language_code)
            
            # Calculate position for translated message (bottom right, above brand)
            if font_large:
                bbox = draw.textbbox((0, 0), translated_message, font=font_large)
                msg_width = bbox[2] - bbox[0]
                msg_height = bbox[3] - bbox[1]
            else:
                msg_width = len(translated_message) * 12
                msg_height = 24

            # Position message - ensure it fits within image bounds
            padding = 30
            
            # Ensure text fits within image width
            if msg_width + (2 * padding) > img.width:
                # Text is too wide, need to wrap or use smaller position
                msg_x = padding
            else:
                # Position from right edge with padding
                msg_x = img.width - msg_width - padding
                
            # Ensure text fits within image height (bottom placement)
            msg_y = max(img.height - msg_height - padding, padding)

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
            
            print(f"🌍 Text direction: {'RTL' if is_rtl else 'LTR'} for language {language_code}")

        # 2. Add country branding text (smaller, above brand logo)
        from .country_language import get_legacy_region_mapping, get_country_by_code
        
        # Handle both legacy region names and country codes
        country_code = get_legacy_region_mapping(country_name) or country_name
        country_info = get_country_by_code(country_code)
        
        if country_info:
            # Use country-specific branding
            region_label = f"Made in {country_info.name}"
        else:
            # Fallback to generic branding
            region_label = f"Made in {country_name}"

        # Calculate position for region label (below brand logo in top left)
        # if font_small:
        #     bbox = draw.textbbox((0, 0), region_label, font=font_small)
        #     region_width = bbox[2] - bbox[0]
        #     region_height = bbox[3] - bbox[1]
        # else:
        #     region_width = len(region_label) * 8
        #     region_height = 16

        # # Position below the brand logo with padding
        # if BRAND_IMAGE_PATH.exists():
        #     region_x = x + (brand_img.width - region_width) // 2
        #     region_y = y + brand_img.height + 10
        # else:
        #     region_x = 20
        #     region_y = 20

        # # Add region label with outline
        # for adj in range(-1, 2):
        #     for adj2 in range(-1, 2):
        #         if adj != 0 or adj2 != 0:
        #             draw.text((region_x + adj, region_y + adj2), region_label, font=font_small, fill=outline_color)

        # # Draw main region text
        # draw.text((region_x, region_y), region_label, font=font_small, fill=text_color)

        # Save the modified image
        img.save(image_path, "PNG", quality=95)
        print(f"🏷️ Added brand overlay, translated message, and localization for {product} in {country_name}")

    return image_path


def generate_with_huggingface(
    prompt: str, 
    width: int, 
    height: int, 
    model: str = None, 
    quality: str = "standard",
    noise_scheduler: str = "ddim",
    unet_backbone: str = "default",
    vae: str = "default",
    guidance_scale: float = 7.5,
    num_inference_steps: int = 30,
    seed: Optional[int] = None
) -> tuple[bytes, dict]:
    """Generate image using Hugging Face API"""
    import time
    start_time = time.time()
    
    # Use provided model or fallback to global default
    model_to_use = model or HF_MODEL
    
    url = f"{HF_BASE_URL}/models/{model_to_use}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Use advanced parameters (override quality-based settings)
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "scheduler": noise_scheduler,
            "unet_backbone": unet_backbone,
            "vae": vae,
        }
    }
    
    # Add seed if provided
    if seed is not None:
        payload["parameters"]["seed"] = seed

    print(f"🚀 Trying Hugging Face model {model_to_use} with {quality} quality...")
    with httpx.Client(timeout=30) as client:  # Shorter timeout for faster fallback
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        generation_time = time.time() - start_time
        metadata = {
            "model": model_to_use,
            "provider": "Hugging Face",
            "generation_time": f"{generation_time:.2f}s",
            "dimensions": f"{width}x{height}",
            "inference_steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "quality": quality
        }

        return response.content, metadata


# COMMENTED OUT - Qwen-Image functionality
# def generate_with_qwen(prompt: str, width: int, height: int) -> tuple[bytes, dict]:
#     """Generate image using Qwen-Image via Diffusers"""
#     import time
#     start_time = time.time()
#     
#     print(f"🎨 Trying Qwen-Image model {QWEN_MODEL}...")
#     
#     try:
#         # Import diffusers and torch
#         from diffusers import DiffusionPipeline
#         import torch
#         
#         # Check if we have GPU available
#         if torch.cuda.is_available():
#             torch_dtype = torch.bfloat16
#             device = "cuda"
#         else:
#             torch_dtype = torch.float32
#             device = "cpu"
#         
#         print(f"🖥️ Using device: {device}")
#         
#         # Load the Qwen-Image pipeline
#         pipe = DiffusionPipeline.from_pretrained(
#             QWEN_MODEL, 
#             torch_dtype=torch_dtype,
#             use_safetensors=True
#         )
#         pipe = pipe.to(device)
#         
#         # Generate image
#         result = pipe(
#             prompt=prompt,
#             width=width,
#             height=height,
#             num_inference_steps=30,
#             guidance_scale=7.5,
#             num_images_per_prompt=1
#         )
#         
#         # Convert PIL image to bytes
#         image = result.images[0]
#         
#         # Convert to bytes
#         import io
#         img_byte_arr = io.BytesIO()
#         image.save(img_byte_arr, format='PNG')
#         image_bytes = img_byte_arr.getvalue()
#         
#         generation_time = time.time() - start_time
#         metadata = {
#             "model": QWEN_MODEL,
#             "provider": "Qwen-Image",
#             "generation_time": f"{generation_time:.2f}s",
#             "dimensions": f"{width}x{height}",
#             "device": device,
#             "inference_steps": 30,
#             "guidance_scale": 7.5
#         }
#         
#         return image_bytes, metadata
#         
#     except Exception as e:
#         print(f"❌ Qwen-Image generation failed: {e}")
#         raise e


def generate_with_openai(prompt: str, width: int, height: int) -> tuple[bytes, dict]:
    """Generate image using OpenAI DALL-E 3"""
    import time
    start_time = time.time()
    
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
        
        generation_time = time.time() - start_time
        metadata = {
            "model": OPENAI_MODEL,
            "provider": "OpenAI",
            "generation_time": f"{generation_time:.2f}s",
            "dimensions": size,
            "quality": "standard"
        }
        
        return response.content, metadata


def generate_single_image(
    prompt: str, 
    campaign_id: str, 
    product: str, 
    country_name: str, 
    campaign_dir: Optional[Path] = None, 
    hf_model: str = "stabilityai/stable-diffusion-xl-base-1.0", 
    image_quality: str = "standard",
    noise_scheduler: str = "ddim",
    unet_backbone: str = "default",
    vae: str = "default",
    guidance_scale: float = 7.5,
    num_inference_steps: int = 30,
    seed: Optional[int] = None
) -> str:
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
    localized_prompt = localize_prompt(prompt, country_name)
    print(f"🌍 Localized prompt for {country_name}: {localized_prompt}")

    # Generate base image (use square format for best quality)
    global _last_image_generation_metadata
    
    # COMMENTED OUT - Qwen-Image logic
    # if hf_model == "Qwen/Qwen-Image":
    #     try:
    #         # Try Qwen-Image first
    #         image_bytes, metadata = generate_with_qwen(localized_prompt, width=1024, height=1024)
    #         _last_image_generation_metadata = metadata
    #         print(f"✅ Qwen-Image generation successful for {product}")
    #     except Exception as e:
    #         print(f"⚠️ Qwen-Image failed for {product}: {e}")
    #         if not OPENAI_API_KEY:
    #             raise Exception("Qwen-Image failed and no OpenAI API key provided")
    #         try:
    #             # Fallback to OpenAI
    #             image_bytes, metadata = generate_with_openai(localized_prompt, width=1024, height=1024)
    #             _last_image_generation_metadata = metadata
    #             print(f"✅ OpenAI fallback successful for {product}")
    #         except Exception as openai_error:
    #             raise Exception(f"Both Qwen-Image and OpenAI failed for {product}. Qwen: {e}, OpenAI: {openai_error}")
    # else:
    
    # Use Hugging Face models (Stable Diffusion)
    try:
        # Try Hugging Face first
        image_bytes, metadata = generate_with_huggingface(
            localized_prompt, 
            width=1024, 
            height=1024, 
            model=hf_model, 
            quality=image_quality,
            noise_scheduler=noise_scheduler,
            unet_backbone=unet_backbone,
            vae=vae,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            seed=seed
        )
        _last_image_generation_metadata = metadata
        print(f"✅ Hugging Face generation successful for {product}")

    except Exception as e:
        print(f"⚠️ Hugging Face failed for {product}: {e}")

        if not OPENAI_API_KEY:
            raise Exception("Hugging Face failed and no OpenAI API key provided")

        try:
            # Fallback to OpenAI
            image_bytes, metadata = generate_with_openai(localized_prompt, width=1024, height=1024)
            _last_image_generation_metadata = metadata
            print(f"✅ OpenAI fallback successful for {product}")

        except Exception as openai_error:
            raise Exception(f"Both Hugging Face and OpenAI failed for {product}. HF: {e}, OpenAI: {openai_error}")

    # Save the base image
    base_image_path = product_dir / "base_image.png"
    with open(base_image_path, "wb") as f:
        f.write(image_bytes)

    print(f"💾 Saved base image for {product} to {base_image_path}")
    return str(base_image_path)


def create_size_variants(base_image_path: str, campaign_id: str, product: str, country_name: str, message: str, campaign_dir: Optional[Path] = None, audience: str = None) -> dict:
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
            final_image_path = add_brand_overlay(str(image_path), product, country_name, message, audience)
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
    country_name: Optional[str] = None,
    message: Optional[str] = None,
    campaign_dir: Optional[Path] = None,
    audience: Optional[str] = None,
    noise_scheduler: str = "ddim",
    unet_backbone: str = "default",
    vae: str = "default",
    guidance_scale: float = 7.5,
    num_inference_steps: int = 30,
    seed: Optional[int] = None,
) -> dict:
    """
    Generate one image and create 3 size variants for a specific product.
    Returns dict with aspect ratios as keys and file paths as values.
    """
    # Validate required parameters
    if not campaign_id or not product or not country_name:
        raise ValueError("campaign_id, product, and country_name are required")
    
    # Ensure campaign_dir is provided
    if campaign_dir is None:
        raise ValueError("campaign_dir is required for proper directory structure")
    
    print(f"🎨 Generating creatives for product '{product}' in campaign_dir: {campaign_dir}")
    
    # Generate the base image for this product (using fixed Stable Diffusion XL)
    base_image_path = generate_single_image(
        prompt, 
        campaign_id, 
        product, 
        country_name, 
        campaign_dir, 
        "stabilityai/stable-diffusion-xl-base-1.0", 
        "standard",
        noise_scheduler=noise_scheduler,
        unet_backbone=unet_backbone,
        vae=vae,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        seed=seed
    )

    # Create size variants for this product
    outputs = create_size_variants(base_image_path, campaign_id, product, country_name, message, campaign_dir, audience)

    return outputs


if __name__ == "__main__":
    # Test the image generation service directly
    print("🧪 Testing image generation service...")
    
    test_prompt = "a hero image for social ad campaign"
    test_campaign_id = "test_campaign_123"
    test_product = "Test Product"
    test_region = "US"
    test_message = "Test message for overlay"
    
    try:
        # Test single image generation
        print(f"📸 Generating base image for: {test_prompt}")
        result = generate_single_image(test_prompt, test_campaign_id, test_product, test_region)
        print(f"✅ Generated base image: {result}")
        
        # Test size variants creation
        if result and "image_path" in result:
            print(f"📐 Creating size variants from: {result['image_path']}")
            variants = create_size_variants(result["image_path"], test_campaign_id, test_product, test_region, test_message)
            print(f"✅ Created size variants: {variants}")
        else:
            print("❌ No base image generated, skipping size variants test")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()