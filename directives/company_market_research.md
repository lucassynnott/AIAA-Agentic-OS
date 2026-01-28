# Company & Offer Market Research

## What This Workflow Is
This workflow conducts comprehensive market research on a company and their offer using Perplexity AI to gather intelligence for VSL funnel creation, positioning strategy, and competitive analysis.

## What It Does
1. Receives company name, website, and offer details as input
2. Conducts multi-source research via Perplexity AI (web, news, competitors)
3. Analyzes target audience, pain points, and market positioning
4. Identifies unique mechanisms and transformation promises
5. Extracts social proof, case studies, and results
6. Compiles research into structured JSON for downstream workflows
7. Returns comprehensive research dossier

## Prerequisites

### Required API Keys (add to .env)
```
PERPLEXITY_API_KEY=your_perplexity_key    # Get from perplexity.ai
OPENAI_API_KEY=your_openai_key            # For synthesis (fallback)
```

### Required Tools
- Python 3.10+
- Perplexity API access

### Installation
```bash
pip install openai requests
```

## How to Run

### Option 1: Direct Python Execution
```bash
python3 execution/research_company_offer.py \
  --company "Acme Corp" \
  --website "https://acmecorp.com" \
  --offer "B2B Lead Generation System" \
  --output .tmp/research/acme_corp.json
```

### Option 2: Via Trigger.dev Task
```bash
python3 execution/test_trigger_task.py \
  --task-id company-market-research \
  --payload '{
    "company": "Acme Corp",
    "website": "https://acmecorp.com",
    "offer": "B2B Lead Generation System",
    "industry": "Marketing Agency"
  }' \
  --wait
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| company | string | Yes | Company name |
| website | string | Yes | Company website URL |
| offer | string | Yes | Product/service being sold |
| industry | string | No | Industry/niche (optional) |
| pricePoint | string | No | Price point or range |
| targetAudience | string | No | Known target audience details |

## Process

### Step 1: Company Overview Research
**Perplexity Query:**
```
Research [COMPANY] ([WEBSITE]). Provide:
- Company overview and mission
- Core products/services
- Target market and ideal customers
- Company size and stage
- Recent news or announcements
- Social media presence
```

**Output:** Company profile JSON

### Step 2: Offer Analysis
**Perplexity Query:**
```
Analyze [OFFER] by [COMPANY]. Provide:
- How the offer works (mechanism)
- Key features and benefits
- Pricing structure if available
- Customer results or case studies
- Unique selling propositions
- Common objections or concerns
```

**Output:** Offer analysis JSON

### Step 3: Target Audience Research
**Perplexity Query:**
```
Research the target audience for [OFFER] in [INDUSTRY]. Provide:
- Demographic profile (titles, company size, etc.)
- Primary pain points and challenges
- Current solutions they're using
- Buying triggers and motivations
- Common objections to similar offers
- Language and terminology they use
```

**Output:** Audience profile JSON

### Step 4: Competitive Landscape
**Perplexity Query:**
```
Research competitors of [COMPANY] offering similar solutions to [OFFER]. Provide:
- Top 3-5 direct competitors
- How they position their offers
- Pricing comparison
- Strengths and weaknesses
- Market gaps and opportunities
```

**Output:** Competitive analysis JSON

### Step 5: Social Proof & Results
**Perplexity Query:**
```
Find case studies, testimonials, and results for [COMPANY] and [OFFER]. Include:
- Quantifiable results (revenue, leads, ROI, etc.)
- Customer success stories
- Reviews and ratings
- Industry recognition or awards
- Media mentions or features
```

**Output:** Social proof JSON

### Step 6: Synthesis
Combines all research sections into unified dossier:
- Executive summary
- Company & offer overview
- Target audience profile (demographics, pain points, desires)
- Unique mechanism
- Transformation promise
- Social proof library
- Competitive positioning
- Recommended messaging angles

**Output:** Complete research dossier (JSON + Markdown)

## Quality Gates

### Pre-Research Validation
- [ ] Company website is accessible and valid
- [ ] Offer description is clear (not generic)
- [ ] Perplexity API key is configured

### Post-Research Validation
- [ ] All 5 research sections completed
- [ ] Minimum 500 words per section
- [ ] At least 3 pain points identified
- [ ] At least 1 unique mechanism found
- [ ] At least 3 social proof elements extracted
- [ ] Target audience clearly defined
- [ ] Research dossier saved to output path

### Error Handling
- **Website unreachable:** Proceed with Perplexity search only
- **Limited social proof:** Flag warning but continue
- **No competitors found:** Research similar offers in industry
- **Perplexity rate limit:** Wait and retry with exponential backoff

## Outputs

### JSON Structure
```json
{
  "company": {
    "name": "Acme Corp",
    "website": "https://acmecorp.com",
    "overview": "...",
    "size": "11-50 employees",
    "industry": "Marketing Agency"
  },
  "offer": {
    "name": "B2B Lead Generation System",
    "description": "...",
    "mechanism": "AI-powered outbound system",
    "price": "$997/mo",
    "features": ["...", "..."]
  },
  "targetAudience": {
    "demographics": "B2B service CEOs, 20-100 employees",
    "painPoints": ["Inconsistent lead flow", "High CAC", "..."],
    "desires": ["Predictable revenue", "Scalable growth", "..."],
    "language": ["qualified leads", "sales pipeline", "..."]
  },
  "transformation": {
    "before": "Unpredictable revenue, feast or famine",
    "after": "Consistent 20+ qualified calls per month",
    "mechanism": "AI-driven outbound system"
  },
  "socialProof": {
    "results": [
      {
        "client": "ABC Agency",
        "metric": "150% revenue increase",
        "timeframe": "90 days"
      }
    ],
    "testimonials": ["..."],
    "caseStudies": ["..."]
  },
  "competitors": [
    {
      "name": "Competitor A",
      "positioning": "...",
      "price": "$1,200/mo"
    }
  ],
  "messaging": {
    "hooks": ["..."],
    "angles": ["..."],
    "objections": ["Too expensive", "..."]
  }
}
```

### Markdown Report
Human-readable research report with sections matching JSON structure.

## Integration with VSL Funnel

This workflow is the **first step** in the VSL funnel creation pipeline:

```
1. Market Research (this workflow)
   ↓
