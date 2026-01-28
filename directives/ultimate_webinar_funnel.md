# Ultimate Webinar Funnel Generator

## What This Workflow Is
**Complete webinar funnel system** that generates registration pages, email sequences, webinar scripts, and follow-up campaigns. Creates everything needed to run high-converting webinar funnels for course launches, coaching programs, or high-ticket services.

## What It Does
1. Generates webinar registration page copy
2. Creates reminder email sequences
3. Produces full webinar presentation script
4. Generates slides outline
5. Creates post-webinar follow-up sequences
6. Produces replay page copy
7. Creates urgency/deadline campaigns

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
GOOGLE_APPLICATION_CREDENTIALS=path   # Google Docs/Slides
```

### Required Skill Bibles
- `SKILL_BIBLE_webinar_funnel_building.md`
- `SKILL_BIBLE_webinar_mastery.md`
- `SKILL_BIBLE_webinar_funnel_launch.md`
- `SKILL_BIBLE_webinar_live_events.md`
- `SKILL_BIBLE_vsl_writing_production.md`

## How to Run

```bash
python3 execution/generate_webinar_funnel.py \
  --topic "How to Scale Your Agency to $100K/Month" \
  --presenter "John Smith" \
  --offer "Agency Accelerator Program" \
  --price 2997 \
  --webinar-date "2026-02-15" \
  --target-audience "Agency owners at $10-30K/month" \
  --include-slides
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| topic | string | Yes | Webinar topic/title |
| presenter | string | Yes | Who's presenting |
| offer | string | Yes | What you're selling |
| price | int | Yes | Offer price |
| webinar-date | date | No | Date of live webinar |
| target-audience | string | Yes | Who should attend |
| webinar-length | int | No | 60, 90, or 120 minutes |
| evergreen | flag | No | Make evergreen automated |
| include-slides | flag | No | Generate slide outline |

## Process

### Phase 1: Registration Page

**Headline Formula:**
"How to [Achieve Desirable Result] Without [Common Obstacle]"

**Page Elements:**
- Attention-grabbing headline
- Subheadline with date/time
- 3-5 "You'll Learn" bullets
- About the presenter
- Urgency (limited spots)
- Registration form

### Phase 2: Pre-Webinar Email Sequence

**Email 1: Confirmation (Immediate)**
- Thank them for registering
- Add to calendar links
- What they'll learn
- Prep instructions

**Email 2: Reminder (24 hours before)**
- Reminder of value
- Date/time/link
- What to have ready
- Build anticipation

**Email 3: Reminder (1 hour before)**
- Starting soon
- Direct link
- Quick wins they'll get

**Email 4: It's Live (Start time)**
- We're starting
- Direct link
- Don't miss this

### Phase 3: Webinar Presentation Script

**Perfect Webinar Structure (90 min):**

```
INTRO (5 min)
- Welcome and housekeeping
- Your story (credibility)
- Promise of the webinar

THE ONE THING (5 min)
- Reframe their thinking
- The secret/mechanism
- Why this is different

SECRET 1 (15 min)
- Internal belief shift
- Story + teaching
- Mini breakthrough

SECRET 2 (15 min)
- External belief shift
- Story + teaching
- More value

SECRET 3 (15 min)
- Market belief shift
- Story + teaching
- Stack value

THE STACK (10 min)
- Present the offer
- Build the value stack
- Reveal the price

THE CLOSE (15 min)
- Handle objections
- Urgency/scarcity
- Clear CTA
- Q&A

BONUS (10 min)
- Fast-action bonuses
- Final push
- Recap and close
```

### Phase 4: Post-Webinar Sequence

**Day 0 (After webinar):**
- Replay link (48-hour access)
- Offer summary
- Bonus reminder

**Day 1:**
- Case study/testimonial
- Objection handling
- Deadline reminder

**Day 2:**
- FAQ email
- Countdown to deadline
- Final bonuses revealed

**Day 3 (Deadline):**
- Final reminder (AM)
- Last chance (PM)
- Doors closing (Final)

### Phase 5: Replay Page

**Elements:**
- Replay video embed
- Time-sensitive messaging
- Offer summary
- CTA button
- FAQ
- Testimonials

## Output Structure
```
.tmp/webinar_funnels/{topic_slug}/
├── registration/
│   ├── registration_page.md
│   └── thank_you_page.md
├── emails/
│   ├── pre_webinar_sequence.md
│   └── post_webinar_sequence.md
├── presentation/
│   ├── full_script.md
│   ├── slides_outline.md
│   └── speaker_notes.md
├── replay/
│   └── replay_page.md
├── offer/
│   ├── offer_stack.md
│   └── objection_handlers.md
└── result.json
```

## Webinar Script Template

### Opening (5 min)
```
"Welcome everyone to [Webinar Title]...

Over the next [X] minutes, I'm going to show you exactly 
how to [achieve main result] without [common obstacle].

My name is [Name], and [quick credibility statement]...

Before we dive in, I want you to know that everything 
I'm sharing today actually works. I've helped [number] 
[people] achieve [result]...

So if you're ready to [transformation], let's get started..."
```

### Teaching Section (45 min)
```
"The first thing you need to understand is [Secret 1]...

[Story that illustrates the point]

Here's what this means for you...

[Tactical teaching with examples]

Now that you understand [Secret 1], let's talk about 
[Secret 2]..."
```

### Transition to Offer (5 min)
```
"Now, I've shown you what to do and why it works...

But here's the thing - knowing what to do and actually 
doing it are two different things...

That's why I created [Offer Name]...

It's the fastest way to [achieve result] because 
[reason]..."
```

### The Offer (15 min)
```
"Here's everything you get when you join [Program Name]:

Component 1: [Name] (Value: $X)
[Description and benefit]

Component 2: [Name] (Value: $X)
[Description and benefit]

[Continue stacking...]

Total Value: $[Sum]

But you're not paying that...

Your investment today is just $[Price]..."
```

### Close (10 min)
```
"Now, I know some of you might be thinking [objection]...

Let me address that...

[Handle objection]

Here's my promise to you...

[Guarantee]

If you're ready to [transformation], click the button 
below and join us inside [Program]...

But you need to act now because [urgency/scarcity]...

[Final CTA]"
```

## Quality Gates

### Pre-Webinar Checklist
- [ ] Registration page converts 30%+
- [ ] Email sequence automated
- [ ] Presentation polished
- [ ] Slides created and tested
- [ ] Offer page ready
- [ ] Payment processing tested
- [ ] Calendar/reminders set

### Webinar Metrics
| Metric | Target |
|--------|--------|
| Registration rate | 30-40% |
| Show-up rate | 30-50% |
| Pitch retention | 50%+ |
| Conversion rate | 5-15% |
| Revenue per registrant | $50-200 |
