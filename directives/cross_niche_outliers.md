# Cross-Niche Outlier Detection (Dec 5, 2025)

## Goal
Identify high-performing videos from adjacent business niches to extract transferable content patterns, hooks, and structures. These outliers provide inspiration for content ideation without being directly competitive or overly technical.

## Two Approaches Available

### 1. TubeLab API (RECOMMENDED)
**Script:** `execution/scrape_cross_niche_tubelab.py`

Uses TubeLab's pre-built outlier database (4M+ videos). More reliable than yt-dlp.

**Pros:**
- Pre-calculated outlier scores (no channel average calculations needed)
- No rate limiting issues
- Fast and reliable

**Cons:**
- Costs 5 credits per query
- Limited to TubeLab's indexed videos

**Quick start:**
```bash
# Default: 1 query = 5 credits, ~100 outliers from last 30 days
python3 execution/scrape_cross_niche_tubelab.py

# Custom search term
python3 execution/scrape_cross_niche_tubelab.py --terms "business strategy"

# Multiple queries (uses more credits)
python3 execution/scrape_cross_niche_tubelab.py --queries 3 --terms "entrepreneur" "business" "productivity"

# Skip transcripts (faster, cheaper Claude costs)
python3 execution/scrape_cross_niche_tubelab.py --skip_transcripts
```

### 2. yt-dlp Scraping (LEGACY)
**Script:** `execution/scrape_cross_niche_outliers.py`

Direct YouTube scraping. Free but unreliable due to rate limiting.

**Pros:**
- Free (no API credits)
- Full control over channels and keywords

**Cons:**
- yt-dlp rate limiting causes 80%+ failures
- Slow (calculates channel averages manually)
- Unreliable results

**When to use:** Only if TubeLab credits are exhausted.

---

## Key Differences from `youtube_outliers.md`
- **youtube_outliers.md**: Monitors your core niche (AI agents, automation) for competitive intelligence
- **cross_niche_outliers.md**: Monitors broad business/productivity topics for content patterns and hooks
- Both generate 3 title variants per outlier adapted to your channel

## Prerequisites
- `TUBELAB_API_KEY` for TubeLab API (recommended approach)
- `ANTHROPIC_API_KEY` for Claude summaries and title variant generation
- `APIFY_API_TOKEN` for fallback transcript fetching (optional)
- OAuth credentials for Google Sheets (credentials.json + token.json)

## Tools/Scripts
- **Recommended:** [execution/scrape_cross_niche_tubelab.py](../execution/scrape_cross_niche_tubelab.py) (TubeLab API)
- **Legacy:** [execution/scrape_cross_niche_outliers.py](../execution/scrape_cross_niche_outliers.py) (yt-dlp)

## Keyword Strategy

### Tier 1: Adjacent Business/Tech (High Audience Overlap)
Focus: People interested in AI/automation but from business angle
- "AI for business"
- "ChatGPT business use cases"
- "automation tools for entrepreneurs"
- "no-code automation"
- "productivity AI tools"
- "business process automation"

### Tier 2: Broad Business Performance (Universal Patterns)
Focus: Proven content patterns from successful business creators
- "scale your business"
- "grow your startup"
- "solopreneur success"
- "founder productivity"
- "business systems that scale"
- "entrepreneur time management"

### Tier 3: Money/Revenue Hooks (High Engagement)
Focus: Financial triggers that work across niches
- "increase revenue"
- "passive income systems"
- "profitable business models"
- "10x your income"
- "business growth strategy"

### Tier 4: Personal Brand/Creator Economy
Focus: Content creation strategies that work
- "YouTube strategy"
- "content creation tips"
- "personal brand building"
- "creator monetization"

## Channel Monitoring (EXPANDED - 12 Channels)

In addition to keywords, monitor specific high-performing business channels:

**Tier S (Must Monitor):**
- Alex Hormozi - Business scaling, systems
- My First Million - Business ideas, trends
- Starter Story - Founder interviews, tactics

**Tier A (High Value):**
- Colin and Samir - Creator economy insights
- Ali Abdaal - Productivity, systems

**Tier B (Additional Sources):**
- Think Media - YouTube strategy
- Iman Gadzhi - Agency/entrepreneurship
- Pat Flynn - Online business
- GaryVee - Hustle/motivation content
- MrBeast - Viral hooks and storytelling
- Justin Welsh - Solopreneur/personal brand
- Charlie Morgan - High-ticket sales/agency

## Process

