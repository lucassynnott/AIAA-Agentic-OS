# Generate Content Calendar

## What This Workflow Is
This workflow generates a complete content calendar with topics, hooks, and posting schedules across multiple platforms, output to Google Sheets.

## What It Does
1. Takes your content pillars and target platforms
2. Generates topic ideas for each pillar
3. Creates platform-specific hooks
4. Assigns optimal posting dates
5. Exports to Google Sheets

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- OpenAI API access
- Google OAuth credentials

### Installation
```bash
pip install openai google-api-python-client gspread
```

## How to Run

### Step 1: Generate Calendar
```bash
python3 execution/create_content_calendar.py \
  --pillars "cold email tips,agency growth,case studies" \
  --platforms "twitter,linkedin" \
  --weeks 4 \
  --output_sheet "[SHEET_URL or NEW]"
```

### Quick One-Liner
```bash
python3 execution/create_content_calendar.py --pillars "pillar1,pillar2" --platforms "twitter,linkedin" --weeks 4
```

## Goal
Create a structured content calendar with topics, hooks, and posting schedule. Output to Google Sheets for easy team collaboration.

## Inputs
- **Niche/Industry**: What space you're creating content for
- **Target Audience**: Who you're trying to reach
- **Content Pillars**: 3-5 main themes (e.g., "cold email tips", "agency growth", "client case studies")
- **Platforms**: Where content will be posted (Twitter, LinkedIn, YouTube, etc.)
- **Timeframe**: How many weeks/months to plan
- **Posting Frequency**: Posts per week per platform

## Process

### 1. Define Content Strategy
Gather from user:
- What's your unique angle/expertise?
- What content has performed well before?
- What are your goals? (leads, brand awareness, thought leadership)
- Any specific topics to cover or avoid?

### 2. Generate Topic Ideas
Use AI to brainstorm topics for each content pillar:

```
For each content pillar, generate:
- 10 educational topics (how-to, tips, frameworks)
- 5 story-based topics (case studies, lessons learned)
- 5 contrarian takes (myths, unpopular opinions)
- 5 engagement topics (questions, polls, discussions)
```

### 3. Create Content Hooks
For each topic, generate platform-specific hooks:

**Twitter/X Format:**
- Hook (first line that stops scroll)
- Thread outline (5-7 points)
- CTA

**LinkedIn Format:**
- Hook (pattern interrupt)
- Story/insight structure
- Engagement question

**YouTube Format:**
- Title options (3)
- Thumbnail concept
- Video outline

### 4. Build Calendar Structure
Create Google Sheet with tabs:
- **Overview**: Monthly view with content mix
- **Twitter**: Daily posts with hooks and threads
- **LinkedIn**: 3-5 posts/week with full drafts
- **YouTube**: Weekly video topics and outlines

### 5. Schedule Distribution
Assign dates based on:
- Optimal posting times per platform
- Content variety (don't post same pillar back-to-back)
- Key dates/events in industry

### 6. Export to Sheet
```bash
python3 execution/create_content_calendar.py \
  --pillars "pillar1,pillar2,pillar3" \
  --platforms "twitter,linkedin" \
  --weeks 4 \
  --output_sheet "[SHEET_URL or NEW]"
```

## Output Schema

### Overview Tab
| Week | Monday | Tuesday | Wednesday | Thursday | Friday |
|------|--------|---------|-----------|----------|--------|
| 1 | Twitter: [Topic] | LinkedIn: [Topic] | Twitter: [Topic] | YouTube: [Topic] | Twitter: [Topic] |

### Platform Tab (e.g., Twitter)
| Date | Pillar | Topic | Hook | Full Content | Status | Performance |
|------|--------|-------|------|--------------|--------|-------------|
| Jan 6 | Growth | Cold email myths | "Stop doing this..." | [Thread text] | Draft | - |

## Content Formulas

### High-Performing Hook Patterns
1. **Contrarian**: "Stop [common advice]. Here's what actually works:"
2. **Story**: "I went from [bad state] to [good state] in [time]. Here's how:"
3. **List**: "[Number] [things] that [benefit]:"
4. **Question**: "Why do most [people] fail at [thing]?"
5. **Statement**: "[Bold claim]. Let me explain:"

### Content Mix (per week)
- 40% Educational (tips, how-to, frameworks)
- 25% Story/Case Study (results, lessons)
- 20% Engagement (questions, polls)
- 15% Promotional (offers, CTAs)

## Integration with Other Workflows
- Use `directives/write_twitter_thread.md` to expand topics into full threads
- Use `directives/write_linkedin_post.md` for long-form posts
- Use `directives/youtube_script_creator.md` for video scripts

## Edge Cases
- **Writer's block**: Use AI to generate variations on proven topics
- **Low engagement**: Analyze top performers, double down on what works
- **Platform algorithm changes**: Diversify content types, test new formats

## Deliverable
Google Sheet URL with complete content calendar, ready for execution.

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_content_strategy.md](../skills/SKILL_BIBLE_hormozi_content_strategy.md)**
- 30-day content strategy framework
- Content pillars and mix
- Engagement optimization

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Content marketing principles
- Audience building
- Platform-specific strategies

**[SKILL_BIBLE_hormozi_lead_generation.md](../skills/SKILL_BIBLE_hormozi_lead_generation.md)**
- Content as lead generation
- Value-first approach
- Content-to-conversion
