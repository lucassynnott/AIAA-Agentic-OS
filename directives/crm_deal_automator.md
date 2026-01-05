# CRM Deal Stage Automation

## What This Workflow Is
This workflow automates CRM actions based on deal stage changes - creating tasks, sending notifications, triggering sequences, and updating records automatically.

## What It Does
1. Monitors deal stage changes via webhook or polling
2. Executes automation rules for each stage
3. Creates tasks and sends notifications
4. Triggers email sequences
5. Updates related records

## Prerequisites

### Required API Keys (add to .env)
```
HUBSPOT_API_KEY=your_hubspot_key          # Or SALESFORCE, PIPEDRIVE credentials
SLACK_WEBHOOK_URL=your_slack_webhook      # For notifications
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- CRM with API access

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Configure Rules
Create `rules.json`:
```json
{
  "qualified": {"notify": "ae-team", "task": "Schedule discovery call"},
  "demo_scheduled": {"sequence": "pre-demo-prep"},
  "closed_won": {"slack": "#wins", "trigger": "onboarding"}
}
```

### Step 2: Start Automation
```bash
python3 execution/crm_stage_automation.py \
  --crm hubspot \
  --rules rules.json \
  --watch continuous
```

### Step 3: Manual Trigger (Testing)
```bash
python3 execution/crm_stage_automation.py \
  --crm hubspot \
  --deal_id "[DEAL_ID]" \
  --stage "qualified"
```

### Quick One-Liner
```bash
python3 execution/crm_stage_automation.py --crm hubspot --rules rules.json --watch
```

## Goal
Automate CRM updates, tasks, and notifications based on deal stage changes.

## Inputs
- **CRM**: HubSpot, Salesforce, Pipedrive, GoHighLevel
- **Pipeline Stages**: Your deal stages
- **Automation Rules**: What happens at each stage

## Stage Automation Map

### Stage: Lead
**Triggers:**
- Create contact record
- Send intro email sequence
- Assign to SDR

### Stage: Qualified
**Triggers:**
- Update lead score
- Notify AE
- Schedule discovery call
- Research dossier generated

### Stage: Demo Scheduled
**Triggers:**
- Send calendar confirmation
- Prep materials generated
- Reminder sequence started

### Stage: Proposal Sent
**Triggers:**
- Log proposal in CRM
- Start follow-up sequence
- Alert manager if >$X deal

### Stage: Negotiation
**Triggers:**
- Notify legal (if needed)
- Track proposal views
- Alert if stuck >7 days

### Stage: Closed Won
**Triggers:**
- 🎉 Slack celebration
- Trigger onboarding
- Generate invoice
- Update forecasting

### Stage: Closed Lost
**Triggers:**
- Log loss reason
- Add to nurture sequence
- Schedule re-engagement (90 days)

## Process
```bash
python3 execution/crm_stage_automation.py \
  --crm hubspot \
  --rules rules.json \
  --watch continuous
```

## Automation Examples

**Time-based:**
- If in stage >X days → Alert
- If no activity >Y days → Task created

**Value-based:**
- If deal >$10k → Notify VP
- If enterprise → Add to high-touch sequence

**Activity-based:**
- If email opened → Update score
- If proposal viewed → Alert rep

## Integrations
- CRM API (HubSpot, Salesforce)
- Slack
- Email
- Task management
