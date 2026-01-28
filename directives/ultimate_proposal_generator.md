# Ultimate Proposal Generator

## What This Workflow Is
**Complete proposal and pitch deck generation system** that creates professional, high-converting proposals for agency services. Includes discovery call prep, proposal copy, pricing options, case studies, and follow-up sequences. Built to close more deals with less effort.

## What It Does
1. Researches prospect's company and challenges
2. Generates customized proposal copy
3. Creates pricing tiers and options
4. Includes relevant case studies
5. Produces executive summary
6. Creates pitch deck slides
7. Generates follow-up sequence

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
PERPLEXITY_API_KEY=your_key           # Company research
GOOGLE_APPLICATION_CREDENTIALS=path   # Google Docs/Slides
```

### Required Skill Bibles
- `SKILL_BIBLE_client_proposals_pitch_decks.md`
- `SKILL_BIBLE_offer_creation_pricing.md`
- `SKILL_BIBLE_high_ticket_sales_process.md`
- `SKILL_BIBLE_discovery_call_mastery.md`
- `SKILL_BIBLE_roi_calculator_creation.md`

## How to Run

```bash
# Full proposal generation
python3 execution/generate_proposal.py \
  --prospect-company "Acme Corp" \
  --prospect-name "John Smith" \
  --prospect-title "CEO" \
  --service "Meta Ads Management" \
  --monthly-retainer 5000 \
  --include-case-studies \
  --include-pitch-deck

# Quick proposal
python3 execution/generate_proposal.py \
  --prospect-company "Acme Corp" \
  --service "Lead Generation" \
  --budget-range "3000-5000" \
  --format "google_doc"
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| prospect-company | string | Yes | Company name |
| prospect-name | string | No | Contact name |
| prospect-title | string | No | Contact title |
| service | string | Yes | Service being proposed |
| monthly-retainer | int | No | Base monthly fee |
| budget-range | string | No | Client's budget range |
| pain-points | list | No | Known pain points |
| goals | list | No | Client's goals |
| include-case-studies | flag | No | Add case studies |
| include-pitch-deck | flag | No | Generate slides |
| format | enum | No | "pdf", "google_doc", "markdown" |

## Process

### Phase 1: Prospect Research
1. Research company via Perplexity
2. Find recent news/funding
3. Identify potential pain points
4. Research competitors
5. Estimate current marketing spend

### Phase 2: Proposal Structure

**Executive Summary (1 page):**
- Understanding their situation
- Proposed solution overview
- Expected outcomes
- Investment summary

**The Challenge (1 page):**
- Current pain points
- Cost of inaction
- Market opportunity

**Our Solution (2-3 pages):**
- Service description
- Methodology/process
- Deliverables
- Timeline

**Case Studies (1-2 pages):**
- Similar client success stories
- Specific metrics/results
- Testimonials

**Investment Options (1 page):**
- 3 pricing tiers
- What's included in each
- Payment terms
- Guarantees

**Next Steps (1 page):**
- How to proceed
- Onboarding process
- Start date options

### Phase 3: Pricing Strategy

**Tier Structure:**
```
Starter: $X/mo
- Core deliverables
- Basic support
- Monthly reporting

Growth: $Y/mo (Most Popular)
- Everything in Starter
- Advanced features
- Priority support
- Weekly check-ins

Scale: $Z/mo
- Everything in Growth
- Custom additions
- Dedicated manager
- Performance guarantees
```

### Phase 4: Follow-Up Sequence

**Day 1:** Proposal sent email
**Day 3:** Check-in email
**Day 7:** Value-add email
**Day 14:** Final follow-up

## Output Structure
```
.tmp/proposals/{prospect_slug}/
├── research/
│   ├── company_research.md
│   └── competitive_analysis.md
├── proposal/
│   ├── full_proposal.md
│   ├── executive_summary.md
│   └── pricing_options.md
├── pitch_deck/
│   ├── slides.md
│   └── speaker_notes.md
├── follow_up/
│   └── email_sequence.md
├── exports/
│   ├── proposal.pdf
│   └── proposal_google_doc_url.txt
└── result.json
```

## Quality Gates

### Pre-Send Checklist
- [ ] Company name spelled correctly
- [ ] Contact name and title verified
- [ ] Service matches their needs
- [ ] Pricing within their budget
- [ ] Case studies relevant
- [ ] No generic/template language visible
- [ ] Proposal formatted professionally
- [ ] Links working

## Integration with Other Workflows

- `ai_prospect_researcher.md` - Deep research
- `roi_calculator_creation.md` - ROI projections
- `client_onboarding.md` - Post-close process
- `follow_up_sequence.md` - Automated follow-up
