# Ad Creative Generator

## What This Workflow Is
This workflow generates ad copy and creative concepts for Meta, Google, and LinkedIn ads with multiple variations for A/B testing.

## What It Does
1. Takes product/service and audience info
2. Generates platform-specific ad copy
3. Creates multiple headline/body variations
4. Suggests visual concepts
5. Outputs ready-to-launch ad sets

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For ad copy generation
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai
```

## How to Run

### Step 1: Generate Ad Creative
```bash
python3 execution/generate_ad_creative.py \
  --product "[PRODUCT]" \
  --audience "[AUDIENCE]" \
  --platform meta \
  --type image \
  --variations 5 \
  --output .tmp/ads/
```

### Quick One-Liner
```bash
python3 execution/generate_ad_creative.py --product "[PRODUCT]" --platform meta --variations 5
```

## Goal
Generate ad copy and creative concepts for Meta, Google, and LinkedIn ads.

## Inputs
- **Product/Service**: What you're advertising
- **Target Audience**: Who you're targeting
- **Platform**: Meta, Google, LinkedIn
- **Ad Type**: Image, video, carousel
- **Objective**: Awareness, traffic, conversions

## Process

### 1. Generate Ad Concepts
```bash
python3 execution/generate_ad_creative.py \
  --product "[PRODUCT]" \
  --audience "[AUDIENCE]" \
  --platform meta \
  --type image \
  --variations 5 \
  --output .tmp/ads/
```

### 2. Ad Copy Structure

**Meta (Facebook/Instagram):**
```
PRIMARY TEXT (125 chars):
[Hook + Value Prop + CTA]

HEADLINE (40 chars):
[Benefit-focused headline]

DESCRIPTION (30 chars):
[Supporting detail]
```

**Google Search:**
```
HEADLINE 1 (30 chars): [Primary benefit]
HEADLINE 2 (30 chars): [Secondary benefit]
HEADLINE 3 (30 chars): [CTA or differentiator]
DESCRIPTION 1 (90 chars): [Expanded value prop]
DESCRIPTION 2 (90 chars): [Social proof or offer]
```

**LinkedIn:**
```
INTRO TEXT (150 chars):
[Professional hook + value]

HEADLINE (70 chars):
[Benefit for business]
```

### 3. Copy Formulas

**Problem-Solution:**
"Tired of [problem]? [Product] helps you [solution]."

**Social Proof:**
"Join [X] companies who [benefit] with [product]."

**Curiosity:**
"The secret to [result] that [audience] are using."

**Direct Offer:**
"Get [benefit] in [timeframe]. [CTA]."

### 4. Creative Concepts
For each ad, generate:
- Headline options (3-5)
- Body copy options (3-5)
- Image/video concept
- CTA button text

### 5. A/B Test Sets
Generate variations for testing:
- Different hooks
- Different benefits
- Different CTAs
- Different visuals

## Output
```json
{
  "ad_set_1": {
    "headline": "[Headline]",
    "primary_text": "[Text]",
    "description": "[Desc]",
    "cta": "Learn More",
    "image_concept": "[Visual description]"
  }
}
```

## Integrations
- OpenAI (copy)
- DALL-E (image concepts)

## Cost
- ~$0.05-0.10 per ad set

## Related Skill Bibles

Load these skill bibles for high-converting ad creative:

**[SKILL_BIBLE_meta_ads_manager_technical.md](../skills/SKILL_BIBLE_meta_ads_manager_technical.md)** (PRIMARY)
- Complete Meta Ads Manager technical setup and optimization
- Pixel implementation, Conversions API, audience infrastructure
- Persona-led creative diversification (90% success rate)
- Andromeda update strategies and incremental reach optimization
- Campaign structure, budget allocation, and scaling frameworks

**[SKILL_BIBLE_hormozi_paid_ads_mastery.md](../skills/SKILL_BIBLE_hormozi_paid_ads_mastery.md)**
- Complete paid ads framework (30 minutes condensed)
- Ad structure and hook formulas
- Platform-specific optimization tactics

**[SKILL_BIBLE_hormozi_ad_analysis.md](../skills/SKILL_BIBLE_hormozi_ad_analysis.md)**
- Analysis of top-performing ads (Superbowl tier list)
- What makes ads convert vs fail
- Creative direction insights

**[SKILL_BIBLE_hormozi_marketing_strategy_ryan.md](../skills/SKILL_BIBLE_hormozi_marketing_strategy_ryan.md)**
- Ryan Reynolds $1.3B marketing strategy
- Attention-grabbing creative concepts
- Brand voice in advertising

**[SKILL_BIBLE_hormozi_customer_acquisition_fast.md](../skills/SKILL_BIBLE_hormozi_customer_acquisition_fast.md)**
- Fast customer acquisition through ads
- Offer positioning in ad copy
- Direct response ad principles
