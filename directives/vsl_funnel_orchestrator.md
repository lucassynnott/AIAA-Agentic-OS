# VSL Funnel Orchestrator (Master Workflow)

## What This Workflow Is
**Master orchestrator** that coordinates the complete VSL funnel creation pipeline. Single entry point that triggers all sub-workflows in sequence, manages data flow, handles errors, and delivers final outputs.

## What It Does
1. Receives company and offer details from user
2. Triggers market research workflow (Perplexity)
3. Triggers VSL script writer (uses research)
4. Triggers sales page writer (uses research + script)
5. Triggers email sequence writer (uses all previous outputs)
6. Triggers Google Doc creator for all deliverables
7. Triggers Slack notifier with completion status
8. Returns all document links and execution metadata

## Prerequisites

### Required API Keys (add to .env)
```
PERPLEXITY_API_KEY=your_perplexity_key    # Market research
OPENROUTER_API_KEY=your_openrouter_key    # AI generation
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # Doc creation
SLACK_WEBHOOK_URL=your_slack_webhook      # Notifications
```

### Required Skill Bibles
All skill bibles loaded by sub-workflows:
- `SKILL_BIBLE_vsl_writing_production.md`
- `SKILL_BIBLE_vsl_script_mastery_fazio.md`
- `SKILL_BIBLE_funnel_copywriting_mastery.md`
- `SKILL_BIBLE_cold_email_mastery.md`
- `SKILL_BIBLE_email_campaign_copy_design.md`

### Installation
```bash
pip install anthropic openai requests google-api-python-client
```

## How to Run

### Option 1: Via Trigger.dev (Recommended)
```bash
python3 execution/test_trigger_task.py \
  --task-id vsl-funnel-orchestrator \
  --payload '{
    "company": "Acme Corp",
    "website": "https://acmecorp.com",
    "offer": "B2B Lead Generation System",
    "pricePoint": "$1,997/mo",
    "industry": "Marketing Agency",
    "vslLength": "medium",
    "vslStyle": "education"
  }' \
  --wait
```

### Option 2: Direct Python Execution
```bash
python3 execution/generate_complete_vsl_funnel.py \
  --company "Acme Corp" \
  --website "https://acmecorp.com" \
  --offer "B2B Lead Generation System" \
  --price "$1,997/mo"
```