### 1. Video Discovery (UPDATED)
- Search each keyword (**50 videos per keyword**, configurable days back)
- Monitor listed channels (**last 15 videos per channel**, up from 10)
- Deduplicate by video ID
- Filter out noise (music, gaming, etc.)
- **Result: typically find 30-35 unique videos within 90-day window**

### 2. Outlier Scoring (UPDATED)
- Calculate outlier score: (video views / channel average views)
- Apply recency boost:
  - Videos <1 day old: 2.0x multiplier
  - Videos <3 days old: 1.5x multiplier
  - Videos <7 days old: 1.2x multiplier
- **Threshold: 1.1x or higher (10% above channel average)**
- **Target: ~20 outliers per run**

### 3. Cross-Niche Scoring
Add a second score to prioritize transferable content:

**Cross-Niche Potential Score = Base Score × Modifiers**

**Modifiers:**
- **-20% per technical term** (API, Python, code, framework, SDK)
- **+30% for money hooks** ($, revenue, income, profit, money)
- **+20% for time hooks** (faster, save time, productivity, efficient)
- **+20% for curiosity gaps** (?, "this changed everything", "nobody talks about")
- **+10% for listicles** (numbers in title: "7 ways", "3 secrets")

### 4. Transcript & Summary (2-TIER SYSTEM)
**Transcript Fetching:**
1. **Try youtube-transcript-api first** (free, fast)
   - Direct API call to YouTube
   - 1-second rate limit between requests
   - Retry once on 429 errors
2. **Fallback to Apify karamelo/youtube-transcripts** (free tier available)
   - Used when YouTube API fails or rate-limited
   - Reliable for most videos
   - ~20-30 seconds per video

**Summarization with Claude Sonnet 4.5:**
- Core hook/angle and why it works
- Key content structure or pattern
- How to adapt this for AI/automation content
- Brief and actionable (3-4 sentences)

**NEW: Raw Transcript Storage:**
- Full transcript saved to "Raw Transcript" column for deeper analysis
- Useful for finding exact hooks, quotes, and script structure

### 5. Title Variant Generation (NEW!)
For each outlier, Claude automatically generates 3 title variants:
- Analyzes original title's hook, emotional trigger, structure
- Adapts to your specific niche (AI agents, automation, LangGraph, CrewAI, etc.)
- Ensures variants are meaningfully different from each other
- Keeps under 100 characters (YouTube best practice)

### 6. Output to Google Sheet (19 COLUMNS)
Create new sheet with columns (sorted by publish date, most recent first):
1. **Cross-Niche Score** (transferability metric)
2. Outlier Score (with recency boost)
3. Raw Outlier Score (without recency boost)
4. Days Old
5. Content Category (auto-tagged: Money, Productivity, Creator, Business, AI/Tech, General)
6. Title (original)
7. Video Link
8. View Count
9. Duration (min)
10. Channel Name
11. Channel Avg Views
12. Thumbnail (IMAGE formula)
13. Summary (with pattern analysis)
14. **Title Variant 1** ⭐ NEW
15. **Title Variant 2** ⭐ NEW
16. **Title Variant 3** ⭐ NEW
17. **Raw Transcript** ⭐ NEW - Full transcript for deeper analysis
18. Publish Date
19. Source

## Execution

### Recommended Command (Default - Finds ~20 Outliers)
```bash
python3 execution/scrape_cross_niche_outliers.py
```
Uses default settings: 90 days, 1.1 min_score, all keywords+channels

### Fast Test Mode (Skip Transcripts)
```bash
python3 execution/scrape_cross_niche_outliers.py --skip_transcripts
```
Same outlier detection, but skips transcripts/summaries (10x faster)

### Keywords Only (No Channel Monitoring)
```bash
python3 execution/scrape_cross_niche_outliers.py --keywords_only
```
Faster but may find fewer outliers (~5-10 instead of ~20)

### All Options
- `--limit N`: Process only first N outliers (useful for testing)
- `--days N`: Look back N days (default: **90** - optimized for ~20 outliers)
- `--min_score X`: Minimum outlier score (default: **1.1** = 10% above average)
- `--keywords_only`: Skip channel monitoring (faster but fewer results)
- `--channels_only`: Skip keyword searches (channels only)
- `--skip_transcripts`: Skip transcript fetching and summarization (10x faster, no summaries/raw transcripts)

## Configuration

