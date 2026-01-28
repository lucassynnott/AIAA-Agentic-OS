#!/usr/bin/env python3
"""
Ad Creative Generator - Generate ad copy AND images for Facebook, Google, LinkedIn ads.

Usage:
    python3 execution/generate_ad_creative.py \
        --product "SaaS Tool" \
        --platform "facebook" \
        --goal "conversions" \
        --audience "B2B marketers" \
        --generate-images \
        --output .tmp/ad_creative
"""

import argparse
import json
import os
import re
import sys
import time
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


def get_client() -> OpenAI:
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def call_llm(client: OpenAI, system: str, user: str, temp: float = 0.7) -> str:
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=get_model(),
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=temp, max_tokens=4000
            )
            return resp.choices[0].message.content
        except Exception as e:
            if attempt == 2: raise e
    return ""


def load_skill_bible() -> str:
    """Load Meta Ads Manager skill bible for enhanced context."""
    skill_path = Path(__file__).parent.parent / "skills" / "SKILL_BIBLE_meta_ads_manager_technical.md"
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        sections = []
        if "## Core Principles" in content:
            start = content.find("## Core Principles")
            end = content.find("## Complete Process", start)
            if end > start:
                sections.append(content[start:end])
        if "## Best Practices" in content:
            start = content.find("## Best Practices")
            end = content.find("## Common Mistakes", start)
            if end > start:
                sections.append(content[start:end])
        return "\n\n".join(sections)
    return ""


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


def generate_ads(client: OpenAI, product: str, platform: str, goal: str, audience: str, offer: str) -> dict:
    """Generate ad creative with structured output for image generation."""
    
    skill_context = ""
    if platform in ["facebook", "meta"]:
        skill_context = load_skill_bible()

    platform_specs = {
        "facebook": {"headline_chars": 40, "primary_text": 125, "description": 30},
        "google": {"headline_chars": 30, "description": 90},
        "linkedin": {"headline_chars": 70, "intro_text": 150},
        "tiktok": {"headline_chars": 100, "description": 150}
    }
    
    specs = platform_specs.get(platform, platform_specs["facebook"])

    system_prompt = f"""You are an expert {platform} ads copywriter. Generate ad creative in JSON format."""
    
    user_prompt = f"""Create 3 ad variations for {platform}:

PRODUCT/SERVICE: {product}
TARGET AUDIENCE: {audience}
CAMPAIGN GOAL: {goal}
OFFER: {offer or "Not specified"}

Return JSON with this structure:
{{
    "ads": [
        {{
            "ad_number": 1,
            "angle": "Pain Point Focus",
            "headlines": ["Headline 1", "Headline 2", "Headline 3"],
            "primary_text": "Main body copy under {specs.get('primary_text', 125)} chars",
            "description": "Link description",
            "cta": "Learn More",
            "image_prompt": "Detailed image generation prompt for this ad - include style, colors, composition, mood. For ad creative, 1:1 square format."
        }},
        {{
            "ad_number": 2,
            "angle": "Benefit/Outcome Focus",
            ...
        }},
        {{
            "ad_number": 3,
            "angle": "Social Proof/Urgency",
            ...
        }}
    ]
}}

ANGLES:
1. Pain Point Focus - Agitate the problem
2. Benefit/Outcome Focus - Show transformation
3. Social Proof/Urgency - Create FOMO

IMAGE PROMPT REQUIREMENTS:
- Professional advertising style
- Bold text overlays with headline
- High contrast, readable on mobile
- Include the actual headline text in the image
- Specify colors, layout, and mood

Return ONLY valid JSON."""

    result = call_llm(client, system_prompt, user_prompt, temp=0.7)
    
    try:
        json_match = re.search(r'\{[\s\S]*\}', result)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        pass
    
    return {"ads": [], "raw_output": result}


def main():
    parser = argparse.ArgumentParser(description="Generate ad creative with images")
    parser.add_argument("--product", "-p", required=True, help="Product/service")
    parser.add_argument("--platform", "-l", default="facebook",
        choices=["facebook", "google", "linkedin", "tiktok"])
    parser.add_argument("--goal", "-g", default="conversions",
        choices=["conversions", "leads", "traffic", "awareness", "engagement"])
    parser.add_argument("--audience", "-a", required=True, help="Target audience")
    parser.add_argument("--offer", "-f", default="", help="Special offer/discount")
    parser.add_argument("--generate-images", action="store_true", help="Generate actual ad images")
    parser.add_argument("--output", "-o", default=".tmp/ad_creative")
    
    args = parser.parse_args()
    
    print(f"\n📢 Ad Creative Generator")
    print(f"   Product: {args.product}")
    print(f"   Platform: {args.platform}")
    print(f"   Goal: {args.goal}")
    print(f"   Audience: {args.audience}")
    print(f"   Generate Images: {args.generate_images}\n")
    
    # Setup output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    client = get_client()
    
    print("🎨 Generating ad copy...")
    ad_data = generate_ads(client, args.product, args.platform, args.goal, args.audience, args.offer)
    
    # Save JSON data
    json_path = output_dir / "ad_creative.json"
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
                img_path = images_dir / f"ad_{ad_num}_{angle.lower().replace(' ', '_').replace('/', '_')}.png"
                
                if generate_image_nano_banana(image_prompt, str(img_path)):
                    print(f"   ✅ Saved: {img_path.name}")
                    ad["image_path"] = str(img_path)
                else:
                    print(f"   ❌ Failed to generate")
        
        # Update JSON with image paths
        with open(json_path, "w") as f:
            json.dump(ad_data, f, indent=2)
    
    # Generate markdown summary
    md_output = f"""# Ad Creative: {args.product}

**Platform:** {args.platform.title()}
**Goal:** {args.goal}
**Audience:** {args.audience}
**Offer:** {args.offer or "None"}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

"""
    
    for ad in ad_data.get("ads", []):
        md_output += f"""## Ad {ad.get('ad_number', '?')}: {ad.get('angle', 'Unknown')}

**Headlines:**
"""
        for h in ad.get("headlines", []):
            md_output += f"- {h}\n"
        
        md_output += f"""
**Primary Text:** {ad.get('primary_text', '')}

**Description:** {ad.get('description', '')}

**CTA:** {ad.get('cta', 'Learn More')}

**Image Prompt:** {ad.get('image_prompt', '')}

"""
        if ad.get("image_path"):
            md_output += f"**Generated Image:** `{ad['image_path']}`\n\n"
        
        md_output += "---\n\n"
    
    md_path = output_dir / "ad_creative.md"
    md_path.write_text(md_output, encoding="utf-8")
    
    print(f"\n✅ Ad creative complete!")
    print(f"   📄 Markdown: {md_path}")
    print(f"   📊 JSON: {json_path}")
    if args.generate_images:
        print(f"   🖼️ Images: {output_dir}/images/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
