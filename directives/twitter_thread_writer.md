# Twitter/X Thread Writer

## What This Workflow Is
This workflow generates Twitter/X threads optimized for virality with compelling hooks, clear structure, and engagement-driving CTAs.

## What It Does
1. Takes your topic and desired thread length
2. Creates a scroll-stopping hook
3. Structures content into 280-char tweets
4. Numbers and formats for readability
5. Adds recap and CTA to final tweet

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # Or ANTHROPIC_API_KEY
```

### Required Tools
- Python 3.10+
- OpenAI or Anthropic API access

### Installation
```bash
pip install openai anthropic
```

## How to Run

### Step 1: Generate an Educational Thread
```bash
python3 execution/generate_twitter_thread.py \
  --topic "How to write cold emails that get replies" \
  --length medium \
  --style educational \
  --output .tmp/thread.md
```

### Step 2: Generate a Story Thread
```bash
python3 execution/generate_twitter_thread.py \
  --topic "How I built a 6-figure agency in 12 months" \
  --length long \
  --style story \
  --cta follow
```

### Step 3: Generate a Breakdown Thread
```bash
python3 execution/generate_twitter_thread.py \
  --topic "Analyzing Apple's marketing strategy" \
  --length medium \
  --style breakdown
```

### Quick One-Liner
```bash
python3 execution/generate_twitter_thread.py --topic "Your Topic" --length medium --style educational
```

### Batch Generate
```bash
python3 execution/generate_twitter_thread.py --topics topics.txt --batch --output .tmp/threads/
```

## Goal
Generate viral Twitter threads with strong hooks, clear structure, and engagement optimization.

## Inputs
- **Topic**: Thread subject
- **Thread Length**: Short (5 tweets), Medium (10), Long (15+)
- **Style**: Educational, Story, Breakdown, Listicle
- **CTA**: Follow, Retweet, Reply, Link

## Process

### 1. Generate Thread
```bash
python3 execution/generate_twitter_thread.py \
  --topic "[TOPIC]" \
  --length medium \
  --style breakdown
```

### 2. Thread Structure

**Tweet 1: Hook**
```
[Pattern interrupt or bold claim]

[Promise of value]

🧵 Thread:
```

**Tweets 2-N: Body**
```
[Number]. [Point]

[Explanation or example]
```

**Final Tweet: CTA**
```
TL;DR:
• [Point 1]
• [Point 2]
• [Point 3]

If this was helpful:
1. Follow @handle for more
2. RT tweet 1 to share
```

### 3. Hook Formulas

**Curiosity**
> "I spent 100 hours studying [X]. Here's what most people miss:"

**Results**
> "This strategy helped me [result]. Here's the playbook:"

**Contrarian**
> "Everyone says [common belief]. They're wrong. Here's why:"

**Story**
> "5 years ago I was [bad state]. Here's how I [transformation]:"

**Breakdown**
> "I analyzed [thing]. Here are 10 insights:"

### 4. Tweet-by-Tweet Template

```
Tweet 1 (Hook):
[Bold statement + promise]
Thread 🧵

Tweet 2:
First, let's understand [context].
[Key background]

Tweet 3:
1/ [First point]
[Explanation]
[Example if needed]

Tweet 4:
2/ [Second point]
[Explanation]

...continue pattern...

Tweet N-1:
The biggest mistake people make:
[Common error + correction]

Tweet N (CTA):
To recap:
• Point 1
• Point 2
• Point 3

Follow for more [topic] content.
RT tweet 1 to help others.
```

### 5. Formatting Rules
- 280 char limit per tweet
- Start threads with hook + "🧵"
- Number points (1/, 2/, etc.)
- Use line breaks for readability
- Emojis okay but don't overdo
- End with clear CTA

## Thread Types

### Educational
Share knowledge, how-to content.

### Story Thread
Personal narrative with lessons.

### Breakdown
Analyze a company, strategy, or concept.

### Curation
Best resources, tools, or examples.

### Prediction/Opinion
Hot takes on industry trends.

## Output Format
```
THREAD: [Title]

---
Tweet 1:
[Content]

---
Tweet 2:
[Content]

---
[Continue...]

---
Tweet N:
[CTA tweet]

---

Suggested posting time: [Time]
```

## Integrations Required
- OpenAI/Anthropic API

## Cost Estimate
- ~$0.03-0.08 per thread

## Pro Tips
- Post threads 8-10am or 4-6pm
- Quote tweet your own hook after 2 hours
- Reply to every comment
- Space tweets 1-2 min apart when posting

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_content_strategy.md](../skills/SKILL_BIBLE_hormozi_content_strategy.md)**
- Content strategy framework
- Thread structure optimization
- Engagement tactics

**[SKILL_BIBLE_hormozi_persuasion_speaking.md](../skills/SKILL_BIBLE_hormozi_persuasion_speaking.md)**
- Hook formulas
- Compelling storytelling
- Attention-grabbing techniques

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Social media marketing principles
- Audience growth
- Content positioning
