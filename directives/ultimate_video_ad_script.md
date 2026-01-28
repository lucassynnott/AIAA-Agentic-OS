# Ultimate Video Ad Script Generator

## What This Workflow Is
**Complete video ad script generation system** that creates scripts for Meta, YouTube, TikTok, and UGC-style ads. Produces hook variations, full scripts, shot lists, and performance predictions.

## What It Does
1. Generates attention-grabbing hooks
2. Creates full video scripts
3. Produces shot-by-shot breakdowns
4. Develops multiple ad angles
5. Creates A/B test variations
6. Generates thumbnail concepts

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI script generation
```

### Required Skill Bibles
- `SKILL_BIBLE_ad_creative_hooks.md`
- `SKILL_BIBLE_vsl_writing_production.md`
- `SKILL_BIBLE_youtube_script_writing.md`
- `SKILL_BIBLE_ad_copywriting.md`

## How to Run

```bash
python3 execution/generate_video_ad_script.py \
  --product "Fitness App" \
  --offer "7-day free trial" \
  --target-audience "Busy professionals wanting to get fit" \
  --platform "meta" \
  --ad-length 30 \
  --style "ugc" \
  --variations 3
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| product | string | Yes | Product/service |
| offer | string | Yes | What you're promoting |
| target-audience | string | Yes | Who you're targeting |
| platform | enum | Yes | "meta", "youtube", "tiktok" |
| ad-length | int | No | 15, 30, or 60 seconds |
| style | enum | No | "ugc", "polished", "talking_head" |
| variations | int | No | Number of script variations |

## Process

### Phase 1: Hook Generation

**Hook Categories:**
1. Question Hook - "Are you still doing X?"
2. Controversial Hook - "Stop doing X immediately"
3. Story Hook - "I was in your position..."
4. Result Hook - "How I achieved X in Y days"
5. Fear Hook - "The hidden danger of X"
6. Curiosity Hook - "What nobody tells you about X"

**Generate 5 hooks per variation**

### Phase 2: Script Structure

**15-Second Script:**
```
0-3s: HOOK (attention grabber)
3-8s: PROBLEM (agitate pain point)
8-12s: SOLUTION (introduce product)
12-15s: CTA (clear action)
```

**30-Second Script:**
```
0-5s: HOOK (pattern interrupt)
5-12s: PROBLEM (expand on pain)
12-20s: SOLUTION (show product benefits)
20-25s: PROOF (testimonial/result)
25-30s: CTA (urgency + action)
```

**60-Second Script:**
```
0-5s: HOOK
5-15s: PROBLEM (deep dive)
15-30s: SOLUTION (features + benefits)
30-45s: PROOF (multiple proof points)
45-55s: HANDLE OBJECTION
55-60s: CTA
```

### Phase 3: Shot List

For each script section:
- Camera angle
- B-roll suggestions
- Text overlay
- Audio/music cue
- Talent direction

### Phase 4: Variations

**Generate by:**
- Different hooks
- Different proof points
- Different CTAs
- Different presenters/voices

## Output Structure
```
.tmp/video_ad_scripts/{product_slug}/
├── hooks/
│   └── hook_variations.md
├── scripts/
│   ├── script_v1.md
│   ├── script_v2.md
│   └── script_v3.md
├── production/
│   ├── shot_lists.md
│   └── b_roll_suggestions.md
├── thumbnails/
│   └── thumbnail_concepts.md
└── result.json
```

## Script Templates

### UGC Style (30s)
```
HOOK (0-3s):
[Person looks at camera, frustrated]
"I was so tired of [problem]..."

PROBLEM (3-10s):
[B-roll of struggle]
"Every day I would [pain point]. It was exhausting
and nothing seemed to work."

SOLUTION (10-20s):
[Show product in use]
"Then I found [product]. Within [timeframe], 
I noticed [specific benefit]."

PROOF (20-25s):
[Show result/transformation]
"Now I [positive outcome] and I've [specific result]."

CTA (25-30s):
[Hold up product/point to screen]
"Link in bio for [offer]. Trust me, you need this."
```

### Talking Head (30s)
```
HOOK (0-3s):
"If you're struggling with [problem], watch this."

PROBLEM (3-10s):
"Most [audience] try [wrong solution] but it 
doesn't work because [reason]."

SOLUTION (10-20s):
"That's why I created [product]. It [key benefit]
without [common objection]."

PROOF (20-25s):
"We've helped [number] [audience] achieve [result]."

CTA (25-30s):
"Click below to [specific action]. [Urgency element]."
```

## Quality Gates

### Pre-Production Checklist
- [ ] Hook grabs attention in 3 seconds
- [ ] Script matches platform style
- [ ] CTA is clear and specific
- [ ] Timing matches requirements
- [ ] Proof points are accurate
- [ ] Language matches audience
- [ ] No policy violations

### Performance Predictions
| Element | Impact |
|---------|--------|
| Strong hook | +30% view-through |
| Social proof | +25% conversion |
| Clear CTA | +20% clicks |
| Platform-native | +15% engagement |
