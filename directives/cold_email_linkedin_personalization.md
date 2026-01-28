# Cold Email Campaign with LinkedIn Personalization

## What This Workflow Does
End-to-end cold email campaign creation:
1. Scrapes leads from target industry/location
2. Scrapes actual LinkedIn posts from each lead
3. Generates truly personalized first lines based on real post content
4. Creates campaign in Instantly with proper variable formatting
5. Uploads leads with all variables correctly mapped

## Prerequisites

### Required API Keys (add to .env)
```
APIFY_API_TOKEN=your_apify_token
INSTANTLY_API_KEY=your_instantly_v2_key
OPENROUTER_API_KEY=your_openrouter_key  # Or OPENAI_API_KEY or ANTHROPIC_API_KEY
```

### Required Tools
- Python 3.10+
- Apify account with credits (~$2-5 per 25 leads with LinkedIn scraping)
- Instantly account with API v2 key

### Pre-Flight Check
Before running, verify Apify credits at https://console.apify.com/billing
- Lead scraping: ~$0.50-1.00 for 25 leads
- LinkedIn scraping: ~$0.50-0.75 for 25 profiles
- **Minimum recommended: $2-3 per campaign**

### Installation
```bash
pip install apify-client openai requests python-dotenv anthropic
```

## Choose Your Approach

### Option A: Full Pipeline (Simple filters)
Use `cold_email_pipeline.py` for basic campaigns. Supports industry, location, and minimum employee count.

### Option B: Individual Scripts (Advanced filters)
Use the step-by-step scripts for precise targeting with employee ranges, revenue filters, seniority levels, and job titles.

---

## Option A: Quick Start (Full Pipeline)

Best for simple campaigns with basic filtering:

```bash
python3 execution/cold_email_pipeline.py \
  --industry "SaaS companies" \
  --location "San Francisco" \
  --employee_count 50 \
  --limit 25 \
  --campaign_name "SF SaaS Outreach - Jan 2026"
```

**Limitations:** Only supports minimum employee count, no revenue filter, no job title filter.

---

## Option B: Step-by-Step Process (Recommended)

Use individual scripts for precise targeting with full filter control.

### Step 1: Scrape Leads with Advanced Filters

**IMPORTANT: Location Filter Format**
The Apify actor requires specific location formats:
- `--contact_location` must be country or state level: `"california, us"`, `"united states"`, `"germany"`
- `--contact_city` for city-level filtering: `"San Francisco"`, `"New York"`

**Example: SaaS Founders in SF, 25-150 employees, $1M+ revenue**
```bash
python3 execution/scrape_leads_apify.py \
  --fetch_count 25 \
  --contact_job_title "CEO" "Founder" "Co-Founder" \
  --contact_location "california, us" \
  --contact_city "San Francisco" \
  --company_keywords "SaaS" \
  --seniority_level "founder" "c_suite" \
  --size "21-50" "51-100" "101-200" \
  --min_revenue "1M" \
  --output_prefix "sf_saas_founders"
```

**Available Size Ranges:**
`"1-10"`, `"11-20"`, `"21-50"`, `"51-100"`, `"101-200"`, `"201-500"`, `"501-1000"`, `"1001-2000"`, `"2001-5000"`, `"5001-10000"`

**Available Seniority Levels:**
`"founder"`, `"c_suite"`, `"partner"`, `"vp"`, `"head"`, `"director"`, `"manager"`, `"senior"`, `"entry"`

**Apify Actor:** `IoSHqwTR9YGhzccez` (Apollo-style lead scraper)

### Step 2: Scrape LinkedIn Posts + Generate First Lines
```bash
python3 execution/scrape_linkedin_posts_personalize.py \
  --input .tmp/leads/sf_saas.json \
  --output .tmp/leads/sf_saas_personalized.json \
  --posts_per_profile 5
```

**Apify Actor:** `supreme_coder/linkedin-post`

This script:
- Takes LinkedIn URLs from the leads
- Scrapes actual post content from each profile
- Uses Claude/GPT to write first lines that reference SPECIFIC content from their posts
- Outputs high-confidence (from posts) and medium-confidence (from headline) leads

### Step 3: Create Instantly Campaign
```bash
python3 execution/instantly_create_campaigns.py \
  --client_name "YourCompany" \
  --client_description "We help SaaS companies automate outbound" \
  --offers "Free audit|Demo call|Pilot program" \
  --dry_run
```

Or create manually in Instantly with these variables:
- `{{firstName}}` - Lead's first name
- `{{companyName}}` - Company name
- `{{icebreaker}}` - Personalized first line
- `{{personalization}}` - Same as icebreaker (built-in)
- `{{sendingAccountFirstName}}` - Your name (auto-filled)

