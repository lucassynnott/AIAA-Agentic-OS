# AI Prospect Research Agent

## What This Workflow Is
This workflow creates an AI research agent that automatically gathers intelligence on prospects and their companies, producing comprehensive dossiers for sales call preparation and personalized outreach.

## What It Does
1. Takes prospect name, company, and domain as inputs
2. Searches multiple data sources (web, LinkedIn, news, Crunchbase)
3. Synthesizes findings into a structured dossier
4. Identifies pain points, talking points, and potential objections
5. Outputs in JSON, Markdown, or Google Doc format

## Prerequisites

### Required API Keys (add to .env)
```
PERPLEXITY_API_KEY=your_perplexity_key    # For web research
OPENAI_API_KEY=your_openai_key            # For synthesis
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # For Google Docs output
```

### Required Tools
- Python 3.10+
- Perplexity API access (recommended) or OpenAI with browsing
- Google OAuth credentials (optional, for Docs output)

### Installation
```bash
pip install openai requests google-api-python-client beautifulsoup4
```

## How to Run

### Step 1: Research a Single Prospect
```bash
python3 execution/research_prospect_deep.py \
  --name "John Smith" \
  --company "Acme Corp" \
  --domain "acmecorp.com" \
  --output .tmp/dossier.json
```

### Step 2: Batch Research (Multiple Prospects)
```bash
python3 execution/research_prospect_deep.py \
  --input prospects.csv \
  --output_dir .tmp/dossiers/
```

### Step 3: Export to Google Doc (Optional)
```bash
python3 execution/export_to_gdoc.py \
  .tmp/dossier.json \
  --title "Dossier - John Smith - Acme Corp"
```

### Quick One-Liner
```bash
python3 execution/research_prospect_deep.py --name "Jane Doe" --company "TechCo" --domain "techco.com" --format markdown
```

### Batch Research from Sheet
```bash
python3 execution/read_sheet.py "[SHEET_URL]" -o .tmp/prospects.json && \
python3 execution/research_prospect_deep.py --input .tmp/prospects.json --output_dir .tmp/dossiers/
```

## Goal
Automatically research prospects and companies to generate comprehensive dossiers for sales prep.

## Inputs
- **Prospect Name**: Full name
- **Company Name**: Company they work at
- **Company Domain**: Website URL (optional)
- **LinkedIn URL**: Profile link (optional)

## Tools/Scripts
- `execution/research_prospect_deep.py` - Deep research agent
- `execution/web_scraper.py` - Website content extraction

## Process

### 1. Trigger Research
```bash
python3 execution/research_prospect_deep.py \
  --name "John Smith" \
  --company "Acme Corp" \
  --domain "acmecorp.com" \
  --output .tmp/dossier.json
```

### 2. Data Sources
The agent searches:
- Company website (About, Team, Blog)
- LinkedIn (profile, posts, activity)
- News (Google News, TechCrunch, etc.)
- Funding databases (Crunchbase)
- Job postings (LinkedIn, Indeed)
- Podcasts/interviews
- Social media

### 3. Dossier Structure

```markdown
# Prospect Dossier: [Name]

## Person Overview
- **Name**: John Smith
- **Title**: VP of Sales
- **Tenure**: 2 years at company
- **Previous**: Director of Sales at XYZ Corp
- **LinkedIn**: [URL]

## Company Overview
- **Company**: Acme Corp
- **Industry**: B2B SaaS
- **Size**: 50-100 employees
- **Funding**: Series A ($10M)
- **Founded**: 2019
- **HQ**: San Francisco, CA

## Recent News
- [Date] Announced partnership with BigCo
- [Date] Raised Series A from Top VC
- [Date] Launched new product feature

## Hiring Signals
- 3 open SDR positions
- Hiring VP of Marketing
- → Indicates growth mode

## Tech Stack
- CRM: Salesforce
- Marketing: HubSpot
- Outreach: Outreach.io

## Pain Points (Inferred)
1. Scaling sales team rapidly
2. Pipeline generation at scale
3. Sales/marketing alignment

## Talking Points
- Congrats on Series A
- Ask about SDR hiring challenges
- Reference their new product launch

## Potential Objections
- "We already use [competitor]"
- "Not a priority right now"
- "Budget locked for the year"
```

### 4. Output Formats
- **JSON**: For programmatic use
- **Markdown**: For human reading
- **Google Doc**: For team sharing

## Use Cases

### Pre-Call Research
Run before discovery calls to prepare relevant questions.

### Personalized Outreach
Use insights for email/LinkedIn personalization.

### Account Planning
Build account plans for enterprise deals.

### Competitive Intelligence
Understand prospect's current stack and pain points.

## Integrations Required
- Perplexity API (research)
- OpenAI/Anthropic (synthesis)
- Google Docs API (optional)

## Cost Estimate
- ~$0.10-0.20 per full dossier
- **50 prospects: ~$10**

## Edge Cases
- Private company: Limited data, focus on job posts
- New executive: Check previous company history
- No LinkedIn: Use alternative sources
