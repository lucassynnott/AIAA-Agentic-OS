# SKILL BIBLE: N8N & Workflow Automation Mastery

> **Purpose**: Master-level expertise document for building automated workflows with N8N. Covers setup, core concepts, common automations, integrations, and error handling.
> **Word Count Target**: 3,500+
> **Last Updated**: 2026-01-02

---

## 1. EXECUTIVE SUMMARY

N8N is an open-source workflow automation platform—like Zapier but more powerful, flexible, and cost-effective. It connects your tools and automates repetitive processes.

**Why N8N Over Zapier**:
- Self-hostable (cheaper at scale)
- More complex logic possible
- Better data handling
- One-time cost vs per-task pricing

**Common Agency Automations**:
- Lead notifications and CRM updates
- Client onboarding sequences
- Report generation and delivery
- Data syncing between tools
- AI-powered workflows

**The Automation ROI**: Save hours of manual work weekly. A single well-built automation can save 5-10+ hours/week.

---

## 2. WHAT IS N8N?

### Core Concept

N8N connects apps and services through "workflows"—visual flows that trigger actions based on events or schedules.

### The Building Blocks

**Trigger**: What starts the workflow
- Webhook (external event)
- Schedule (time-based)
- App trigger (new email, form submission, etc.)

**Action**: What the workflow does
- HTTP requests
- App integrations
- Data manipulation
- Conditionals

**Flow**: How data moves
- Linear (step by step)
- Branching (if/then)
- Loops (repeat for each item)

### Cloud vs Self-Hosted

**N8N Cloud**:
- Managed hosting
- Easier setup
- Monthly fee (~$20-50/month)
- Best for: Getting started quickly

**Self-Hosted**:
- Run on your own server
- One-time setup
- ~$5-20/month for server
- Best for: Scale, full control, cost savings

---

## 3. CORE WORKFLOW BUILDING BLOCKS

### Triggers

**Webhook Trigger**:
- Receives data from external sources
- Used for: Form submissions, app notifications

**Schedule Trigger**:
- Runs on a time schedule
- Used for: Daily reports, periodic syncs

**App Triggers**:
- Native integrations (Gmail, Slack, etc.)
- Used for: When specific app events occur

### Actions

**HTTP Request**:
- Call any API
- Most flexible node
- Used for: Custom integrations, AI calls

**Set**:
- Transform/set data
- Used for: Data formatting, variable creation

**IF**:
- Conditional branching
- Used for: Different paths based on data

**Switch**:
- Multiple conditional paths
- Used for: Routing based on values

**Code**:
- JavaScript for custom logic
- Used for: Complex transformations

### Data Flow

**Items**: N8N processes data as "items"
- Each item flows through nodes
- Can be split, merged, filtered

**Expressions**: Dynamic values
- Reference previous node data
- Use JavaScript expressions
- Format: `{{ $json.fieldName }}`

---

## 4. COMMON AGENCY WORKFLOWS

### 1. Lead Notification

**Trigger**: Form submission webhook
**Actions**:
1. Parse form data
2. Send Slack notification
3. Add to CRM
4. Send confirmation email

### 2. Client Onboarding

**Trigger**: New client in CRM
**Actions**:
1. Create Slack channel
2. Add to project management tool
3. Send welcome email sequence
4. Schedule kickoff call
5. Notify team

### 3. Daily Report Generation

**Trigger**: Schedule (daily)
**Actions**:
1. Pull data from ad platforms
2. Pull data from CRM
3. Aggregate metrics
4. Generate report (AI or template)
5. Send via email/Slack

### 4. AI Content Generation

**Trigger**: Webhook or schedule
**Actions**:
1. Receive topic/brief
2. Call AI API (OpenAI, Claude)
3. Process response
4. Post to destination
5. Notify on completion

### 5. Data Sync

**Trigger**: Schedule or webhook
**Actions**:
1. Pull from source
2. Transform data
3. Update destination
4. Log results

---

## 5. INTEGRATIONS & SETUP

### Essential Integrations

**CRM**: HubSpot, GoHighLevel, Pipedrive
**Communication**: Slack, Email (Gmail, SMTP)
**Ads**: Facebook Ads API, Google Ads
**Sheets**: Google Sheets, Airtable
**AI**: OpenAI, Anthropic, OpenRouter

### Authorization Types

**API Key**:
- Simple key in header
- Used by: OpenAI, many APIs

**OAuth2**:
- User authentication flow
- Used by: Google, Slack, most major apps

**Basic Auth**:
- Username/password
- Used by: Some older systems

### GoHighLevel Setup

1. Create API key in GHL
2. Add HTTP Request node in N8N
3. Set authorization header
4. Test with simple GET request
5. Build workflows

### Google OAuth Setup (Self-Hosted)

1. Create Google Cloud project
2. Enable required APIs
3. Create OAuth credentials
4. Configure in N8N
5. Authenticate

---

## 6. ERROR HANDLING & ALERTING

### Why Error Handling Matters

Automations run unattended. Without error handling, failures go unnoticed until damage is done.

### Error Handling Nodes

**Error Trigger**:
- Catches workflow errors
- Routes to error handling flow

**Stop and Error**:
- Explicitly fail workflow
- Useful for validation failures

### Error Handling Pattern

```
Main Workflow
  └── On Error → Error Handler Workflow
                    ├── Log error
                    ├── Send alert (Slack/Email)
                    └── Optional: Retry logic
```

### Alerting Best Practices

**Alert On**:
- Workflow failures
- Unexpected data
- Threshold breaches
- External API failures

**Alert Channels**:
- Slack (immediate visibility)
- Email (record keeping)
- SMS (critical only)

