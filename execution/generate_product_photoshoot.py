#!/usr/bin/env python3
"""
Product Photoshoot Generator

Generates 5 AI product photoshoot images using Fal.ai Nano Banana Pro.
Uploads to Google Drive and sends Slack notification.

Usage:
    python3 execution/generate_product_photoshoot.py \
        --image "path/to/product.png" \
        --brand "Brand Name" \
        --website "brand.com" \
        --niche "Skincare"
"""

import argparse
import base64
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# Configuration
# =============================================================================

FAL_API_KEY = os.getenv("FAL_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CONTENT_CHANNEL_ID = os.getenv("SLACK_CONTENT_CHANNEL_ID")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

# Scene types for the 5 prompts
SCENE_TYPES = [
    "Hero Product Shot",
    "Lifestyle Context",
    "Detail/Texture Focus",
    "Aspirational Scene",
    "Creative/Artistic"
]


# =============================================================================
# Image Upload (direct to Fal.ai CDN)
# =============================================================================

def upload_to_fal(image_path: str) -> str:
    """Upload image directly to Fal.ai CDN and return URL."""
    print(f"   Uploading to Fal.ai CDN...")
    
    # Get file info
    file_name = Path(image_path).name
    content_type = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
    
    with open(image_path, "rb") as f:
        file_data = f.read()
    
    # Step 1: Get upload URL from Fal.ai
    resp = requests.post(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        headers={
            "Authorization": f"Key {FAL_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "file_name": file_name,
            "content_type": content_type
        },
        timeout=30
    )
    
    if not resp.ok:
        # Fallback: Use base64 data URL
        print(f"   Using base64 fallback...")
        encoded = base64.b64encode(file_data).decode()
        return f"data:{content_type};base64,{encoded}"
    
    upload_data = resp.json()
    upload_url = upload_data.get("upload_url")
    file_url = upload_data.get("file_url")
    
    # Step 2: Upload file to the presigned URL
    upload_resp = requests.put(
        upload_url,
        data=file_data,
        headers={"Content-Type": content_type},
        timeout=120
    )
    
    if upload_resp.ok:
        print(f"   ✓ Uploaded to Fal.ai CDN")
        return file_url
    else:
        # Fallback to base64
        print(f"   Using base64 fallback...")
        encoded = base64.b64encode(file_data).decode()
        return f"data:{content_type};base64,{encoded}"


# =============================================================================
# Image Analysis (describe the product)
# =============================================================================

def analyze_product_image(image_url: str) -> str:
    """Use GPT-4o to describe the product in the image."""
    print("   Analyzing product image...")
    
    from openai import OpenAI
    
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
        model = "gpt-4o"
    elif OPENROUTER_API_KEY:
        client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
        model = "openai/gpt-4o"
    else:
        raise Exception("No OpenAI or OpenRouter API key configured")
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the product in this image. Go into detail about its shape, colors, materials, and any visible features."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        max_tokens=500
    )
    
    description = response.choices[0].message.content
    print(f"   ✓ Product analyzed")
    return description


# =============================================================================
# Market Research (Perplexity)
# =============================================================================

def research_brand_icp(brand_name: str, website: str, niche: str) -> dict:
    """Research the brand and ICP using Perplexity for better prompt context."""
    print("   Researching brand and target audience...")
    
    if not PERPLEXITY_API_KEY:
        print("   ⚠️ Perplexity API key not configured, skipping research")
        return {}
    
    research_prompt = f"""Research this brand for product photography context:

BRAND: {brand_name}
WEBSITE: {website}
NICHE: {niche}

Provide a concise research summary covering:

1. BRAND IDENTITY
- Brand positioning (premium/mid-market/budget)
- Brand personality and tone
- Visual style and aesthetic
- Key brand colors and design elements

2. TARGET AUDIENCE (ICP)
- Primary demographic (age, gender, income level)
- Psychographics (lifestyle, values, aspirations)
- What problems does this brand solve for them?
- What emotional benefits do they seek?

3. COMPETITIVE POSITIONING
- How does this brand differentiate?
- Key competitors and how this brand stands apart
- Unique selling propositions

4. PHOTOGRAPHY RECOMMENDATIONS
- What visual style would resonate with this audience?
- Recommended color palettes and moods
- Props and settings that would appeal to the ICP
- Lifestyle contexts that match the target audience

Keep the response concise but actionable for product photography direction."""

    try:
        resp = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": "You are a brand research expert providing insights for product photography direction. Be concise and actionable."},
                    {"role": "user", "content": research_prompt}
                ],
                "max_tokens": 1500,
                "temperature": 0.3
            },
            timeout=60
        )
        
        if resp.ok:
            result = resp.json()
            research_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print("   ✓ Brand research complete")
            return {
                "research_text": research_text,
                "brand_name": brand_name,
                "website": website,
                "niche": niche
            }
        else:
            print(f"   ⚠️ Perplexity error: {resp.status_code} - {resp.text[:200]}")
            return {}
    except Exception as e:
        print(f"   ⚠️ Research error: {e}")
        return {}


