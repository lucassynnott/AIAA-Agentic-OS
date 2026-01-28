# Slack Notifier

## What This Workflow Is
Utility workflow that sends formatted Slack notifications with workflow completion status, links to deliverables, and execution metadata.

## What It Does
1. Receives workflow completion data
2. Formats message with status, links, and metadata
3. Sends to specified Slack channel
4. Handles errors gracefully (doesn't break parent workflow)

## Prerequisites

### Required Environment Variables
```
SLACK_WEBHOOK_URL=your_webhook_url
SLACK_CHANNEL=#client-deliverables
```

### Installation
```bash
pip install requests
```

## Inputs
- `workflowName` (string): Name of completed workflow
- `status` ("success" | "failed" | "partial"): Execution status
- `deliverables` (array): List of output links/files
- `metadata` (object): Execution details (duration, errors, etc.)
- `company` (string, optional): Client company name

## Process
1. Format Slack message with blocks
2. Add status emoji (✅ success, ❌ failed, ⚠️ partial)
3. Include all deliverable links
4. Add execution metadata (time, errors)
5. Send via webhook
6. Log response (don't throw on failure)

## Outputs
```json
{
  "sent": true,
  "messageId": "slack_msg_123",
  "channel": "#client-deliverables",
  "timestamp": "2026-01-05T12:00:00Z"
}
```

## Example Message
```
✅ VSL Funnel Complete: Acme Corp

**Deliverables:**
📄 Market Research: [Link]
🎬 VSL Script: [Link]
📝 Sales Page Copy: [Link]
📧 Email Sequence (7 emails): [Link]

**Execution Time:** 4m 32s
**Status:** All workflows successful
```

## Integration
Position 6/7 (final step) in VSL funnel pipeline. Called after all documents created.
