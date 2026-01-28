# Ultimate AI Automation Builder

## What This Workflow Is
**Complete AI automation design and documentation system** that creates n8n/Make workflows, AI agent architectures, and automation SOPs. Produces workflow diagrams, node configurations, and deployment guides for building automated systems.

## What It Does
1. Analyzes business process to automate
2. Designs workflow architecture
3. Generates node-by-node configuration
4. Creates API integration specs
5. Produces testing protocols
6. Generates client documentation
7. Creates maintenance guides

## Prerequisites

### Required API Keys
```
OPENROUTER_API_KEY=your_key           # AI design
```

### Required Skill Bibles
- `SKILL_BIBLE_n8n_workflow_automation.md`
- `SKILL_BIBLE_n8n_workflow_building.md`
- `SKILL_BIBLE_ai_automation_agency.md`
- `SKILL_BIBLE_monetizable_agentic_workflows.md`
- `SKILL_BIBLE_ai_agent_setup.md`

## How to Run

```bash
python3 execution/generate_automation.py \
  --process "Lead intake and CRM entry" \
  --trigger "Typeform submission" \
  --actions "Enrich lead, add to CRM, send Slack notification, trigger email sequence" \
  --platform "n8n" \
  --include-error-handling
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| process | string | Yes | Process to automate |
| trigger | string | Yes | What starts the workflow |
| actions | string | Yes | Steps to perform |
| platform | enum | No | "n8n", "make", "zapier" |
| include-error-handling | flag | No | Add error handling |
| complexity | enum | No | "simple", "medium", "complex" |

## Process

### Phase 1: Process Analysis

**Document:**
- Current manual process
- Time/effort spent
- Error rate
- Volume/frequency

**Identify:**
- Trigger events
- Required integrations
- Decision points
- Output requirements

### Phase 2: Workflow Architecture

**Components:**
1. Trigger Node
2. Data Processing Nodes
3. API Integration Nodes
4. Conditional Logic
5. Output/Action Nodes
6. Error Handling

**Architecture Diagram:**
```
[Trigger] → [Validate] → [Process] → [Output]
                ↓
           [Error Handler]
```

### Phase 3: Node Configuration

For each node:
- Node type
- Configuration settings
- Input/output mapping
- Credentials required
- Error handling

### Phase 4: Testing Protocol

1. Unit test each node
2. Integration test full workflow
3. Edge case testing
4. Load testing (if high volume)
5. Failure recovery testing

### Phase 5: Documentation

**Client Documentation:**
- What the automation does
- How to trigger it
- Expected outputs
- How to monitor
- Common issues

**Technical Documentation:**
- Node configurations
- API credentials needed
- Environment variables
- Deployment steps
- Maintenance schedule

## Output Structure
```
.tmp/automations/{process_slug}/
├── design/
│   ├── architecture.md
│   └── workflow_diagram.md
├── implementation/
│   ├── n8n_workflow.json
│   ├── node_configs/
│   └── credentials_needed.md
├── testing/
│   ├── test_cases.md
│   └── test_results.md
├── documentation/
│   ├── client_guide.md
│   └── technical_docs.md
└── result.json
```

## Common Automation Templates

### Lead Intake Automation
```
Typeform → Enrich (Clearbit) → CRM (HubSpot) → Slack → Email (ConvertKit)
```

### Social Media Scheduling
```
Airtable → Format Content → Buffer/Hootsuite → Log Result
```

### Client Reporting
```
Schedule (Cron) → Pull Data (APIs) → Process → Generate Report → Send Email
```

### Invoice Processing
```
Email (Invoice) → Extract Data (AI) → Validate → Add to Accounting → Notify
```

## Quality Gates

### Pre-Deploy Checklist
- [ ] All nodes tested individually
- [ ] Full workflow tested end-to-end
- [ ] Error handling covers all failure points
- [ ] Credentials securely stored
- [ ] Rate limits considered
- [ ] Logging enabled
- [ ] Documentation complete
- [ ] Client trained on monitoring