### Hardcoded in Script (UPDATED SETTINGS)
```python
# User's channel niche (UPDATE THIS to match your content)
USER_CHANNEL_NICHE = "AI agents, automation, LangGraph, CrewAI, agentic workflows"

# Thresholds (UPDATED for ~20 outliers)
MAX_VIDEOS_PER_KEYWORD = 50  # Up from 30
MAX_VIDEOS_PER_CHANNEL = 15  # Up from 10
DAYS_BACK = 90  # Up from 60 (3 months of data)
MIN_OUTLIER_SCORE = 1.1  # Down from 1.5 (10% above average)
MIN_VIDEO_DURATION_SECONDS = 180  # Filter out shorts
MIN_VIEW_COUNT = 1000  # Minimum views to consider

# Keywords
CROSS_NICHE_KEYWORDS = [17 business/productivity focused keywords]

# Channel IDs (EXPANDED to 12 channels)
BUSINESS_CHANNELS = {
    "UCMrnHNmYzP3LgvKzyq0ILgw": "Alex Hormozi",
    "UCwgz-59Z39I8-ZrrHjy6nKw": "My First Million",
    "UC6vIIrBduMs-M_xCD1glYKA": "Starter Story",
    "UCWsV__V0nANOeXa1bWgN3Xw": "Colin and Samir",
    "UCoOae5nYA7VqaXzerajD0lg": "Ali Abdaal",
    "UCxJKUPx-EEUvk78sP2oItWQ": "Think Media",
    "UCyg6_Bvlx7vwhh_UOVJPqpQ": "Iman Gadzhi",
    "UCBseUxfzQNM5u5H-c67a5wg": "Pat Flynn",
    "UCL9ed3FYKf4zZKDt11nQo5w": "GaryVee",
    "UCX6OQ3DkcsbYNE6H8uQQuVA": "MrBeast",
    "UCbiGcwDWZjz05njNPrJU7jA": "Justin Welsh",
    "UCeVMnSShP_Iviwkknt83cww": "Charlie Morgan"
}

# Scoring modifiers
TECHNICAL_TERMS = ["API", "Python", "code", "SDK", ...]
MONEY_HOOKS = ["$", "revenue", "income", "profit", ...]
TIME_HOOKS = ["faster", "save time", "productivity", ...]
CURIOSITY_HOOKS = ["?", "secret", "nobody", ...]
```

## Use Cases

### 1. Content Calendar Planning
- Review top 10 cross-niche outliers weekly
- Use the 3 title variants as starting points for your videos
- Adapt the content structure and hooks to your niche

### 2. Title A/B Testing
- Use generated title variants to A/B test on your channel
- Each variant preserves the hook but varies the angle
- Pick the one that resonates most with your audience

### 3. Hook Research
- Study high-performing thumbnails
- Analyze opening lines from transcripts (if available)
- Build swipe file of proven patterns

### 4. Format Inspiration
- Notice what structures work (listicles, case studies, contrarian takes)
- Identify emerging content trends before they hit your niche

## Edge Cases & Troubleshooting

### Getting Fewer Than ~20 Outliers?
**Current default settings are optimized to find ~20 outliers.** If you're getting fewer:
1. **Increase lookback window**: `--days 120` or `--days 180` (4-6 months)
2. **Lower threshold**: `--min_score 1.05` (5% above average)
3. **Check that you're not using `--keywords_only`** (use full mode with channels)

### Getting Too Many Outliers?
If you want to be more selective:
1. **Raise threshold**: `--min_score 1.2` or `--min_score 1.3`
2. **Shorten lookback**: `--days 60` or `--days 30`
3. Review cross-niche scores - top 10-15 are usually the most transferable

### Transcript Errors
- **2-tier system handles most failures gracefully**
- youtube-transcript-api tries first, Apify fallback second
- If both fail, summary will be "No transcript available"
- Title variants still generated from title alone
- Use `--skip_transcripts` to speed up runs if you don't need summaries/transcripts

### yt-dlp Timeouts
- Some keywords may timeout (acquisition.com, scaling without burnout, etc.)
- Some channels may timeout (Pat Flynn, GaryVee, Iman Gadzhi sometimes)
- Script continues with remaining keywords/channels
- This is normal and expected - you'll still get ~20 outliers

### Other Issues
- **Viral but irrelevant**: If score >5x, may be celebrity/news-driven (check cross-niche score)
- **Seasonal content**: Holiday/event-driven outliers may not be evergreen
- **Duplicate videos**: Automatically handled by deduplication logic
- **Low quality outliers**: Sort by cross-niche score - top results are most transferable

## Output (Deliverable)
- **Google Sheet**: "Cross-Niche Outliers v2 - [timestamp]"
- **~100 outliers** with 19 columns per row
- Sorted by publish date (most recent first)
- Includes 3 title variants + raw transcript per outlier
- No local files (intermediate data in `.tmp/`)