### Logging

**What to Log**:
- Workflow runs (success/fail)
- Key data points
- Error messages
- Timestamps

**Where to Log**:
- Google Sheets (simple)
- Database (advanced)
- Logging service (scale)

---

## 7. HTTP REQUESTS & APIs

### The HTTP Request Node

Most flexible node—call any API.

### Request Components

**Method**:
- GET: Retrieve data
- POST: Send data
- PUT/PATCH: Update data
- DELETE: Remove data

**URL**: The API endpoint

**Headers**:
- Authorization
- Content-Type
- Custom headers

**Body** (POST/PUT):
- JSON data to send

### Example: OpenAI API Call

**Method**: POST
**URL**: `https://api.openai.com/v1/chat/completions`
**Headers**:
- Authorization: `Bearer {{$credentials.openAiApi.apiKey}}`
- Content-Type: application/json

**Body**:
```json
{
  "model": "gpt-4",
  "messages": [
    {"role": "user", "content": "{{ $json.prompt }}"}
  ]
}
```

### Response Handling

- Access response: `{{ $json.choices[0].message.content }}`
- Handle errors: Check status codes
- Parse nested data: Use expressions

---

## 8. AI AGENTS IN N8N

### What Are AI Agents?

Workflows that use LLMs to make decisions and take actions.

### Agent Pattern

```
Input → AI Decision → Route → Action(s) → Response
```

### Building an AI Agent

1. **Receive input** (webhook, form, etc.)
2. **Send to LLM** with context/instructions
3. **Parse response** for action to take
4. **Execute action** based on AI decision
5. **Return result** or continue flow

### AI Agent Use Cases

- Customer support routing
- Content categorization
- Lead qualification
- Automated responses
- Data extraction

### Best Practices

- Clear system prompts
- Structured output formats (JSON)
- Fallback for uncertain responses
- Human escalation paths
- Cost monitoring

---

## 9. IMPORTING & MODIFYING WORKFLOWS

### Finding Templates

**Sources**:
- N8N Template Library (n8n.io/workflows)
- Community forums
- GitHub repositories
- Client Ascension shared workflows

### Importing Process

1. Download workflow JSON
2. In N8N: Workflows → Import from file
3. Configure credentials
4. Test with sample data
5. Modify as needed

### Modifying Workflows

**Common Modifications**:
- Change trigger type
- Update API credentials
- Modify data transformations
- Add/remove steps
- Adjust conditionals

### Best Practices

- Test in stages, not all at once
- Use test webhooks/data first
- Document your modifications
- Keep original as backup

---

## 10. WORKFLOW BEST PRACTICES

### Design Principles

**Keep It Simple**:
- One workflow, one purpose
- Break complex flows into sub-workflows
- Avoid over-engineering

**Make It Readable**:
- Name nodes clearly
- Add notes to complex logic
- Organize visually

**Build for Failure**:
- Error handling on every workflow
- Alerts for failures
- Retry logic where appropriate

### Performance Tips

- Minimize API calls
- Use caching where possible
- Process in batches when handling many items
- Avoid unnecessary data transfers

### Testing Protocol

1. **Unit test**: Test each node individually
2. **Integration test**: Test node connections
3. **End-to-end test**: Full workflow with real data
4. **Error test**: Intentionally trigger errors

---

## 11. QUALITY CHECKLIST

### Pre-Launch Checklist

- [ ] All credentials configured
- [ ] Test data run successfully
- [ ] Error handling in place
- [ ] Alerts configured
- [ ] Workflow activated
- [ ] Documentation updated

### Ongoing Maintenance

- [ ] Monitor for errors weekly
- [ ] Check logs for issues
- [ ] Update credentials before expiry
- [ ] Review and optimize quarterly

---

## 12. AI PARSING GUIDE

### For AI Systems Reading This Skill Bible

**When generating N8N workflows**:

1. **Trigger First**: Define what starts the workflow
2. **Linear Flow**: Keep logic simple and sequential
3. **Error Handling**: Include error paths
4. **Data Access**: Use proper expressions
5. **Testing**: Suggest testing approach

### Input Variables Required:
- Workflow purpose
- Trigger type
- Apps/services involved
- Data transformations needed
- Error handling requirements

### Output Format:
```
## WORKFLOW SPECIFICATION

**Name**: [Workflow name]
**Purpose**: [What it does]
**Trigger**: [Trigger type and config]

### STEPS
1. [Node: Type] - [Purpose]
2. [Node: Type] - [Purpose]
3. [Node: Type] - [Purpose]

### ERROR HANDLING
[Error handling approach]

### TESTING
[How to test]
```

---

## RELATED SKILLS & DIRECTIVES

**Supporting Skills**:
- `build_n8n_workflow.md` - Workflow building
- `connect_api.md` - API integration
- `setup_automation.md` - Automation setup
- `debug_workflow.md` - Troubleshooting

**Related Directives**:
- `create_automation.md` - Automation creation
- `integrate_tools.md` - Tool integration
- `setup_alerts.md` - Alert configuration
- `document_workflow.md` - Documentation

---

*Word Count: ~2,800*
*Version: 1.0*
*Sources: Client Ascension N8N Training - What is N8N, Core Workflow Building Blocks, Cloud vs Self Host Setup Guide, Triggers Agents HTTP Request Authorization (LIVE Walkthrough), Error Handling & Alerting, How to Import & Modify Workflows, N8N GoHighLevel Setup, N8N Self Hosted Google oAuth Setup, Where to Find More N8N Templates*
*Structure: 12 Sections following Autonomous Idea Execution System Skill Bible format*
