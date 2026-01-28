# Ultimate Local Newsletter Generator

## What This Workflow Is
A fully automated local newsletter workflow that scrapes events and news from local sources (Instagram, Facebook, web aggregators), deduplicates content, and generates ready-to-publish newsletters on autopilot. Based on Aniket Panjwani's local newsletter automation methodology.

## What It Does
1. Scrapes local events from Instagram profiles, Facebook event URLs, and web aggregators
2. Researches events via Perplexity AI with compelling descriptions and ticket links
3. Deduplicates events using fuzzy matching
4. Stores events in SQLite database for tracking
5. Fetches location header images from Unsplash
6. Generates beautiful email-ready HTML newsletters with:
   - Location header image with dark overlay
   - Inter font typography
   - Event descriptions written as ad copy
   - Direct ticket/registration links for each event
   - Price badges and "Get Tickets" buttons
7. Publishes directly to ConvertKit/Kit as draft or sends immediately

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_key           # For AI content generation
SCRAPECREATORS_API_KEY=your_key       # For Instagram scraping (scrapecreators.com)
FIRECRAWL_API_KEY=your_key            # For web aggregator scraping (firecrawl.dev)
PERPLEXITY_API_KEY=your_key           # For local event research with descriptions
UNSPLASH_ACCESS_KEY=your_key          # For header images (unsplash.com/developers)
CONVERTKIT_API_KEY=your_key           # For newsletter publishing (kit.com)
```

### Required Tools
- Python 3.10+
- requests, beautifulsoup4, rapidfuzz (deduplication)
- SQLite (built-in)

### Installation
```bash
pip install requests beautifulsoup4 rapidfuzz python-dotenv jinja2
```

## How to Run

### Quick Start (One Command)
```bash
python3 execution/generate_local_newsletter.py \
  --location "Austin, TX" \
  --instagram "@austin_events,@do512,@austinfoodie" \
  --web-sources "https://do512.com/events,https://austin.culturemap.com/events" \
  --newsletter-name "Austin Weekly" \
  --days 7
```

### Step-by-Step Process

#### Step 1: Setup Sources Configuration
```bash
python3 execution/generate_local_newsletter.py \
  --setup \
  --location "Austin, TX"
```
This creates a `config/local_newsletter_sources.yaml` file.

#### Step 2: Research & Scrape Events
```bash
python3 execution/generate_local_newsletter.py \
  --research \
  --location "Austin, TX"
```

#### Step 3: Generate Newsletter
```bash
python3 execution/generate_local_newsletter.py \
  --write \
  --location "Austin, TX" \
  --newsletter-name "Austin Weekly"
```

#### Step 4: Full Automation Run
```bash
python3 execution/generate_local_newsletter.py \
  --full-run \
  --location "Austin, TX"
