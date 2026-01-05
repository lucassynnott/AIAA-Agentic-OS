# YouTube Script Generator

## What This Workflow Is
This workflow generates complete, ready-to-record YouTube video scripts with attention-grabbing hooks, structured content, and engagement-optimized CTAs.

## What It Does
1. Researches top-performing videos on your topic
2. Analyzes competitor hooks, structures, and what works
3. Generates a full script with timestamps
4. Creates title options, thumbnail concepts, and descriptions
5. Outputs everything in a ready-to-use format

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # Or ANTHROPIC_API_KEY
PERPLEXITY_API_KEY=your_perplexity_key    # For research (optional)
```

### Required Tools
- Python 3.10+
- OpenAI or Anthropic API access

### Installation
```bash
pip install openai anthropic requests
```

## How to Run

### Step 1: Research Topic (Optional but Recommended)
```bash
python3 execution/research_topic.py \
  "cold email strategies 2024" \
  --competitor_videos 5 \
  --output .tmp/research.json
```

### Step 2: Generate Script
```bash
python3 execution/generate_youtube_script.py \
  --topic "5 Cold Email Mistakes Killing Your Reply Rates" \
  --audience "B2B sales reps and agency owners" \
  --length medium \
  --style educational \
  --research .tmp/research.json \
  --output .tmp/script.md
```

### Step 3: Review Output
Open `.tmp/script.md` to see:
- 3 title options
- 3 thumbnail concepts
- Full timestamped script
- SEO description
- Tags list

### Quick One-Liner
```bash
python3 execution/generate_youtube_script.py \
  --topic "How to Build a Lead Gen Agency in 2024" \
  --audience "aspiring agency owners" \
  --length medium \
  --style educational
```

### Without Research (Faster)
```bash
python3 execution/generate_youtube_script.py --topic "Your Topic" --audience "Target Audience" --length short
```

## Goal
Generate complete YouTube video scripts with hooks, structure, and CTAs optimized for engagement.

## Inputs
- **Topic**: Video subject
- **Target Audience**: Who you're creating for
- **Video Length**: Short (5-8 min), Medium (10-15 min), Long (20+ min)
- **Style**: Educational, Story-based, Listicle, Tutorial
- **Tone**: Professional, Casual, Energetic

## Tools/Scripts
- `execution/generate_youtube_script.py` - Script generator
- `execution/research_topic.py` - Topic research

## Process

### 1. Topic Research
```bash
python3 execution/research_topic.py "[TOPIC]" \
  --competitor_videos 5 \
  --output .tmp/research.json
```

Analyzes:
- Top-performing videos on topic
- Common hooks and structures
- Audience questions (comments)
- Keyword opportunities

### 2. Generate Script
```bash
python3 execution/generate_youtube_script.py \
  --topic "[TOPIC]" \
  --audience "[AUDIENCE]" \
  --length medium \
  --style educational \
  --research .tmp/research.json \
  --output .tmp/script.md
```

### 3. Script Structure

```markdown
# [VIDEO TITLE]

## HOOK (0:00-0:30)
[Pattern interrupt + promise]

"Most people think [common belief], but after [credibility], 
I discovered [contrarian insight]. In this video, I'll show you 
[specific outcome] in [timeframe]."

## INTRO (0:30-1:00)
[Context + roadmap]

"Here's what we'll cover:
1. [Point 1]
2. [Point 2]
3. [Point 3]
Plus, I'll share [bonus] at the end."

## MAIN CONTENT

### Section 1: [Topic] (1:00-4:00)
[Key point]
[Example/Story]
[Actionable takeaway]

### Section 2: [Topic] (4:00-7:00)
[Key point]
[Example/Story]
[Actionable takeaway]

### Section 3: [Topic] (7:00-10:00)
[Key point]
[Example/Story]
[Actionable takeaway]

## RECAP (10:00-10:30)
"So to recap:
1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]"

## CTA (10:30-11:00)
"If you found this valuable, hit subscribe and the bell.
Drop a comment with [engagement question].
Check out [related video] next."

## END SCREEN (11:00-11:15)
[Suggested videos overlay]
```

### 4. Hook Formulas

**Curiosity Gap**
> "The #1 mistake killing your [X] (and it's not what you think)"

**Contrarian**
> "Stop doing [common advice] - here's what actually works"

**Story**
> "I went from [bad state] to [good state] in [time] - here's how"

**Result**
> "This strategy generated [specific result] in [timeframe]"

**Question**
> "Why do 90% of [people] fail at [thing]?"

### 5. Output Includes
- Full script (word-for-word)
- Timestamp breakdown
- B-roll suggestions
- Title options (3)
- Thumbnail concepts (3)
- Description template
- Tags list

## Output Format
```
Title Options:
1. "[Primary title]"
2. "[Alternative 1]"
3. "[Alternative 2]"

Thumbnail Concepts:
1. [Face + text overlay: "X"]
2. [Before/after comparison]
3. [Shocking stat visual]

Script: [Full markdown script]

Description: [SEO-optimized description]

Tags: [tag1], [tag2], [tag3]...
```

## Integrations Required
- OpenAI/Anthropic API
- YouTube API (optional, for research)

## Cost Estimate
- ~$0.10-0.20 per script
- Research adds ~$0.05

## Edge Cases
- Trending topic: Include timeliness hooks
- Evergreen content: Focus on searchability
- Tutorial: Add step numbers and timestamps
