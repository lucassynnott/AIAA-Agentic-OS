# Team Task Assignment

## What This Workflow Is
This workflow automatically assigns tasks to team members based on skills, current capacity, and workload balance.

## What It Does
1. Receives new task to assign
2. Analyzes skill requirements
3. Checks team member availability
4. Assigns to optimal match
5. Notifies assignee via Slack

## Prerequisites

### Required API Keys (add to .env)
```
ASANA_API_KEY=your_asana_key              # Or project management
SLACK_WEBHOOK_URL=your_slack_webhook
```

### Installation
```bash
pip install requests
```

## How to Run
```bash
python3 execution/assign_task.py --task_id "[ID]" --team_sheet "[SHEET_URL]"
```

## Goal
Automatically assign tasks to team members based on skills, capacity, and workload.

## Inputs
- **Task**: What needs to be done
- **Team**: Available team members
- **Criteria**: Skills, availability, current load

## Process

### 1. Analyze Task
```bash
python3 execution/assign_task.py \
  --task "[TASK_DESCRIPTION]" \
  --team_data team.json \
  --output .tmp/assignment.json
```

### 2. Assignment Criteria

**Skills Match:**
- Required skills for task
- Team member capabilities
- Experience level needed

**Availability:**
- Current workload
- Scheduled time off
- Other commitments

**Load Balancing:**
- Hours assigned this week
- Number of active tasks
- Priority of existing work

### 3. Assignment Algorithm
```
Score = (Skill Match * 0.4) + 
        (Availability * 0.3) + 
        (Load Balance * 0.2) +
        (Past Performance * 0.1)
```

### 4. Assignment Output
```json
{
  "task": "Create landing page for Client X",
  "assigned_to": "Jane Smith",
  "reason": "Best skill match (design), 60% capacity",
  "due_date": "2024-01-20",
  "alternatives": [
    {"name": "John Doe", "score": 82},
    {"name": "Bob Wilson", "score": 71}
  ]
}
```

### 5. Notifications
- Assignee: Task details + due date
- Manager: Assignment confirmation
- Client: Work started notification

### 6. Round-Robin Fallback
If all team members equal:
- Rotate assignments
- Track assignment history
- Ensure fair distribution

## Integrations
- Project management
- Calendar (availability)
- Slack

## Cost
- Automation: Free
