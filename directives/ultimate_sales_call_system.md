# Ultimate Sales Call System

## What This Workflow Is
**Complete sales call preparation and execution system** that generates discovery scripts, objection handlers, pricing presentations, and follow-up sequences. Built for agencies closing high-ticket deals.

## What It Does
1. Researches prospect before call
2. Generates discovery questions
3. Creates objection handling scripts
4. Produces pricing presentation
5. Generates follow-up sequences
6. Creates call summary templates
7. Tracks conversion metrics

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI script generation
PERPLEXITY_API_KEY=your_key           # Prospect research
```

### Required Skill Bibles
- `SKILL_BIBLE_discovery_call_mastery.md`
- `SKILL_BIBLE_objection_handling_mastery.md`
- `SKILL_BIBLE_objection_handling_advanced.md`
- `SKILL_BIBLE_high_ticket_sales_process.md`
- `SKILL_BIBLE_sales_training_complete.md`
- `SKILL_BIBLE_sales_closing_mastery.md`

## How to Run

```bash
python3 execution/generate_sales_call_prep.py \
  --prospect-company "Acme Corp" \
  --prospect-name "John Smith" \
  --service "Meta Ads Management" \
  --price-range "3000-7000" \
  --call-type "discovery" \
  --include-research
```

## Process

### Phase 1: Pre-Call Research

**Research Points:**
- Company background
- Recent news/funding
- Current marketing efforts
- Competitors
- Potential pain points
- Decision-making structure

### Phase 2: Discovery Script

**Opening (2 min):**
```
"Thanks for taking the time, [Name]. 
Before we dive in, I'd love to learn more about 
what prompted you to take this call today..."
```

**Situation Questions (10 min):**
1. Tell me about your current [marketing/lead gen] setup
2. What's working well right now?
3. Where are you seeing the biggest challenges?
4. What's your team structure look like?
5. What tools/platforms are you using?

**Problem Questions (10 min):**
1. What happens when [problem occurs]?
2. How long has this been an issue?
3. What have you tried to solve it?
4. Why didn't that work?
5. What's this costing you in [time/money/opportunity]?

**Implication Questions (5 min):**
1. If this continues, what happens in 6 months?
2. How is this affecting your [team/growth/revenue]?
3. What would change if this was solved?

**Need-Payoff Questions (5 min):**
1. If we could [solve problem], what would that mean for you?
2. What would achieving [goal] allow you to do?
3. How would that impact your business?

### Phase 3: Objection Handlers

**"It's too expensive":**
```
"I totally understand budget is a concern. Help me 
understand - when you say it's too expensive, is it 
that you don't see the value, or that you genuinely 
don't have the budget right now?

[If value] Let me help you see the ROI...
[If budget] What would you need to see to make this 
work? Is there a way to start smaller?
```

**"I need to think about it":**
```
"Absolutely, I want you to feel confident about this. 
What specifically would you like to think through? 
Is there anything I can clarify right now?

Often when people say they need to think about it, 
there's a specific concern. What's holding you back?"
```

**"I need to talk to my partner/team":**
```
"Makes total sense - important decisions should 
involve key stakeholders. 

What do you think their biggest concerns would be?
Would it help if I joined that conversation to 
answer any questions directly?"
```

**"We're not ready right now":**
```
"I appreciate that. Help me understand what 'ready' 
looks like for you?

What would need to change for this to be the right 
time?"
```

**"We've been burned before":**
```
"I'm sorry to hear that. What happened?

[Listen carefully]

Here's how we're different... [specific differentiators]

And here's our guarantee/process to prevent that..."
```

### Phase 4: Close Structure

**Trial Close:**
```
"Based on everything we've discussed, it sounds like 
[service] would help you [achieve result]. Is that 
right?

Great. Here's what working together looks like..."
```

**Present the Offer:**
- Recap their problems and goals
- Present solution
- Walk through deliverables
- Show pricing
- Explain next steps

**Handle Final Objections:**
- Use prepared handlers
- Confirm resolved
- Move to commitment

**Get Commitment:**
```
"So here's where we are - you said [goal], and we've 
shown you how we can get you there.

What questions do you have before we get started?"

[Handle questions]

"Great. Let's do this. I'll send over the contract 
and we'll get your kickoff scheduled for [date]."
```

### Phase 5: Post-Call Follow-Up

**Immediately After:**
- Send summary email
- Include next steps
- Attach relevant resources

**If Not Closed:**
- Day 1: Recap + address concerns
- Day 3: Value-add content
- Day 7: Check-in
- Day 14: Final follow-up

## Output Structure
```
.tmp/sales_calls/{prospect_slug}/
├── research/
│   ├── prospect_research.md
│   └── company_intel.md
├── scripts/
│   ├── discovery_script.md
│   ├── presentation_script.md
│   └── objection_handlers.md
├── follow_up/
│   ├── summary_template.md
│   └── follow_up_sequence.md
├── tracking/
│   └── call_notes_template.md
└── result.json
```

## Quality Gates

### Pre-Call Checklist
- [ ] Prospect researched
- [ ] Discovery questions ready
- [ ] Objection handlers reviewed
- [ ] Pricing prepared
- [ ] Calendar clear
- [ ] Tech tested (Zoom, etc.)
- [ ] CRM updated

### Call Metrics
| Metric | Target |
|--------|--------|
| Show rate | 80%+ |
| Discovery complete | 90%+ |
| Proposal sent | 60%+ |
| Close rate | 20-30% |
