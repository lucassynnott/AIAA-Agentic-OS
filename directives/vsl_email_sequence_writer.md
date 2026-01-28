# VSL Email Sequence Writer

## What This Workflow Is
Generates 5-7 email nurture sequence for VSL funnel viewers who didn't book immediately. Includes indoctrination, value delivery, objection handling, and urgency escalation.

## What It Does
1. Receives research, VSL script, and sales page copy
2. Generates 7-email sequence:
   - Email 1: "Did you watch?" (immediate follow-up)
   - Email 2: Indoctrination (your story/credentials)
   - Email 3: Case study deep dive
   - Email 4: Mechanism explanation
   - Email 5: Objection crusher
   - Email 6: Urgency reminder (spots filling)
   - Email 7: Last chance (deadline)
3. Each email has: subject line, preview text, body copy, PS, CTA
4. Outputs ready-to-use email copy

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key
```

### Required Skills
- `skills/SKILL_BIBLE_cold_email_mastery.md`
- `skills/SKILL_BIBLE_value_dense_emails.md`
- `skills/SKILL_BIBLE_email_campaign_copy_design.md`

## Inputs
- `vslScript` (from VSL Writer)
- `salesPageCopy` (from Sales Page Writer)
- `researchData` (from Market Research)
- `sequenceLength`: 5 | 7 (default: 7)
- `emailFrequency`: "daily" | "every-other-day"

## Process
1. Load skill bible email frameworks
2. Extract key elements (mechanism, objections, proof)
3. Generate Email 1 (immediate, "did you watch?")
4. Generate Email 2-3 (value, indoctrination)
5. Generate Email 4-5 (mechanism deep dive, objections)
6. Generate Email 6-7 (urgency, last chance)
7. Create 2 subject line options per email
8. Add PS sections with secondary CTAs

## Outputs
- 7 complete emails (Markdown format)
- Subject line variations (2 per email)
- Email metadata (send timing, segmentation)

## Integration
Position 4/7 in VSL funnel pipeline.
**Inputs:** Research, VSL script, sales page → **Outputs:** Email sequence → Google Doc Creator

## Related Skill Bibles

### PRIMARY: Max Sturtevant's $40M+ Email Methodology

**[SKILL_BIBLE_sturtevant_email_master_system.md](../skills/SKILL_BIBLE_sturtevant_email_master_system.md)** ⭐ ESSENTIAL
- Complete email system (6,968 words)
- SCE Framework (Skimmable, Clear, Engaging)
- 75-word max body copy rule

**[SKILL_BIBLE_sturtevant_copywriting.md](../skills/SKILL_BIBLE_sturtevant_copywriting.md)** ⭐ FOR SEQUENCES
- Email copywriting formulas (5,395 words)
- Subject line swipe files
- CTA optimization

**[SKILL_BIBLE_sturtevant_welcome_flow.md](../skills/SKILL_BIBLE_sturtevant_welcome_flow.md)**
- Sequence structure blueprint (7,281 words)
- Value-first positioning
- Educational email tactics

### SUPPLEMENTARY: Sales Psychology

**[SKILL_BIBLE_hormozi_email_marketing_complete.md](../skills/SKILL_BIBLE_hormozi_email_marketing_complete.md)**
- Sales psychology for email
- Urgency and scarcity frameworks

**[SKILL_BIBLE_hormozi_sales_training.md](../skills/SKILL_BIBLE_hormozi_sales_training.md)**
- Objection handling for email copy
- Closing psychology in written form
