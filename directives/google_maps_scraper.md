# Google Maps Business Scraper

## What This Workflow Is
This workflow scrapes local business listings from Google Maps to build targeted lead lists for B2B outreach to local service providers, healthcare practices, restaurants, and other location-based businesses.

## What It Does
1. Searches Google Maps for businesses matching your category and location
2. Extracts business data (name, address, phone, website, rating, reviews)
3. Optionally scrapes emails from business websites
4. Enriches missing contact data using email finder APIs
5. Exports clean lead list to Google Sheets

## Prerequisites

### Required API Keys (add to .env)
```
APIFY_API_TOKEN=your_apify_token          # Get from console.apify.com
HUNTER_API_KEY=your_hunter_key            # Optional for email enrichment
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Google OAuth credentials (`credentials.json`)
- Active Apify account

### Installation
```bash
pip install apify-client google-api-python-client gspread beautifulsoup4
```

## How to Run

### Step 1: Define Your Search
Choose your target:
- Business category (e.g., "Plumbers", "Dentists", "Marketing Agencies")
- Location (e.g., "Miami, FL", "Austin, TX", "Los Angeles")
- Optional filters: minimum rating, minimum reviews

### Step 2: Test Scrape
```bash
python3 execution/scrape_google_maps.py \
  --query "Plumbers in Miami, FL" \
  --max_items 25 \
  --min_rating 4.0 \
  --output .tmp/test_gmaps.json
```

### Step 3: Full Scrape
```bash
python3 execution/scrape_google_maps.py \
  --query "Plumbers in Miami, FL" \
  --max_items 500 \
  --min_rating 4.0 \
  --output .tmp/gmaps_leads.json
```

### Step 4: Extract Emails from Websites
```bash
python3 execution/scrape_website_emails.py \
  .tmp/gmaps_leads.json \
  --output .tmp/gmaps_with_emails.json
```

### Step 5: Export to Google Sheets
```bash
python3 execution/update_sheet.py \
  .tmp/gmaps_with_emails.json \
  --title "GMaps Plumbers - Miami"
```

### Quick One-Liner
```bash
python3 execution/scrape_google_maps.py --query "Dentists in Austin, TX" --max_items 500 && \
python3 execution/scrape_website_emails.py .tmp/gmaps_leads.json && \
python3 execution/update_sheet.py .tmp/gmaps_with_emails.json --title "Dentists Austin"
```

## Goal
Scrape local businesses from Google Maps by category and location for B2B lead generation.

## Inputs
- **Business Category**: Type of business (e.g., "Plumbers", "Dentists", "Restaurants")
- **Location**: City, state, or region (e.g., "Miami, FL", "Los Angeles")
- **Lead Count**: Number of businesses to scrape
- **Filters**: Rating, reviews count, open now (optional)

## Tools/Scripts
- `execution/scrape_google_maps.py` - Google Maps scraper
- `execution/enrich_emails.py` - Email finder
- `execution/update_sheet.py` - Export to Sheets

## Process

### 1. Define Search Query
```bash
python3 execution/scrape_google_maps.py \
  --query "Plumbers in Miami, FL" \
  --max_items 500 \
  --min_rating 4.0
```

### 2. Test Scrape (25 businesses)
Verify:
- Correct business category
- Location accuracy
- Data quality (phone, website present)

### 3. Full Scrape
Run complete scrape with filters.

Output fields:
- Business Name
- Address
- Phone Number
- Website
- Rating
- Reviews Count
- Business Hours
- Google Maps URL

### 4. Website Email Extraction
For businesses with websites:
```bash
python3 execution/scrape_website_emails.py .tmp/gmaps_leads.json
```

### 5. Email Enrichment (if needed)
```bash
python3 execution/enrich_emails.py .tmp/gmaps_leads.json
```

### 6. Export to Google Sheets
```bash
python3 execution/update_sheet.py .tmp/enriched_leads.json --title "GMaps [CATEGORY] - [LOCATION]"
```

## Output Schema
| Column | Description |
|--------|-------------|
| business_name | Company name |
| address | Full address |
| city | City |
| state | State/Province |
| phone | Phone number |
| website | Business website |
| email | Contact email |
| rating | Google rating (1-5) |
| reviews | Number of reviews |
| gmaps_url | Google Maps link |

## Integrations Required
- Apify (Google Maps scraper)
- Google Sheets API

## Cost Estimate
- Apify: ~$0.01/business
- **500 leads: ~$5-10**

## Best Use Cases
- Local service businesses (plumbers, electricians, HVAC)
- Healthcare (dentists, chiropractors, clinics)
- Restaurants and hospitality
- Professional services (lawyers, accountants)
- Real estate agencies

## Edge Cases
- No website listed: Skip email extraction
- Duplicate listings: Dedupe by phone number
- Chain locations: Filter by "single location" if needed

## Pro Tips
- Scrape by ZIP code for granular targeting
- Filter by review count (>10 = established business)
- Use rating filter to target quality businesses
