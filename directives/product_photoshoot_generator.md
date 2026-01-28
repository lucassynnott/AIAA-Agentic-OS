# Product Photoshoot Generator

> **Status:** ✅ Tested & Working | **Last Updated:** January 6, 2026

## What This Workflow Is
Generates 5 professional AI product photoshoot images using Fal.ai Nano Banana Pro. Takes a product image, analyzes it, generates branded prompts, creates 5 distinct photo styles, uploads to Google Drive, and notifies via Slack.

## What It Does
1. Uploads product image directly to Fal.ai CDN
2. Analyzes product with GPT-4o vision
3. **Researches brand and ICP via Perplexity** (brand identity, target audience, photography recommendations)
4. Generates 5 branded photoshoot prompts via AI (Claude) - informed by research
5. Creates 5 images with Fal.ai Nano Banana Pro
6. Downloads and uploads to Google Drive
7. Sends Slack notification with Drive link

## The 5 Photo Styles
1. **Hero Product Shot** - Clean, e-commerce ready, minimal background
2. **Lifestyle Context** - Product in natural use environment
3. **Detail/Macro Focus** - Close-up on textures and craftsmanship
4. **Aspirational Scene** - Premium, luxury positioning
5. **Creative/Artistic** - Unconventional angle for social media impact

## Prerequisites

### Required API Keys (configured in .env)
```bash
# Fal.ai
FAL_API_KEY=832eef9f-...              # Your Fal.ai API key

# AI (for prompt generation and image analysis)
OPENAI_API_KEY=sk-...                 # For GPT-4o vision
OPENROUTER_API_KEY=sk-or-...          # Alternative for Claude

# Google Drive (OAuth)
GOOGLE_DRIVE_FOLDER_ID=...            # Where to save images

# Slack
SLACK_BOT_TOKEN=xoxb-...
SLACK_CONTENT_CHANNEL_ID=C0...        # Where to post notifications
```

### Installation
```bash
pip install requests openai google-api-python-client google-auth-oauthlib python-dotenv
```

## How to Run

### CLI Command
```bash
python3 execution/generate_product_photoshoot.py \
  --image "path/to/product.png" \
  --brand "Brand Name" \
  --website "brand.com" \
  --niche "Skincare"
```

### Full Options
```bash
python3 execution/generate_product_photoshoot.py \
  --image "product.png" \
  --brand "Luxe Cosmetics" \
  --website "luxecosmetics.com" \
  --niche "Premium Skincare" \
  --goals "Holiday campaign imagery" \
  --context "Target audience is women 25-45, premium positioning"
```

## Inputs
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| image | file path | Yes | Product image (PNG preferred) |
| brand | string | Yes | Brand name |
| website | string | No | Brand website for research |
| niche | string | No | Brand niche (default: E-commerce) |
| goals | string | No | Photoshoot goals |
| context | string | No | Additional context |

## Process Flow

### 1. Upload Image to Fal.ai CDN
Product image is uploaded directly to Fal.ai's CDN storage. Falls back to base64 data URL if CDN upload fails.

### 2. Analyze Product Image
GPT-4o vision analyzes the product image and generates a detailed description including:
- Product shape and form
- Colors and materials
- Visible features and details
- Overall aesthetic

### 3. Research Brand & ICP (Perplexity)
Perplexity researches the brand and target audience to inform photography direction:
- **Brand Identity:** Positioning, personality, visual style, key colors
- **Target Audience (ICP):** Demographics, psychographics, problems solved, emotional benefits
- **Competitive Positioning:** Differentiation, USPs, competitors
- **Photography Recommendations:** Visual style, color palettes, props, settings, lifestyle contexts

### 4. Generate 5 Photoshoot Prompts
AI (Claude or GPT-4) generates 5 distinct Nano Banana prompts based on:
- Brand identity research
- Product description
- Target audience
- Photoshoot goals

Each prompt follows the structure:
```
"[Product] photographed in [setting], [arrangement], surrounded by [props], 
[lighting], [color palette], [camera angle], [mood], professional product 
photography, high resolution, 8K quality"
```

### 5. Create Images via Fal.ai
For each of the 5 prompts:
- Submit job to `fal-ai/nano-banana/edit` queue
- Poll status every 30 seconds
- Retrieve completed image URL
- Download image locally

### 6. Upload to Google Drive
- Create brand folder in configured Drive location
- Upload all 5 images with descriptive filenames
- Generate shareable folder URL

### 7. Send Slack Notification
Rich block notification including:
- Brand name
- Number of images generated
- List of 5 deliverables
- Clickable link to Google Drive folder

## Output

### Local Files
```
.tmp/photoshoot_{brand}_{timestamp}/
├── 01_Hero_Product_Shot.png
├── 02_Lifestyle_Context.png
├── 03_Detail_Texture_Focus.png
├── 04_Aspirational_Scene.png
├── 05_Creative_Artistic.png
└── results.json
```

### results.json Schema
```json
{
  "brand_name": "Brand Name",
  "website": "brand.com",
  "niche": "Skincare",
  "timestamp": "20260106_120000",
  "original_image_url": "https://fal.ai/cdn/...",
  "product_description": "A sleek glass bottle...",
  "prompts": ["prompt1", "prompt2", ...],
  "images": [
    {
      "scene_type": "Hero Product Shot",
      "prompt": "...",
      "fal_url": "https://fal.ai/...",
      "local_path": ".tmp/.../01_Hero_Product_Shot.png",
      "drive_url": "https://drive.google.com/..."
    }
  ],
  "drive_folder_url": "https://drive.google.com/drive/folders/..."
}
```

## Error Handling
| Scenario | Behavior |
|----------|----------|
| Fal.ai CDN upload fails | Falls back to base64 data URL |
| Image analysis fails | Falls back to generic description |
| Fal.ai timeout (10 min) | Raises exception for that image, continues |
| Drive upload fails | Logs warning, images saved locally |
| Slack fails | Logs warning, continues |

## Performance
- Image upload: ~2 seconds
- Image analysis: ~5 seconds
- Prompt generation: ~10 seconds
- Each Fal.ai image: 1-3 minutes
- **Total workflow time: ~8-15 minutes**

## API Endpoints Used
- **Fal.ai CDN:** `POST https://rest.alpha.fal.ai/storage/upload/initiate`
- **Fal.ai Queue:** `POST https://queue.fal.run/fal-ai/nano-banana/edit`
- **Fal.ai Status:** `GET https://queue.fal.run/fal-ai/nano-banana/requests/{id}/status`
- **Google Drive:** OAuth file upload
- **Slack:** `POST https://slack.com/api/chat.postMessage`

## Tested Example

```bash
# Download a product image
curl -o .tmp/monster_ultra.jpg "https://example.com/product.jpg"

# Run photoshoot generator
python3 execution/generate_product_photoshoot.py \
  --image ".tmp/monster_ultra.jpg" \
  --brand "Monster Energy" \
  --website "monsterenergy.com" \
  --niche "Energy Drinks" \
  --goals "Lifestyle and action sports imagery"

# Output:
# ✅ 5 images generated
# 📁 .tmp/photoshoot_Monster_Energy_20260106_165614/
# 🔗 https://drive.google.com/drive/folders/...
```

## Related Files
- `execution/generate_product_photoshoot.py` - Main execution script (500+ lines)
- `N8N Workflows/Workflows/Ecom Email Marketing Agency/Product Photoshoot Generator.json` - Original N8N workflow

## Original N8N Workflow
Converted from: `Product Photoshoot Generator.json`
Last tested: January 6, 2026 - Monster Energy Ultra photoshoot successful