# Ultimate LinkedIn Outreach System

## What This Workflow Is
**Complete LinkedIn outreach campaign system** that generates connection requests, follow-up sequences, content strategies, and profile optimization. Built for agencies doing LinkedIn-based prospecting.

## What It Does
1. Optimizes LinkedIn profile for prospecting
2. Generates connection request messages
3. Creates follow-up message sequences
4. Produces engagement content strategy
5. Generates personalization at scale
6. Creates tracking and optimization system

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI message generation
PERPLEXITY_API_KEY=your_key           # Prospect research
APIFY_API_TOKEN=your_key              # LinkedIn scraping (optional)
```

### Required Skill Bibles
- `SKILL_BIBLE_linkedin_outreach.md`
- `SKILL_BIBLE_linkedin_post_writing.md`
- `SKILL_BIBLE_dream_100_outreach.md`
- `SKILL_BIBLE_cold_dm_email_conversion.md`

## How to Run

```bash
python3 execution/generate_linkedin_outreach.py \
  --target-icp "Marketing Directors at SaaS companies" \
  --offer "Lead generation services" \
  --daily-connections 20 \
  --sequence-length 4 \
  --include-content-strategy \
  --include-profile-optimization
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| target-icp | string | Yes | Ideal customer profile |
| offer | string | Yes | What you're selling |
| daily-connections | int | No | Connections per day |
| sequence-length | int | No | Follow-up messages |
| include-content-strategy | flag | No | Add content plan |
| include-profile-optimization | flag | No | Add profile review |

## Process

### Phase 1: Profile Optimization

**Headline Formula:**
"I help [ICP] achieve [result] | [Credibility] | [CTA]"

**About Section:**
- Hook (first 2 lines crucial)
- Problem you solve
- Your unique approach
- Social proof
- CTA

**Featured Section:**
- Lead magnet
- Case study
- Video introduction

### Phase 2: Connection Request Templates

**Template 1: Mutual Connection**
```
Hi [Name],

I noticed we're both connected to [Mutual Connection] - 
small world! I work with [ICP] on [result] and your 
work at [Company] caught my attention.

Would love to connect.

[Your Name]
```

**Template 2: Content Engagement**
```
Hi [Name],

Really enjoyed your post about [topic] - especially 
the point about [specific detail]. 

I also work in [space] and thought it'd be great 
to connect.

[Your Name]
```

**Template 3: Industry Insight**
```
Hi [Name],

I've been researching [industry] trends and noticed 
[Company] is doing interesting work in [area].

Would love to connect and share some insights I've 
found that might be relevant.

[Your Name]
```

### Phase 3: Follow-Up Sequence

**Message 1 (After connection, Day 1):**
```
Thanks for connecting, [Name]!

I noticed you're [their role/doing X]. I work with 
[similar companies] helping them [achieve result].

Curious - what's your biggest challenge with [relevant area]?

[Your Name]
```

**Message 2 (Day 3-4):**
```
Hi [Name],

Thought you might find this interesting - [share 
relevant content/insight].

We recently helped [similar company] achieve [result].

Happy to share more if it's relevant to what you're 
working on.

[Your Name]
```

**Message 3 (Day 7):**
```
Hi [Name],

I don't want to be pushy, but I've been working with 
a few [companies like theirs] on [solving problem].

Would you be open to a quick 15-minute chat to see 
if there's a fit?

Either way, no pressure - happy to stay connected.

[Your Name]
```

**Message 4 (Day 14, final):**
```
Hi [Name],

Last message from me - I'll stop reaching out.

If you ever want to discuss [topic/challenge], 
I'm here.

Wishing you and the [Company] team continued success!

[Your Name]
```

### Phase 4: Content Strategy

**Weekly Content Mix:**
- 2 Educational posts (tips, frameworks)
- 1 Personal story/lesson
- 1 Social proof (case study, testimonial)
- 1 Engagement post (question, poll)

**Content Themes:**
- Day-to-day insights
- Client wins (anonymized if needed)
- Industry observations
- Personal journey/lessons
- Value-add content (tips, resources)

### Phase 5: Engagement Strategy

**Daily Activities:**
- Comment on 10 posts (target ICPs)
- Engage with your commenters
- Share relevant content
- React to ICP content

**Comment Formula:**
"[Observation about their point] + [Your perspective] + [Question or expansion]"

## Output Structure
```
.tmp/linkedin_outreach/{campaign_slug}/
├── profile/
│   ├── profile_optimization.md
│   └── featured_section.md
├── messages/
│   ├── connection_requests.md
│   └── follow_up_sequence.md
├── content/
│   ├── content_strategy.md
│   └── post_templates.md
├── engagement/
│   └── engagement_playbook.md
├── tracking/
│   └── metrics_template.csv
└── result.json
```

## Quality Gates

### Pre-Launch Checklist
- [ ] Profile optimized
- [ ] Messages personalized
- [ ] Daily limits set (20-30 connections)
- [ ] Content calendar created
- [ ] Tracking system ready
- [ ] Engagement strategy defined

### Performance Benchmarks
| Metric | Target |
|--------|--------|
| Connection acceptance | 30-40% |
| Response rate | 15-25% |
| Meeting book rate | 5-10% |
| Content engagement | 3-5% |

## Safety Guidelines

**DO:**
- Personalize every message
- Focus on value first
- Respect "no" or no response
- Stay within platform limits
- Build genuine relationships

**DON'T:**
- Send automated spam
- Pitch in connection request
- Follow up more than 4 times
- Exceed daily limits
- Use fake profiles
