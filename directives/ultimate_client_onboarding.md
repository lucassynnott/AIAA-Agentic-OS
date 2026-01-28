# Ultimate Client Onboarding System

## What This Workflow Is
**Complete client onboarding automation** that handles everything from contract signing to project kickoff. Creates intake forms, sends welcome sequences, sets up project management, schedules kickoff calls, and establishes communication channels. Built for agencies that want to deliver a premium onboarding experience.

## What It Does
1. Generates customized intake questionnaire
2. Creates welcome email sequence
3. Sets up project management workspace
4. Schedules kickoff call with agenda
5. Creates client communication channels
6. Generates onboarding checklist
7. Produces SOW/contract from templates
8. Sends automated reminders

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI content generation
GOOGLE_APPLICATION_CREDENTIALS=path   # Google Docs/Sheets
SLACK_WEBHOOK_URL=your_webhook        # Slack notifications
```

### Required Skill Bibles
- `SKILL_BIBLE_client_onboarding_ops.md`
- `SKILL_BIBLE_client_onboarding_forms.md`
- `SKILL_BIBLE_client_communication_setup.md`
- `SKILL_BIBLE_client_operations_retention.md`
- `SKILL_BIBLE_agency_checklist_az.md`

## How to Run

```bash
# Full onboarding setup
python3 execution/client_onboarding_system.py \
  --client-name "Acme Corp" \
  --client-email "john@acmecorp.com" \
  --service-type "Meta Ads Management" \
  --package "Growth ($5,000/mo)" \
  --start-date "2026-02-01" \
  --kickoff-days 3

# Existing client refresh
python3 execution/client_onboarding_system.py \
  --client-name "Acme Corp" \
  --refresh-onboarding \
  --update-questionnaire
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client-name | string | Yes | Client company name |
| client-email | string | Yes | Primary contact email |
| service-type | string | Yes | Service being delivered |
| package | string | Yes | Package/tier purchased |
| start-date | date | Yes | Project start date |
| kickoff-days | int | No | Days until kickoff (default: 5) |
| account-manager | string | No | Assigned AM |
| slack-channel | string | No | Dedicated Slack channel |

## Process

### Phase 1: Intake Questionnaire Generation
Create customized questionnaire based on service type:

**For Paid Ads Clients:**
- Current ad spend and platforms
- Past campaign performance
- Target CPA/ROAS goals
- Existing pixel/tracking setup
- Creative assets available
- Competitor information
- Brand guidelines

**For Lead Gen Clients:**
- Target ICP details
- Current sales process
- CRM/tech stack
- Qualification criteria
- Territory restrictions
- Compliance requirements

**For Content/Social Clients:**
- Brand voice guidelines
- Content pillars/topics
- Approval process
- Existing content assets
- Competitor accounts
- Posting frequency preferences

### Phase 2: Welcome Email Sequence

**Email 1: Welcome (Immediate)**
- Personal welcome from AM/founder
- What to expect next
- Link to intake questionnaire
- Contact information

**Email 2: Questionnaire Reminder (Day 2)**
- Friendly reminder
- Why the questionnaire matters
- Direct link to form

**Email 3: Kickoff Prep (Day 3)**
- Kickoff meeting scheduled
- Agenda preview
- What to prepare
- Team introductions

**Email 4: Day Before Kickoff**
- Meeting reminder
- Final checklist
- Tech check (Zoom link, etc.)

### Phase 3: Project Setup

**ClickUp/Asana/Monday Workspace:**
- Create project
- Add client as guest
- Set up task templates
- Create milestones
- Assign team members

**Google Drive:**
- Create client folder structure
- Upload brand assets
- Share with client
- Set permissions

**Slack Channel (if applicable):**
- Create dedicated channel
- Add client contacts
- Post welcome message
- Pin important links

### Phase 4: Kickoff Call Preparation

**Generate Agenda:**
1. Introductions (5 min)
2. Questionnaire review (15 min)
3. Goals & KPIs alignment (15 min)
4. Timeline & milestones (10 min)
5. Communication protocols (5 min)
6. Q&A (10 min)

**Create Slide Deck:**
- Welcome slide
- Team introductions
- Understanding your goals
- Our process overview
- Timeline visualization
- Communication plan
- Next steps

### Phase 5: Document Generation

**Statement of Work (SOW):**
- Scope of services
- Deliverables list
- Timeline
- Pricing breakdown
- Terms and conditions
- Signatures

**Client Success Plan:**
- 30/60/90 day milestones
- Key metrics to track
- Check-in schedule
- Escalation procedures

### Phase 6: Automated Reminders

Set up recurring reminders:
- Questionnaire incomplete (daily until done)
- Kickoff approaching (1 day before)
- First deliverable due (3 days before)
- Monthly check-in (recurring)
- Contract renewal (60 days before)

## Output Structure
```
.tmp/client_onboarding/{client_slug}/
├── intake/
│   ├── questionnaire.md
│   ├── questionnaire_link.txt
│   └── responses.json (once filled)
├── emails/
│   ├── welcome_sequence.md
│   └── email_templates/
├── project_setup/
│   ├── workspace_checklist.md
│   ├── folder_structure.md
│   └── channel_setup.md
├── kickoff/
│   ├── agenda.md
│   ├── presentation.md
│   └── meeting_notes_template.md
├── documents/
│   ├── sow_template.md
│   └── success_plan.md
├── automations/
│   └── reminder_schedule.json
└── result.json
```

## Questionnaire Templates

### Universal Questions
1. What are your top 3 goals for this engagement?
2. What does success look like in 90 days?
3. Who are your main competitors?
4. What's your current biggest challenge?
5. Who are the key stakeholders/approvers?
6. What's your preferred communication style?
7. Are there any hard deadlines we should know about?
8. What's worked well with agencies in the past?
9. What hasn't worked with agencies before?
10. Anything else we should know?

### Service-Specific Questions
(Loaded from skill bibles based on service type)

## Quality Gates

### Pre-Kickoff Checklist
- [ ] Intake questionnaire completed
- [ ] Contract signed
- [ ] Payment received/invoiced
- [ ] Project workspace created
- [ ] Slack channel set up
- [ ] Assets uploaded
- [ ] Kickoff scheduled
- [ ] Team briefed

### Post-Kickoff Checklist
- [ ] Meeting notes shared
- [ ] Action items assigned
- [ ] Timeline confirmed
- [ ] First milestone scheduled
- [ ] Check-in cadence established
- [ ] Success metrics defined

## Error Handling

| Error | Solution |
|-------|----------|
| Questionnaire not filled | Escalate to AM, call client |
| Assets not provided | Send reminder, offer help |
| Kickoff no-show | Reschedule immediately |
| Scope creep early | Reference SOW, clarify scope |

## Integration with Other Workflows

- `stripe_client_onboarding.md` - Payment processing
- `create_proposal.md` - Proposal generation
- `client_reporting.md` - Ongoing reporting
- `client_qbr_generator.md` - Quarterly reviews

## Self-Annealing Notes

### What Works
- Personal video welcome increases engagement
- Clear timeline reduces client anxiety
- Over-communication in week 1 builds trust
- Templates save time, customization builds rapport

### What Doesn't Work
- Generic onboarding (feels impersonal)
- Too many forms (causes fatigue)
- No clear next steps (creates confusion)
- Delayed first deliverable (loses momentum)

### Continuous Improvement
- Survey clients on onboarding experience
- Track time-to-first-deliverable
- Monitor questionnaire completion rate
- A/B test welcome sequences
