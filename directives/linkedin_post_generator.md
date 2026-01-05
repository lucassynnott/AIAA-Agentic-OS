# AI LinkedIn Post Generator

## What This Workflow Is
This workflow generates LinkedIn posts optimized for engagement using proven frameworks, strong hooks, and algorithm-friendly formatting.

## What It Does
1. Takes your topic or idea as input
2. Selects the best post structure for your goal
3. Generates hook + body + CTA
4. Formats for LinkedIn algorithm optimization
5. Suggests posting times and hashtags

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

### Step 1: Generate a Story Post
```bash
python3 execution/generate_linkedin_post.py \
  --topic "How I landed my first client" \
  --type story \
  --tone casual \
  --cta comments \
  --output .tmp/linkedin_post.md
```

### Step 2: Generate a Tips Post
```bash
python3 execution/generate_linkedin_post.py \
  --topic "Cold email best practices" \
  --type tips \
  --tone professional \
  --cta dms
```

### Step 3: Generate a Contrarian Post
```bash
python3 execution/generate_linkedin_post.py \
  --topic "Why cold calling is dead" \
  --type contrarian \
  --tone casual \
  --cta comments
```

### Quick One-Liner
```bash
python3 execution/generate_linkedin_post.py --topic "Your Topic" --type story --tone casual
```

### Batch Generate (Content Calendar)
```bash
python3 execution/generate_linkedin_post.py \
  --topics topics.txt \
  --batch \
  --output .tmp/posts/
```

## Goal
Generate engaging LinkedIn posts optimized for the algorithm with hooks, formatting, and CTAs.

## Inputs
- **Topic/Idea**: What to post about
- **Post Type**: Story, Tips, Contrarian, Question, Carousel
- **Tone**: Professional, Casual, Inspirational
- **CTA**: What action you want (comments, DMs, link clicks)

## Process

### 1. Generate Post
```bash
python3 execution/generate_linkedin_post.py \
  --topic "[TOPIC]" \
  --type story \
  --tone casual \
  --cta comments
```

### 2. Post Structures

**Story Post**
```
[Hook - 1 line that stops scroll]

[Setup - context in 2-3 lines]

[Conflict - the problem/challenge]

[Resolution - what happened]

[Lesson - the takeaway]

[CTA - engagement question]
```

**Tips/Listicle Post**
```
[Hook - provocative statement]

Here's what I learned:

1. [Tip 1]
↳ [Explanation]

2. [Tip 2]
↳ [Explanation]

3. [Tip 3]
↳ [Explanation]

[CTA]
```

**Contrarian Post**
```
[Hot take that challenges conventional wisdom]

Here's why everyone's wrong:

[Argument 1]
[Argument 2]
[Argument 3]

[Nuanced conclusion]

Agree or disagree? 👇
```

### 3. Hook Formulas

- "I was wrong about [X]. Here's what I learned."
- "Stop [common advice]. Do this instead:"
- "[Number] years ago, I [failure]. Today, [success]."
- "Unpopular opinion: [contrarian take]"
- "The best [role] I know all do this:"
- "I asked [impressive person] for advice. Their answer surprised me."

### 4. Formatting Rules
- First line = hook (most important)
- Short paragraphs (1-2 sentences)
- Use line breaks liberally
- Emojis sparingly (1-3 max)
- End with question or CTA
- No external links in post (comment instead)

### 5. Output
```markdown
**Hook:**
[First line]

**Body:**
[Full post content]

**CTA:**
[Engagement prompt]

**Best Time to Post:**
[Recommendation based on audience]

**Hashtags (optional):**
#tag1 #tag2 #tag3
```

## Post Types

### Story (Highest engagement)
Personal narrative with lesson learned.

### Tips/Value (High saves)
Actionable advice in list format.

### Contrarian (High comments)
Challenge common beliefs, spark debate.

### Question (High comments)
Ask audience for opinions/experiences.

### Carousel (High impressions)
Multi-slide visual content.

## Integrations Required
- OpenAI/Anthropic API

## Cost Estimate
- ~$0.02-0.05 per post

## Pro Tips
- Post 3-5x per week for growth
- Engage in comments within first hour
- Reply to every comment
- Best times: 7-8am, 12pm, 5-6pm (audience timezone)
