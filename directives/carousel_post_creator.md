# Carousel Post Creator

## What This Workflow Is
This workflow generates complete LinkedIn/Instagram carousel posts including slide content, design specs, and captions optimized for engagement.

## What It Does
1. Takes your topic and generates carousel structure
2. Creates copy for each slide (hook, value, CTA)
3. Outputs design-ready slide content
4. Generates caption with hashtags
5. Optionally creates designed PNG slides

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For content generation
CANVA_API_KEY=your_canva_key              # Optional for design
```

### Required Tools
- Python 3.10+
- OpenAI API access
- Optional: Canva API or Placid for design

### Installation
```bash
pip install openai requests
```

## How to Run

### Step 1: Generate Carousel Content
```bash
python3 execution/generate_carousel.py \
  --topic "5 Cold Email Mistakes" \
  --slides 8 \
  --platform linkedin \
  --output .tmp/carousel.json
```

### Step 2: Create Designed Slides (Optional)
```bash
python3 execution/design_carousel.py \
  --content .tmp/carousel.json \
  --style minimalist \
  --output .tmp/carousel_slides/
```

### Quick One-Liner
```bash
python3 execution/generate_carousel.py --topic "Your Topic" --slides 8 --platform linkedin
```

## Goal
Generate LinkedIn/Instagram carousel posts with designed slides and copy.

## Inputs
- **Topic**: What the carousel is about
- **Slides**: Number of slides (5-10)
- **Platform**: LinkedIn or Instagram
- **Style**: Minimalist, Bold, Professional

## Process

### 1. Generate Content
```bash
python3 execution/generate_carousel.py \
  --topic "[TOPIC]" \
  --slides 8 \
  --platform linkedin \
  --output .tmp/carousel.json
```

### 2. Carousel Structure

**Slide 1: Hook**
- Bold statement or question
- Creates curiosity
- "Swipe to learn..."

**Slides 2-7: Value**
- One point per slide
- Short text (10-20 words)
- Visual hierarchy

**Slide 8: Summary**
- Recap key points
- Reinforce value

**Slide 9: CTA**
- Follow, save, share
- Link in bio/comments

### 3. Slide Templates

**Tip Slide:**
```
[Number emoji]

[TIP HEADLINE]

[1-2 sentence explanation]
```

**Stat Slide:**
```
[BIG NUMBER]

[What it means]
```

**Quote Slide:**
```
"[Quote text]"

— [Attribution]
```

### 4. Design Specs
- Size: 1080x1080 (square) or 1080x1350 (portrait)
- Font: Bold, readable
- Colors: Consistent brand palette
- Whitespace: Generous margins

### 5. Output
```
carousel/
  ├── slide_1.png
  ├── slide_2.png
  ├── ...
  ├── slide_N.png
  └── caption.txt
```

## Caption Template
```
[Hook - expand on slide 1]

[Key takeaways in bullets]

Which tip will you try first? 👇

Save this for later 📌
Share with someone who needs this

#hashtag1 #hashtag2 #hashtag3
```

## Integrations
- OpenAI (content)
- Canva API or Placid (design)

## Cost
- Content: ~$0.05
- Design: ~$0.10/slide
- **10-slide carousel: ~$1.00**

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_content_strategy.md](../skills/SKILL_BIBLE_hormozi_content_strategy.md)**
- Content structure optimization
- Engagement tactics
- Value-driven content

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Visual content principles
- Social media marketing
- Audience engagement

**[SKILL_BIBLE_hormozi_persuasion_speaking.md](../skills/SKILL_BIBLE_hormozi_persuasion_speaking.md)**
- Hook formulas
- Compelling storytelling
- CTA optimization
