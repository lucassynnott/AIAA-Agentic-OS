# YouTube Scriptwriter Workflow

## What This Workflow Is
A comprehensive YouTube script generation system that creates professional, high-converting scripts based on best practices. It researches the subject, analyzes their existing content style, researches the topic deeply, and produces 3000-6000 word scripts.

## What It Does
1. Gathers information about who the script is for
2. Scrapes existing YouTube content for voice/style reference
3. Scrapes other social channels for additional context
4. Conducts deep market research on the video topic via Perplexity
5. Researches the subject/creator themselves
6. Writes a comprehensive YouTube script (3000-6000 words)
7. Creates a Google Doc with the script
8. Sends Slack notification with details

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_key        # AI generation (Claude/GPT)
PERPLEXITY_API_KEY=your_key        # Market research
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # Google Docs
SLACK_WEBHOOK_URL=your_webhook     # Notifications
```

### Required Skill Bibles
- `SKILL_BIBLE_youtube_lead_generation.md` - Core scriptwriting principles
- `SKILL_BIBLE_copywriting_fundamentals.md` - Writing techniques

### Installation
```bash
pip install openai requests google-api-python-client google-auth yt-dlp python-dotenv
```

## How to Run
```bash
# Full workflow
python3 execution/generate_youtube_script_workflow.py \
  --creator "John Smith" \
  --youtube-channel "https://www.youtube.com/@johnsmith" \
  --topic "How to build an AI automation agency in 2026" \
  --video-type "educational" \
  --target-length "medium"

# Minimal (will prompt for details)
python3 execution/generate_youtube_script_workflow.py
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| creator | string | Yes | Name of the person the script is for |
| youtube_channel | string | No | Their YouTube channel URL |
| twitter | string | No | Twitter/X profile URL |
| linkedin | string | No | LinkedIn profile URL |
| instagram | string | No | Instagram profile URL |
| topic | string | Yes | The video topic/title |
| video_type | enum | Yes | "educational", "story", "case-study", "interview" |
| target_length | enum | No | "short" (3000w), "medium" (4500w), "long" (6000w) |
| target_audience | string | No | Who the video is for |
| call_to_action | string | No | What action viewers should take |
| key_points | string | No | Specific points to cover |

## Process

### Step 1: Information Gathering
**Quality Gate:** Must have creator name and video topic at minimum

If interactive mode:
- Ask who the script is for
- Ask for their YouTube channel URL
- Ask for other social profiles
- Ask for video topic and type

### Step 2: Content Reference Gathering
**YouTube Channel Analysis:**
- Download transcripts of 3-5 recent videos using yt-dlp
- Parse transcripts to clean text
- Analyze for:
  - Speaking style and tone
  - Common phrases and vocabulary
  - Video structure patterns
  - Hook styles used
  - CTA patterns

**Social Media Analysis:**
- Scrape recent posts/tweets for voice reference
- Note topics they discuss
- Identify audience engagement patterns

**Output:** Creator voice profile + content reference file

### Step 3: Topic Research (Perplexity)
Research queries:
1. "Latest information and trends about [topic]"
2. "Common questions people have about [topic]"
3. "Best practices and expert opinions on [topic]"
4. "Statistics and data related to [topic]"
5. "Common misconceptions about [topic]"

**Output:** Research document with facts, stats, and insights

### Step 4: Creator Research (Perplexity)
Research queries:
1. "[Creator name] professional background and expertise"
2. "[Creator name] business and offerings"
3. "[Creator name] content style and audience"

**Output:** Creator context for personalization

### Step 5: Script Generation
Load skill bible: `SKILL_BIBLE_youtube_lead_generation.md`

Generate script following structure:
1. **Hook (30-60 seconds)**
   - Pattern interrupt or bold claim
   - Single subject, single question
   - Visual hook suggestions

2. **Opening (2-3 minutes)**
   - Proof/credibility establishment
   - Promise of what they'll learn
   - Preview of content structure

3. **Body Sections (main content)**
   - Start each section with WHY
   - Provide actionable HOW
   - Include stories/examples
   - Demonstrate expertise where possible
   - Maintain high value-per-minute

4. **CTA and Close (1-2 minutes)**
   - Recap key points
   - Clear call to action
   - Future-pacing/motivation

**Word Count Targets:**
- Short: 3000 words (~15-20 min video)
- Medium: 4500 words (~25-30 min video)
- Long: 6000 words (~35-45 min video)

**Quality Gates:**
- [ ] Hook uses single subject, single question principle
- [ ] Each section starts with WHY before HOW
- [ ] Includes at least 3 stories/examples
- [ ] Has specific stats/data from research
- [ ] CTA is clear and actionable
- [ ] Word count within target range

### Step 6: Google Doc Creation
- Title format: "[Creator Name] - [Video Title] - Script v1"
- Include metadata header:
  - Video Type
  - Target Length
  - Word Count
  - Target Audience
  - Main CTA
- Full script with section headers

### Step 7: Slack Notification
Send notification with:
- Script title
- Video type
- Word count
- Target length
- Google Doc link
- Key topics covered
- Suggested thumbnail concepts

## Output Schema
```json
{
  "creator": "John Smith",
  "video_title": "How to Build an AI Automation Agency",
  "video_type": "educational",
  "word_count": 4532,
  "estimated_length": "28 minutes",
  "script_file": ".tmp/youtube_scripts/johnsmith_ai_agency_script.md",
  "google_doc_url": "https://docs.google.com/...",
  "research_file": ".tmp/youtube_scripts/johnsmith_ai_agency_research.md",
  "sections": [
    {"name": "Hook", "word_count": 150},
    {"name": "Opening", "word_count": 450},
    {"name": "Section 1: Why AI Agencies", "word_count": 800},
    ...
  ],
  "key_topics": ["AI automation", "agency model", "client acquisition"],
  "suggested_thumbnails": ["Before/after transformation", "AI robot visual"]
}
```

## Edge Cases

### No YouTube Channel
- Skip transcript analysis
- Rely more heavily on research and best practices
- Ask for voice/tone preferences

### Private/No Social Profiles
- Proceed with topic research only
- Use generic best practices for style

### Short Topic
- Expand research queries
- Look for related subtopics
- Suggest content expansion areas

### Niche/Technical Topic
- Include glossary of terms
- Suggest analogies for complex concepts
- Recommend visual aids

## Quality Gates

### Pre-Execution
- [ ] Creator name provided
- [ ] Video topic provided
- [ ] At least one content reference source OR style preferences
- [ ] API keys configured

### Post-Execution
- [ ] Script is 3000-6000 words
- [ ] Hook follows best practices
- [ ] Each section has clear structure
- [ ] Research integrated naturally
- [ ] Voice matches creator style (if reference available)
- [ ] Google Doc created successfully
- [ ] Slack notification sent

## Self-Annealing Notes

### What Works Well
- Transcript analysis captures voice authentically
- Perplexity provides current, relevant research
- Section-by-section generation maintains quality

### Improvements to Make
- Add A/B hook variants
- Include timestamp suggestions
- Generate accompanying LinkedIn/Twitter posts
- Create video outline PDF

## Related Directives
- [company_market_research.md](./company_market_research.md)
- [google_doc_creator.md](./google_doc_creator.md)
- [slack_notifier.md](./slack_notifier.md)
