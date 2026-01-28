# Ultimate Agency Pricing Strategy

## What This Workflow Is
**Complete pricing and packaging system** for agencies optimizing their revenue. Produces pricing tiers, package structures, ROI calculators, and value propositions.

## What It Does
1. Analyzes market pricing
2. Creates pricing tiers
3. Generates package structures
4. Produces ROI calculators
5. Creates value propositions
6. Generates objection handlers

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI analysis
PERPLEXITY_API_KEY=your_key           # Market research
```

### Required Skill Bibles
- `SKILL_BIBLE_pricing_strategy.md`
- `SKILL_BIBLE_premium_pricing_strategy.md`
- `SKILL_BIBLE_pricing_psychology_negotiation.md`
- `SKILL_BIBLE_offer_creation_pricing.md`
- `SKILL_BIBLE_high_ticket_offer_creation.md`
- `SKILL_BIBLE_roi_calculator_creation.md`

## How to Run

```bash
python3 execution/generate_pricing_strategy.py \
  --service "Meta Ads Management" \
  --target-market "E-commerce brands $1-10M" \
  --current-pricing "2000-3000" \
  --competitor-range "1500-5000" \
  --include-roi-calculator
```

## Process

### Phase 1: Market Analysis

**Research:**
- Competitor pricing
- Market rates
- Value perception
- Willingness to pay

**Positioning:**
- Budget tier
- Mid-market tier
- Premium tier
- Enterprise tier

### Phase 2: Pricing Models

**Retainer Model:**
- Fixed monthly fee
- Predictable revenue
- Scope-based

**Performance Model:**
- Base + performance bonus
- Aligned incentives
- Variable revenue

**Project Model:**
- One-time fee
- Scope-defined
- Clear deliverables

**Hybrid Model:**
- Retainer + performance
- Best of both
- Flexible structure

### Phase 3: Package Structure

**Tier 1: Starter**
- Entry-level pricing
- Core deliverables
- Basic support
- Self-service elements

**Tier 2: Growth (Most Popular)**
- Mid-tier pricing
- Full deliverables
- Priority support
- Regular check-ins

**Tier 3: Scale**
- Premium pricing
- Everything in Growth+
- Dedicated team
- Performance guarantees

### Phase 4: Value Stack

**Core Service:**
- Main deliverable
- Primary value

**Add-Ons:**
- Additional services
- Incremental value
- Upsell opportunities

**Bonuses:**
- Fast-action incentives
- Perceived value boosters
- Risk reducers

### Phase 5: ROI Calculator

**Inputs:**
- Current metrics
- Industry benchmarks
- Service impact estimates

**Outputs:**
- Projected ROI
- Break-even analysis
- Monthly/annual returns

## Output Structure
```
.tmp/pricing_strategy/{service_slug}/
├── market/
│   └── market_analysis.md
├── pricing/
│   ├── pricing_tiers.md
│   └── package_structure.md
├── value/
│   ├── value_stack.md
│   └── roi_calculator.md
├── sales/
│   ├── value_proposition.md
│   └── objection_handlers.md
└── result.json
```

## Pricing Templates

### 3-Tier Structure
```
STARTER: $2,000/mo
├── Core ad management
├── Monthly reporting
├── Email support
└── Best for: Testing the waters

GROWTH: $4,000/mo ⭐ Most Popular
├── Everything in Starter
├── Creative strategy
├── Weekly calls
├── Priority support
├── A/B testing
└── Best for: Scaling brands

SCALE: $7,000/mo
├── Everything in Growth
├── Dedicated strategist
├── Daily optimization
├── Unlimited creative
├── Performance guarantee
└── Best for: Aggressive growth
```

### Value-Based Pricing Formula
```
Price = (Expected ROI × Client Budget × 0.10-0.20)

Example:
- Client ad spend: $50,000/mo
- Expected ROAS improvement: 50%
- Additional revenue: $25,000
- Your fee: $2,500-5,000/mo (10-20% of value created)
```

## Objection Handlers

**"It's too expensive":**
```
"I understand budget is important. Let me ask - 
what would hitting [goal] be worth to your business?

If we generate [expected results], your return 
would be [$X]. Does that make the investment 
more reasonable?"
```

**"Competitor charges less":**
```
"You're right - there are cheaper options. But 
here's what you're really comparing:

[Their approach] vs [Your approach]

The difference in results typically outweighs 
the difference in price. Would you rather save 
$1,000/month or make $10,000 more?"
```

## Quality Gates

### Pricing Checklist
- [ ] Market rates researched
- [ ] Value quantified
- [ ] Tiers differentiated
- [ ] ROI demonstrated
- [ ] Objections handled
- [ ] Tested with prospects

### Pricing Metrics
| Metric | Target |
|--------|--------|
| Close rate | 25%+ |
| Price objections | <30% |
| Upsell rate | 20%+ |
| Churn | <5% |
