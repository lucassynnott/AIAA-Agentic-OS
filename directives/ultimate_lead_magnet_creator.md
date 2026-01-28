# Ultimate Lead Magnet Creator

## What This Workflow Is
**Complete lead magnet generation system** that creates high-value downloadable resources to capture leads. Produces PDF guides, checklists, templates, and email sequences for nurturing captured leads.

## What It Does
1. Identifies optimal lead magnet type
2. Generates lead magnet content
3. Creates landing page copy
4. Produces thank-you page content
5. Generates nurture email sequence
6. Creates promotion strategy

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
GOOGLE_APPLICATION_CREDENTIALS=path   # Docs creation
```

### Required Skill Bibles
- `SKILL_BIBLE_lead_generation_mastery.md`
- `SKILL_BIBLE_lead_magnet_ad_funnels.md`
- `SKILL_BIBLE_email_sequence_writing.md`
- `SKILL_BIBLE_landing_page_copywriting.md`

## How to Run

```bash
python3 execution/generate_lead_magnet.py \
  --topic "How to Scale Your Agency" \
  --target-audience "Agency owners at $10-50K/month" \
  --magnet-type "checklist" \
  --offer-to-sell "Agency Accelerator Program" \
  --include-landing-page \
  --include-email-sequence
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| topic | string | Yes | Lead magnet topic |
| target-audience | string | Yes | Who it's for |
| magnet-type | enum | No | Type of lead magnet |
| offer-to-sell | string | No | What you want them to buy |
| include-landing-page | flag | No | Generate landing page |
| include-email-sequence | flag | No | Generate email nurture |

## Lead Magnet Types

### Checklist
- Quick wins
- Easy to consume
- High perceived value
- Example: "7-Point Agency Audit Checklist"

### PDF Guide
- Deep dive on topic
- 5-15 pages
- Comprehensive but actionable
- Example: "Complete Guide to Meta Ads for Agencies"

### Template/Swipe File
- Ready-to-use resource
- Saves time
- Immediate value
- Example: "10 High-Converting Cold Email Templates"

### Calculator/Tool
- Interactive resource
- Quantifies value
- Example: "Agency Pricing Calculator"

### Mini-Course
- Video/email series
- Higher engagement
- Example: "5-Day Lead Gen Bootcamp"

## Process

### Phase 1: Lead Magnet Content

**Checklist Structure:**
1. Compelling title
2. Introduction (why this matters)
3. 7-15 actionable items
4. Quick win for each item
5. CTA to next step

**PDF Guide Structure:**
1. Cover page
2. Introduction/why read this
3. Core content (3-5 chapters)
4. Action steps
5. About the author
6. CTA/next steps

### Phase 2: Landing Page Copy

**Headline:** "[Number] [Thing] to [Achieve Result]"

**Subheadline:** "Free [Format] reveals exactly how to [benefit]"

**Bullet Points:**
- What they'll learn #1
- What they'll learn #2
- What they'll learn #3

**Form:** Name + Email

**CTA:** "Get Free Access" / "Download Now"

### Phase 3: Thank You Page

**Delivery:**
- Confirm delivery method
- Download link or email note

**Next Step CTA:**
- Book a call
- Watch video
- Join community

### Phase 4: Email Nurture Sequence

**Email 1 (Immediate):** Delivery
- Deliver the resource
- How to use it
- Quick win

**Email 2 (Day 1):** Quick Win
- One tactical tip
- Build on lead magnet
- Engagement question

**Email 3 (Day 3):** Case Study
- Success story
- Results achieved
- How they did it

**Email 4 (Day 5):** Common Mistake
- What people get wrong
- How to avoid it
- Your solution

**Email 5 (Day 7):** Soft Pitch
- Introduce your offer
- How it helps further
- CTA to learn more

## Output Structure
```
.tmp/lead_magnets/{topic_slug}/
├── magnet/
│   ├── content.md
│   └── design_brief.md
├── landing/
│   ├── landing_page.md
│   └── thank_you_page.md
├── emails/
│   └── nurture_sequence.md
├── promotion/
│   └── promotion_strategy.md
└── result.json
```

## Quality Gates

### Lead Magnet Checklist
- [ ] Solves specific problem
- [ ] Provides quick win
- [ ] High perceived value
- [ ] Easy to consume (<10 min)
- [ ] Branded professionally
- [ ] Clear next step

### Conversion Benchmarks
| Metric | Target |
|--------|--------|
| Landing page opt-in | 30-50% |
| Email open rate | 50%+ (day 1) |
| Email click rate | 5%+ |
| Lead to call | 3-5% |
