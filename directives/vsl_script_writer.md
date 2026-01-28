# VSL Script Writer

## What This Workflow Is
This workflow generates high-converting VSL (Video Sales Letter) scripts using proven direct response frameworks from the VSL Writing & Production Mastery skill bible. Optimized for B2B service businesses selling $1K-$20K offers.

## What It Does
1. Receives market research dossier and offer details
2. Loads VSL skill bible frameworks
3. Generates 3 powerful hook options using different psychological triggers
4. Writes complete VSL script following 10-part structure
5. Includes pattern interrupts, proof elements, and objection handling
6. Outputs structured script with timestamps and delivery notes
7. Returns formatted script ready for teleprompter

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key    # For Claude Opus 4.5
ANTHROPIC_API_KEY=your_anthropic_key      # Alternative
```

### Required Skill Bibles
- `skills/SKILL_BIBLE_vsl_writing_production.md` - 10-part framework
- `skills/SKILL_BIBLE_vsl_script_mastery_fazio.md` - Advanced techniques
- `skills/SKILL_BIBLE_funnel_copywriting_mastery.md` - Direct response principles

### Required Tools
- Python 3.10+
- Access to Claude Opus 4.5 (via OpenRouter or Anthropic)

### Installation
```bash
pip install anthropic openai
```

## How to Run

### Option 1: Standalone (with research file)
```bash
python3 execution/generate_vsl_script.py \
  --research .tmp/research/acme_corp.json \
  --length "medium" \
  --style "education" \
  --output .tmp/vsl/acme_vsl_script.md
```

### Option 2: Via Trigger.dev (orchestrated)
```bash
python3 execution/test_trigger_task.py \
  --task-id vsl-script-writer \
  --payload '{
    "researchData": {...},
    "vslLength": "medium",
    "vslStyle": "education"
  }' \
  --wait
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| researchData | object | Yes | Market research dossier from previous workflow |
| vslLength | string | No | "mini" (1000+ words, 7-10min), "medium" (3000+ words, 20-25min), "long" (10,000+ words, 60+ min) |
| vslStyle | string | No | "education", "story", "case-study" |
| pricePoint | string | No | Explicit price if not in research |
| urgencyType | string | No | "scarcity", "time-limited", "bonus-stack" |

## VSL Length Standards

| Length | Minimum Words | Target Range | Duration | Use Case |
|--------|---------------|--------------|----------|----------|
| **Mini** | 1,000 | 1,000-1,500 | 7-10 min | Low-ticket offers ($100-$500), quick wins |
| **Medium (DEFAULT)** | 3,000 | 3,000-4,000 | 20-25 min | Mid-ticket offers ($1K-$5K), standard B2B |
| **Long** | 10,000 | 10,000-15,000 | 60-90 min | High-ticket ($10K+), complex transformations |

## Process

### Step 1: Load Context
Load all required skill bibles and extract frameworks:
- 10-part VSL structure
- Hook formulas (7 types)
- Problem agitation techniques
- Proof stack methodologies
- CTA frameworks

### Step 2: Generate Hook Options
Create 3 different hooks using proven formulas:

**Hook Formula 1: Bold Claim + Curiosity**
```
"What if I told you that [BOLD RESULT] without [COMMON PAIN]?
In the next [X] minutes, I'm going to show you exactly how..."
```

**Hook Formula 2: Pattern Interrupt + Question**
```
"Stop me if you've heard this before: [COMMON SCENARIO]...
Here's why that's completely backwards..."
```

**Hook Formula 3: Social Proof + Promise**
```
"I've helped [X] companies in [INDUSTRY] achieve [RESULT].
And today I'm going to share the exact system..."
```

**Output:** 3 hook variations with psychological trigger notes

### Step 3: Structure VSL Script (10-Part Framework)

**Part 1: Hook (0:00-0:30)**
- Selected hook from Step 2
- Pattern interrupt
- Avatar identification
- Curiosity gap

**Part 2: Problem Identification (0:30-2:00)**
- Mirror internal dialogue
- Agitate top 3 pain points from research
- "You've probably tried..." (list failed solutions)
- Validate their frustration

**Part 3: Credibility (2:00-3:00)**
- Brief authority establishment
- Social proof intro (metrics)
- "I've been where you are"
- Transition to solution

**Part 4: Solution Introduction (3:00-4:00)**
- Name the mechanism/system
- High-level overview
- Why it works (unique insight)
- Differentiation from competitors

**Part 5: Mechanism Deep Dive (4:00-8:00)**
- How it works (3-5 steps)
- Why each step matters
- Proof for each claim
- Address obvious objections

**Part 6: Social Proof Stack (8:00-10:00)**
- Case study 1 (most impressive result)
- Case study 2-3 (relatable results)
- Testimonial montage
- Results timeline

**Part 7: Offer Reveal (10:00-12:00)**
- What you get (core offer)
- Bonus stack (value building)
- Total value calculation
- Price reveal with context

**Part 8: Urgency & Scarcity (12:00-13:00)**
- Limited spots/time reason
- What happens if they wait
- Missed opportunity cost
- Deadline clear

**Part 9: Guarantee (13:00-13:30)**
- Risk reversal
- Clear terms
- Confidence statement
- Remove buying fear

**Part 10: Call to Action (13:30-15:00)**
- Clear next step (book call)
- What happens on the call
- Final urgency reminder
- Button/calendar link

### Step 4: Add Delivery Notes
For each section, add:
- Recommended tone/pacing
- Emphasis points (BOLD)
- Pause indicators (...)
- Graphics/B-roll suggestions
- On-screen text cues

