# Full Campaign Pipeline

## What This Workflow Is

A complete end-to-end campaign generation system that takes a client from research through live campaign assets. Generates everything needed for a full Meta Ads campaign with landing pages, CRM setup, and follow-up automation.

## What It Does

1. **Client Research** - Deep market research using Perplexity AI
2. **Meta Ads Setup** - Complete campaign structure with targeting
3. **Ad Copy** - 10+ ad copy variations across formats
4. **Ad Images** - AI-generated ad creative prompts and images
5. **Landing Page** - Full sales page with all sections
6. **Landing Page Images** - Visual assets for each section
7. **CRM Pipeline** - Complete pipeline and automation setup
8. **Follow-up Sequences** - Email and SMS nurture sequences

## Prerequisites

**Required API Keys:**
- `OPENROUTER_API_KEY` - For Claude (copy, pages, sequences)
- `PERPLEXITY_API_KEY` - For research (optional but recommended)

**Optional:**
- `OPENAI_API_KEY` - For DALL-E image generation

**Installation:**
```bash
pip install requests python-dotenv openai
```

## How to Run

```bash
# Basic usage
python3 execution/full_campaign_pipeline.py \
  --client "Acme Corp" \
  --website "https://acmecorp.com" \
  --offer "AI Lead Generation" \
  --budget 5000

# Full options
python3 execution/full_campaign_pipeline.py \
  --client "Premium Coaching" \
  --website "https://premiumcoaching.com" \
  --offer "Executive Coaching Program" \
  --budget 10000 \
  --output-dir .tmp/campaigns/premium
```

## Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `--client` | string | Yes | - | Client/company name |
| `--website` | string | Yes | - | Client website URL |
| `--offer` | string | Yes | - | Main offer/product name |
| `--budget` | float | No | 5000 | Monthly ad budget |
| `--output-dir` | string | No | .tmp/campaigns | Output directory |

## Process

### Phase 1: Client Research
**Input:** Company name, website, offer
**Output:** `01_research.json`, `01_research.md`

- Company overview and positioning
- Target audience demographics
- Pain points and desires
- Competitor analysis
- Transformation promise
- Messaging hooks and angles

### Phase 2: Meta Ads Setup
**Input:** Research dossier, budget
**Output:** `02_meta_ads_setup.json`, `02_meta_ads_setup.md`

- Campaign structure (CBO/ABO)
- Ad set configurations (3-5)
- Targeting definitions
- Cold, warm, lookalike audiences
- Budget allocation
- Testing strategy

### Phase 3: Ad Copy
**Input:** Research dossier, hooks
**Output:** `03_ad_copy.md`

10 ad variations across:
- Problem-Agitate-Solve (3)
- Story-Based (3)
- Direct Response (2)
- Social Proof (2)

Each includes:
- Primary text
- Headline (40 chars)
- Description (30 chars)
- CTA recommendation

### Phase 4: Ad Images
**Input:** Offer, audience
**Output:** `04_ad_images.md`, `images/ad_*.png`

5 image concepts:
- Problem visualization
- Solution/transformation
- Social proof style
- Pattern interrupt
- Lifestyle/aspiration

Each with:
- DALL-E 3 prompt
- Dimension recommendations
- Text overlay suggestions

### Phase 5: Landing Page
**Input:** Research, transformation
**Output:** `05_landing_page.md`

Complete page structure:
- Above the fold (headline, subhead, CTA)
- Problem section
- Solution section
- Benefits bullets
- Social proof
- FAQ
- Final CTA
- Form fields

### Phase 6: Landing Page Images
**Input:** Page structure
**Output:** `06_landing_page_images.md`, `images/lp_*.png`

5 section images:
- Hero image
- Problem section
- Solution section
- Results/social proof
- About/trust

### Phase 7: CRM Setup
**Input:** Client info, offer
**Output:** `07_crm_setup.md`

- Pipeline stages (10+)
- Lead scoring criteria
- Automation triggers
- Tags and labels
- Custom fields
- Integration points

### Phase 8: Follow-up Sequences
**Input:** Research, objections
**Output:** `08_followup_sequences.md`

5 complete sequences:
1. **Welcome** (5 emails) - Post opt-in
2. **Pre-Call** (3 emails + 2 SMS) - After booking
3. **No-Show** (4 emails + 2 SMS) - Missed appointment
4. **Post-Call Nurture** (7 emails) - Didn't close
5. **Long-term Nurture** (ongoing framework)

## Outputs

```
.tmp/campaigns/acme_corp/
├── 00_campaign_master.json    # Master index
├── 01_research.json          # Research data
├── 01_research.md            # Research report
├── 02_meta_ads_setup.json    # Campaign config
├── 02_meta_ads_setup.md      # Campaign docs
├── 03_ad_copy.md             # 10 ad variations
├── 04_ad_images.md           # Image prompts
├── 05_landing_page.md        # Full page copy
├── 06_landing_page_images.md # LP image prompts
├── 07_crm_setup.md           # Pipeline config
├── 08_followup_sequences.md  # All sequences
└── images/                   # Generated images
    ├── ad_image_1.png
    ├── ad_image_2.png
    └── lp_image_1.png
```

## Quality Gates

- [ ] Research includes 5+ pain points
- [ ] 10 ad copy variations generated
- [ ] Landing page has all 7 sections
- [ ] 5 email sequences with complete emails
- [ ] All files saved successfully

## Time & Cost Estimates

**Time:** 10-15 minutes total

**Cost per campaign:**
| Component | Cost |
|-----------|------|
| Perplexity research | ~$0.10 |
| Claude (8 phases) | ~$0.50 |
| DALL-E images (6) | ~$0.30 |
| **Total** | **~$0.90** |

## Integration Points

### Meta Ads API
The `02_meta_ads_setup.json` contains structured data that can be used with:
- Facebook Marketing API
- Third-party tools (Revealbot, AdEspresso)

### CRM Integration
The `07_crm_setup.md` is formatted for:
- GoHighLevel
- HubSpot
- Close.io
- Pipedrive

### Email Platforms
The `08_followup_sequences.md` can be imported to:
- ActiveCampaign
- ConvertKit
- Instantly
- GoHighLevel

## Related Skill Bibles

**[SKILL_BIBLE_meta_ads_manager_technical.md](../skills/SKILL_BIBLE_meta_ads_manager_technical.md)** (PRIMARY FOR META ADS)
- Complete Meta Ads Manager technical setup and optimization
- Pixel implementation, Conversions API, audience infrastructure
- Persona-led creative diversification (90% success rate in CPM/CPL improvement)
- Andromeda update strategies and incremental reach optimization
- Campaign structure, budget allocation, and scaling frameworks

**[SKILL_BIBLE_hormozi_paid_ads_mastery.md](../skills/SKILL_BIBLE_hormozi_paid_ads_mastery.md)**
- Paid ads framework and strategy
- Ad creative principles and hooks
- Platform optimization tactics

**[SKILL_BIBLE_agency_funnel_building.md](../skills/SKILL_BIBLE_agency_funnel_building.md)**
- Landing page optimization
- Conversion funnel design
- Lead generation best practices

## Related Workflows

- `youtube_knowledge_miner.md` - Learn best practices first
- `youtube_to_campaign_pipeline.md` - Complete automation
- `vsl_funnel_orchestrator.md` - VSL-focused campaigns
