# Ultimate Content Calendar Generator

## What This Workflow Is
**Complete content planning and calendar system** that generates 30-90 days of content ideas, topics, and hooks across all platforms. Creates platform-specific content with posting schedules, hashtags, and repurposing strategies. Built for content agencies and social media managers.

## What It Does
1. Researches trending topics in the niche
2. Generates content pillars and themes
3. Creates platform-specific content ideas
4. Produces posting calendar with optimal times
5. Generates hooks, captions, and hashtags
6. Creates repurposing workflows
7. Builds content batching schedules

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
PERPLEXITY_API_KEY=your_key           # Trend research
```

### Required Skill Bibles
- `SKILL_BIBLE_content_calendar_creation.md`
- `SKILL_BIBLE_content_strategy_growth.md`
- `SKILL_BIBLE_content_marketing.md`
- `SKILL_BIBLE_linkedin_post_writing.md`
- `SKILL_BIBLE_twitter_thread_writing.md`
- `SKILL_BIBLE_youtube_script_writing.md`

## How to Run

```bash
# Full content calendar (30 days)
python3 execution/generate_content_calendar.py \
  --client "Acme Corp" \
  --industry "B2B SaaS" \
  --platforms "linkedin,twitter,instagram" \
  --content-pillars "product tips,industry insights,behind the scenes" \
  --posts-per-week 5 \
  --days 30

# Extended calendar (90 days)
python3 execution/generate_content_calendar.py \
  --client "Acme Corp" \
  --industry "Marketing Agency" \
  --platforms "all" \
  --days 90 \
  --include-video-scripts

# Repurposing calendar
python3 execution/generate_content_calendar.py \
  --source-content blog_posts.json \
  --repurpose-to "linkedin,twitter,instagram,youtube_shorts"
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client | string | Yes | Client/brand name |
| industry | string | Yes | Industry/niche |
| platforms | list | Yes | Target platforms |
| content-pillars | list | No | Main content themes |
| posts-per-week | int | No | Posts per platform per week |
| days | int | No | Calendar duration (30/60/90) |
| include-video-scripts | flag | No | Generate video content |
| source-content | path | No | Content to repurpose |
| brand-voice | string | No | Tone/style description |

## Process

### Phase 1: Trend & Topic Research

**Industry Trends:**
- Current news and events
- Emerging topics
- Seasonal opportunities
- Competitor content analysis

**Audience Interests:**
- Common questions
- Pain points
- Aspirations
- Engagement patterns

**Content Performance:**
- Top-performing formats
- Optimal posting times
- Best hashtags
- Engagement benchmarks

### Phase 2: Content Pillar Development

**Pillar Framework:**
```
Pillar 1: Educational (40%)
├── How-to guides
├── Tips and tricks
├── Industry insights
└── Tutorials

Pillar 2: Social Proof (25%)
├── Customer stories
├── Case studies
├── Results/metrics
└── Testimonials

Pillar 3: Behind the Scenes (20%)
├── Team content
├── Process reveals
├── Company culture
└── Day-in-the-life

Pillar 4: Engagement (15%)
├── Questions
├── Polls
├── Trends/memes
└── User-generated content
```

### Phase 3: Platform-Specific Content Generation

**LinkedIn:**
- Long-form posts (1300+ characters)
- Personal storytelling
- Industry insights
- Carousel documents
- Professional tone

**Twitter/X:**
- Thread format (5-10 tweets)
- Single tweet zingers
- Quote tweets/commentary
- Engagement prompts
- Casual/witty tone

**Instagram:**
- Carousel posts (5-10 slides)
- Reels scripts (15-60 sec)
- Stories storyboards
- Static post captions
- Visual-first approach

**YouTube:**
- Video scripts
- Shorts scripts (60 sec)
- Thumbnail concepts
- SEO titles and descriptions

**TikTok:**
- Trend-based content
- Hook-focused scripts
- Duet/stitch opportunities
- Trending sounds

### Phase 4: Calendar Generation

**Weekly Structure:**
```
Monday: Educational (long-form)
Tuesday: Social Proof
Wednesday: Engagement/Question
Thursday: Behind the Scenes
Friday: Educational (quick tip)
Weekend: Repurposed/Evergreen
```

**Posting Times (Platform-Specific):**
| Platform | Best Times |
|----------|------------|
| LinkedIn | 7-8 AM, 12 PM, 5-6 PM (Tue-Thu) |
| Twitter | 8 AM, 12 PM, 4 PM (Mon-Fri) |
| Instagram | 11 AM, 2 PM, 7 PM (Mon-Sat) |
| YouTube | 2-4 PM (Thu-Sat) |
| TikTok | 7-9 AM, 12-3 PM, 7-11 PM |

