"""
GramSetu AI - Visual Studio & Image Generation Tool
"""
import urllib.parse
import random
import re

def create_image_payload(prompt: str) -> dict:
    clean = re.sub(r'^/image\s*', '', prompt, flags=re.IGNORECASE)
    clean = re.sub(r'^(?:generate image|photo banao|image banao|picture banao|generate visual)\s*', '', clean, flags=re.IGNORECASE).strip()
    if not clean:
        clean = "Lush green Indian crop field with drip irrigation in morning light"

    enhanced = f"{clean}, high resolution, photorealistic, 8k, detailed rural scenery"
    encoded = urllib.parse.quote(enhanced)
    seed = random.randint(1000, 999999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true&seed={seed}"

    return {
        "tool_name": "AI Visual Studio",
        "prompt": clean,
        "image_url": image_url,
        "badge": "🎨 Tool Executed: AI Visual Studio"
    }
