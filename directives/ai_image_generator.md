# AI Image Generator

## What This Workflow Is
This workflow generates custom images using DALL-E or other AI models for use in content, ads, and social media.

## What It Does
1. Takes image description prompt
2. Applies style and size parameters
3. Generates multiple variations
4. Saves to output folder
5. Returns image URLs/paths

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For DALL-E
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai requests
```

## How to Run

### Step 1: Generate Image
```bash
python3 execution/generate_image.py \
  --prompt "Professional businessman smiling, corporate headshot" \
  --style photorealistic \
  --size 1024x1024 \
  --variations 4 \
  --output .tmp/images/
```

### Quick One-Liner
```bash
python3 execution/generate_image.py --prompt "[DESCRIPTION]" --size 1024x1024
```

## Goal
Generate custom images for content, ads, and social media using AI.

## Inputs
- **Prompt**: Description of desired image
- **Style**: Photorealistic, illustration, 3D, etc.
- **Size**: Square, portrait, landscape
- **Quantity**: Number of variations

## Process

### 1. Generate Image
```bash
python3 execution/generate_image.py \
  --prompt "[DESCRIPTION]" \
  --style photorealistic \
  --size 1024x1024 \
  --variations 4 \
  --output .tmp/images/
```

### 2. Prompt Best Practices
```
[Subject], [Style], [Lighting], [Composition], [Details]

Example:
"Professional businessman smiling, corporate headshot, 
soft studio lighting, clean white background, 
high quality, 8k"
```

### 3. Style Options
- Photorealistic
- Digital illustration
- 3D render
- Watercolor
- Minimalist
- Vintage/retro
- Anime/cartoon

### 4. Use Cases

**Social Media:**
- Post graphics
- Story backgrounds
- Profile images
- Quote cards

**Marketing:**
- Ad creatives
- Landing page heroes
- Email headers
- Blog featured images

**Branding:**
- Logo concepts
- Brand imagery
- Product mockups

### 5. Output Options
- PNG (transparent bg)
- JPEG (compressed)
- WebP (web optimized)

### 6. Prompt Templates

**Product Shot:**
```
[Product] on [surface], professional product photography,
soft lighting, [brand colors], minimalist, high detail
```

**Lifestyle:**
```
[Person description] using [product/service], candid shot,
natural lighting, [setting], warm tones
```

**Abstract:**
```
Abstract [concept] visualization, [colors], 
flowing shapes, modern, digital art
```

## Integrations
- DALL-E 3
- Midjourney
- Stable Diffusion
- Google Imagen

## Cost
- DALL-E: ~$0.04/image
- Midjourney: $10-30/mo unlimited
