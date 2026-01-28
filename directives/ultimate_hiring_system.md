# Ultimate Agency Hiring System

## What This Workflow Is
**Complete hiring and team building system** for agencies scaling their teams. Produces job descriptions, interview scripts, scorecards, and onboarding materials.

## What It Does
1. Creates job descriptions
2. Generates interview scripts
3. Produces evaluation scorecards
4. Creates offer templates
5. Generates onboarding checklists
6. Produces training materials

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
```

### Required Skill Bibles
- `SKILL_BIBLE_team_hiring_management.md`
- `SKILL_BIBLE_hiring_team_building.md`
- `SKILL_BIBLE_agency_hiring_system.md`
- `SKILL_BIBLE_a_player_training.md`

## How to Run

```bash
python3 execution/generate_hiring_materials.py \
  --role "Meta Ads Specialist" \
  --level "Mid" \
  --salary-range "60000-80000" \
  --department "Paid Media" \
  --include-onboarding
```

## Process

### Phase 1: Job Description

**Structure:**
- About the company
- About the role
- Responsibilities
- Requirements
- Nice-to-haves
- Benefits
- How to apply

### Phase 2: Interview Process

**Screening Call (15 min):**
- Background overview
- Motivation check
- Salary expectations
- Availability

**Technical Interview (45 min):**
- Role-specific questions
- Skill assessment
- Problem-solving
- Portfolio review

**Culture Fit (30 min):**
- Values alignment
- Work style
- Team dynamics
- Growth mindset

**Final Interview (30 min):**
- Leadership/Founder
- Vision alignment
- Final questions
- Next steps

### Phase 3: Evaluation Scorecard

**Criteria (1-5 scale):**
- Technical skills
- Communication
- Problem-solving
- Culture fit
- Growth potential
- Role-specific competencies

**Red Flags:**
- Poor communication
- Blame others
- No questions asked
- Salary-only focus
- Bad-mouths past employers

**Green Flags:**
- Takes ownership
- Asks great questions
- Shows genuine interest
- Admits weaknesses
- Growth mindset

### Phase 4: Offer Template

**Elements:**
- Position title
- Start date
- Compensation
- Benefits
- Reporting structure
- Terms

### Phase 5: Onboarding

**Week 1:**
- Day 1: Welcome, tech setup, intro calls
- Day 2: Company overview, culture
- Day 3: Role-specific training
- Day 4: Shadow team members
- Day 5: First small project

**Week 2-4:**
- Gradual client exposure
- Supervised work
- Regular check-ins
- Documentation review
- Tool mastery

**30/60/90 Day Plan:**
- Clear milestones
- Performance metrics
- Check-in schedule
- Feedback loops

## Output Structure
```
.tmp/hiring/{role_slug}/
├── job_description/
│   └── jd.md
├── interviews/
│   ├── screening_script.md
│   ├── technical_interview.md
│   └── culture_fit.md
├── evaluation/
│   └── scorecard.md
├── offer/
│   └── offer_template.md
├── onboarding/
│   ├── first_week.md
│   └── 30_60_90_plan.md
└── result.json
```

## Interview Questions by Role

### Account Manager
1. Tell me about a difficult client situation
2. How do you prioritize multiple clients?
3. Walk me through your communication style
4. How do you handle scope creep?
5. What's your approach to client reporting?

### Media Buyer
1. Walk me through your campaign setup process
2. How do you optimize underperforming campaigns?
3. What's your approach to creative testing?
4. How do you diagnose performance issues?
5. What metrics do you focus on?

### Copywriter
1. Show me your best performing piece
2. How do you approach research?
3. Walk me through your writing process
4. How do you handle feedback?
5. What's your revision process?

### Sales Rep
1. Walk me through your sales process
2. How do you handle objections?
3. Tell me about your biggest deal
4. How do you build pipeline?
5. What's your follow-up process?

## Quality Gates

### Hiring Checklist
- [ ] Job description clear
- [ ] Interview process defined
- [ ] Scorecard ready
- [ ] Team aligned on criteria
- [ ] Onboarding prepared
- [ ] Tools ready

### Hiring Metrics
| Metric | Target |
|--------|--------|
| Time to hire | <30 days |
| Offer acceptance | 80%+ |
| 90-day retention | 90%+ |
| Quality of hire | 4+ rating |
