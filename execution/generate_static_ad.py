#!/usr/bin/env python3
"""
Static Ad Generator - Generate static image ad concepts AND actual images.

Usage:
    python3 execution/generate_static_ad.py \
        --product "SaaS Tool" \
        --offer "50% off" \
        --platform "facebook" \
        --generate-images \
        --output .tmp/static_ads
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests package not installed. Run: pip install requests")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()


def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def generate_image_nano_banana(prompt: str, output_path: str) -> bool:
    """Generate image using fal.ai Nano Banana Pro."""
    fal_key = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY")
    if not fal_key:
        print("    ⚠️ FAL_KEY not set, skipping image generation")
        return False
    
    try:
        response = requests.post(
            "https://fal.run/fal-ai/nano-banana-pro",
            headers={
                "Authorization": f"Key {fal_key}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": prompt,
                "aspect_ratio": "1:1",
                "resolution": "2K"
            },
            timeout=180
        )
        
        if response.status_code == 200:
            result = response.json()
            images = result.get("images", [])
            if images:
                image_url = images[0].get("url")
                if image_url:
                    img_response = requests.get(image_url, timeout=60)
                    if img_response.status_code == 200:
                        with open(output_path, "wb") as f:
                            f.write(img_response.content)
                        return True
        else:
            print(f"    ⚠️ Nano Banana error: {response.status_code}")
        return False
    except Exception as e:
        print(f"    ⚠️ Image generation error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate static ad concepts with images")
    parser.add_argument("--product", "-p", required=True)
    parser.add_argument("--offer", "-o", default="", help="Special offer")
    parser.add_argument("--platform", default="facebook", choices=["facebook", "instagram", "linkedin", "google"])
    parser.add_argument("--audience", "-a", default="", help="Target audience")
    parser.add_argument("--variations", "-v", type=int, default=5)
    parser.add_argument("--generate-images", action="store_true", help="Generate actual ad images")
    parser.add_argument("--output", default=".tmp/static_ads")
    args = parser.parse_args()

    print(f"\n🖼️ Static Ad Generator")
    print(f"   Product: {args.product}")
    print(f"   Platform: {args.platform}")
    print(f"   Variations: {args.variations}")
    print(f"   Generate Images: {args.generate_images}\n")
    
    # Setup output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = get_client()

    print("🎨 Generating ad concepts...")
    
    result = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You create high-converting static ads for {args.platform}. Return JSON format."},
            {"role": "user", "content": f"""Create {args.variations} static ad concepts in JSON:

PRODUCT: {args.product}
OFFER: {args.offer or "No special offer"}
PLATFORM: {args.platform}
AUDIENCE: {args.audience or "General"}

Return JSON:
{{
    "ads": [
        {{
            "ad_number": 1,
            "angle": "Problem-focused",
            "headline": "5 words or less",
            "primary_text": "Feed copy",
            "description": "Link description",
            "cta": "Learn More",
            "visual_concept": "Main image/graphic description",
            "color_scheme": "Colors to use",
            "layout": "Text placement description",
            "image_prompt": "Detailed AI image generation prompt with: style, colors, composition, text overlay positioning. Include the headline text prominently. Format: 1:1 square ad creative for social media. Professional advertising quality."
        }}
    ]
}}

ANGLES TO COVER:
1. Problem-focused - Show the pain
2. Benefit-focused - Show the outcome
3. Social proof - Testimonial style
4. Urgency/scarcity - Limited time
5. Curiosity/question - Pattern interrupt

IMAGE PROMPT REQUIREMENTS:
- Include actual headline text in the image
- Specify exact text positioning (top, center, bottom)
- Include brand colors if mentioned
- Professional advertising photography/design style
- Bold, readable text on mobile
- 1:1 square format

Return ONLY valid JSON."""}
        ],
        temperature=0.8,
        max_tokens=3000
    ).choices[0].message.content

    # Parse JSON
    try:
        json_match = re.search(r'\{[\s\S]*\}', result)
        if json_match:
            ad_data = json.loads(json_match.group())
        else:
            ad_data = {"ads": [], "raw_output": result}
    except json.JSONDecodeError:
        ad_data = {"ads": [], "raw_output": result}
    
    # Save JSON
    json_path = output_dir / "static_ads.json"
    with open(json_path, "w") as f:
        json.dump(ad_data, f, indent=2)
    
    # Generate images if requested
    if args.generate_images and ad_data.get("ads"):
        print("\n🖼️ Generating ad images with Nano Banana Pro...")
        images_dir = output_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        for ad in ad_data["ads"]:
            ad_num = ad.get("ad_number", 1)
            angle = ad.get("angle", "Unknown")
            image_prompt = ad.get("image_prompt", "")
            
            if image_prompt:
                print(f"   Ad {ad_num} ({angle})...")
                safe_angle = angle.lower().replace(' ', '_').replace('/', '_').replace('-', '_')
                img_path = images_dir / f"ad_{ad_num}_{safe_angle}.png"
                
                if generate_image_nano_banana(image_prompt, str(img_path)):
                    print(f"   ✅ Saved: {img_path.name}")
                    ad["image_path"] = str(img_path)
                else:
                    print(f"   ❌ Failed to generate")
        
        # Update JSON with image paths
        with open(json_path, "w") as f:
            json.dump(ad_data, f, indent=2)

    # Generate markdown
    md_output = f"""# Static Ad Concepts

**Product:** {args.product}
**Platform:** {args.platform}
**Offer:** {args.offer or "None"}
**Audience:** {args.audience or "General"}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

"""

    for ad in ad_data.get("ads", []):
        md_output += f"""## Ad {ad.get('ad_number', '?')}: {ad.get('angle', 'Unknown')}

**Headline:** {ad.get('headline', '')}

**Primary Text:** {ad.get('primary_text', '')}

**Description:** {ad.get('description', '')}

**CTA:** {ad.get('cta', 'Learn More')}

**Visual Concept:** {ad.get('visual_concept', '')}

**Color Scheme:** {ad.get('color_scheme', '')}

**Layout:** {ad.get('layout', '')}

**Image Prompt:** {ad.get('image_prompt', '')}

"""
        if ad.get("image_path"):
            md_output += f"**Generated Image:** `{ad['image_path']}`\n\n"
        
        md_output += "---\n\n"

    md_path = output_dir / "static_ads.md"
    md_path.write_text(md_output, encoding="utf-8")
    
    print(f"\n✅ Static ads complete!")
    print(f"   📄 Markdown: {md_path}")
    print(f"   📊 JSON: {json_path}")
    if args.generate_images:
        print(f"   🖼️ Images: {output_dir}/images/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
