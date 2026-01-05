# AI Cold Email Personalizer

## What This Workflow Is
This workflow uses AI to research each prospect and generate hyper-personalized email openers and copy that significantly increase response rates compared to generic templates.

## What It Does
1. Takes your lead list from Google Sheets
2. Researches each prospect (company, LinkedIn, news, job posts)
3. Identifies relevant pain points and talking points
4. Generates personalized first lines for each prospect
5. Writes back to your sheet for use in email campaigns

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For AI generation
PERPLEXITY_API_KEY=your_perplexity_key    # For web research
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Google OAuth credentials (`credentials.json`)
- OpenAI + Perplexity API access

### Installation
```bash
pip install openai requests google-api-python-client gspread
```

## How to Run

### Step 1: Prepare Your Lead Sheet
Ensure your Google Sheet has columns: name, title, company, website (optional: linkedin_url)

### Step 2: Research Prospects
```bash
python3 execution/research_prospect.py \
  "[SHEET_URL]" \
  --output .tmp/research.json
```

### Step 3: Generate Personalized Lines
```bash
python3 execution/personalize_emails_ai.py \
  .tmp/research.json \
  --service "cold email for B2B SaaS" \
  --value_prop "book 30+ meetings/month" \
  --output .tmp/personalized.json
```

### Step 4: Update Your Sheet
```bash
python3 execution/update_sheet.py \
  .tmp/personalized.json \
  "[SHEET_URL]" \
  --add_columns "personalized_first_line,pain_point,research_notes"
```

### Quick One-Liner
```bash
python3 execution/research_prospect.py "[SHEET_URL]" -o .tmp/research.json && \
python3 execution/personalize_emails_ai.py .tmp/research.json --service "your service" && \
python3 execution/update_sheet.py .tmp/personalized.json "[SHEET_URL]"
```

## Goal
Generate hyper-personalized first lines and email copy for each prospect using AI research.

## Inputs
- **Lead List**: Google Sheet with prospect data
- **Service/Offer**: What you're selling
- **Value Proposition**: Key benefit
- **Personalization Depth**: Light (company only) or Deep (individual research)

## Tools/Scripts
- `execution/personalize_emails_ai.py` - AI personalization engine
- `execution/research_prospect.py` - Prospect research
- `execution/update_sheet.py` - Write back to Sheets

## Process

### 1. Research Each Prospect
For each lead, gather:
- Company website content
- Recent news/press releases
- LinkedIn activity (posts, job changes)
- Company hiring signals
- Tech stack (BuiltWith)

```bash
python3 execution/research_prospect.py "[SHEET_URL]" --output .tmp/research.json
```

### 2. Generate Personalized First Lines
```bash
python3 execution/personalize_emails_ai.py .tmp/research.json \
  --service "[YOUR_SERVICE]" \
  --value_prop "[VALUE_PROPOSITION]" \
  --output .tmp/personalized.json
```

AI generates:
- **Personalized opener** (8-20 words)
- **Pain point hook** (based on research)
- **Relevance bridge** (why reaching out now)

### 3. First Line Patterns

**Pattern A: Recent Achievement**
> "Congrats on the Series A - scaling from 20 to 50 employees in 6 months is no joke."

**Pattern B: Content Reference**
> "Your LinkedIn post about cold email deliverability hit home - we see the same issue with clients."

**Pattern C: Company Observation**
> "Noticed you're hiring 3 SDRs - guessing pipeline generation is top priority right now."

**Pattern D: Industry Insight**
> "With Google's new sender requirements, most SaaS companies are scrambling on deliverability."

### 4. Quality Control
AI validates each first line:
- ✅ Specific (not generic)
- ✅ Accurate (fact-checkable)
- ✅ Relevant (ties to offer)
- ✅ Concise (<25 words)

### 5. Update Sheet
```bash
python3 execution/update_sheet.py .tmp/personalized.json "[SHEET_URL]" \
  --add_columns "personalized_first_line,pain_point,research_notes"
```

## Output Schema
| Column | Description |
|--------|-------------|
| personalized_first_line | Custom opener |
| pain_point | Identified problem |
| personalization_source | Where insight came from |
| research_notes | Key findings |
| confidence_score | AI confidence (0-100) |

## Personalization Levels

### Light (Fast, $0.01/lead)
- Company website scan
- Industry-based pain points
- Generic but relevant opener

### Medium ($0.03/lead)
- Company + LinkedIn profile
- Recent news/funding
- Role-specific hooks

### Deep ($0.10/lead)
- Full prospect research
- Content/post analysis
- Competitor intelligence
- Hyper-specific opener

## Integrations Required
- OpenAI/Anthropic API
- Perplexity API (research)
- Google Sheets API

## Example Output

**Input:**
```
Name: John Smith
Title: VP of Sales
Company: Acme SaaS
Website: acmesaas.com
```

**Output:**
```
First Line: "Saw Acme just closed a $5M round - congrats. Guessing pipeline velocity is top priority as you scale the team."
Pain Point: Scaling outbound while maintaining quality
Source: TechCrunch funding announcement + 3 SDR job posts
```

## Edge Cases
- No research found: Use industry-generic personalization
- Outdated info: Flag for manual review
- Competitor customer: Note in research, may deprioritize
