# Ultimate Google Ads Campaign Generator

## What This Workflow Is
**Complete Google Ads campaign system** from keyword research to ad copy generation. Produces search, display, YouTube, and Performance Max campaign structures with all ad assets.

## What It Does
1. Conducts keyword research and grouping
2. Generates ad copy for all formats
3. Creates campaign structure
4. Produces negative keyword lists
5. Generates audience targeting
6. Creates bidding strategy recommendations
7. Builds conversion tracking setup guide

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
PERPLEXITY_API_KEY=your_key           # Competitive research
```

### Required Skill Bibles
- `SKILL_BIBLE_paid_advertising_mastery.md`
- `SKILL_BIBLE_ad_copywriting.md`
- `SKILL_BIBLE_lead_generation_mastery.md`

## How to Run

```bash
python3 execution/generate_google_ads_campaign.py \
  --client "Acme Corp" \
  --product "Project Management Software" \
  --landing-page "https://acme.com/demo" \
  --monthly-budget 10000 \
  --campaign-types "search,youtube" \
  --target-locations "United States"
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client | string | Yes | Client name |
| product | string | Yes | Product/service |
| landing-page | url | Yes | Target landing page |
| monthly-budget | int | Yes | Monthly ad spend |
| campaign-types | list | No | search, display, youtube, pmax |
| target-locations | string | No | Geographic targeting |
| competitors | list | No | Competitor names |

## Process

### Phase 1: Keyword Research

**Keyword Categories:**
- Brand keywords
- Generic/category keywords
- Competitor keywords
- Long-tail keywords
- Problem-aware keywords
- Solution-aware keywords

**Keyword Metrics:**
- Search volume
- Competition level
- Suggested bid
- Commercial intent

### Phase 2: Ad Group Structure

**Themed Ad Groups:**
```
Campaign: [Product] - Search - Non-Brand
├── Ad Group: [Feature 1]
│   └── Keywords: [feature-related terms]
├── Ad Group: [Feature 2]
│   └── Keywords: [feature-related terms]
├── Ad Group: [Problem/Pain Point]
│   └── Keywords: [pain-related terms]
└── Ad Group: [Solution]
    └── Keywords: [solution-related terms]
```

### Phase 3: Ad Copy Generation

**Responsive Search Ads:**
- 15 headlines (30 chars each)
- 4 descriptions (90 chars each)
- Path fields
- Sitelinks
- Callouts
- Structured snippets

**YouTube Ads:**
- Video script (15-30 sec)
- Companion banner copy
- CTA overlay text

### Phase 4: Negative Keywords

**Universal Negatives:**
- Free, cheap, discount (unless relevant)
- Jobs, careers, hiring
- DIY, how to, tutorial (unless content)
- Competitor brand terms (for non-competitor campaigns)

**Industry-Specific Negatives:**
[Generated based on industry]

## Output Structure
```
.tmp/google_ads_campaigns/{client_slug}/
├── keywords/
│   ├── keyword_research.csv
│   ├── keyword_grouping.json
│   └── negative_keywords.csv
├── ads/
│   ├── search_ads.md
│   ├── youtube_scripts.md
│   └── display_copy.md
├── campaign_structure/
│   ├── structure.md
│   └── google_ads_editor_import.csv
├── tracking/
│   └── conversion_setup.md
└── result.json
```

## Quality Gates

### Pre-Launch Checklist
- [ ] Keywords grouped thematically
- [ ] Headlines under 30 characters
- [ ] Descriptions under 90 characters
- [ ] Landing page matches ad message
- [ ] Conversion tracking tested
- [ ] Negative keywords added
- [ ] Extensions configured
- [ ] Budget allocated correctly
