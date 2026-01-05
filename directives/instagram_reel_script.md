# Instagram Reel Script Creator

## What This Workflow Is
This workflow generates complete Instagram Reel scripts with scroll-stopping hooks, structured content, and engagement-optimized CTAs.

## What It Does
1. Takes your topic and desired length
2. Creates attention-grabbing hook (first 3 seconds)
3. Structures content with timing markers
4. Adds text overlay suggestions
5. Includes caption with hashtags

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
```

### Required Tools
- Python 3.10+
- OpenAI API access

### Installation
```bash
pip install openai
```

## How to Run

### Step 1: Generate Script
```bash
python3 execution/generate_reel_script.py \
  --topic "How to write cold emails that get replies" \
  --length 30 \
  --style educational \
  --output .tmp/reel_script.md
```

### Quick One-Liner
```bash
python3 execution/generate_reel_script.py --topic "Your Topic" --length 30 --style educational
```

### Batch Generate
```bash
python3 execution/generate_reel_script.py --topics topics.txt --batch --output_dir .tmp/reels/
```

## Goal
Generate viral Instagram Reel scripts with hooks, talking points, and CTAs.

## Inputs
- **Topic**: What the reel is about
- **Length**: 15s, 30s, 60s, or 90s
- **Style**: Educational, Entertaining, Story, Tutorial
- **Hook Type**: Question, Statement, Controversy

## Process

### 1. Generate Script
```bash
python3 execution/generate_reel_script.py \
  --topic "[TOPIC]" \
  --length 30 \
  --style educational
```

### 2. Script Structure (30s example)

```
HOOK (0-3s):
"[Pattern interrupt that stops the scroll]"

SETUP (3-10s):
"[Context/Problem setup]"

VALUE (10-25s):
"[Main content/tips/story]"
- Point 1
- Point 2
- Point 3

CTA (25-30s):
"[What you want them to do]"
```

### 3. Hook Formulas
- "Stop scrolling if you [problem]"
- "The #1 mistake [audience] make is..."
- "I went from [bad] to [good]. Here's how:"
- "Nobody talks about this but..."
- "[Controversial statement]"

### 4. Output Format
```
TITLE: [Working title]

HOOK (0-3s):
[Exact words to say]

VISUAL: [What's on screen]

BODY (3-25s):
[Script with timing]

TEXT OVERLAY: [On-screen text]

CTA (25-30s):
[Call to action]

CAPTION: [Full caption with hashtags]

AUDIO: [Trending sound suggestion]
```

### 5. Caption Template
```
[Hook repeated/expanded]

[Value summary in bullets]

Save this for later 📌
Follow @handle for more [topic] tips

#hashtag1 #hashtag2 #hashtag3
```

## Content Pillars for Reels
- Quick tips (3 things to...)
- Behind the scenes
- Myth busting
- Before/after
- Day in the life
- Tutorial/how-to

## Integrations
- OpenAI/Anthropic

## Cost
- ~$0.02-0.05 per script
