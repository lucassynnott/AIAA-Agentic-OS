# Launch Cold Email Campaign

## What This Workflow Is
This is an end-to-end workflow that launches a complete cold email campaign: scraping leads, enriching emails, personalizing copy, and loading into Instantly or Smartlead.

## What It Does
1. Scrapes leads from target industry/location
2. Enriches with verified emails
3. Generates personalized first lines
4. Creates campaign in sending platform
5. Configures settings and launches

## Prerequisites

### Required API Keys (add to .env)
```
APIFY_API_TOKEN=your_apify_token          # For scraping
HUNTER_API_KEY=your_hunter_key            # For email enrichment
INSTANTLY_API_KEY=your_instantly_key      # Or SMARTLEAD_API_KEY
OPENAI_API_KEY=your_openai_key            # For personalization
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Warmed email infrastructure
- Sending platform account

### Installation
```bash
pip install apify-client openai requests google-api-python-client
```

## How to Run

### Full Pipeline (Recommended)
```bash
python3 execution/launch_campaign_pipeline.py \
  --industry "SaaS companies" \
  --location "United States" \
  --leads 500 \
  --service "Cold email automation" \
  --value_prop "Book 30+ meetings per month" \
  --platform instantly
```

### Step-by-Step

#### Phase 1: Lead Generation
```bash
python3 execution/scrape_apify.py --industry "SaaS" --location "US" --max_items 500
python3 execution/update_sheet.py .tmp/leads.json --title "SaaS Campaign"
python3 execution/enrich_emails.py "[SHEET_URL]"
```

#### Phase 2: Personalization
```bash
python3 execution/personalize_emails_ai.py --sheet "[SHEET_URL]" --service "Cold email automation"
```

#### Phase 3: Campaign Setup
```bash
python3 execution/instantly_create_campaigns.py \
  --csv .tmp/campaign_upload.csv \
  --campaign_name "SaaS - $(date +%Y-%m-%d)"
```

## Goal
End-to-end workflow to launch a cold email campaign: scrape leads, personalize emails, and load into sending platform (Instantly or Smartlead).

## Inputs
- **Industry**: Target industry (e.g., "SaaS companies", "Dental practices")
- **Location**: Geographic target (e.g., "United States", "London, UK")
- **Lead Count**: Number of leads to scrape (default: 500)
- **Service/Offer**: What you're selling
- **Value Proposition**: Key benefit/result
- **Sending Platform**: "instantly" or "smartlead"

## Prerequisites
- Cold email infrastructure set up (domains warmed, accounts ready)
- API keys configured: `APIFY_API_TOKEN`, `INSTANTLY_API_KEY` or `SMARTLEAD_API_KEY`
- Google OAuth configured for Sheets

## Process

### Phase 1: Lead Generation
Use `directives/scrape_leads.md` to build the lead list.

1. **Test Scrape** (25 leads)
   ```bash
   python3 execution/scrape_apify.py --industry "[INDUSTRY]" --location "[LOCATION]" --max_items 25 --no-email-filter
   ```

2. **Verify Quality**
   - Read `.tmp/test_leads.json`
   - Confirm 80%+ match target industry
   - If not, refine keywords with user

3. **Full Scrape**
   ```bash
   python3 execution/scrape_apify.py --industry "[INDUSTRY]" --location "[LOCATION]" --max_items [LEAD_COUNT] --no-email-filter
   ```

4. **Upload to Google Sheet**
   ```bash
   python3 execution/update_sheet.py .tmp/leads_[timestamp].json --title "[INDUSTRY] Leads - [DATE]"
   ```

5. **Enrich Emails**
   ```bash
   python3 execution/enrich_emails.py [SHEET_URL]
   ```

### Phase 2: Email Personalization
Use the Cold Email Mass Personalizer or Scriptwriter workflows.

6. **Generate Email Scripts**
   - If user provided specific angles: Use `directives/cold_email_scriptwriter.md`
   - For mass personalization: Use `directives/cold_email_mass_personalizer.md`
   
   Required inputs for script generation:
   - Service/Product: [SERVICE]
   - Value Proposition: [VALUE_PROP]
   - Lead data from Sheet

7. **Add Personalized First Lines**
   For each lead, generate a personalized opener based on:
   - Company website content
   - Recent news/LinkedIn activity
   - Role-specific pain points
   
   Output: Personalization columns added to Google Sheet

### Phase 3: Campaign Setup
8. **Prepare CSV for Upload**
   ```bash
   python3 execution/export_campaign_csv.py [SHEET_URL] --output .tmp/campaign_upload.csv
   ```
   
   CSV columns:
   - email
   - first_name
   - last_name
   - company_name
   - personalized_first_line
   - custom_variable_1 (industry-specific)

9. **Create Campaign in Sending Platform**
   
   **For Instantly:**
   ```bash
   python3 execution/instantly_create_campaigns.py \
     --csv .tmp/campaign_upload.csv \
     --campaign_name "[INDUSTRY] - [DATE]" \
     --subject_line "[SUBJECT]" \
     --email_body "[BODY with {{variables}}]"
   ```
   
   **For Smartlead:**
   ```bash
   python3 execution/smartlead_create_campaign.py \
     --csv .tmp/campaign_upload.csv \
     --campaign_name "[INDUSTRY] - [DATE]"
   ```

10. **Configure Campaign Settings**
    - Daily send limit: 40-50 per account
    - Send window: 8am-6pm recipient timezone
    - Follow-up sequence: 3 emails over 7 days
    - Stop on reply: Yes

### Phase 4: Launch & Monitor
11. **Pre-Launch Checklist**
    - [ ] Domain health verified (all green)
    - [ ] Test email sent to personal inbox
    - [ ] Unsubscribe link present
    - [ ] Reply tracking enabled
    - [ ] Bounce handling configured

12. **Launch Campaign**
    - Set status to "Active" in platform
    - First emails send within configured window

13. **Set Up Monitoring**
    - Use `directives/daily_campaign_reports_health_metrics_bounce_rate_alerts.md`
    - Alerts for: bounce rate >3%, reply rate spikes, domain issues

## Outputs
- Google Sheet with enriched leads: `[SHEET_URL]`
- Active campaign in sending platform
- Daily monitoring configured

## Timeline
- Phase 1 (Lead Gen): 15-30 minutes
- Phase 2 (Personalization): 10-20 minutes  
- Phase 3 (Campaign Setup): 10 minutes
- **Total: ~45-60 minutes to launch**

## Edge Cases
- **Low email enrichment rate (<50%)**: Consider different industry/better lead sources
- **Domain health issues**: Pause and warm up more before sending
- **High bounce rate (>5%)**: Stop campaign, verify email list quality
- **Platform API errors**: Check rate limits, retry with backoff

## Quick Launch Command
For experienced users who want to run the full pipeline:
```bash
python3 execution/launch_campaign_pipeline.py \
  --industry "SaaS companies" \
  --location "United States" \
  --leads 500 \
  --service "Cold email automation" \
  --value_prop "Book 30+ meetings per month" \
  --platform instantly
```