## Cost & Time Estimates

### TubeLab API (Recommended)
- **Per Query**: 5 TubeLab credits
- **Default Run**: 1 query = 5 credits → ~100 outliers from last 30 days
- **Claude Costs**: ~$0.15-0.25 per outlier (summary + 3 title variants)
- **Time**: ~5-10 minutes for full run with transcripts
- **Fast mode** (`--skip_transcripts`): ~30 seconds

### yt-dlp (Legacy)
- **TubeLab Credits**: None (free)
- **Claude Costs**: ~$0.15-0.25 per outlier
- **Time**: 15-25 minutes (often fails due to rate limiting)

**Recommended Frequency**: Weekly

## TubeLab API Options

| Flag | Description | Default |
|------|-------------|---------|
| `--queries N` | Number of search queries (5 credits each) | 1 |
| `--terms "a" "b"` | Custom search terms | entrepreneur |
| `--size N` | Results per query | 100 |
| `--min_views N` | Minimum view count | 10,000 |
| `--max_days N` | Max video age in days | 30 (last month) |
| `--min_score X` | Minimum cross-niche score after filtering | 1.5 |
| `--limit N` | Max outliers to process | None |
| `--skip_transcripts` | Skip transcript/summary (faster, cheaper) | False |
| `--workers N` | Parallel workers for content processing | 3 |

**API Features:**
- **Server-side date filtering**: Uses `publishedAtFrom` parameter (ISO 8601 format)
- **English-only results**: `language=en` filter enabled by default
- **Sorted by date**: Most recent videos appear first in the output sheet

## Recent Improvements

### Dec 5, 2025 - API Optimization
**Changes:**
- Default to 1 query (was 3) - single "entrepreneur" keyword for broad coverage
- Server-side date filtering with `publishedAtFrom` parameter (ISO 8601)
- English-only filter (`language=en`) enabled by default
- Results sorted by publish date (most recent first)
- Default 30-day lookback (was 365) for fresher content
- 100 results per query (was 1000)

### Dec 5, 2025 - TubeLab Integration
**Problem Solved**: yt-dlp rate limiting causing 80%+ failures

**Solution**: New TubeLab API-based script that:
- Uses pre-calculated outlier scores from TubeLab's 4M+ video database
- No rate limiting issues
- Faster execution (2-5 min vs 15-25 min)
- Same cross-niche filtering and title variant generation

### Nov 24, 2025 - yt-dlp Version Improvements
- Optimized settings for ~20 outliers
- Expanded to 45+ monitored channels across 8 niches
- Comprehensive exclusion filters (100+ patterns)
- 2-tier transcript system with Apify fallback

## Workflow Integration

### Reading the Output Sheet
The script outputs to Google Sheets. To work with the data:
- Use `gspread` to read the sheet programmatically
- Key columns for downstream use:
  - **Thumbnail URL** (column F): Raw highres URL for face-swapping
  - **Title Variant 1-3**: Pre-generated titles adapted to your niche
  - **Video Link**: YouTube URL for reference

### Thumbnail Recreation
After finding outliers, generate face-swapped thumbnails using [recreate_thumbnails.md](recreate_thumbnails.md):

```bash
# Generate 3 variations from an outlier's thumbnail
python3 execution/recreate_thumbnails.py --source "THUMBNAIL_URL"

# Or from the YouTube video directly
python3 execution/recreate_thumbnails.py --youtube "VIDEO_LINK"

# Then edit as needed
python3 execution/recreate_thumbnails.py --edit ".tmp/thumbnails/20251205/123456_1.png" \
  --prompt "Change text to 'TITLE_VARIANT_1'. Update colors to teal."
```

### Typical Workflow
1. Run cross-niche outliers → get sheet with ~100 outliers (sorted by date)
2. Review recent outliers, filter by Cross-Niche Score if desired
3. Pick one with a good thumbnail and title variant
4. Run thumbnail recreation with that thumbnail URL
5. Edit with your chosen title variant
6. Use the generated thumbnail for your video

## Notes
- **Run this WEEKLY** for content planning (~100 outliers per run)
- **Run youtube_outliers.md DAILY** for competitive monitoring
- Best used together: niche intel + broad inspiration
- Title variants are automatically adapted to your specific channel niche (USER_CHANNEL_NICHE)
- Update USER_CHANNEL_NICHE in the script to match your content focus
- **Default: last 30 days, English-only** - use `--max_days 90` for more historical data
- Use raw transcripts to study exact hooks, opening lines, and script structure
