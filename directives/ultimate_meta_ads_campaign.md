# Ultimate Meta Ads Campaign Generator

## What This Workflow Is
**Complete Meta/Facebook/Instagram ads campaign system** from creative generation to campaign structure. Produces ad copy, creative briefs, audience targeting, campaign structure, and performance optimization recommendations. Built for paid media agencies and in-house teams.

## What It Does
1. Researches competitor ads via Facebook Ad Library
2. Generates ad copy variations (primary text, headlines, descriptions)
3. Creates creative briefs for images/videos
4. Builds campaign structure (campaigns, ad sets, ads)
5. Defines audience targeting strategies
6. Creates A/B testing frameworks
7. Generates performance tracking setup
8. Provides optimization playbook

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI copy generation
PERPLEXITY_API_KEY=your_key           # Competitor research
```

### Required Skill Bibles
- `SKILL_BIBLE_meta_ads_tutorial_facebook_adv.md`
- `SKILL_BIBLE_meta_ads_manager_tutorial_face.md`
- `SKILL_BIBLE_facebook_ads.md`
- `SKILL_BIBLE_ad_creative_hooks.md`
- `SKILL_BIBLE_ad_copywriting.md`
- `SKILL_BIBLE_paid_advertising_mastery.md`

## How to Run

```bash
# Full campaign generation
python3 execution/generate_meta_ads_campaign.py \
  --client "Acme SaaS" \
  --product "Project Management Tool" \
  --offer "14-day free trial" \
  --target-audience "Small business owners, 25-45" \
  --monthly-budget 5000 \
  --objective "conversions" \
  --funnel-stage "cold"

# Creative refresh
python3 execution/generate_meta_ads_campaign.py \
  --client "Acme SaaS" \
  --existing-campaign campaign_data.json \
  --refresh-creatives \
  --variations 10
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client | string | Yes | Client/brand name |
| product | string | Yes | Product/service name |
| offer | string | Yes | What you're promoting |
| target-audience | string | Yes | Audience description |
| monthly-budget | int | Yes | Monthly ad spend |
| objective | enum | Yes | "awareness", "traffic", "conversions", "leads" |
| funnel-stage | enum | No | "cold", "warm", "hot" |
| competitors | list | No | Competitor names to research |
| existing-campaign | path | No | Existing campaign to refresh |
| variations | int | No | Number of ad variations |

## Process

### Phase 1: Competitive Research
1. Scrape Facebook Ad Library for competitor ads
2. Analyze ad copy patterns and hooks
3. Identify winning creative formats
4. Document audience targeting insights

**Output:** Competitive analysis report

### Phase 2: Audience Strategy
Define targeting for each funnel stage:

**Cold Audiences:**
- Interest targeting (detailed)
- Lookalike audiences (1%, 2%, 5%)
- Broad targeting with creative filtering

**Warm Audiences:**
- Website visitors (30/60/90 days)
- Video viewers (25%, 50%, 75%)
- Engagement audiences

**Hot Audiences:**
- Add to cart abandoners
- Past purchasers
- High-intent page visitors

### Phase 3: Ad Copy Generation
Using skill bibles, generate for each creative:

**Primary Text (5 variations):**
- Hook-focused (pattern interrupt)
- Problem-focused (pain point)
- Solution-focused (outcome)
- Story-focused (testimonial)
- FOMO-focused (urgency)

**Headlines (5 variations):**
- Benefit-driven
- Curiosity-driven
- Number-driven
- Question-driven
- Command-driven

**Descriptions (3 variations):**
- Feature list
- Social proof
- Risk reversal

### Phase 4: Creative Briefs
Generate briefs for:

**Static Images:**
- Hero product shot
- Before/after comparison
- Testimonial quote card
- Feature highlight
- Social proof collage

**Video Concepts:**
- UGC-style testimonial
- Product demo
- Problem/solution narrative
- Founder story
- Results showcase

**Carousel Ads:**
- Feature walkthrough
- Customer journey
- Objection handling
- Price breakdown

### Phase 5: Campaign Structure
Build complete campaign architecture:

