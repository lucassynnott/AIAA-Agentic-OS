# AI Thumbnail Generator

## What This Workflow Is
This workflow generates click-worthy YouTube thumbnail concepts and designs with optimized text, colors, and composition.

## What It Does
1. Analyzes video title for thumbnail angles
2. Generates 3-5 thumbnail concepts
3. Creates text overlay suggestions
4. Outputs design-ready specifications
5. Optionally generates actual thumbnails

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For concepts
DALL_E_API_KEY=your_dalle_key             # Optional for image generation
```

### Required Tools
- Python 3.10+
- OpenAI API access
- Optional: DALL-E or Canva API

### Installation
```bash
pip install openai pillow
```

## How to Run

### Step 1: Generate Concepts
```bash
python3 execution/generate_thumbnail_concepts.py \
  --title "5 Cold Email Mistakes Killing Your Replies" \
  --style bold \
  --output .tmp/concepts.json
```

### Step 2: Create Thumbnails
```bash
python3 execution/create_thumbnails.py \
  --concepts .tmp/concepts.json \
  --face_image photo.jpg \
  --output .tmp/thumbnails/
```

### Quick One-Liner
```bash
python3 execution/generate_thumbnail_concepts.py --title "Your Video Title" --style bold
```

## Goal
Generate click-worthy YouTube thumbnails with faces, text, and emotion.

## Inputs
- **Video Title**: What the video is about
- **Face Image**: Photo of creator (optional)
- **Style**: Clean, Bold, Dramatic, Minimal
- **Emotion**: Surprise, Excitement, Curiosity, Shock

## Process

### 1. Generate Concepts
```bash
python3 execution/generate_thumbnail_concepts.py \
  --title "[VIDEO_TITLE]" \
  --style bold \
  --output .tmp/concepts.json
```

### 2. Thumbnail Best Practices
- **Face**: Close-up with exaggerated emotion
- **Text**: 3-5 words max, high contrast
- **Colors**: Bright, contrasting (yellow, red, blue)
- **Composition**: Rule of thirds, face on one side
- **Curiosity gap**: Create intrigue

### 3. Generate Thumbnails
```bash
python3 execution/create_thumbnails.py \
  --concepts .tmp/concepts.json \
  --face_image photo.jpg \
  --output .tmp/thumbnails/
```

### 4. Output Options (3-5 variations)
```
thumbnail_1.png - [Description]
thumbnail_2.png - [Description]
thumbnail_3.png - [Description]
```

### 5. Thumbnail Formulas

**Before/After**
[Before state] → [After state]

**Number + Benefit**
"7 [Things] That [Result]"

**Question**
"Why [Surprising Thing]?"

**Statement**
"[Bold Claim]"

**Comparison**
"[Thing A] vs [Thing B]"

## Text Overlay Rules
- Max 5 words
- High contrast (white with black outline)
- Large, bold font
- Don't cover face

## Integrations
- DALL-E/Midjourney (backgrounds)
- Canva API (composition)
- Face detection (positioning)

## Cost
- ~$0.10-0.20 per thumbnail set