### Phase 5: Content Creation

For each post:

**Hook Generation (3 variations):**
- Question hook
- Statement hook
- Story hook

**Full Caption/Copy:**
- Opening hook
- Value delivery
- Call to action
- Hashtags (platform-appropriate)

**Visual Direction:**
- Image concept
- Design notes
- Brand colors/fonts
- Required assets

### Phase 6: Repurposing Workflow

**Content Cascade:**
```
1 Long-Form Video (YouTube)
├── 3 YouTube Shorts
├── 1 Blog Post
│   ├── 3 LinkedIn Posts
│   ├── 5 Twitter Threads
│   └── 2 Email Newsletters
├── 5 TikToks/Reels
├── 10 Story Slides
└── 15 Quote Graphics
```

## Output Structure
```
.tmp/content_calendars/{client_slug}/
├── research/
│   ├── trends.md
│   ├── competitor_content.md
│   └── audience_insights.json
├── strategy/
│   ├── content_pillars.md
│   └── platform_strategy.md
├── calendar/
│   ├── master_calendar.csv
│   ├── linkedin_calendar.csv
│   ├── twitter_calendar.csv
│   ├── instagram_calendar.csv
│   └── youtube_calendar.csv
├── content/
│   ├── linkedin/
│   │   ├── week_01/
│   │   └── week_02/
│   ├── twitter/
│   ├── instagram/
│   └── youtube/
├── assets/
│   ├── design_briefs/
│   └── image_concepts/
├── repurposing/
│   └── content_cascade.md
└── result.json
```

## Content Templates

### LinkedIn Post Template
```markdown
**Hook:** {Opening line that stops the scroll}

{Story/insight paragraph 1}

{Story/insight paragraph 2}

Key takeaways:
→ {Point 1}
→ {Point 2}
→ {Point 3}

{Call to action}

---

{Hashtags: 3-5 relevant}
```

### Twitter Thread Template
```markdown
🧵 {Hook tweet - make them want to read more}

1/ {First point - expand on hook}

2/ {Second point - build on previous}

3/ {Third point - add value}

4/ {Fourth point - practical example}

5/ {Fifth point - actionable tip}

6/ {Wrap up - summarize key insight}

7/ {CTA - follow, retweet, reply}
```

### Instagram Carousel Template
```markdown
Slide 1: {Bold hook/question}
Slide 2: {Problem statement}
Slide 3: {Point 1}
Slide 4: {Point 2}
Slide 5: {Point 3}
Slide 6: {Point 4}
Slide 7: {Point 5}
Slide 8: {Summary}
Slide 9: {CTA - save, share, follow}
Slide 10: {About/promo}
```

## Quality Gates

### Pre-Publish Checklist
- [ ] Hook is attention-grabbing
- [ ] Value is clear and actionable
- [ ] CTA is included
- [ ] Hashtags researched (platform-appropriate)
- [ ] Visual assets prepared
- [ ] Scheduled at optimal time
- [ ] Proofread for errors
- [ ] Brand voice consistent

### Performance Benchmarks
| Platform | Engagement Rate Target |
|----------|----------------------|
| LinkedIn | 2-4% |
| Twitter | 1-3% |
| Instagram | 3-6% |
| YouTube | 5% CTR |
| TikTok | 5-10% |

## Error Handling

| Error | Solution |
|-------|----------|
| No trending topics | Use evergreen content |
| Low engagement | Adjust posting times/hooks |
| Content fatigue | Rotate pillars/formats |
| Platform algorithm change | Monitor and adapt |

## Integration with Other Workflows

- `linkedin_post_generator.md` - LinkedIn content
- `twitter_thread_writer.md` - Twitter threads
- `instagram_reel_script.md` - Reels scripts
- `youtube_script_creator.md` - Video scripts
- `carousel_post_creator.md` - Carousel design

## Self-Annealing Notes

### What Works
- Consistency beats volume
- Hooks determine success
- Repurposing multiplies output
- Batching saves time

### What Doesn't Work
- Posting without strategy
- Ignoring platform nuances
- Generic content across platforms
- Inconsistent posting schedule

### Continuous Improvement
- Track top-performing content monthly
- Analyze engagement patterns
- Update pillar distribution based on data
- Test new formats quarterly