### Option 3: Simple One-Liner
```bash
python3 execution/generate_complete_vsl_funnel.py \
  --company "[COMPANY]" \
  --website "[URL]" \
  --offer "[OFFER]"
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| company | string | Yes | Company name |
| website | string | Yes | Company website URL |
| offer | string | Yes | Product/service being sold |
| pricePoint | string | No | Price ($XXX or range) |
| industry | string | No | Industry/niche |
| targetAudience | string | No | Known audience details |
| vslLength | enum | No | "short", "medium", "long" (default: "medium") |
| vslStyle | enum | No | "education", "story", "case-study" (default: "education") |
| emailSequenceLength | number | No | 5 or 7 emails (default: 7) |
| urgencyType | enum | No | "scarcity", "time-limited", "bonus-stack" |
| googleFolderId | string | No | Drive folder for documents |
| slackChannel | string | No | Slack channel for notification |

## Process

### Step 1: Validate Inputs
**Quality Gate:**
- [ ] Company name provided
- [ ] Website URL is valid and accessible
- [ ] Offer description is clear (not generic)
- [ ] All required API keys configured

**Error Handling:**
- Missing inputs → Return clear error message
- Invalid website → Proceed with Perplexity search only
- Missing API keys → Fail fast with configuration instructions

### Step 2: Market Research (Workflow #1)
**Trigger:** `company_market_research` workflow

**Inputs:**
```json
{
  "company": "Acme Corp",
  "website": "https://acmecorp.com",
  "offer": "B2B Lead Generation System",
  "industry": "Marketing Agency",
  "pricePoint": "$1,997/mo"
}
```

**Outputs:**
```json
{
  "company": {...},
  "offer": {...},
  "targetAudience": {...},
  "transformation": {...},
  "socialProof": {...},
  "competitors": [...],
  "messaging": {...}
}
```

**Quality Gate:**
- [ ] Research completed successfully
- [ ] Minimum 3 pain points identified
- [ ] At least 1 social proof element found
- [ ] Target audience clearly defined

**Error Handling:**
- Research fails → Retry once, then fail workflow
- Limited data → Continue with warning flag
- No social proof → Proceed but flag for manual collection

**Checkpoint:** Save research to `.tmp/vsl_funnel_{company_slug}/01_research.json`

### Step 3: VSL Script Writer (Workflow #2)
**Trigger:** `vsl_script_writer` workflow

**Inputs:**
```json
{
  "researchData": {...},  // from Step 2
  "vslLength": "medium",
  "vslStyle": "education"
}
```

**Outputs:**
```json
{
  "fullScript": "...",  // Markdown with delivery notes
  "hookOptions": [...],  // 3 hook variations
  "scriptMetadata": {
    "wordCount": 1847,
    "estimatedLength": "13:45",
    "proofPoints": 4
  }
}
```

**Quality Gate:**
- [ ] Script follows 10-part structure
- [ ] Hook options generated (3 variations)
- [ ] Minimum 3 proof points included
- [ ] Script length within target (±2 min)

**Error Handling:**
- Script generation fails → Retry with adjusted parameters
- Quality gate fails → Regenerate problematic section

**Checkpoint:** Save script to `.tmp/vsl_funnel_{company_slug}/02_vsl_script.md`

### Step 4: Sales Page Writer (Workflow #3)
**Trigger:** `vsl_sales_page_writer` workflow

**Inputs:**
```json
{
  "vslScript": {...},  // from Step 3
  "researchData": {...},  // from Step 2
  "pageStyle": "full"
}
```

**Outputs:**
```json
{
  "salesPageCopy": "...",  // Full page copy (Markdown)
  "headlineOptions": [...],  // 3 variations
  "ctaVariations": [...],  // Multiple CTA options
  "faqSection": "..."
}
```

**Quality Gate:**
- [ ] Headline options generated (3 variations)
- [ ] Benefit bullets match VSL script
- [ ] Testimonials section included
- [ ] CTA is clear and specific
- [ ] FAQ addresses top objections

**Checkpoint:** Save to `.tmp/vsl_funnel_{company_slug}/03_sales_page.md`

### Step 5: Email Sequence Writer (Workflow #4)
**Trigger:** `vsl_email_sequence_writer` workflow

**Inputs:**
```json
{
  "vslScript": {...},  // from Step 3
  "salesPageCopy": {...},  // from Step 4
  "researchData": {...},  // from Step 2
  "sequenceLength": 7
}
```

**Outputs:**
```json
{
  "emails": [
    {
      "emailNumber": 1,
      "subject": "...",
      "subjectVariation": "...",
      "body": "...",
      "cta": "...",
      "sendTiming": "immediate"
    },
    // ... 6 more emails
  ],
  "sequenceMetadata": {
    "totalEmails": 7,
    "frequency": "daily"
  }
}
```

**Quality Gate:**
- [ ] All 7 emails generated
- [ ] Each email has 2 subject line options
- [ ] Email progression logical (value → urgency)
- [ ] CTAs clear in every email

**Checkpoint:** Save to `.tmp/vsl_funnel_{company_slug}/04_email_sequence.md`

### Step 6: Google Doc Creation (Workflow #5)
**Trigger:** `google_doc_creator` workflow (4 times in parallel)

**Document 1: Market Research**
```json
{
  "content": "...",  // from Step 2
  "title": "Acme Corp - Market Research",
  "folderId": "...",
  "shareWith": []
}
```

**Document 2: VSL Script**
```json
{
  "content": "...",  // from Step 3
  "title": "Acme Corp - VSL Script",
  "folderId": "...",
  "shareWith": []
}
```

**Document 3: Sales Page Copy**
```json
{
  "content": "...",  // from Step 4
  "title": "Acme Corp - Sales Page",
  "folderId": "...",
  "shareWith": []
}
```

**Document 4: Email Sequence**
```json
{
  "content": "...",  // from Step 5
  "title": "Acme Corp - Email Sequence (7 emails)",
  "folderId": "...",
  "shareWith": []
}
```

**Outputs:**
```json
{
  "documents": [
    {
      "title": "Acme Corp - Market Research",
      "url": "https://docs.google.com/document/d/abc123/edit"
    },
    {
      "title": "Acme Corp - VSL Script",
      "url": "https://docs.google.com/document/d/def456/edit"
    },
    {
      "title": "Acme Corp - Sales Page",
      "url": "https://docs.google.com/document/d/ghi789/edit"
    },
    {
      "title": "Acme Corp - Email Sequence",
      "url": "https://docs.google.com/document/d/jkl012/edit"
    }
  ]
}
```

**Quality Gate:**
- [ ] All 4 documents created successfully
- [ ] Documents formatted correctly
- [ ] Shareable links working

**Error Handling:**
- Google API error → Retry 3 times
- Still failing → Save as local Markdown files instead
- Continue to Slack notification

### Step 7: Slack Notification (Workflow #6)
**Trigger:** `slack_notifier` workflow

**Inputs:**
```json
{
  "workflowName": "VSL Funnel Complete",
  "status": "success",
  "company": "Acme Corp",
  "deliverables": [
    {
      "name": "Market Research",
      "url": "https://docs.google.com/document/d/abc123/edit"
    },
    {
      "name": "VSL Script",
      "url": "https://docs.google.com/document/d/def456/edit"
    },
    {
      "name": "Sales Page Copy",
      "url": "https://docs.google.com/document/d/ghi789/edit"
    },
    {
      "name": "Email Sequence (7 emails)",
      "url": "https://docs.google.com/document/d/jkl012/edit"
    }
  ],
  "metadata": {
    "executionTime": "4m 32s",
    "vslLength": "13:45 (estimated)",
    "emailCount": 7
  }
}
```

**Output:** Slack message sent

**Error Handling:**
- Slack webhook fails → Log error but don't fail workflow
- Notification is non-critical, workflow still succeeds

### Step 8: Return Final Output
**Orchestrator Returns:**
```json
{
  "success": true,
  "company": "Acme Corp",
  "offer": "B2B Lead Generation System",
  "executionTime": "4m 32s",
  "deliverables": {
    "marketResearch": {
      "file": ".tmp/vsl_funnel_acme_corp/01_research.json",
      "doc": "https://docs.google.com/document/d/abc123/edit"
    },
    "vslScript": {
      "file": ".tmp/vsl_funnel_acme_corp/02_vsl_script.md",
      "doc": "https://docs.google.com/document/d/def456/edit",
      "estimatedLength": "13:45"
    },
    "salesPage": {
      "file": ".tmp/vsl_funnel_acme_corp/03_sales_page.md",
      "doc": "https://docs.google.com/document/d/ghi789/edit"
    },
    "emailSequence": {
      "file": ".tmp/vsl_funnel_acme_corp/04_email_sequence.md",
      "doc": "https://docs.google.com/document/d/jkl012/edit",
      "emailCount": 7
    }
  },
  "errors": [],
  "warnings": [
    "Limited social proof found (2 elements, recommended: 3+)"
  ]
}
```

## Quality Gates (Master Workflow)

### Pre-Execution Checklist
- [ ] All required API keys configured
- [ ] Input validation passed
- [ ] Skill bibles accessible
- [ ] Google OAuth authenticated

### Post-Execution Validation
- [ ] All 6 sub-workflows completed
- [ ] 4 Google Docs created
- [ ] Slack notification sent
- [ ] No critical errors
- [ ] Execution time < 10 minutes

## Error Handling Strategy

| Error Type | Strategy |
|------------|----------|
| Research fails | Retry once → Fail workflow |
| VSL generation fails | Retry with adjusted params → Fail workflow |
| Sales page fails | Retry → Continue with VSL only |
| Email sequence fails | Retry → Continue with partial deliverables |
| Google Docs fails | Save local files → Continue |
| Slack notification fails | Log error → Workflow still succeeds |

**Philosophy:** Fail fast on critical workflows (research, VSL), degrade gracefully on delivery workflows (Docs, Slack).

## Edge Cases

### Edge Case 1: Partial Data Scenario
**Problem:** Research returns limited information (no social proof, few pain points).

**Solution:**
- Flag warnings in research output
- VSL script adapts (more mechanism focus, less proof stack)
- Email sequence emphasizes logic over testimonials
- Notify user via Slack about manual data collection needed

### Edge Case 2: API Rate Limiting
**Problem:** Perplexity or OpenRouter rate limits hit mid-execution.

**Solution:**
- Implement exponential backoff (wait 10s, 30s, 60s)
- Checkpoint each workflow completion (can resume)
- If all retries exhausted, pause and notify user
- Provide resume capability with checkpoint data

### Edge Case 3: Very High/Low Price Points
**Problem:** $100 offer or $50K offer requires different approaches.

**Adjustments:**
- Low price ($100-$500): Shorter VSL ("short"), fewer objections
- Mid price ($1K-$10K): Standard approach ("medium")
- High price ($10K+): Longer VSL ("long"), more credibility/proof

Pass price adjustment automatically based on detected/provided price.

### Edge Case 4: Multiple Parallel Requests
**Problem:** User triggers multiple VSL funnels simultaneously.

**Solution:**
- Each execution isolated with unique ID (`vsl_funnel_{company_slug}_{timestamp}`)
- Separate .tmp directories
- Separate Google Drive folders
- Queue if necessary (Trigger.dev handles concurrency)

## Success Metrics

- **End-to-End Success Rate:** 95%+
- **Average Execution Time:** 4-6 minutes
- **User Satisfaction:** Deliverables require minimal editing
- **Downstream Conversion:** VSL/funnel performs (tracked separately)

## Integration with Trigger.dev

This orchestrator is **perfect for Trigger.dev** because:

1. **Long-running:** 4-6 minute execution with checkpoints
2. **Multiple steps:** 6 sequential workflows with data passing
3. **Error handling:** Retries, graceful degradation
4. **Observability:** Full execution logs per workflow
5. **Human-in-loop (optional):** Can add approval after research

**Trigger.dev Benefits:**
- Automatic retries on sub-workflow failures
- Checkpoint-resume if mid-execution failure
- Full execution trace in dashboard
- Webhook triggering from external forms

## Self-Annealing Notes

### What Works Well
- Sequential pipeline with checkpoints prevents data loss
- Parallel Google Doc creation saves time
- Graceful degradation keeps workflow completing
- Slack notification provides instant visibility

### What Doesn't Work
- Skipping research produces generic outputs
- Running all in one prompt creates inconsistent quality
- No error handling causes complete failures

### Improvements Over Time
- Add human approval checkpoint after research
- Cache similar company research (avoid duplicate Perplexity calls)
- Build feedback loop (track which VSLs convert best)
- Create industry-specific templates (SaaS, agency, ecommerce)
- Add A/B testing capability (generate 2 VSL variations)

## Related Directives

- [company_market_research.md](./company_market_research.md) - Workflow #1
- [vsl_script_writer.md](./vsl_script_writer.md) - Workflow #2
- [vsl_sales_page_writer.md](./vsl_sales_page_writer.md) - Workflow #3
- [vsl_email_sequence_writer.md](./vsl_email_sequence_writer.md) - Workflow #4
- [google_doc_creator.md](./google_doc_creator.md) - Workflow #5
- [slack_notifier.md](./slack_notifier.md) - Workflow #6

## Related Skill Bibles

Load these skill bibles for complete VSL funnel creation:

**[SKILL_BIBLE_landing_page_ai_mastery.md](../skills/SKILL_BIBLE_landing_page_ai_mastery.md)** (PRIMARY FOR LANDING PAGES)
- Complete landing page optimization framework
- AI-powered content creation and design automation
- Conversion-first design philosophy
- Mobile-first responsive design principles
- A/B testing and optimization methodologies

**[SKILL_BIBLE_vsl_writing_production.md](../skills/SKILL_BIBLE_vsl_writing_production.md)**
- 10-part VSL structure framework
- Hook formulas and pattern interrupts
- Direct response principles

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- 14 years of marketing advice
- Funnel strategy principles
- Conversion psychology

**[SKILL_BIBLE_hormozi_sales_training.md](../skills/SKILL_BIBLE_hormozi_sales_training.md)**
- Ultimate sales training framework
- Objection handling for VSL scripts
- Closing psychology

**[SKILL_BIBLE_hormozi_email_marketing_complete.md](../skills/SKILL_BIBLE_hormozi_email_marketing_complete.md)**
- Complete email marketing framework
- Follow-up sequence optimization
- Revenue-driving email tactics

**[SKILL_BIBLE_hormozi_10x_pricing.md](../skills/SKILL_BIBLE_hormozi_10x_pricing.md)**
- Pricing psychology for offers
- Value stack creation
- Premium positioning in funnels
