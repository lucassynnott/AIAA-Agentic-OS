# Ultimate Niche Research System

## What This Workflow Is
**Complete niche research and validation system** for agencies exploring new markets. Produces market analysis, ICP profiles, competitive landscape, and go-to-market strategy.

## What It Does
1. Researches market size and trends
2. Identifies ideal customer profile
3. Maps competitive landscape
4. Analyzes pricing and positioning
5. Validates demand signals
6. Creates go-to-market strategy

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI analysis
PERPLEXITY_API_KEY=your_key           # Market research
```

### Required Skill Bibles
- `SKILL_BIBLE_agency_positioning_niching.md`
- `SKILL_BIBLE_competitive_analysis.md`
- `SKILL_BIBLE_offer_positioning.md`
- `SKILL_BIBLE_competitive_advantage_strategy.md`

## How to Run

```bash
python3 execution/research_niche.py \
  --niche "Dental practices" \
  --service "Local SEO and Google Ads" \
  --location "United States" \
  --include-competitors \
  --include-gtm-strategy
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| niche | string | Yes | Target niche/industry |
| service | string | Yes | Service you'd offer |
| location | string | No | Geographic focus |
| include-competitors | flag | No | Analyze competitors |
| include-gtm-strategy | flag | No | Create GTM plan |

## Process

### Phase 1: Market Analysis

**Size & Growth:**
- Total addressable market
- Serviceable market
- Growth trends
- Industry dynamics

**Key Players:**
- Major companies
- Revenue ranges
- Common pain points
- Buying behavior

**Trends:**
- Technology adoption
- Regulatory changes
- Economic factors
- Emerging opportunities

### Phase 2: ICP Development

**Firmographic Profile:**
- Company size (employees/revenue)
- Industry sub-segment
- Location
- Technology stack
- Growth stage

**Buyer Persona:**
- Title/role
- Responsibilities
- Goals and KPIs
- Pain points
- Buying triggers
- Information sources

**Buying Process:**
- Decision makers
- Influencers
- Timeline
- Budget range
- Evaluation criteria

### Phase 3: Competitive Analysis

**Direct Competitors:**
- Who they are
- What they offer
- Pricing
- Positioning
- Strengths/weaknesses

**Indirect Competitors:**
- Alternative solutions
- In-house options
- Status quo

**Differentiation Opportunities:**
- Underserved segments
- Unmet needs
- Positioning gaps

### Phase 4: Demand Validation

**Signals to Check:**
- Google search volume
- Social media discussions
- Industry forums/groups
- Job postings
- Funding/investment activity

**Validation Methods:**
- Keyword research
- Social listening
- Survey/interview prospects
- Analyze competitor success

### Phase 5: Go-to-Market Strategy

**Positioning:**
- Unique value proposition
- Messaging framework
- Key differentiators

**Lead Generation:**
- Best channels
- Content strategy
- Outbound approach

**Pricing Strategy:**
- Market rate analysis
- Value-based pricing
- Package structure

**Launch Plan:**
- 30/60/90 day milestones
- Resources needed
- Success metrics

## Output Structure
```
.tmp/niche_research/{niche_slug}/
├── market/
│   ├── market_analysis.md
│   └── trends.md
├── icp/
│   ├── ideal_customer.md
│   └── buyer_personas.md
├── competitive/
│   ├── competitor_analysis.md
│   └── differentiation.md
├── validation/
│   └── demand_signals.md
├── strategy/
│   ├── positioning.md
│   └── gtm_plan.md
└── result.json
```

## ICP Template

```markdown
# Ideal Customer Profile: [Niche]

## Company Profile
- **Industry:** [Specific sub-segment]
- **Size:** [X-Y employees / $X-Y revenue]
- **Location:** [Geographic focus]
- **Tech Stack:** [Key technologies]
- **Growth Stage:** [Startup/Growth/Mature]

## Buyer Persona
- **Title:** [Decision maker title]
- **Reports To:** [Manager/C-suite]
- **Responsible For:** [Key areas]

## Goals
1. [Primary goal]
2. [Secondary goal]
3. [Tertiary goal]

## Pain Points
1. [Pain point 1]
2. [Pain point 2]
3. [Pain point 3]

## Buying Triggers
- [Trigger event 1]
- [Trigger event 2]
- [Trigger event 3]

## Objections
1. [Common objection 1]
2. [Common objection 2]

## Where They Hang Out
- [Platform/community 1]
- [Platform/community 2]
- [Publication/event]
```

## Quality Gates

### Research Checklist
- [ ] Market size quantified
- [ ] ICP clearly defined
- [ ] 5+ competitors analyzed
- [ ] Demand validated
- [ ] Pricing researched
- [ ] GTM plan actionable

### Validation Criteria
| Criteria | Minimum |
|----------|---------|
| Market size | $1B+ TAM |
| Growth rate | 5%+ YoY |
| Competition | Not saturated |
| Willingness to pay | Validated |
