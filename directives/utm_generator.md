# UTM Link Generator + Tracker

## What This Workflow Is
This workflow generates consistent UTM-tagged links following naming conventions and tracks campaign performance in a central sheet.

## What It Does
1. Takes campaign parameters
2. Generates UTM link with naming conventions
3. Creates short link (optional)
4. Logs to tracking sheet
5. Enables attribution tracking

## Prerequisites

### Required API Keys (add to .env)
```
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
BITLY_API_KEY=your_bitly_key              # Optional for short links
```

### Installation
```bash
pip install gspread google-auth requests
```

## How to Run
```bash
python3 execution/generate_utm.py --url "[BASE_URL]" --source "linkedin" --medium "social" --campaign "[NAME]"
```

## Goal
Generate consistent UTM-tagged links and track campaign performance.

## Inputs
- **Base URL**: Landing page URL
- **Campaign Name**: What you're promoting
- **Source**: Where traffic comes from
- **Medium**: Type of channel
- **Content**: Specific ad/post variation

## Process

### 1. Generate UTM Links
```bash
python3 execution/generate_utm.py \
  --url "https://example.com/landing" \
  --campaign "summer_sale" \
  --source "facebook" \
  --medium "paid_social" \
  --content "video_ad_v1" \
  --output .tmp/utm_links.json
```

### 2. UTM Parameter Standards
```
utm_source: Traffic source (facebook, google, email)
utm_medium: Channel type (cpc, email, social)
utm_campaign: Campaign name (summer_sale_2024)
utm_content: Ad/content variation (video_v1)
utm_term: Keyword (optional, for search)
```

### 3. Naming Convention
```
utm_source: lowercase, no spaces (facebook, linkedin)
utm_medium: standardized (paid_social, organic_social, email)
utm_campaign: date_name (2024_01_summer_sale)
utm_content: descriptive (carousel_testimonial_v2)
```

### 4. Output
```
Original: https://example.com/landing

Tagged: https://example.com/landing?utm_source=facebook&utm_medium=paid_social&utm_campaign=2024_01_summer_sale&utm_content=video_ad_v1

Short: https://yourl.ink/abc123 (optional)
```

### 5. Link Shortening (Optional)
- Bitly
- Rebrandly
- Custom short domain

### 6. Tracking Dashboard
```markdown
# UTM Performance Report

## By Campaign
| Campaign | Clicks | Conversions | CVR |
|----------|--------|-------------|-----|
| summer_sale | 5,000 | 250 | 5% |

## By Source
| Source | Clicks | Conv | Cost | CPA |
|--------|--------|------|------|-----|
| facebook | 3,000 | 150 | $500 | $3.33 |
| google | 2,000 | 100 | $400 | $4.00 |
```

### 7. Best Practices
- Be consistent with naming
- Use lowercase only
- No special characters
- Document all campaigns
- Shorten for social media

## Integrations
- Google Analytics
- URL shortener
- Spreadsheet tracking

## Cost
- Free (self-managed)
- Bitly: Free-$35/mo