### Step 5: Quality Gate Validation
Check script against skill bible requirements:
- [ ] Hook stops scroll within 3 seconds
- [ ] Problem agitation is specific (not generic)
- [ ] Mechanism has unique name/insight
- [ ] At least 3 proof elements included
- [ ] Price anchored with value stack
- [ ] CTA is clear and specific
- [ ] Script length matches target
- [ ] All claims have supporting evidence

### Step 6: Format Output
Generate two versions:
1. **Teleprompter Version** - Clean script, large text, pauses marked
2. **Production Version** - Full script with delivery notes, graphics cues, timestamps

## Quality Gates

### Pre-Generation Validation
- [ ] Research dossier loaded successfully
- [ ] At least 3 pain points available
- [ ] At least 1 social proof element present
- [ ] Offer mechanism clearly defined
- [ ] Skill bibles loaded into context

### Post-Generation Validation
- [ ] Script follows 10-part structure
- [ ] Hook tested against 3-second rule
- [ ] Minimum 3 case studies/proof points
- [ ] Price reveal has proper value stacking
- [ ] CTA specifies exact next step
- [ ] Length matches target (±2 minutes)
- [ ] Tone appropriate for B2B audience
- [ ] No generic platitudes or fluff

## Outputs

### 1. Full VSL Script (Markdown)
```markdown
# VSL Script: [Company] - [Offer]

**Target Length:** 12-15 minutes
**Style:** Education-based
**Generated:** 2026-01-05

---

## HOOK (0:00-0:30)

[Selected hook with delivery notes]

**Graphics:** Show [specific visual]
**Tone:** Confident, curious

---

## PROBLEM (0:30-2:00)

[Problem agitation section]

**On-screen text:** "Sound familiar?"

---

[Continue through all 10 parts...]
```

### 2. Hook Options Document
```markdown
# Hook Options for [Company]

## Option 1: Bold Claim (Recommended)
[Hook text]
**Why this works:** [psychological trigger]

## Option 2: Pattern Interrupt
[Hook text]
**Why this works:** [psychological trigger]

## Option 3: Social Proof
[Hook text]
**Why this works:** [psychological trigger]
```

### 3. Script Metadata (JSON)
```json
{
  "scriptId": "vsl_acme_20260105",
  "company": "Acme Corp",
  "offer": "B2B Lead Generation System",
  "targetLength": "12-15 minutes",
  "actualWordCount": 1847,
  "estimatedLength": "13:45",
  "style": "education",
  "hookSelected": "option1",
  "proofPoints": 4,
  "painPointsAddressed": 3,
  "generatedAt": "2026-01-05T12:00:00Z"
}
```

## Integration with VSL Funnel Pipeline

Position in pipeline:
```
1. Market Research ✅
   ↓
2. VSL Script Writer (this workflow) ← You are here
   ↓
3. Sales Page Writer
   ↓
4. Email Sequence Writer
   ↓
5. Google Doc Creator
   ↓
6. Slack Notifier
```

**Inputs:** Research dossier from workflow #1
**Outputs:** VSL script passed to workflow #3 (sales page)

## Edge Cases

### Edge Case 1: Limited Social Proof
**Scenario:** Research found <2 case studies.

**Solution:**
- Use indirect proof (industry statistics)
- Leverage founder credentials
- Reference similar company results
- Focus more on mechanism/logic
- Flag for manual social proof collection

### Edge Case 2: Complex Technical Offer
**Scenario:** Highly technical B2B SaaS or service.

**Solution:**
- Simplify mechanism into 3-step process
- Use analogies from research
- Focus on business outcomes over features
- Add "how it works" visual suggestions
- Create glossary section for production

### Edge Case 3: Very High Price Point ($10K+)
**Scenario:** Premium offer requiring trust building.

**Solution:**
- Extend credibility section (3-5 minutes)
- Add more proof stack elements
- Emphasize risk reversal heavily
- Include implementation/onboarding details
- Recommend "long" VSL format (20-25 min)

### Edge Case 4: Multiple Target Avatars
**Scenario:** Offer serves different customer types.

**Solution:**
- Create separate scripts per avatar
- OR use "whether you're [AVATAR A] or [AVATAR B]" framing
- Focus on universal pain points first
- Branch proof stack by avatar
- Consider modular script with avatar-specific sections

## Success Metrics

- Script generation time: 2-3 minutes
- Hook selection confidence: >80%
- Script structure adherence: 100%
- Quality gate pass rate: 95%+
- Estimated vs actual VSL length: ±10%
- Downstream workflow success (sales page generation): 90%+

## Skill Bible Integration

This directive directly implements frameworks from:

**[SKILL_BIBLE_vsl_writing_production.md](../skills/SKILL_BIBLE_vsl_writing_production.md)**
- 10-part VSL structure (sections 3)
- Hook formulas (section 3.1)
- Direct response principles (section 2)
- Proof stacking (section 3.6)

**[SKILL_BIBLE_vsl_script_mastery_fazio.md](../skills/SKILL_BIBLE_vsl_script_mastery_fazio.md)**
- Advanced pattern interrupts
- Objection handling sequences
- Tonality and pacing guidelines

**[SKILL_BIBLE_funnel_copywriting_mastery.md](../skills/SKILL_BIBLE_funnel_copywriting_mastery.md)**
- Value stacking methodology
- Urgency/scarcity frameworks
- CTA optimization

## Self-Annealing Notes

### What Works Well
- 10-part structure creates consistent, high-quality scripts
- Loading skill bibles ensures framework adherence
- Multiple hook options allow A/B testing
- Delivery notes improve production quality

### What Doesn't Work
- Skipping research phase produces generic scripts
- One-size-fits-all approach fails for edge cases
- Ignoring price point context creates weak value stacks

### Improvements Over Time
- Build hook formula library by industry
- Create proven transition templates
- Develop objection hierarchy by offer type
- Add style guide for different VSL tones
- Track which hooks convert best (feedback loop)
