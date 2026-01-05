# Competitor Monitoring Dashboard

## What This Workflow Is
This workflow monitors your competitors across web, social media, ads, and reviews, generating regular intelligence reports to help you identify opportunities and threats.

## What It Does
1. Tracks competitor website changes (pricing, features, messaging)
2. Monitors social media activity and engagement
3. Captures new ad creatives from Facebook Ad Library
4. Tracks keyword ranking changes
5. Aggregates reviews and sentiment across platforms
6. Generates weekly competitive intelligence reports

## Prerequisites

### Required API Keys (add to .env)
```
SEMRUSH_API_KEY=your_semrush_key          # Or AHREFS_API_KEY
OPENAI_API_KEY=your_openai_key            # For AI analysis
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- SEMrush or Ahrefs API access
- Web scraping capabilities

### Installation
```bash
pip install beautifulsoup4 requests openai google-api-python-client
```

## How to Run

### Step 1: Configure Competitors
Create `competitors.json`:
```json
{
  "competitors": [
    {"name": "Competitor A", "domain": "competitor-a.com", "social": "@competitor_a"},
    {"name": "Competitor B", "domain": "competitor-b.com", "social": "@competitor_b"}
  ]
}
```

### Step 2: Run Monitoring
```bash
python3 execution/monitor_competitors.py \
  --config competitors.json \
  --areas "website,social,ads,seo" \
  --output .tmp/competitor_data.json
```

### Step 3: Generate Report
```bash
python3 execution/generate_competitive_report.py \
  --data .tmp/competitor_data.json \
  --output .tmp/competitive_report.html
```

### Quick One-Liner
```bash
python3 execution/monitor_competitors.py --config competitors.json && \
python3 execution/generate_competitive_report.py --data .tmp/competitor_data.json
```

### Weekly Automated Report (Cron)
```bash
0 9 * * 1 cd /path/to/project && python3 execution/run_competitor_report.py --email "team@company.com"
```

## Goal
Track competitor activity across web, social, and ads to identify opportunities and threats.

## Inputs
- **Competitors**: List of competitor domains/brands
- **Monitor Areas**: Website, Social, Ads, SEO, Reviews
- **Alert Threshold**: What triggers notifications
- **Report Frequency**: Daily, Weekly

## Tools/Scripts
- `execution/monitor_competitors.py` - Data collection
- `execution/generate_competitive_report.py` - Report generation

## Process

### 1. Configure Monitoring
```bash
python3 execution/monitor_competitors.py \
  --competitors "competitor1.com,competitor2.com,competitor3.com" \
  --areas "website,social,ads,seo" \
  --output .tmp/competitor_data.json
```

### 2. Monitoring Areas

**Website Changes**
- New pages/features
- Pricing changes
- Messaging updates
- Team changes
- Blog posts

**Social Media**
- Post frequency
- Engagement rates
- Content themes
- Follower growth
- Viral content

**Advertising**
- New ad creatives
- Ad copy themes
- Targeting (inferred)
- Spend estimates
- Landing pages

**SEO**
- Keyword rankings
- New content
- Backlink changes
- Domain authority

**Reviews**
- G2, Capterra scores
- New reviews
- Common complaints
- Feature requests

### 3. Generate Dashboard
```bash
python3 execution/generate_competitive_report.py \
  --data .tmp/competitor_data.json \
  --output .tmp/competitive_report.html
```

### 4. Report Structure

```markdown
# Competitive Intelligence Report
**Period:** [Date Range]

## Executive Summary
[Key changes and opportunities]

## Competitor Overview
| Competitor | Traffic Est. | Social Followers | Review Score |
|------------|--------------|------------------|--------------|
| [Name 1] | [X] | [Y] | [Z] |
| [Name 2] | [X] | [Y] | [Z] |

## Website Changes

### [Competitor 1]
- 🆕 New pricing page launched
- 📝 Updated homepage messaging
- ➕ Added [feature] to product

### [Competitor 2]
- 💰 Raised prices by 15%
- 🏷️ New case study published

## Social Media Activity

### Top Performing Content
| Competitor | Post | Engagement |
|------------|------|------------|
| [Name] | [Post summary] | [X likes] |

### Content Themes This Week
- [Theme 1]: [X posts]
- [Theme 2]: [X posts]

## Advertising Intel

### New Ads Detected
[Screenshots/descriptions]

### Ad Copy Patterns
- [Pattern 1]
- [Pattern 2]

### Estimated Ad Spend
| Competitor | Est. Monthly Spend |
|------------|-------------------|
| [Name 1] | $X |
| [Name 2] | $X |

## SEO Changes

### Keyword Movement
| Keyword | You | Comp 1 | Comp 2 |
|---------|-----|--------|--------|
| [KW 1] | #X | #Y | #Z |

### New Content Published
- [Competitor]: [Article title]

## Review Sentiment

### Recent Reviews
⭐⭐⭐⭐⭐ "[Positive review quote]" - [Competitor]
⭐⭐ "[Negative review quote]" - [Competitor]

### Common Complaints
- [Competitor 1]: [Issue]
- [Competitor 2]: [Issue]

## Opportunities Identified
1. [Opportunity based on competitor weakness]
2. [Gap in competitor content/features]
3. [Underserved segment]

## Threats to Watch
⚠️ [Potential threat 1]
⚠️ [Potential threat 2]
```

### 5. Alerts
Trigger notifications for:
- Major pricing changes
- New feature launches
- Viral content
- Negative PR
- Key hire announcements

## Integrations Required
- Web scraping (changes detection)
- Social media APIs
- Facebook Ad Library
- SEO tools (Ahrefs, SEMrush)
- Review platforms APIs

## Cost Estimate
- SEO tools: $99-199/mo
- Social monitoring: $50-100/mo
- Custom scraping: ~$20/mo

## Automation
- Daily data collection
- Weekly summary reports
- Real-time alerts for major changes