### Step 4: Upload Leads to Campaign
```bash
python3 execution/upload_leads_instantly.py \
  --input .tmp/leads/sf_saas_personalized.json \
  --campaign_id "your-campaign-id" \
  --clean
```

**IMPORTANT Instantly API v2 Notes:**
- Use `campaign` field (NOT `campaign_id`) when adding leads
- Use `personalization` field for the `{{personalization}}` variable
- Custom variables go in `custom_variables` object
- Use PATCH endpoint to update existing leads' personalization
- If leads already exist, delete them first with `--clean` flag

## Variable Mapping Reference

| Template Variable | API Field | Notes |
|------------------|-----------|-------|
| `{{firstName}}` | `first_name` | Auto-mapped to `firstName` in payload |
| `{{lastName}}` | `last_name` | Auto-mapped to `lastName` in payload |
| `{{companyName}}` | `company_name` | Auto-mapped to `companyName` in payload |
| `{{personalization}}` | `personalization` | Top-level field, use PATCH to update |
| `{{icebreaker}}` | `custom_variables.icebreaker` | Custom variable in payload |
| `{{sendingAccountFirstName}}` | N/A | System variable, auto-filled |

## Email Template Best Practices

```html
<p>Hi {{firstName}},</p>

<p>{{icebreaker}}</p>

<p>We help companies like {{companyName}} [value prop].</p>

<p>Worth a quick chat?</p>

<p>{{sendingAccountFirstName}}</p>
```

**Key points:**
- Always start with `Hi {{firstName}},`
- Put `{{icebreaker}}` on its own line after greeting
- Reference `{{companyName}}` in the value prop
- Keep emails under 100 words
- End with soft CTA + `{{sendingAccountFirstName}}`

## Troubleshooting

### "Apify: By launching this job you will exceed your remaining usage"
Insufficient Apify credits. Check balance at https://console.apify.com/billing and add funds.
- Lead scraping (25 leads): ~$0.50-1.00
- LinkedIn scraping (25 profiles): ~$0.50-0.75
- **Recommended minimum: $2-3 per campaign**

### "Input is not valid: Field input.contact_location"
The Apify actor requires specific location formats:
- **Wrong:** `"San Francisco"`, `"SF"`, `"San Francisco, CA"`
- **Correct:** `"california, us"`, `"united states"`, `"new york, us"`

Use `--contact_city` for city-level filtering alongside `--contact_location` for state/country.

### "Personalization not showing"
The Instantly API v2 doesn't update `personalization` on POST for existing leads. Solutions:
1. Use `--clean` flag to delete existing leads first
2. Use PATCH endpoint to update: `upload_leads_instantly.py` handles this automatically

### "Variables showing as {{variable}}"
Variable names are case-sensitive. Ensure:
- Template uses `{{firstName}}` (camelCase)
- Lead data has matching field in payload

### "Leads not in campaign"
Use `campaign` field (not `campaign_id`) in API calls:
```python
payload = {
    "campaign": "campaign-uuid-here",  # Correct
    # "campaign_id": "...",  # Wrong - will be ignored
    "email": "...",
    ...
}
```

### "body/campaign_schedule/schedules/0/timezone must be equal to one of the allowed values"
Instantly requires specific timezone formats. Valid examples:
- **Correct:** `"America/Chicago"`, `"America/New_York"`, `"Europe/London"`, `"UTC"`
- **May fail:** `"America/Los_Angeles"` (use `"America/Chicago"` or `"US/Pacific"`)

## Output Files

- `.tmp/leads/[prefix]_[timestamp].json` - Raw scraped leads
- `.tmp/leads/[prefix]_[timestamp].csv` - CSV format for review
- `.tmp/leads/[prefix]_personalized.json` - Leads with personalized first lines

## Integrations
- **Apify**: Lead scraping (`IoSHqwTR9YGhzccez`), LinkedIn post scraping (`supreme_coder/linkedin-post`)
- **OpenRouter/OpenAI/Anthropic**: First line generation (Claude Sonnet or GPT-4o)
- **Instantly**: Campaign creation, lead upload (API v2)

## Cost Estimates
- Apify lead scraping: ~$0.02-0.04/lead
- LinkedIn post scraping: ~$0.02-0.03/profile
- LLM first lines: ~$0.001-0.005/lead
- **Total: ~$0.06-0.12/personalized lead**
- **25-lead campaign: ~$2-3 total**

## Performance Notes
- Lead scraping: ~2-5 min for 25 leads
- LinkedIn scraping: ~3-5 min for 25 profiles (batched)
- Personalization: ~30 sec for 25 leads
- Campaign creation + upload: ~30 sec
- **Total pipeline time: ~6-12 min for 25 leads**
