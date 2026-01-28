# YouTube Knowledge Miner

## What This Workflow Is

An automated system that extracts best practices and how-to knowledge from top YouTube channels in any niche, converts video content into structured manuals, and generates comprehensive skill bibles for AI automation.

## What It Does

1. **Find Top Channels** - Search YouTube for authority channels in your niche
2. **Extract Best Videos** - Get highest-performing educational videos
3. **Get Transcripts** - Use transcript APIs (Supadata, TranscriptAPI, or YouTube captions)
4. **Convert to Manuals** - Transform transcripts into structured how-to guides
5. **Filter Quality** - Rate and filter manuals worth keeping
6. **Generate Skill Bibles** - Synthesize multiple sources into comprehensive guides

## Prerequisites

**Required API Keys:**
- `OPENROUTER_API_KEY` - For Claude manual generation
- YouTube Data API enabled in Google Cloud Console

**Transcript APIs (at least one recommended):**
- `SUPADATA_API_KEY` - Primary transcript API (supadata.ai) - Free: 100/mo, Pro: $9/1000
- `TRANSCRIPTAPI_KEY` - Secondary transcript API (transcriptapi.com) - $5/mo starter

**Optional:**
- `GOOGLE_API_KEY` - For Gemini Flash (cheaper alternative to Claude)

**Installation:**
```bash
pip install google-api-python-client google-auth google-auth-oauthlib youtube-transcript-api python-dotenv requests
```

**Transcript Fallback Chain:**
1. Supadata API (if SUPADATA_API_KEY set)
2. TranscriptAPI (if TRANSCRIPTAPI_KEY set)
3. youtube-transcript-api (free, may be rate limited)

## How to Run

```bash
# Basic usage - mine knowledge from a niche
python3 execution/youtube_knowledge_miner.py \
  --niche "meta ads" "facebook advertising" \
  --max-channels 10 \
  --videos-per-channel 5

# Use Gemini for cheaper processing
python3 execution/youtube_knowledge_miner.py \
  --niche "cold email" "lead generation" \
  --use-gemini \
  --max-channels 5

# Full options
python3 execution/youtube_knowledge_miner.py \
  --niche "landing page copywriting" \
  --max-channels 15 \
  --videos-per-channel 10 \
  --min-subscribers 10000 \
  --min-views 10000 \
  --min-skill-rating 8 \
  --output-dir .tmp/landing_page_knowledge \
  --parallel 5
```

## Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--niche` | list | Yes | - | Keywords to search (can provide multiple) |
| `--max-channels` | int | No | 10 | Maximum channels to analyze |
| `--videos-per-channel` | int | No | 5 | Videos to process per channel |
| `--min-subscribers` | int | No | 5000 | Minimum channel subscribers |
| `--min-views` | int | No | 5000 | Minimum video views |
| `--min-skill-rating` | int | No | 7 | Minimum quality rating (1-10) |
| `--use-gemini` | flag | No | False | Use Gemini Flash (cheaper) |
| `--output-dir` | string | No | .tmp/knowledge_mine | Output directory |
| `--parallel` | int | No | 1 | Parallel video processing |

## Process

### Step 1: Channel Discovery
- Search YouTube Data API for channels matching keywords
- Filter by subscriber count and video count
- Rank by authority metrics

### Step 2: Video Selection
- Get uploads playlist for each channel
- Filter by view count and duration (min 5 minutes)
- Select top-performing educational content

### Step 3: Transcript Retrieval
- Try Supadata API first (fast, reliable)
- Fall back to TranscriptAPI if needed
- Final fallback to youtube-transcript-api (free, may be rate limited)

### Step 4: Manual Generation
- Send transcript to Claude/Gemini
- Generate structured how-to format:
  - Executive Summary
  - Key Concepts
  - Step-by-Step Process
  - Best Practices
  - Common Mistakes
  - Tools/Resources Mentioned
  - Actionable Takeaways
  - Skill Rating (1-10)

### Step 5: Quality Filtering
- AI rates each manual 1-10
- Filter by minimum rating (default: 7)
- Rank by potential automation value

### Step 6: Skill Bible Synthesis
- Combine multiple high-quality manuals
- Generate comprehensive skill bible
- Save to skills/ directory

## Outputs

```
.tmp/knowledge_mine/
├── channels.json           # Found channels
├── videos.json            # Selected videos
├── manuals/               # Individual how-to manuals
│   ├── video_title_1.md
│   └── video_title_2.md
├── manuals_index.json     # Manual metadata with ratings
└── SKILL_BIBLE_*.md       # Generated skill bible
```

## Quality Gates

- [ ] Found at least 3 qualifying channels
- [ ] Processed at least 5 videos successfully
- [ ] At least 3 manuals rated 7+
- [ ] Skill bible generated and saved

## Cost Estimates

| Component | Cost per Video |
|-----------|---------------|
| YouTube Data API | Free (10K quota/day) |
| Supadata transcript | ~$0.01 (1 credit) |
| TranscriptAPI | ~$0.005 (1 credit) |
| Claude manual generation | ~$0.03/video |
| Gemini (alternative) | ~$0.001/video |

**Typical run (10 channels, 5 videos each):**
- 50 videos
- Supadata: ~$0.50
- Claude: ~$1.50
- **Total: ~$2.00**

## Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your_key        # Claude via OpenRouter

# Transcript APIs (at least one recommended)
SUPADATA_API_KEY=your_key          # supadata.ai
TRANSCRIPTAPI_KEY=your_key         # transcriptapi.com

# Optional
GOOGLE_API_KEY=your_key            # Gemini (--use-gemini flag)
```

## Related Workflows

- `youtube_channel_finder.md` - Just find channels
- `full_campaign_pipeline.md` - Use skill bibles in campaigns
- `youtube_to_campaign_pipeline.md` - Complete automation
