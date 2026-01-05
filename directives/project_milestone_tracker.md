# Project Milestone Tracker

## What This Workflow Is
This workflow tracks project milestones, sends progress notifications, and alerts stakeholders when deadlines are at risk.

## What It Does
1. Loads milestones from project management
2. Checks status on schedule
3. Calculates completion vs timeline
4. Sends progress updates
5. Alerts on delays or blockers

## Prerequisites

### Required API Keys (add to .env)
```
ASANA_API_KEY=your_asana_key              # Or project management tool
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Required Tools
- Python 3.10+
- Project management API

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Check Milestones
```bash
python3 execution/check_milestones.py \
  --project_id "[ID]" \
  --output .tmp/milestone_status.json
```

### Quick One-Liner (Weekly Cron)
```bash
python3 execution/check_milestones.py --project_id "[ID]"
```

## Goal
Track project milestones and automatically notify stakeholders of progress and delays.

## Inputs
- **Project Data**: Milestones, due dates, owners
- **Source**: Asana, Monday, ClickUp, Google Sheets
- **Notification Rules**: When to alert

## Process

### 1. Sync Project Data
```bash
python3 execution/sync_milestones.py \
  --source asana \
  --project_id "[ID]" \
  --output .tmp/milestones.json
```

### 2. Milestone Statuses
- ✅ Completed
- 🟢 On Track
- 🟡 At Risk (within 2 days of due)
- 🔴 Overdue

### 3. Notification Rules

**Daily Summary (9am):**
- Milestones due today
- Overdue items
- Items at risk

**Immediate Alerts:**
- Milestone completed
- Item becomes overdue
- Blocker added

**Weekly Report:**
- Progress overview
- Timeline changes
- Resource concerns

### 4. Notification Format
```markdown
# Project Update: [PROJECT NAME]
**Date:** [DATE]

## Due Today
- [ ] [Milestone 1] - Owner: [Name]
- [ ] [Milestone 2] - Owner: [Name]

## Overdue ⚠️
- [Milestone] - Due: [Date] - [X days late]

## Completed This Week ✅
- [Milestone 1]
- [Milestone 2]

## Coming Up (Next 7 Days)
- [Milestone] - Due: [Date]
```

### 5. Auto-Actions
- Update client on completions
- Escalate overdue items
- Adjust dependent milestones
- Send reminder 2 days before due

## Integrations
- Project management (Asana, Monday)
- Slack
- Email
- CRM

## Cost
- API calls: Free
- Automation: Free
