# Yelp + Trustpilot Review Scraper

## What This Workflow Is
This workflow scrapes reviews from Yelp and Trustpilot to identify businesses with pain points that match your solution for targeted outreach.

## What It Does
1. Scrapes reviews by category/keyword
2. Analyzes for pain points
3. Identifies negative review patterns
4. Extracts business contact info
5. Prioritizes outreach targets

## Prerequisites

### Required API Keys (add to .env)
```
APIFY_API_TOKEN=your_apify_token
OPENAI_API_KEY=your_openai_key
```

### Installation
```bash
pip install apify-client openai
```

## How to Run
```bash
python3 execution/scrape_reviews.py --platform yelp --category "restaurants" --city "Austin"
```

## Goal
Scrape reviews from Yelp and Trustpilot to find businesses with pain points for outreach.

## Inputs
- **Business Category**: Type to search
- **Location**: Geographic area
- **Review Keywords**: Pain points to find
- **Rating Filter**: Target rating range

## Process

### 1. Scrape Reviews
```bash
python3 execution/scrape_reviews.py \
  --platform yelp \
  --category "marketing agency" \
  --location "Los Angeles" \
  --keywords "slow,expensive,unresponsive" \
  --output .tmp/reviews.json
```

### 2. Data Collected
- Business name
- Website
- Phone
- Rating
- Review count
- Recent reviews (text)
- Common complaints

### 3. Pain Point Analysis
AI analyzes reviews for:
- Service complaints
- Speed issues
- Communication problems
- Price concerns
- Quality issues

### 4. Lead Scoring
| Signal | Score |
|--------|-------|
| Negative reviews mentioning your service area | +20 |
| Recent negative reviews (last 30 days) | +15 |
| Multiple reviews with same complaint | +10 |
| Business has website | +10 |

### 5. Output
```json
{
  "business_name": "ABC Marketing",
  "website": "abcmarketing.com",
  "yelp_rating": 3.2,
  "review_count": 45,
  "pain_points": [
    "Clients complain about slow turnaround",
    "Multiple reviews mention poor communication"
  ],
  "outreach_angle": "Speed and communication",
  "score": 75
}
```

### 6. Outreach Template
```
Subject: Noticed [COMPANY]'s reviews

Hi [NAME],

I was researching [INDUSTRY] agencies and noticed 
some of your reviews mention [PAIN POINT].

We actually specialize in solving that exact problem -
we help companies like yours [SOLUTION].

Would you be open to a quick chat about how we 
could help?
```

## Integrations
- Apify (scraping)
- OpenAI (analysis)
- Google Sheets

## Cost
- Scraping: ~$0.02/business
- Analysis: ~$0.01/business