# =============================================================================
# Generate Prompts (5 different scenes)
# =============================================================================

def generate_photoshoot_prompts(brand_name: str, website: str, niche: str, 
                                 product_description: str, goals: str = "", context: str = "",
                                 brand_research: dict = None) -> list:
    """Generate 5 Nano Banana prompts for different photoshoot scenes."""
    print("   Generating photoshoot prompts...")
    
    from openai import OpenAI
    
    if OPENROUTER_API_KEY:
        client = OpenAI(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
        model = "anthropic/claude-sonnet-4"
    else:
        client = OpenAI(api_key=OPENAI_API_KEY)
        model = "gpt-4o"
    
    system_prompt = """You are an expert AI prompt engineer specializing in product photography prompts for Nano Banana (Fal.ai).
    
Your task is to create 5 distinct, production-ready prompts that will generate professional product photos.

Each prompt should be 80-120 words and follow this structure:
"[Product] photographed in [setting], [arrangement], surrounded by [props], [lighting], [color palette], [camera angle], [mood], professional product photography, high resolution, 8K quality"

The 5 scenes must be:
1. HERO SHOT - Clean, e-commerce ready, minimal background
2. LIFESTYLE - Product in natural use environment with lifestyle elements
3. DETAIL/MACRO - Close-up focusing on textures and craftsmanship
4. ASPIRATIONAL - Premium, luxury positioning with elevated styling
5. CREATIVE - Artistic, unconventional angle for social media impact"""

    # Include brand research if available
    research_section = ""
    if brand_research and brand_research.get("research_text"):
        research_section = f"""
BRAND & ICP RESEARCH:
{brand_research.get('research_text')}
"""

    user_prompt = f"""Create 5 Nano Banana prompts for this product photoshoot:

BRAND: {brand_name}
WEBSITE: {website}
NICHE: {niche}
PRODUCT DESCRIPTION: {product_description}
PHOTOSHOOT GOALS: {goals or 'General product photography for e-commerce and marketing'}
ADDITIONAL CONTEXT: {context or 'None'}
{research_section}
Use the brand research above to inform your prompt choices - match the visual style, color palettes, 
settings, and props to what will resonate with the target audience (ICP).

Return ONLY the 5 prompts in this exact format:

PROMPT 1 (Hero Shot):
"[prompt text here]"

PROMPT 2 (Lifestyle):
"[prompt text here]"

PROMPT 3 (Detail/Macro):
"[prompt text here]"

PROMPT 4 (Aspirational):
"[prompt text here]"

PROMPT 5 (Creative):
"[prompt text here]"

Do not include any other text, explanations, or formatting. Just the 5 labeled prompts."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    output = response.choices[0].message.content
    
    # Parse the prompts
    prompts = []
    import re
    matches = re.findall(r'PROMPT \d+[^"]*"([^"]+)"', output, re.DOTALL)
    
    if matches:
        prompts = [m.strip() for m in matches]
    else:
        # Fallback: split by PROMPT and extract quoted content
        sections = output.split("PROMPT")
        for section in sections[1:]:
            quoted = re.search(r'"([^"]+)"', section)
            if quoted:
                prompts.append(quoted.group(1).strip())
    
    if len(prompts) < 5:
        print(f"   ⚠️ Only extracted {len(prompts)} prompts, expected 5")
    
    print(f"   ✓ Generated {len(prompts)} prompts")
    return prompts[:5]


# =============================================================================
# Fal.ai Image Generation
# =============================================================================

def create_image_fal(prompt: str, image_url: str, scene_type: str) -> str:
    """Create image using Fal.ai Nano Banana Pro (edit endpoint)."""
    print(f"   Creating {scene_type}...")
    
    # Submit job to queue - using nano-banana-pro/edit for better quality
    resp = requests.post(
        "https://queue.fal.run/fal-ai/nano-banana-pro/edit",
        headers={
            "Authorization": f"Key {FAL_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "prompt": f"{scene_type} - {prompt}",
            "image_urls": [image_url],
            "aspect_ratio": "1:1",
            "resolution": "2K"
        },
        timeout=60
    )
    
    if not resp.ok:
        raise Exception(f"Fal.ai error: {resp.status_code} - {resp.text}")
    
    request_id = resp.json().get("request_id")
    
    # Poll for completion
    for attempt in range(20):  # Max 10 minutes
        time.sleep(30)
        
        status_resp = requests.get(
            f"https://queue.fal.run/fal-ai/nano-banana-pro/requests/{request_id}/status",
            headers={"Authorization": f"Key {FAL_API_KEY}"},
            timeout=30
        )
        
        if status_resp.ok:
            status_data = status_resp.json()
            if status_data.get("status") == "COMPLETED":
                # Get the result
                result_resp = requests.get(
                    status_data.get("response_url"),
                    headers={"Authorization": f"Key {FAL_API_KEY}"},
                    timeout=30
                )
                if result_resp.ok:
                    result = result_resp.json()
                    image_url = result.get("images", [{}])[0].get("url")
                    print(f"   ✓ {scene_type} complete")
                    return image_url
            elif status_data.get("status") == "FAILED":
                raise Exception(f"Fal.ai job failed: {status_data}")
    
    raise Exception("Fal.ai timeout after 10 minutes")


def download_image(url: str, output_path: str) -> str:
    """Download image from URL to local file."""
    resp = requests.get(url, timeout=60)
    if resp.ok:
        with open(output_path, "wb") as f:
            f.write(resp.content)
        return output_path
    raise Exception(f"Failed to download image: {resp.status_code}")


# =============================================================================
# Google Drive Upload
# =============================================================================

def upload_to_drive(file_path: str, filename: str, folder_id: str = None) -> dict:
    """Upload file to Google Drive."""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        creds = None
        if os.path.exists('token_docs.json'):
            creds = Credentials.from_authorized_user_file('token_docs.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token_docs.json', 'w') as token:
                token.write(creds.to_json())
        
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {'name': filename}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(file_path, mimetype='image/png')
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        return {
            "id": file.get("id"),
            "url": file.get("webViewLink")
        }
    except Exception as e:
        print(f"   ⚠️ Drive upload error: {e}")
        return None


def create_drive_folder(folder_name: str, parent_id: str = None) -> str:
    """Create a folder in Google Drive."""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        creds = Credentials.from_authorized_user_file('token_docs.json')
        service = build('drive', 'v3', credentials=creds)
        
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')
    except Exception as e:
        print(f"   ⚠️ Folder creation error: {e}")
        return None


# =============================================================================
# Slack Notification
# =============================================================================

def send_slack_notification(brand_name: str, drive_url: str, image_count: int):
    """Send Slack notification with results."""
    if not SLACK_BOT_TOKEN or not SLACK_CONTENT_CHANNEL_ID:
        print("   ⚠️ Slack not configured")
        return
    
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "📸 Product Photoshoot Complete", "emoji": True}
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Client:*\n{brand_name}"},
                {"type": "mrkdwn", "text": f"*Images:*\n{image_count} generated"}
            ]
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*🎨 Photoshoot Deliverables:*\n• Hero Product Shot (E-commerce Ready)\n• Lifestyle Context Scene\n• Detail/Texture Macro Shot\n• Aspirational Brand Scene\n• Creative/Artistic Composition"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*📁 View Images:*\n<{drive_url}|Open in Google Drive>"}
        }
    ]
    
    resp = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "channel": SLACK_CONTENT_CHANNEL_ID,
            "text": f"Product photoshoot complete for {brand_name}",
            "blocks": blocks
        },
        timeout=30
    )
    
    if resp.ok and resp.json().get("ok"):
        print("   ✓ Slack notification sent")
    else:
        print(f"   ⚠️ Slack error: {resp.json().get('error', 'unknown')}")


# =============================================================================
# Main Orchestration
# =============================================================================

def generate_photoshoot(image_path: str, brand_name: str, website: str, niche: str,
                        goals: str = "", context: str = ""):
    """Main photoshoot generation workflow."""
    
    print(f"\n📸 Product Photoshoot Generator")
    print(f"   Brand: {brand_name}")
    print(f"   Image: {image_path}\n")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f".tmp/photoshoot_{brand_name.replace(' ', '_')}_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        "brand_name": brand_name,
        "website": website,
        "niche": niche,
        "timestamp": timestamp,
        "images": []
    }
    
    # Step 1: Upload original image to Fal.ai
    print("1️⃣ Uploading original image...")
    image_url = upload_to_fal(image_path)
    results["original_image_url"] = image_url
    
    # Step 2: Analyze product
    print("\n2️⃣ Analyzing product...")
    product_description = analyze_product_image(image_url)
    results["product_description"] = product_description
    
    # Step 3: Research brand and ICP (Perplexity)
    print("\n3️⃣ Researching brand and target audience...")
    brand_research = research_brand_icp(brand_name, website, niche)
    results["brand_research"] = brand_research.get("research_text", "")
    
    # Step 4: Generate prompts
    print("\n4️⃣ Generating photoshoot prompts...")
    prompts = generate_photoshoot_prompts(
        brand_name, website, niche, 
        product_description, goals, context,
        brand_research=brand_research
    )
    results["prompts"] = prompts
    
    # Step 5: Generate images with Fal.ai
    print("\n5️⃣ Generating images with Fal.ai...")
    generated_images = []
    for i, (prompt, scene_type) in enumerate(zip(prompts, SCENE_TYPES)):
        try:
            fal_image_url = create_image_fal(prompt, image_url, scene_type)
            
            # Download locally
            local_path = output_dir / f"{i+1:02d}_{scene_type.replace('/', '_').replace(' ', '_')}.png"
            download_image(fal_image_url, str(local_path))
            
            generated_images.append({
                "scene_type": scene_type,
                "prompt": prompt,
                "fal_url": fal_image_url,
                "local_path": str(local_path)
            })
        except Exception as e:
            print(f"   ⚠️ Failed to generate {scene_type}: {e}")
    
    results["images"] = generated_images
    print(f"   ✓ Generated {len(generated_images)} images")
    
    # Step 6: Upload to Google Drive
    print("\n6️⃣ Uploading to Google Drive...")
    folder_id = create_drive_folder(f"{brand_name} - Photoshoot - {timestamp}", GOOGLE_DRIVE_FOLDER_ID)
    
    drive_files = []
    for img in generated_images:
        upload_result = upload_to_drive(
            img["local_path"],
            Path(img["local_path"]).name,
            folder_id
        )
        if upload_result:
            drive_files.append(upload_result)
            img["drive_url"] = upload_result.get("url")
    
    drive_folder_url = f"https://drive.google.com/drive/folders/{folder_id}" if folder_id else None
    results["drive_folder_url"] = drive_folder_url
    print(f"   ✓ Uploaded {len(drive_files)} files to Drive")
    
    # Step 7: Send Slack notification
    print("\n7️⃣ Sending Slack notification...")
    if drive_folder_url:
        send_slack_notification(brand_name, drive_folder_url, len(generated_images))
    
    # Save results
    results_path = output_dir / "results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Photoshoot complete!")
    print(f"   📁 Output folder: {output_dir}")
    print(f"   📄 Results: {results_path}")
    if drive_folder_url:
        print(f"   🔗 Google Drive: {drive_folder_url}")
    
    return results


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Product Photoshoot Generator")
    parser.add_argument("--image", "-i", required=True, help="Path to product image (PNG preferred)")
    parser.add_argument("--brand", "-b", required=True, help="Brand name")
    parser.add_argument("--website", "-w", default="", help="Brand website")
    parser.add_argument("--niche", "-n", default="E-commerce", help="Brand niche")
    parser.add_argument("--goals", "-g", default="", help="Photoshoot goals")
    parser.add_argument("--context", "-c", default="", help="Additional context")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        sys.exit(1)
    
    if not FAL_API_KEY:
        print("Error: FAL_API_KEY not configured in .env")
        sys.exit(1)
    
    results = generate_photoshoot(
        args.image, args.brand, args.website, args.niche,
        args.goals, args.context
    )
    
    return 0 if results.get("images") else 1


if __name__ == "__main__":
    sys.exit(main())