2. VSL Script Writer (uses research)
   ↓
3. Sales Page Writer (uses research)
   ↓
4. Email Sequence Writer (uses research)
   ↓
5. Google Doc Creator (formats outputs)
   ↓
6. Slack Notifier (alerts completion)
```

Research output is passed as context to all downstream workflows.

## Edge Cases

### Edge Case 1: Startup with No Public Info
**Scenario:** New company with minimal online presence.

**Solution:**
- Focus on industry research instead of company-specific
- Research similar successful companies
- Use founder LinkedIn profiles for insights
- Flag as "limited data" in output

### Edge Case 2: Sensitive/Private Offers
**Scenario:** Company doesn't publicly advertise pricing or details.

**Solution:**
- Research industry standards and norms
- Analyze competitor pricing models
- Make educated estimates with confidence scores
- Note assumptions in research output

### Edge Case 3: Highly Technical Offers
**Scenario:** Complex B2B SaaS or technical services.

**Solution:**
- Break down technical jargon into plain language
- Focus on business outcomes over features
- Research pain points from user forums
- Consult technical documentation if public

## Success Metrics

- Research completion rate: 95%+
- Average research time: 3-5 minutes
- Pain points identified: 5-10 per research
- Social proof elements: 3-5 minimum
- Downstream workflow success rate: 90%+ (research quality indicator)

## Related Skills

- [SKILL_BIBLE_vsl_writing_production.md](../skills/SKILL_BIBLE_vsl_writing_production.md) - VSL frameworks
- [SKILL_BIBLE_funnel_copywriting_mastery.md](../skills/SKILL_BIBLE_funnel_copywriting_mastery.md) - Positioning
- [SKILL_BIBLE_copywriting_fundamentals.md](../skills/SKILL_BIBLE_copywriting_fundamentals.md) - Market research for copy

## Self-Annealing Notes

### What Works Well
- Perplexity provides comprehensive, current information
- Multi-query approach covers all angles
- Structured JSON output integrates seamlessly with VSL writer

### What Doesn't Work
- Single broad query misses depth
- Relying only on website misses market context
- Not extracting specific results/metrics reduces VSL credibility

### Improvements Over Time
- Add competitor sentiment analysis
- Include pricing psychology insights
- Extract more granular pain point hierarchy
- Build research template library by industry

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Market research principles
- Customer insight extraction
- Competitive positioning

**[SKILL_BIBLE_hormozi_lead_generation.md](../skills/SKILL_BIBLE_hormozi_lead_generation.md)**
- Target market definition
- Pain point identification
- Value proposition development

**[SKILL_BIBLE_hormozi_customer_acquisition_fast.md](../skills/SKILL_BIBLE_hormozi_customer_acquisition_fast.md)**
- Market opportunity analysis
- Acquisition channel research
- Customer journey mapping
