# YouTube Channel Finder

## What This Workflow Is

A comprehensive YouTube channel discovery system that searches by keywords, scrapes channel data, and filters by engagement metrics (subscribers, views, video count) to identify top-performing channels in any niche. Perfect for finding influencers, competitors, Dream 100 prospects, or content research.

## What It Does

1. Searches YouTube for channels matching your keywords
2. Scrapes detailed channel information (subscribers, verified status, descriptions)
3. Filters and ranks channels by your criteria
4. Exports structured data for outreach or analysis (JSON and CSV)

## Prerequisites

**Required API Keys:**
- `SERPAPI_API_KEY` - For YouTube search (get from serpapi.com)

**Installation:**
```bash
pip install requests python-dotenv
```

**Required Skill Bibles:**
- `SKILL_BIBLE_youtube_lead_generation.md`
- `SKILL_BIBLE_dream_100_strategy.md`

## How to Run

```bash
# Basic search - find channels about a topic
python3 execution/scrape_youtube_channels.py \
  --keywords "email marketing agency" \
  --max-results 50

# Advanced search with filters
python3 execution/scrape_youtube_channels.py \
  --keywords "cold email outreach" "lead generation tips" \
  --min-subscribers 10000 \
  --max-subscribers 500000 \
  --min-videos 20 \
  --sort-by subscribers \
  --max-results 100

# Search with location/language filters
python3 execution/scrape_youtube_channels.py \
  --keywords "marketing agency" \
  --language en \
  --country US \
  --max-results 50

# Export to CSV for outreach
python3 execution/scrape_youtube_channels.py \
  --keywords "SMMA" "agency owner" \
  --min-subscribers 5000 \
  --output-format csv \
  --max-results 100
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `--keywords` | string(s) | Yes | Search terms to find channels (can provide multiple) |
| `--max-results` | int | No | Maximum channels to return (default: 50) |
| `--min-subscribers` | int | No | Minimum subscriber count filter |
| `--max-subscribers` | int | No | Maximum subscriber count filter |
| `--min-videos` | int | No | Minimum video count filter |
| `--min-views` | int | No | Minimum total view count filter |
| `--sort-by` | string | No | Sort by: subscribers, views, videos, relevance (default: relevance) |
| `--language` | string | No | Filter by language (e.g., en, es, de) |
| `--country` | string | No | Filter by country code (e.g., US, UK, CA) |
| `--output-format` | string | No | Output format: json, csv, both (default: json) |
| `--output-prefix` | string | No | Custom prefix for output filename |

## Process

### Step 1: Keyword Search
- Takes your keywords and searches YouTube
- Uses Apify's YouTube scraper to find matching channels
- Respects language and country filters if provided

### Step 2: Channel Data Extraction
For each channel found, extracts:
- Channel name and handle (@username)
- Channel URL
- Subscriber count
- Total view count
- Video count
- Channel description
- Join date
- Profile image URL
- Banner image URL
- Recent video performance

### Step 3: Filtering
Applies your filters:
- Subscriber range (min/max)
- Minimum video count
- Minimum total views
- Removes duplicates

### Step 4: Ranking & Sorting
Sorts results by your chosen metric:
- `subscribers` - Largest channels first
- `views` - Most viewed channels first
- `videos` - Most prolific creators first
- `relevance` - YouTube's relevance ranking

### Step 5: Export
Saves results to:
- `.tmp/youtube_channels_<timestamp>.json` - Full data
- `.tmp/youtube_channels_<timestamp>.csv` - Spreadsheet format (if requested)

## Output Format

### JSON Output
```json
{
  "search_params": {
    "keywords": ["email marketing agency"],
    "filters": {
      "min_subscribers": 10000,
      "max_subscribers": 500000
    }
  },
  "total_found": 47,
  "channels": [
    {
      "channel_name": "Alex Hormozi",
      "channel_handle": "@AlexHormozi",
      "channel_url": "https://youtube.com/@AlexHormozi",
      "channel_id": "UCE7-H4IhwZHwzxh_5RmXCkQ",
      "subscribers": 2890000,
      "total_views": 245000000,
      "video_count": 487,
      "description": "Business tips and strategies...",
      "join_date": "2020-03-15",
      "profile_image": "https://...",
      "banner_image": "https://...",
      "country": "US",
      "recent_videos": [
        {
          "title": "How to Get Customers",
          "views": 1200000,
          "published": "2025-12-15"
        }
      ]
    }
  ]
}
```

### CSV Output Columns
- channel_name
- channel_handle
- channel_url
- subscribers
- total_views
- video_count
- description
- join_date
- country

## Quality Gates

- [ ] At least 1 keyword provided
- [ ] APIFY_API_TOKEN is set
- [ ] Results returned from Apify
- [ ] Filters applied correctly
- [ ] Output file created successfully
- [ ] No duplicate channels in results

## Use Cases

### Dream 100 Prospecting
Find influencers in your niche with engaged audiences:
```bash
python3 execution/scrape_youtube_channels.py \
  --keywords "agency owner" "marketing tips" \
  --min-subscribers 10000 \
  --max-subscribers 100000 \
  --min-videos 50 \
  --sort-by subscribers
```

### Competitor Research
Find competitors in your space:
```bash
python3 execution/scrape_youtube_channels.py \
  --keywords "cold email agency" "outbound marketing" \
  --min-subscribers 1000 \
  --sort-by views
```

### Content Research
Find top creators to study their content:
```bash
python3 execution/scrape_youtube_channels.py \
  --keywords "YouTube growth tips" \
  --min-subscribers 50000 \
  --sort-by views \
  --max-results 25
```

### Influencer Outreach List
Build a list of potential partners:
```bash
python3 execution/scrape_youtube_channels.py \
  --keywords "ecommerce" "Shopify" "dropshipping" \
  --min-subscribers 5000 \
  --max-subscribers 200000 \
  --output-format csv
```

## Edge Cases

- **No results found** → Try broader keywords or remove filters
- **Rate limiting** → Apify handles this, but large requests may take longer
- **Invalid channel data** → Script skips channels with missing critical data
- **Duplicate channels** → Automatically deduplicated by channel ID

## Related Directives

- `dream_100_instagram_personalized_dm_automation.md` - Outreach after finding channels
- `ai_prospect_researcher.md` - Deep research on specific creators
- `linkedin_lead_scraper.md` - Find creator's business profiles
- `youtube_script_creator.md` - Analyze top creators' content style

## Pricing

SerpAPI YouTube Search costs:
- 1 search credit per request
- Free tier: 100 searches/month
- Paid plans start at $75/month for 5,000 searches

Typical usage: Finding 50 channels uses 2-3 searches (~$0.03-0.05)
