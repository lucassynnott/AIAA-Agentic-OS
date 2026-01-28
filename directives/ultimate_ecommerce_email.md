# Ultimate E-commerce Email System

## What This Workflow Is
**Complete e-commerce email marketing system** that generates automated flows, campaign copy, and revenue optimization strategies. Built for e-commerce agencies managing Klaviyo/email marketing.

## What It Does
1. Creates automated email flows (welcome, cart, post-purchase)
2. Generates campaign copy and designs
3. Produces segmentation strategies
4. Creates A/B testing frameworks
5. Generates promotional calendars
6. Produces deliverability optimization

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
```

### Required Skill Bibles
- `SKILL_BIBLE_ecommerce_email_marketing.md`
- `SKILL_BIBLE_ecom_email_marketing_v2.md`
- `SKILL_BIBLE_klaviyo_mastery.md`
- `SKILL_BIBLE_email_sequence_writing.md`
- `SKILL_BIBLE_email_deliverability.md`
- `SKILL_BIBLE_cart_abandonment_recovery.md`
- `SKILL_BIBLE_welcome_flow_optimization.md`

## How to Run

```bash
python3 execution/generate_ecommerce_emails.py \
  --brand "Acme Store" \
  --industry "Fashion DTC" \
  --aov 85 \
  --flows "welcome,cart,post_purchase,winback" \
  --campaigns-per-month 8 \
  --include-calendar
```

## Core Email Flows

### Welcome Flow (5-7 emails)
**Email 1 (Immediate):** Welcome + discount
**Email 2 (Day 1):** Brand story
**Email 3 (Day 2):** Bestsellers
**Email 4 (Day 4):** Social proof
**Email 5 (Day 7):** Discount reminder
**Email 6 (Day 10):** Educational content
**Email 7 (Day 14):** Last chance

### Abandoned Cart Flow (3-4 emails)
**Email 1 (1 hour):** Reminder
**Email 2 (24 hours):** Social proof
**Email 3 (48 hours):** Incentive
**Email 4 (72 hours):** Last chance

### Browse Abandonment (2-3 emails)
**Email 1 (4 hours):** Reminder
**Email 2 (24 hours):** Related products
**Email 3 (48 hours):** Social proof

### Post-Purchase Flow (4-5 emails)
**Email 1 (Immediate):** Order confirmation
**Email 2 (Day 3):** Shipping update
**Email 3 (Day 7):** How to use
**Email 4 (Day 14):** Review request
**Email 5 (Day 21):** Cross-sell

### Winback Flow (3-4 emails)
**Email 1 (30 days):** We miss you
**Email 2 (45 days):** Special offer
**Email 3 (60 days):** Last chance
**Email 4 (90 days):** Sunset

## Campaign Types

### Promotional Campaigns
- Flash sales
- Holiday promotions
- New product launches
- VIP exclusives
- BOGO offers

### Content Campaigns
- Educational content
- Behind the scenes
- User-generated content
- Brand stories
- Lifestyle content

### Engagement Campaigns
- Surveys
- Polls
- Reviews request
- Social contests
- Loyalty updates

## Segmentation Strategy

### Engagement Segments
- Engaged (opened in 30 days)
- Semi-engaged (opened in 60 days)
- At-risk (no open in 90 days)
- Inactive (no open in 120+ days)

### Purchase Segments
- Never purchased
- 1x buyer
- Repeat buyer (2-3x)
- VIP (4+ purchases)
- High AOV
- Low AOV

### Behavioral Segments
- Recent browsers
- Cart abandoners
- Discount shoppers
- Full-price buyers
- Category preferences

## Output Structure
```
.tmp/ecommerce_emails/{brand_slug}/
├── flows/
│   ├── welcome_flow.md
│   ├── cart_abandonment.md
│   ├── post_purchase.md
│   ├── browse_abandonment.md
│   └── winback.md
├── campaigns/
│   ├── campaign_templates.md
│   └── calendar.csv
├── segments/
│   └── segmentation_strategy.md
├── optimization/
│   ├── ab_testing.md
│   └── deliverability.md
└── result.json
```

## Email Templates

### Welcome Email 1
```
Subject: Welcome to [Brand]! Here's 10% off 🎉

Hey [First Name],

Welcome to the [Brand] family!

We're thrilled to have you. To say thanks, here's 
10% off your first order:

[CODE: WELCOME10]

What makes us different:
• [Unique selling point 1]
• [Unique selling point 2]
• [Unique selling point 3]

Ready to shop? Check out our bestsellers:

[Product Grid]

[Shop Now Button]

See you soon,
The [Brand] Team

P.S. This code expires in 7 days!
```

### Cart Abandonment Email 1
```
Subject: You left something behind...

Hey [First Name],

Looks like you left some items in your cart!

[Cart Contents]

Good news - they're still available (for now).

[Complete My Order Button]

Need help? Reply to this email or chat with us.

[Brand] Team
```

## Quality Gates

### Flow Checklist
- [ ] All flows configured
- [ ] Timing optimized
- [ ] Subject lines A/B tested
- [ ] Mobile responsive
- [ ] Unsubscribe working
- [ ] Tracking in place

### Performance Benchmarks
| Flow | Open Rate | Click Rate | Conv Rate |
|------|-----------|------------|-----------|
| Welcome | 50%+ | 10%+ | 5%+ |
| Cart | 45%+ | 15%+ | 10%+ |
| Post-Purchase | 60%+ | 8%+ | 3%+ |
| Winback | 25%+ | 5%+ | 2%+ |