```

### Weekly Automation (Cron)
```bash
# Every Tuesday at 8am - scrape and generate newsletter
0 8 * * 2 cd /path/to/project && python3 execution/generate_local_newsletter.py --full-run --location "Austin, TX"
```

## Goal
Generate hyper-local newsletters that aggregate events from multiple sources, providing value to local communities while requiring minimal manual effort.

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| location | string | Yes | City/area (e.g., "Austin, TX") |
| instagram | string | No | Comma-separated Instagram handles |
| web-sources | string | No | Comma-separated event website URLs |
| facebook-urls | string | No | Direct Facebook event URLs |
| newsletter-name | string | No | Name of newsletter |
| days | int | No | Days ahead to look for events (default: 7) |
| template | string | No | Newsletter template style |

## Process

### Phase 1: Source Configuration

1. **Define Location**
   - City/metro area
   - Neighborhoods to cover
   - Event radius (if applicable)

2. **Configure Sources**
   ```yaml
   # config/local_newsletter_sources.yaml
   location: "Austin, TX"
   
   instagram:
     - handle: "@do512"
       category: "events"
       priority: high
     - handle: "@austin_events"
       category: "events"
       priority: medium
     - handle: "@austinfoodie"
       category: "food"
       priority: medium
   
   web_aggregators:
     - url: "https://do512.com/events"
       name: "Do512"
       discovery_method: "crawl"
       category: "events"
     - url: "https://austin.culturemap.com/events"
       name: "CultureMap"
       discovery_method: "scrape"
   
   facebook_events: []  # Add specific event URLs as needed
   
   newsletter:
     name: "Austin Weekly"
     frequency: "weekly"
     sections:
       - "Featured Events"
       - "Music & Nightlife"
       - "Food & Drink"
       - "Arts & Culture"
       - "Family-Friendly"
       - "Free Events"
   ```

### Phase 2: Event Research & Scraping

1. **Perplexity AI Research** (Primary Source)
   - Query: "Find all events in [LOCATION] from [START_DATE] to [END_DATE]"
   - Request: Event name, date/time, venue, price, ticket URL, compelling description
   - Perplexity searches the web and returns current, verified events
   - This is the most reliable source for descriptions and URLs

2. **Instagram Scraping** (via ScrapeCreators API)
   - Fetch recent posts from configured profiles
   - Extract event details from captions
   - Parse dates, times, locations
   - Best for: Local venue accounts, event promoters

3. **Web Aggregator Scraping** (via Firecrawl)
   - Map: Get list of event URLs from sites like do512.com
   - Scrape: Get full content from each URL
   - Extract: Parse event structured data
   - Note: Can be slow, use as supplementary source

4. **URL Enrichment**
   - Events missing `source_url` get auto-enriched
   - Lookup table for common venues/events:
     ```python
     url_mappings = {
         "free week": "https://do512.com/p/free-week",
         "sxsw": "https://www.sxsw.com",
         "acl": "https://www.aclfestival.com",
         "stubbs": "https://stubbsaustin.com",
         "mohawk": "https://mohawkaustin.com",
         # Add your city's common venues
     }
     ```
   - Fallback: Generate do512 search URL

5. **Deduplication**
   - Fuzzy match event names (rapidfuzz, 85% threshold)
   - Match by venue + date
   - Keep entry with best description/URL

### Phase 3: Event Storage

SQLite database schema:
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    unique_key TEXT UNIQUE,  -- hash of normalized title + date + venue
    title TEXT,
    description TEXT,
    date DATE,
    time TEXT,
    end_date DATE,
    venue TEXT,
    address TEXT,
    category TEXT,
    source TEXT,
    source_url TEXT,
    image_url TEXT,
    price TEXT,
    is_free BOOLEAN,
    is_featured BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scraped_urls (
    url TEXT PRIMARY KEY,
    source TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Phase 4: Newsletter Generation

1. **Fetch Header Image**
   - Call Unsplash API with location query (e.g., "Austin skyline cityscape")
   - Get landscape-oriented image for email header
   - Cache image URL for reuse

2. **Query Events**
   - Filter by date range (next 7 days)
   - Group by category
   - Sort by date/priority

3. **Generate Content**
   - Write intro (AI-generated based on top events)
   - Each event gets:
     - Bold title with link to tickets/info
     - Date, time, and venue
     - **Compelling description written as ad copy** (2-3 sentences)
     - Price badge
     - "Get Tickets →" button

4. **Email HTML Template Structure**

```html
<!-- Header with Location Image -->
<td style="background: linear-gradient(rgba(30,30,30,0.6), rgba(30,30,30,0.6)), 
           url('[UNSPLASH_IMAGE]'); background-size: cover;">
    <h1 style="font-family: 'Inter'; color: #fff;">[NEWSLETTER_NAME]</h1>
    <p>[DATE_RANGE] • [LOCATION]</p>
</td>

<!-- Intro Section -->
<p style="font-size: 26px; font-weight: 700;">Hey [CITY] locals! 👋</p>
<p>[AI_GENERATED_INTRO]</p>

<!-- Category Sections with Color-Coded Headers -->
<!-- Each event card includes: -->
<div>
    <p><a href="[EVENT_URL]">[EVENT_TITLE]</a></p>
    <p>📅 [DATE] • [TIME] • 📍 [VENUE]</p>
    <p>[AD_COPY_DESCRIPTION - sells the event, describes the vibe]</p>
    <span>[PRICE]</span>
    <a href="[EVENT_URL]">Get Tickets →</a>
</div>

