# Ultimate Case Study Generator

## What This Workflow Is
**Complete case study creation system** that generates compelling success stories from client results. Produces written case studies, video scripts, and social proof assets for sales and marketing.

## What It Does
1. Structures client interview questions
2. Generates written case study
3. Creates video testimonial script
4. Produces social media snippets
5. Generates sales deck slides
6. Creates objection-handling assets

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
```

### Required Skill Bibles
- `SKILL_BIBLE_testimonials_case_studies.md`
- `SKILL_BIBLE_social_proof_flywheel.md`
- `SKILL_BIBLE_client_proposals_pitch_decks.md`

## How to Run

```bash
python3 execution/generate_case_study.py \
  --client-name "Acme Corp" \
  --service "Meta Ads Management" \
  --results "3x ROAS, $500K in revenue" \
  --timeline "90 days" \
  --include-video-script \
  --include-social-snippets
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client-name | string | Yes | Client company |
| service | string | Yes | Service delivered |
| results | string | Yes | Key results achieved |
| timeline | string | Yes | Time to achieve |
| challenge | string | No | Initial challenge |
| industry | string | No | Client's industry |
| include-video-script | flag | No | Generate video script |
| include-social-snippets | flag | No | Generate social posts |

## Process

### Phase 1: Client Interview Questions

**The Before:**
1. What was your situation before working with us?
2. What challenges were you facing?
3. What had you tried before?
4. What was at stake if you didn't solve this?

**The During:**
1. Why did you choose to work with us?
2. What was the process like?
3. What surprised you during the engagement?
4. How was the communication/support?

**The After:**
1. What results did you achieve?
2. What changed in your business?
3. What's the biggest impact?
4. Would you recommend us? Why?

### Phase 2: Case Study Structure

**The Problem (25%):**
- Client background
- Situation before
- Specific challenges
- What they tried
- Stakes/consequences

**The Solution (25%):**
- Why they chose us
- Our approach
- Key strategies used
- Process overview
- Timeline

**The Results (50%):**
- Quantified outcomes
- Before/after comparison
- Testimonial quotes
- Business impact
- Future outlook

### Phase 3: Written Case Study

**Format:**
```
[Client Name]: [Headline with Result]

At a Glance:
• Industry: [Industry]
• Service: [Service]
• Timeline: [Timeline]
• Result: [Key Metric]

The Challenge
[2-3 paragraphs on the problem]

The Solution
[2-3 paragraphs on approach]

The Results
[Results with specific numbers]

"[Key testimonial quote]"
- [Client Name, Title, Company]

Key Takeaways:
• [Learning 1]
• [Learning 2]
• [Learning 3]
```

### Phase 4: Video Testimonial Script

**60-Second Version:**
```
HOOK (0-5s):
"We went from [before] to [after] in just [timeline]."

PROBLEM (5-15s):
"Before working with [Agency], we were struggling 
with [problem]. We tried [solutions] but nothing 
worked."

SOLUTION (15-30s):
"Then we found [Agency]. They [unique approach], 
which was completely different from anything we'd 
tried before."

RESULTS (30-50s):
"The results were incredible. We achieved [specific 
results]. Our [metric] went from [X] to [Y]."

RECOMMENDATION (50-60s):
"If you're struggling with [problem], I'd highly 
recommend [Agency]. They [key differentiator]."
```

### Phase 5: Social Proof Assets

**LinkedIn Post:**
```
We just hit a major milestone with our client [Name]...

📊 The numbers:
• [Before]: [Metric]
• [After]: [Metric]
• [Timeline]

Here's what made the difference:

1. [Strategy 1]
2. [Strategy 2]
3. [Strategy 3]

"[Short testimonial quote]" - [Client Name]

Want similar results? DM me "RESULTS"
```

**Twitter Thread:**
```
1/ Case study thread: How we helped [Client] 
achieve [result] in [timeline] 🧵

2/ The problem:
[Brief problem statement]

3/ What they tried before:
[Previous failed solutions]

4/ Our approach:
[3 key strategies]

5/ The results:
[Specific metrics]

6/ The lesson:
[Key takeaway]

7/ Want the full breakdown? Reply "CASE STUDY"
```

**One-Liner:**
"We helped [Client] achieve [result] in [timeline]."

## Output Structure
```
.tmp/case_studies/{client_slug}/
├── interview/
│   └── interview_questions.md
├── case_study/
│   ├── full_case_study.md
│   └── executive_summary.md
├── video/
│   └── testimonial_script.md
├── social/
│   ├── linkedin_post.md
│   └── twitter_thread.md
├── sales/
│   └── objection_handler.md
└── result.json
```

## Quality Gates

### Case Study Checklist
- [ ] Specific, quantified results
- [ ] Compelling before/after story
- [ ] Client-approved quotes
- [ ] Professional formatting
- [ ] Multiple formats created
- [ ] Easy to repurpose

### Impact Benchmarks
| Usage | Lift |
|-------|------|
| Sales deck | +25% close rate |
| Website | +15% conversion |
| Email | +20% click rate |
| Social | +30% engagement |
