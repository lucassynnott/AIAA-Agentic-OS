# Ultimate Cold Email Campaign Generator

## What This Workflow Is
**Complete end-to-end cold email campaign system** that handles everything from prospect research to campaign launch. Generates personalized email sequences, validates leads, sets up sending infrastructure, and manages inbox responses. The ultimate tool for B2B lead generation agencies.

## What It Does
1. Takes target ICP and offer details
2. Researches and builds qualified lead lists
3. Validates emails for deliverability
4. Generates hyper-personalized email sequences
5. Creates A/B test variations
6. Sets up sending schedules
7. Exports to Instantly/Smartlead format
8. Creates follow-up sequences based on engagement

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI personalization
PERPLEXITY_API_KEY=your_key           # Prospect research
APIFY_API_TOKEN=your_key              # LinkedIn scraping (optional)
```

### Required Skill Bibles
- `SKILL_BIBLE_cold_email_mastery.md`
- `SKILL_BIBLE_cold_email_infrastructure.md`
- `SKILL_BIBLE_email_deliverability.md`
- `SKILL_BIBLE_cold_email_script_writing.md`
- `SKILL_BIBLE_ai_mass_personalization.md`
- `SKILL_BIBLE_lead_list_building.md`

## How to Run

```bash
# Full campaign generation
python3 execution/generate_cold_email_campaign.py \
  --sender-name "John Smith" \
  --sender-company "Growth Agency" \
  --offer "Lead generation for B2B SaaS" \
  --target-icp "Marketing directors at SaaS companies, 50-200 employees" \
  --lead-source "linkedin" \
  --lead-count 500 \
  --sequence-length 5 \
  --personalization-level "high"

# Quick campaign (existing leads)
python3 execution/generate_cold_email_campaign.py \
  --leads-file leads.csv \
  --offer "AI automation services" \
  --sequence-length 3 \
  --output-format "instantly"
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sender-name | string | Yes | Your name |
| sender-company | string | Yes | Your company name |
| offer | string | Yes | What you're selling |
| target-icp | string | Yes | Ideal customer profile |
| lead-source | enum | No | "linkedin", "apollo", "manual" |
| lead-count | int | No | Number of leads to find |
| leads-file | path | No | Existing leads CSV |
| sequence-length | int | No | 3, 5, or 7 emails |
| personalization-level | enum | No | "low", "medium", "high" |
| output-format | enum | No | "instantly", "smartlead", "csv" |

## Process

### Phase 1: Lead Research & Building (if no leads file)
1. Parse ICP into searchable criteria
2. Use Perplexity to find target companies
3. Scrape LinkedIn for decision makers
4. Enrich with company data (size, revenue, tech stack)
5. Validate email addresses

**Quality Gates:**
- [ ] Minimum 80% email validation rate
- [ ] All leads match ICP criteria
- [ ] Company data enrichment complete

### Phase 2: Personalization Research
For each lead, AI researches:
- Recent company news/funding
- LinkedIn activity/posts
- Company pain points
- Mutual connections
- Tech stack/tools used

**Output:** Personalization data JSON per lead

### Phase 3: Email Sequence Generation
Using skill bibles, generate:

**Email 1: Pattern Interrupt**
- Personalized opening line
- Clear value proposition
- Soft CTA (reply/question)

**Email 2: Case Study**
- Reference relevant result
- Similar company success story
- Social proof

**Email 3: Value Add**
- Free resource/insight
- Industry observation
- Authority positioning

**Email 4: FOMO/Urgency**
- Limited spots/time
- Competitor mention
- Pain amplification

**Email 5: Breakup**
- Last chance messaging
- Direct ask
- Clear next step

### Phase 4: A/B Testing Setup
Generate variations for:
- Subject lines (3 per email)
- Opening lines (2 per email)
- CTAs (2 per email)

### Phase 5: Export & Scheduling
- Format for Instantly/Smartlead
- Set optimal send times
- Configure follow-up delays
- Export campaign files

## Output Structure
```
.tmp/cold_email_campaigns/{campaign_name}/
├── leads/
│   ├── leads_validated.csv
│   ├── leads_enriched.json
│   └── personalization_data.json
├── sequences/
│   ├── sequence_main.md
│   ├── sequence_a_test.md
│   └── sequence_b_test.md
├── exports/
│   ├── instantly_import.csv
│   ├── smartlead_import.csv
│   └── subject_line_variants.csv
├── analytics/
│   └── campaign_summary.json
└── result.json
```

## Email Templates (Skill Bible Integration)

### High-Converting Cold Email Framework
From `SKILL_BIBLE_cold_email_mastery.md`:

**Subject Line Formulas:**
- "Quick question about [specific thing]"
- "[Mutual connection] mentioned you"
- "Idea for [company name]"
- "[Competitor] is doing this..."

**Opening Lines:**
- Personalized observation about their company
- Reference to recent achievement/news
- Mutual connection or shared experience
- Industry-specific insight

**Body Structure:**
- 1 sentence problem identification
- 1 sentence solution hint
- 1 sentence credibility (subtle)
- 1 sentence CTA (question, not ask)

**CTA Types:**
- "Does this resonate?"
- "Worth a quick chat?"
- "Would this help?"
- "Interested in learning more?"

## Quality Gates

### Pre-Launch Checklist
- [ ] All emails under 100 words
- [ ] Subject lines under 40 characters
- [ ] No spam trigger words
- [ ] Personalization tokens filled
- [ ] Unsubscribe link included
- [ ] Sender domain warmed up
- [ ] SPF/DKIM/DMARC configured

### Campaign Metrics Targets
- Open rate: 45%+
- Reply rate: 8%+
- Positive reply rate: 3%+
- Meeting book rate: 1%+

## Error Handling

| Error | Solution |
|-------|----------|
| Lead scraping fails | Fall back to manual CSV import |
| Email validation <80% | Re-verify with secondary service |
| AI generation fails | Use template fallbacks |
| Export format error | Validate CSV structure |

## Integration with Other Workflows

- `ai_prospect_researcher.md` - Deep prospect research
- `company_market_research.md` - Company analysis
- `follow_up_sequence.md` - Post-reply automation
- `sales_call_summarizer.md` - Meeting notes

## Self-Annealing Notes

### What Works
- Personalized first lines increase replies 3x
- 3-5 email sequences outperform longer ones
- Morning sends (8-10am) get best opens
- Tuesday-Thursday optimal send days

### What Doesn't Work
- Generic templates (low reply rates)
- Long emails (>150 words)
- Multiple CTAs per email
- Aggressive/salesy language

### Continuous Improvement
- Track which personalization types perform best
- A/B test subject line formulas
- Monitor deliverability scores
- Update templates based on reply patterns
