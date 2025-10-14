from PIL import Image, ImageDraw
import os
from pathlib import Path

ASPECT_RATIOS = {
    "1_1": (1080, 1080),
    "9_16": (1080, 1920),
    "16_9": (1920, 1080)
}

def generate_creatives(base_image: str, message: str, out_dir: str):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    results = {}

    img = Image.open(base_image)

    for tag, (w, h) in ASPECT_RATIOS.items():
        canvas = img.resize((w, h))
        draw = ImageDraw.Draw(canvas)
        draw.text((50, 50), message, fill="white")
        out_path = os.path.join(out_dir, f"creative_{tag}.png")
        canvas.save(out_path)
        results[tag] = out_path

    return results