<!-- Footer with Share CTA -->
<p>Enjoying [NEWSLETTER_NAME]? Forward to a friend!</p>
```

5. **Event Description Guidelines**
   
   Each event description should:
   - **Sell the experience** - What will attendees feel/enjoy?
   - **Be specific** - Mention unique aspects, not generic phrases
   - **Create urgency** - Why attend THIS event?
   - **Include atmosphere** - Describe the vibe, energy, crowd
   
   **Good Example:**
   > "Experience Austin's legendary free music festival featuring 100+ local bands across downtown venues. From indie rock to hip-hop, discover your new favorite artist while hopping between iconic clubs like Mohawk and Stubb's. The streets come alive with music lovers enjoying the best of Austin's independent music scene."
   
   **Bad Example:**
   > "A music festival happening downtown with various bands performing."

6. **Required Event Fields for Quality Output**
   - `title` - Event name
   - `date` - YYYY-MM-DD format
   - `time` - Start time (optional)
   - `venue` - Venue name
   - `description` - 2-3 sentence ad copy
   - `price` - Dollar amount or "Free"
   - `source_url` - Ticket/registration link
   - `category` - For section grouping

### Phase 5: Output & Delivery

1. **Generate Outputs**
   - Markdown file for review
   - HTML for email platforms
   - JSON for API integrations

2. **Platform Integration**
   - Beehiiv-ready HTML
   - ConvertKit-compatible format
   - Raw markdown for manual editing

## Quality Gates

- [ ] Events have valid dates (not in past)
- [ ] No duplicate events in final output
- [ ] All required fields present (title, date, venue)
- [ ] Links are valid and working
- [ ] Categories properly assigned
- [ ] Word count appropriate for email

## Newsletter Types

### Weekly Digest (Default)
- All events for upcoming 7 days
- Full descriptions for featured
- Table format for others

### Weekend Preview
- Friday-Sunday events only
- More editorial commentary
- Shorter, more curated

### Daily Brief
- Events for next 24-48 hours
- Very short format
- Quick scanning

### Monthly Overview
- High-level preview
- Major events only
- Planning-focused

## Monetization Ideas

1. **Sponsorship Sections**
   - "Sponsored Event of the Week"
   - Banner ads between sections

2. **Affiliate Links**
   - Ticket platforms (Eventbrite, etc.)
   - Restaurant reservations

3. **Premium Tier**
   - Early access
   - Exclusive events
   - Discounts

## Edge Cases

| Scenario | Solution |
|----------|----------|
| No events found | Show message, suggest sources |
| Duplicate from multiple sources | Fuzzy dedup, keep best details |
| Event in past | Filter out in query |
| Missing date | Attempt parse, or exclude |
| Instagram API rate limit | Cache results, exponential backoff |
| Web scraping blocked | Rotate user agents, use Firecrawl |

## Automation Tips

### Full Autopilot Setup
1. Configure sources once
2. Set up cron job for weekly runs
3. Output to draft folder
4. Quick human review (5 min)
5. Schedule send in email platform

### Semi-Automated
1. Run research weekly
2. Human curates featured events
3. AI generates newsletter draft
4. Human edits and sends

## Related Directives
- `directives/newsletter_writer.md` - General newsletter framework
- `directives/ultimate_content_calendar.md` - Content planning

## Related Skill Bibles
- `skills/SKILL_BIBLE_sturtevant_email_master_system.md` - Email best practices
- `skills/SKILL_BIBLE_local_seo.md` - Local audience understanding

## ConvertKit / Kit Integration

### API Publishing
```bash
# Create as draft in ConvertKit
python3 execution/generate_local_newsletter.py \
  --location "Austin, TX" \
  --publish \
  --publish-status draft

# Send immediately to all subscribers
python3 execution/generate_local_newsletter.py \
  --location "Austin, TX" \
  --publish \
  --publish-status send
```

### Required Environment Variables
```
CONVERTKIT_API_KEY=kit_xxxxx
```

### Full Automation Example
```bash
# Weekly cron job - creates draft every Tuesday at 8am
0 8 * * 2 cd /path/to/project && python3 execution/generate_local_newsletter.py \
  --full-run --location "Austin, TX" --publish --publish-status draft
```

## External Resources
- [Aniket Panjwani's local_media_tools](https://github.com/aniketpanjwani/local_media_tools) - Reference implementation
- [ScrapeCreators API](https://scrapecreators.com/) - Instagram scraping
- [Firecrawl](https://firecrawl.dev/) - Web scraping API
- [ConvertKit/Kit API Docs](https://developers.kit.com/) - Newsletter publishing API
