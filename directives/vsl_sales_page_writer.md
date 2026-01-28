# VSL Sales Page Writer

## What This Workflow Is
Generates high-converting sales page copy to accompany VSL, including headline, subhead, video embed section, bullet points, testimonials, offer details, and CTA buttons.

## What It Does
1. Receives VSL script and market research
2. Creates compelling headline + subhead
3. Writes benefit bullets below video
4. Formats testimonials section
5. Creates offer/pricing section
6. Writes FAQ section addressing objections
7. Generates strong CTA copy
8. Outputs HTML-ready copy

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key
```

### Required Skills
- `skills/SKILL_BIBLE_funnel_copywriting_mastery.md`
- `skills/SKILL_BIBLE_copywriting_fundamentals.md`

## Inputs
- `vslScript` (from VSL Script Writer)
- `researchData` (from Market Research)
- `pageStyle`: "minimal" | "full" | "long-form"

## Process
1. Extract key elements from VSL script (hook, mechanism, results)
2. Create 3 headline options (curiosity, benefit, social proof)
3. Write pre-video copy (pattern interrupt + promise)
4. Generate post-video bullets (transformation, features, bonuses)
5. Format social proof section
6. Write guarantee copy
7. Create multiple CTA variations
8. Add FAQ section (top 5-7 objections)

## Outputs
- Sales page copy (Markdown + HTML)
- 3 headline options for A/B testing
- Multiple CTA button copy variations

## Integration
Position 3/7 in VSL funnel pipeline.
**Inputs:** VSL script, research → **Outputs:** Sales page copy → Email sequence writer

## Related Skill Bibles

**[SKILL_BIBLE_landing_page_ai_mastery.md](../skills/SKILL_BIBLE_landing_page_ai_mastery.md)** (PRIMARY)
- Complete landing page optimization framework
- AI-powered content creation and design automation
- Conversion-first design philosophy
- Mobile-first responsive design principles
- A/B testing and optimization methodologies

**[SKILL_BIBLE_funnel_copywriting_mastery.md](../skills/SKILL_BIBLE_funnel_copywriting_mastery.md)**
- Sales page structure and flow
- Conversion element placement
- CTA optimization

**[SKILL_BIBLE_hormozi_marketing_mastery.md](../skills/SKILL_BIBLE_hormozi_marketing_mastery.md)**
- Landing page psychology
- Headline formulas
- Conversion optimization

**[SKILL_BIBLE_hormozi_10x_sales_process.md](../skills/SKILL_BIBLE_hormozi_10x_sales_process.md)**
- 10x revenue sales process
- Offer presentation
- Value communication

**[SKILL_BIBLE_hormozi_customer_acquisition_fast.md](../skills/SKILL_BIBLE_hormozi_customer_acquisition_fast.md)**
- Fast customer acquisition
- Sales page optimization
- Trust building elements