```
Campaign: [Client] - [Objective] - [Funnel Stage]
├── Ad Set: Cold - Interest Targeting
│   ├── Ad: Hook v1 - Image A
│   ├── Ad: Hook v2 - Image B
│   └── Ad: Hook v3 - Video A
├── Ad Set: Cold - Lookalike 1%
│   ├── Ad: Problem v1 - Image A
│   └── Ad: Problem v2 - Video B
├── Ad Set: Warm - Retargeting
│   ├── Ad: Testimonial v1
│   └── Ad: Offer v1
└── Ad Set: Hot - High Intent
    ├── Ad: FOMO v1
    └── Ad: Direct Response
```

### Phase 6: Optimization Playbook
Create decision framework:

**Day 1-3: Learning Phase**
- Don't touch anything
- Let algorithm learn
- Monitor for policy issues

**Day 4-7: Initial Optimization**
- Kill ads with <1% CTR
- Increase budget on winners
- Test new audiences

**Week 2+: Scaling**
- Duplicate winning ad sets
- Increase budgets 20% every 3 days
- Launch new creatives weekly

## Output Structure
```
.tmp/meta_ads_campaigns/{client_slug}/
├── research/
│   ├── competitor_analysis.md
│   └── ad_library_insights.json
├── audiences/
│   ├── targeting_strategy.md
│   └── audience_definitions.json
├── creatives/
│   ├── ad_copy_variations.md
│   ├── image_briefs.md
│   ├── video_briefs.md
│   └── carousel_concepts.md
├── campaign_structure/
│   ├── campaign_architecture.md
│   └── ads_manager_import.csv
├── optimization/
│   └── playbook.md
└── result.json
```

## Ad Copy Templates

### Hook Formulas (from Skill Bibles)
1. "Stop [doing thing wrong way]"
2. "The [surprising truth] about [topic]"
3. "I [achieved result] in [timeframe]. Here's how:"
4. "Why [common belief] is killing your [desired outcome]"
5. "[Number] [people] are already [getting result]"

### Body Copy Structure
- **Line 1:** Hook/pattern interrupt
- **Line 2:** Problem agitation
- **Line 3:** Solution introduction
- **Line 4:** Key benefit
- **Line 5:** Social proof
- **Line 6:** CTA

### CTA Formulas
- "Click to [get specific result]"
- "Get your free [thing] now"
- "Start your [free trial] today"
- "Join [number] [people] who..."

## Quality Gates

### Pre-Launch Checklist
- [ ] Pixel installed and firing
- [ ] Conversion tracking set up
- [ ] Ad copy within character limits
- [ ] Images 1080x1080 or 1080x1920
- [ ] Video under 15 seconds for Stories
- [ ] Landing page matches ad messaging
- [ ] UTM parameters configured
- [ ] Budget allocated correctly

### Performance Benchmarks
| Metric | Cold | Warm | Hot |
|--------|------|------|-----|
| CTR | 1%+ | 2%+ | 3%+ |
| CPC | <$2 | <$1.50 | <$1 |
| CPM | <$15 | <$12 | <$10 |
| ROAS | 1.5x+ | 3x+ | 5x+ |

## Error Handling

| Error | Solution |
|-------|----------|
| Ad rejected | Review policy, rewrite copy |
| Low delivery | Increase budget or broaden audience |
| High CPC | Test new creatives or audiences |
| Low CTR | Refresh hooks and images |

## Integration with Other Workflows

- `landing_page_generator.md` - Create matching landing pages
- `ad_creative_generator.md` - Generate images/videos
- `full_campaign_pipeline.md` - End-to-end funnel
- `client_reporting.md` - Performance reports

## Self-Annealing Notes

### What Works
- UGC-style video outperforms polished
- Curiosity hooks get highest CTR
- Single-focused ads beat feature lists
- Retargeting should be 20% of budget

### What Doesn't Work
- Text-heavy images
- Multiple CTAs
- Generic stock photos
- Overpromising claims

### Continuous Improvement
- Refresh creatives every 2-3 weeks
- Test new hooks weekly
- Monitor frequency (keep <3)
- Update audiences quarterly
