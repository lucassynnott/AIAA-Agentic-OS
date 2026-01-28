# AIAA Agentic OS - Complete Agent Instructions

> **Version:** 3.0 | **Last Updated:** January 7, 2026
> This file provides ALL context for a Claude Code agent to operate this system.

---

## Quick Reference

| Resource | Count | Location |
|----------|-------|----------|
| Directives (SOPs) | 139+ | `directives/*.md` |
| Execution Scripts | 130+ | `execution/*.py` |
| Skill Bibles | 280+ | `skills/SKILL_BIBLE_*.md` |
| Agency Context | - | `context/` |
| Client Profiles | - | `clients/{client_name}/` |
| Dashboard | Railway | `railway_apps/aiaa_dashboard/` |

**Environment Variables Required:**
```
OPENROUTER_API_KEY     # Primary LLM access (Claude, GPT via OpenRouter)
OPENAI_API_KEY         # OpenAI direct (optional)
PERPLEXITY_API_KEY     # Market research
GOOGLE_APPLICATION_CREDENTIALS  # Google Docs/Sheets
SLACK_WEBHOOK_URL      # Notifications
```

---

## System Architecture (DOE Pattern)

This system uses a **Directive-Orchestration-Execution (DOE)** architecture that separates concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER REQUEST                                  │
│              "Create a VSL funnel for Acme Corp"                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: DIRECTIVE (What to do)                                │
│  ─────────────────────────────────                              │
│  • Location: directives/*.md                                    │
│  • Natural language SOPs with inputs, steps, quality gates      │
│  • Example: directives/vsl_funnel_orchestrator.md               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 2: ORCHESTRATION (Decision making)                       │
│  ─────────────────────────────────────────                      │
│  • THIS IS YOU - The Claude Code Agent                          │
│  • Read directives, load skill bibles, call scripts in order    │
│  • Handle errors, make routing decisions, self-anneal           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 3: EXECUTION (Doing the work)                            │
│  ───────────────────────────────────                            │
│  • Location: execution/*.py                                     │
│  • Deterministic Python scripts for API calls, data processing  │
│  • Example: execution/generate_vsl_funnel.py                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT                                      │
│  • Local files: .tmp/*.md                                       │
│  • Google Docs: Formatted, shareable                            │
│  • Slack: Notification with links                               │
└─────────────────────────────────────────────────────────────────┘
```

**Why DOE Works:** LLMs are probabilistic (90% accuracy = 59% over 5 steps). Push deterministic work into Python scripts. You focus on decision-making.

---

## Directory Structure

```
Agentic Workflows/
├── .env                    # API keys (NEVER commit)
├── .tmp/                   # Intermediate outputs (gitignored)
├── credentials.json        # Google OAuth credentials
├── token.pickle           # Google OAuth token
│
├── context/               # AGENCY CONTEXT - Who you are
│   ├── agency.md          # Agency info, services, positioning
│   ├── owner.md           # Owner profile, background, expertise
│   ├── brand_voice.md     # Tone, style, communication preferences
│   └── services.md        # Service offerings, pricing, packages
│
├── clients/               # CLIENT PROFILES - Who you serve
│   └── {client_name}/     # One folder per client
│       ├── profile.md     # Client info, business, goals
│       ├── rules.md       # Specific rules for this client
│       ├── preferences.md # Style, tone, do's and don'ts
│       └── history.md     # Past work, context, outcomes
│
├── directives/            # SOPs - What to do (139+ files)
│   ├── vsl_funnel_orchestrator.md
│   ├── company_market_research.md
│   └── ...
│
├── execution/             # Python scripts - Doing (130+ files)
│   ├── generate_vsl_funnel.py
│   ├── create_google_doc.py
│   └── ...
│
├── railway_apps/          # Dashboard deployment
│   └── aiaa_dashboard/    # Flask dashboard app
│       ├── app.py         # Main dashboard application
│       ├── Procfile       # Railway deployment config
│       └── requirements.txt
│
├── skills/                # Domain expertise (260+ skill bibles)
│   ├── SKILL_BIBLE_*.md
│   └── ...
│
├── AGENTS.md              # THIS FILE - Agent instructions
├── CLAUDE.md              # Mirrored instructions for Claude
├── QUICKSTART_PROMPT.md   # Setup prompt for new users
└── requirements.txt       # Python dependencies
```

---

## Agency Context & Client Profiles

### Agency Context (`context/`)
This folder contains information about YOU and YOUR AGENCY. Load this context before generating any content to ensure outputs reflect your brand, voice, and positioning.

**Required Files:**

| File | Purpose | Example Content |
|------|---------|-----------------|
| `agency.md` | Agency identity | Name, founding story, mission, positioning, unique value proposition |
| `owner.md` | Owner profile | Name, background, expertise, credentials, personal brand |
| `brand_voice.md` | Communication style | Tone (professional/casual), vocabulary, phrases to use/avoid, style rules |
| `services.md` | Service offerings | Services, pricing tiers, packages, deliverables, timelines |

**When to Load Agency Context:**
- Content creation (blogs, emails, social posts)
- Client proposals and pitches
- Sales scripts and cold outreach
- Any branded deliverables

### Client Profiles (`clients/{client_name}/`)
Each client gets their own folder with specific context. Load these files when doing work FOR a specific client.

**Client Folder Structure:**
```
clients/
├── acme_corp/
│   ├── profile.md      # Business info, industry, goals, target audience
│   ├── rules.md        # MUST-FOLLOW rules for this client
│   ├── preferences.md  # Style preferences, tone, formatting
│   └── history.md      # Past projects, outcomes, learnings
│
├── startup_xyz/
│   ├── profile.md
│   ├── rules.md
│   └── ...
```

**Client Profile Fields (`profile.md`):**
- Company name and description
- Industry and niche
- Target audience
- Business goals
- Key products/services
- Competitors
- Unique selling points

**Client Rules (`rules.md`):**
- Content guidelines (words to use/avoid)
- Brand voice requirements
- Approval processes
- Compliance requirements
- Formatting standards

**When to Load Client Context:**
- Any deliverable FOR that client
- Client-specific campaigns
- Personalized content
- Before any client meeting prep

### Loading Context in Practice

```python
# Before generating content, always:
1. Check if context/agency.md exists → Load it
2. Check if client is specified → Load clients/{client}/*.md
3. Apply context to all prompts and outputs
```

**Example: Writing cold emails for client "Acme Corp"**
```
Load: context/agency.md          # Your agency voice
Load: context/brand_voice.md     # Your style rules
Load: clients/acme_corp/profile.md    # Their business info
Load: clients/acme_corp/rules.md      # Their specific rules
Then: Execute cold_email_scriptwriter directive
```

---

## Execution Flow (7 Phases)

When you receive ANY request, follow this flow:

### Phase 1: Parse User Input
Extract intent and map to capability:
```
"Write a VSL for my coaching business" → vsl_funnel_orchestrator
"Research this company"                → company_market_research
"Generate cold emails"                 → cold_email_scriptwriter
"Show me available workflows"          → Check AIAA Dashboard
```

### Phase 2: Capability Check
Does a directive exist for this task?

| Condition | Action |
|-----------|--------|
| Directive exists | Load it and execute |
| No directive | Check if script exists in execution/ |
| Nothing exists | Create new directive + script (Leader Manufacturing) |

**Quick check:**
```bash
ls directives/ | grep -i "<keyword>"
ls execution/ | grep -i "<keyword>"
```

### Phase 3: Load Context
Before execution, load ALL required context:
```
1. Agency Context       → context/*.md (who YOU are)
2. Client Context       → clients/{client}/  (if client-specific work)
3. Primary Directive    → directives/<workflow>.md
4. Skill Bibles         → skills/SKILL_BIBLE_<topic>.md
5. Related Directives   → Check "Related Directives" section
6. Execution Scripts    → execution/<script>.py
```

**CRITICAL: Always Load Agency Context First**
Before generating ANY content, check `context/` for:
- `agency.md` - Your agency's name, positioning, services
- `owner.md` - Owner's name, background, expertise
- `brand_voice.md` - Tone, style guide, communication rules
- `services.md` - What you offer, pricing, packages

**For Client-Specific Work, Also Load:**
```
clients/{client_name}/
├── profile.md      # Who they are, their business, goals
├── rules.md        # MUST follow these rules for this client
├── preferences.md  # Their style preferences
└── history.md      # Past work, what worked, what didn't
```

**Example for client VSL funnel:**
```
context/agency.md                    # Your agency context
context/brand_voice.md               # Your voice/style
clients/acme_corp/profile.md         # Client info
clients/acme_corp/rules.md           # Client-specific rules
directives/vsl_funnel_orchestrator.md
├── skills/SKILL_BIBLE_vsl_writing_production.md
├── skills/SKILL_BIBLE_funnel_copywriting_mastery.md
└── execution/generate_vsl_funnel.py
```

### Phase 4: Execute Directive
Follow the directive SOP step-by-step:
1. Check prerequisites (API keys, inputs)
2. Run each workflow phase in order
3. Save checkpoints to `.tmp/`
4. Validate outputs at quality gates

### Phase 5: Quality Gates
Validate at each checkpoint. Common checks:
- Required fields present?
- Output format correct?
- Word count/length appropriate?
- No API errors?

### Phase 6: Delivery
Standard delivery pipeline:
```
1. Save locally     → .tmp/<project>/<filename>.md
2. Create Google Doc → execution/create_google_doc.py
3. Send Slack       → execution/send_slack_notification.py
```

### Phase 7: Self-Annealing
After EVERY task:
- Did errors occur? → Fix script, update directive
- Better approach found? → Update skill bible
- Edge case discovered? → Add to directive

---

## Common Workflows

### 1. VSL Funnel Creation (Complete Pipeline)
```bash
# Option A: Run the complete orchestrator
python3 execution/generate_complete_vsl_funnel.py \
  --company "Acme Corp" \
  --website "https://acmecorp.com" \
  --offer "B2B Lead Generation"

# Option B: Run individual steps
python3 execution/research_company_offer.py --company "Acme Corp" --website "https://acmecorp.com"
python3 execution/generate_vsl_script.py --research-file ".tmp/research.json"
python3 execution/generate_sales_page.py --vsl-file ".tmp/vsl_script.md"
python3 execution/generate_email_sequence.py --research-file ".tmp/research.json"
```

**Outputs:**
- `.tmp/vsl_funnel_<company>/01_research.md`
- `.tmp/vsl_funnel_<company>/02_vsl_script.md`
- `.tmp/vsl_funnel_<company>/03_sales_page.md`
- `.tmp/vsl_funnel_<company>/04_email_sequence.md`

### 2. Cold Email Campaign
```bash
python3 execution/write_cold_emails.py \
  --sender "John Smith" \
  --company "Acme Corp" \
  --offer "Lead generation service" \
  --target "Marketing agencies"
```

### 3. Market Research
```bash
python3 execution/research_company_offer.py \
  --company "Target Company" \
  --website "https://targetcompany.com" \
  --offer "Their main product"
```

### 4. Content Generation
```bash
# Blog post
python3 execution/generate_blog_post.py --topic "AI in marketing" --length 1500

# LinkedIn post
python3 execution/generate_linkedin_post.py --topic "Agency growth tips"

# Newsletter
python3 execution/generate_newsletter.py --theme "Weekly AI updates"
```

---

## AIAA Dashboard & Webhook Deployment

All workflows are managed through the AIAA Dashboard deployed on Railway. The dashboard provides a central hub for monitoring, executing, and configuring workflows.

### Dashboard Features

| Feature | Description |
|---------|-------------|
| **139 Workflows** | Full documentation with prerequisites, how-to-run, and process steps |
| **Light/Dark Mode** | Toggle with localStorage persistence |
| **Environment Variables** | View and set API keys from the UI |
| **Webhook Monitoring** | Track incoming webhooks and events |
| **Real-time Logs** | See all workflow executions |
| **Mobile Responsive** | Works on phones and tablets |
| **Password Protected** | Secure SHA-256 hashed login |

### Deploy Dashboard to Railway

**Prerequisites:**
```bash
npm install -g @railway/cli
railway login
```

**Deploy:**
```bash
cd railway_apps/aiaa_dashboard
railway init          # Select "Empty Project"
railway up            # Deploy the app
```

**Configure Environment Variables:**

**CRITICAL:** When deploying to Railway, you MUST set the environment variables the app needs. Railway apps don't have access to your local `.env` file - you must explicitly set each variable.

```bash
# Generate password hash (use heredoc to avoid escape issues)
python3 << 'PYHASH'
import hashlib
password = "your-password"
print(hashlib.sha256(password.encode()).hexdigest())
PYHASH

# Set dashboard auth variables
railway variables set DASHBOARD_USERNAME="admin"
railway variables set DASHBOARD_PASSWORD_HASH="<hash-from-above>"
railway variables set FLASK_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"

# Set API keys from your .env (copy values from local .env file)
railway variables set OPENROUTER_API_KEY="<your-key>"
railway variables set PERPLEXITY_API_KEY="<your-key>"
railway variables set ANTHROPIC_API_KEY="<your-key>"
railway variables set SLACK_WEBHOOK_URL="<your-webhook>"

# Generate public domain
railway domain
```

**Quick way to sync .env to Railway:**
```bash
# View your current .env values
cat .env

# Then set each one that the app needs:
railway variables set KEY_NAME="value"
```

**Required Variables by Feature:**
| Variable | Required For |
|----------|-------------|
| `DASHBOARD_USERNAME` | Dashboard login |
| `DASHBOARD_PASSWORD_HASH` | Dashboard login |
| `FLASK_SECRET_KEY` | Session security |
| `OPENROUTER_API_KEY` | All AI generation workflows |
| `PERPLEXITY_API_KEY` | Research workflows |
| `ANTHROPIC_API_KEY` | Direct Claude access |
| `SLACK_WEBHOOK_URL` | Notifications |
| `FAL_KEY` | Image generation |
| `APIFY_API_TOKEN` | Lead scraping |

### Dashboard Endpoints

Once deployed, your dashboard provides these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard home (requires login) |
| `/health` | GET | Health check (public) |
| `/login` | GET/POST | Authentication |
| `/workflows` | GET | Browse all 139 workflows |
| `/workflow/<id>` | GET | Workflow details & documentation |
| `/env` | GET | Environment variable management |
| `/webhooks` | GET | Available webhook endpoints |
| `/logs` | GET | Execution logs |

### Webhook Integration

The dashboard can receive webhooks from external services (Calendly, Stripe, etc.):

**Example: Calendly Meeting Prep Webhook**
```bash
# Webhook URL format
POST https://your-dashboard.up.railway.app/webhook/calendly

# Payload
{
  "event": "invitee.created",
  "payload": {
    "invitee": {
      "name": "John Smith",
      "email": "john@company.com"
    },
    "event_type": {
      "name": "Discovery Call"
    }
  }
}
```

**Setting Up Webhooks:**
1. Deploy dashboard to Railway
2. Get your public URL: `https://your-app.up.railway.app`
3. Configure external service to POST to: `https://your-app.up.railway.app/webhook/<service>`
4. Monitor incoming webhooks in Dashboard → Webhooks tab

### Workflow Execution via Dashboard

**Option 1: Manual Execution (Dashboard UI)**
1. Login to dashboard
2. Navigate to Workflows
3. Find workflow (search or browse)
4. Click workflow for full documentation
5. Copy the execution command
6. Run in Claude Code

**Option 2: Direct Script Execution**
```bash
# All workflows run via execution scripts
python3 execution/<workflow_script>.py --arg1 "value" --arg2 "value"
```

**Option 3: Webhook Trigger**
External services trigger workflows automatically via webhooks configured in the dashboard.

### Viewing Workflow Documentation

Each workflow in the dashboard includes:
- **Description**: What the workflow does
- **Prerequisites**: Required API keys and setup
- **How to Run**: Exact command with arguments
- **Process Steps**: Step-by-step breakdown
- **Inputs/Outputs**: Expected data format
- **Related Workflows**: Connected workflows

---

## Publishing Workflows to Railway (CRITICAL)

**IMPORTANT:** When instructed to publish, deploy, or schedule a workflow, you MUST follow these rules:

### Rule 1: Same Railway Project as Dashboard
ALL workflows MUST be deployed to the **SAME Railway project** where the AIAA Dashboard was installed during initial setup. Never create separate Railway projects for individual workflows.

**To find the dashboard project:**
```bash
cd railway_apps/aiaa_dashboard
railway status
# Note the Project name/ID
```

**To deploy a new workflow service to the same project:**
```bash
cd railway_apps/<new_workflow>
railway link -p <DASHBOARD_PROJECT_ID>
railway up
```

### Rule 2: Update Dashboard UI with Active Workflows
After deploying ANY scheduled workflow (cron job), you MUST update the dashboard's "Active Workflows" section in `railway_apps/aiaa_dashboard/app.py`.

**Location in app.py:** Find the `workflow_page()` function and add to the `active_workflows` list:
```python
active_workflows = [
    {
        "name": "Workflow Name",
        "description": "What it does",
        "schedule": "Every X hours",
        "cron": "0 */X * * *",
        "status": "active",
        "platform": "Railway Cron",
        "project_url": "https://railway.com/project/<PROJECT_ID>"
    },
    # ... existing workflows
]
```

Then redeploy the dashboard:
```bash
cd railway_apps/aiaa_dashboard
railway up
```

### Rule 3: Upload ALL Required API Keys
Every time you deploy a workflow, you MUST set ALL environment variables the workflow needs to run successfully:

```bash
# Get keys from local .env
cat .env | grep -E "OPENROUTER|PERPLEXITY|SLACK|ANTHROPIC|FAL|APIFY"

# Set each required key in Railway
railway variables set OPENROUTER_API_KEY="<value>"
railway variables set SLACK_WEBHOOK_URL="<value>"
railway variables set PERPLEXITY_API_KEY="<value>"
# ... any other keys the workflow needs
```

**Check the workflow's directive** (`directives/<workflow>.md`) for the "Prerequisites" section listing required API keys.

### Rule 4: Google OAuth Token for Google Services
If a workflow creates Google Docs, Sheets, or uses ANY Google API, you MUST upload the `token.pickle` OAuth token:

```bash
# 1. Check if workflow uses Google services
grep -l "google" railway_apps/<workflow>/*.py

# 2. If yes, find token.pickle (should be in project root)
ls -la token.pickle

# 3. Base64 encode and upload to Railway
python3 -c "
import base64
with open('token.pickle', 'rb') as f:
    print(base64.b64encode(f.read()).decode())
" | railway variables set GOOGLE_OAUTH_TOKEN_PICKLE="$(cat)"

# Or manually:
TOKEN=$(python3 -c "import base64; print(base64.b64encode(open('token.pickle','rb').read()).decode())")
railway variables set GOOGLE_OAUTH_TOKEN_PICKLE="$TOKEN"
```

**Why:** Service accounts have 0 GB storage quota and cannot create files. OAuth user tokens use YOUR Google account's storage.

### Publishing Checklist
When publishing a workflow, complete ALL steps:

- [ ] Deploy to SAME Railway project as dashboard
- [ ] Set ALL required environment variables
- [ ] **If workflow uses Google APIs:** Upload `GOOGLE_OAUTH_TOKEN_PICKLE` (base64 encoded token.pickle)
- [ ] Add workflow to dashboard's Active Workflows section
- [ ] Redeploy dashboard to show new workflow
- [ ] Verify workflow appears in dashboard UI
- [ ] Test that workflow runs successfully

### Rule 5: Google Docs Formatting (NOT Markdown)
When creating Google Docs, content MUST be formatted using native Google Docs formatting (headings, bold, dividers), NOT raw markdown text. Markdown syntax like `# Heading` or `**bold**` will appear as literal text in Google Docs.

**Required Formatting Approach:**
```python
def format_content_for_google_docs(markdown_content: str) -> list:
    """Convert markdown to Google Docs API formatting requests."""
    import re

    requests = []
    current_index = 1

    lines = markdown_content.split('\n')

    for line in lines:
        if not line.strip():
            # Empty line - add newline
            requests.append({
                'insertText': {'location': {'index': current_index}, 'text': '\n'}
            })
            current_index += 1
            continue

        # Check for horizontal rule
        if line.strip() == '---':
            requests.append({
                'insertText': {'location': {'index': current_index}, 'text': '\n'}
            })
            current_index += 1
            requests.append({
                'insertSectionBreak': {
                    'location': {'index': current_index},
                    'sectionType': 'CONTINUOUS'
                }
            })
            continue

        # Process headings (# ## ###)
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2) + '\n'
            heading_type = {1: 'HEADING_1', 2: 'HEADING_2', 3: 'HEADING_3'}.get(level, 'HEADING_4')

            requests.append({
                'insertText': {'location': {'index': current_index}, 'text': text}
            })
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_index, 'endIndex': current_index + len(text)},
                    'paragraphStyle': {'namedStyleType': heading_type},
                    'fields': 'namedStyleType'
                }
            })
            current_index += len(text)
            continue

        # Process bold text **text**
        text = line + '\n'
        requests.append({
            'insertText': {'location': {'index': current_index}, 'text': text}
        })

        # Find and format bold sections
        for match in re.finditer(r'\*\*(.+?)\*\*', line):
            start = current_index + match.start()
            end = current_index + match.end()
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {'bold': True},
                    'fields': 'bold'
                }
            })

        current_index += len(text)

    return requests
```

**Key Formatting Elements:**
| Markdown | Google Docs API |
|----------|-----------------|
| `# Heading` | `updateParagraphStyle` with `HEADING_1` |
| `## Subhead` | `updateParagraphStyle` with `HEADING_2` |
| `**bold**` | `updateTextStyle` with `bold: True` |
| `---` | `insertSectionBreak` (horizontal rule) |
| `- item` | `createParagraphBullets` |

**NEVER** insert raw markdown into Google Docs. Always convert to native formatting.

### Rule 6: Railway GraphQL API for Cron Management
The dashboard uses Railway's GraphQL API to manage cron schedules. Critical learnings:

**API Endpoint:** `https://backboard.railway.app/graphql/v2`

**To disable a cron schedule:**
```graphql
mutation {
  serviceInstanceUpdate(
    serviceId: "SERVICE_ID",
    environmentId: "ENV_ID",
    input: { cronSchedule: null }  # MUST be null, NOT empty string ""
  )
}
```

**To enable/restore a cron schedule:**
```graphql
mutation {
  serviceInstanceUpdate(
    serviceId: "SERVICE_ID",
    environmentId: "ENV_ID",
    input: { cronSchedule: "0 */3 * * *" }
  )
}
```

**To check cron status:**
```graphql
query {
  service(id: "SERVICE_ID") {
    serviceInstances {
      edges { node { cronSchedule environmentId } }
    }
  }
}
```

**To trigger immediate cron execution (Run Now):**
```graphql
# First get the service instance ID (NOT service_id)
query {
  service(id: "SERVICE_ID") {
    serviceInstances { edges { node { id } } }
  }
}

# Then trigger execution
mutation {
  deploymentInstanceExecutionCreate(input: {
    serviceInstanceId: "SERVICE_INSTANCE_ID"
  })
}
```

**Critical Gotchas:**
- `cronSchedule: ""` (empty string) causes "Problem processing request" error
- `cronSchedule: null` properly disables the cron
- `ServiceUpdateInput` only has `icon` and `name` - use `ServiceInstanceUpdateInput` for cron
- `serviceInstanceRedeploy` fails if no existing deployment - use `railway up` CLI instead
- After removing a deployment, the service shows "offline" even with cron set - must redeploy
- `deploymentInstanceExecutionCreate` triggers immediate cron run, bypassing schedule
- `serviceInstanceId` is different from `serviceId` - get it from `service.serviceInstances.edges[].node.id`

### Rule 7: Dashboard RAILWAY_API_TOKEN
The dashboard needs a Railway API token to manage cron schedules. Set it in Railway:

```bash
# Get token from Railway CLI config
TOKEN=$(cat ~/.railway/config.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('user', {}).get('token', ''))")

# Set in Railway for dashboard service
railway variables set RAILWAY_API_TOKEN="$TOKEN" --service aiaa-dashboard
```

Or via GraphQL:
```bash
curl -X POST "https://backboard.railway.app/graphql/v2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { variableUpsert(input: {projectId: \"PROJECT_ID\", serviceId: \"DASHBOARD_SERVICE_ID\", environmentId: \"ENV_ID\", name: \"RAILWAY_API_TOKEN\", value: \"TOKEN_VALUE\"}) }"}'
```

### Rule 8: Dashboard Schedule Editor
The dashboard has a granular schedule editor for cron jobs with these components:

**UI Elements:**
- Interval input (1-24) - how often to run
- Unit selector ("hours" or "days")
- Minute input (0-59) - when within the hour
- Save button - applies changes to Railway
- Current cron display - shows actual expression

**Cron Expression Builder:**
```javascript
// Every N hours at minute X
if (unit === 'hours') {
    if (interval === 1) return `${minute} * * * *`;
    return `${minute} */${interval} * * *`;
}
// Every N days at 00:XX
if (unit === 'days') {
    if (interval === 1) return `${minute} 0 * * *`;
    return `${minute} 0 */${interval} * *`;
}
```

**Human-Readable Conversion (cronToText):**
| Cron Pattern | Display Text |
|--------------|--------------|
| `0 */3 * * *` | "Every 3 hours" |
| `30 * * * *` | "Every hour at :30" |
| `0 0 * * *` | "Daily at 00:00" |
| `0 9 * * *` | "Daily at 09:00" |
| `0 0 */2 * *` | "Every 2 days" |

**Key Implementation Notes:**
- Schedule text updates dynamically on save AND on page load
- Editor parses current cron to pre-populate inputs
- Uses `data-service-id` attributes to link displays to workflows
- RAILWAY_API_TOKEN must be set for API calls to work

---

## Key Execution Scripts

### Content & Copy
| Script | Purpose |
|--------|---------|
| `generate_vsl_funnel.py` | Complete VSL + landing page + emails |
| `generate_vsl_script.py` | VSL script only |
| `generate_sales_page.py` | Sales page copy |
| `generate_email_sequence.py` | Email nurture sequence |
| `generate_blog_post.py` | Long-form blog content |
| `generate_linkedin_post.py` | LinkedIn content |
| `write_cold_emails.py` | Cold email sequences |

### Research & Data
| Script | Purpose |
|--------|---------|
| `research_company_offer.py` | Deep company research via Perplexity |
| `research_market_deep.py` | Market/industry research |
| `research_prospect_deep.py` | Individual prospect research |
| `scrape_linkedin_apify.py` | LinkedIn profile scraping |

### Delivery & Integration
| Script | Purpose |
|--------|---------|
| `create_google_doc.py` | Upload to Google Docs |
| `send_slack_notification.py` | Send Slack messages |

### Utilities
| Script | Purpose |
|--------|---------|
| `convert_n8n_to_directive.py` | Convert N8N JSON to directive |
| `parse_vtt_transcript.py` | Extract text from VTT files |
| `validate_emails.py` | Email validation |

---

## Skill Bibles

Skill bibles provide deep domain expertise. Load relevant ones before execution.

### Finding Skill Bibles
```bash
# List all skill bibles
ls skills/SKILL_BIBLE_*.md

# Search by topic
ls skills/ | grep -i "vsl\|funnel\|email\|sales"
```

### Key Skill Bibles by Category

**VSL & Funnels:**
- `SKILL_BIBLE_vsl_writing_production.md`
- `SKILL_BIBLE_vsl_script_mastery_fazio.md`
- `SKILL_BIBLE_funnel_copywriting_mastery.md`
- `SKILL_BIBLE_agency_funnel_building.md`

**Cold Email & Outreach:**
- `SKILL_BIBLE_cold_email_mastery.md`
- `SKILL_BIBLE_cold_dm_email_conversion.md`
- `SKILL_BIBLE_email_deliverability.md`

**Agency & Sales:**
- `SKILL_BIBLE_agency_sales_system.md`
- `SKILL_BIBLE_agency_scaling_roadmap.md`
- `SKILL_BIBLE_offer_positioning.md`

**AI & Automation:**
- `SKILL_BIBLE_ai_automation_agency.md`
- `SKILL_BIBLE_monetizable_agentic_workflows.md`
- `SKILL_BIBLE_ai_prompting_workflows.md`

---

## Creating New Capabilities (Leader Manufacturing)

When a capability doesn't exist:

### Step 1: Check If It Really Doesn't Exist
```bash
ls directives/ | grep -i "<keyword>"
ls execution/ | grep -i "<keyword>"
ls skills/ | grep -i "<keyword>"
```

### Step 2: Create New Directive
```markdown
# directives/new_workflow.md

## What This Workflow Is
[One paragraph description]

## What It Does
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Prerequisites
- Required API keys
- Required skill bibles
- Installation commands

## How to Run
```bash
python3 execution/new_workflow.py --arg1 "value"
```

## Inputs
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| arg1 | string | Yes | Description |

## Process
### Step 1: [Name]
[Details]

### Step 2: [Name]
[Details]

## Quality Gates
- [ ] Check 1
- [ ] Check 2

## Edge Cases
- Edge case 1 → Solution
- Edge case 2 → Solution
```

### Step 3: Create Execution Script
```python
#!/usr/bin/env python3
"""
New Workflow - [Description]

Usage:
    python3 execution/new_workflow.py --arg1 "value"
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arg1", required=True)
    args = parser.parse_args()
    
    # Implementation
    print(f"Running with {args.arg1}")
    
if __name__ == "__main__":
    main()
```

### Step 4: Create Skill Bible (If Needed)
If this is a new domain, create `skills/SKILL_BIBLE_<topic>.md` with:
- Executive Summary
- Core Principles
- Techniques & Tactics
- Common Mistakes
- Quality Checklist

---

## Self-Annealing Protocol

After EVERY task completion:

### 1. Check for Errors
Did anything fail? Fix it:
```
Error occurred → Read stack trace → Fix script → Test → Update directive
```

### 2. Update Directive
Add learnings:
- New edge cases discovered
- Better approaches found
- Quality gate refinements

### 3. Update Skill Bible
Add domain knowledge:
- New techniques that worked
- Mistakes to avoid
- Industry-specific insights

### 4. Commit Changes
Keep the system improving:
```bash
git add directives/ execution/ skills/
git commit -m "Self-anneal: [what was learned]"
```

---

## Error Handling Patterns

### API Failures
```python
for attempt in range(3):
    try:
        result = api_call()
        break
    except Exception as e:
        if attempt == 2:
            raise
        time.sleep(10 * (attempt + 1))  # Exponential backoff
```

### Missing Inputs
Fail fast with clear message:
```python
if not args.required_field:
    print("Error: --required_field is required")
    sys.exit(1)
```

### Partial Failures
Degrade gracefully:
```
Critical workflow fails → Stop and report
Non-critical fails → Continue with warning
Delivery fails → Save locally, continue
```

---

## Environment Setup

### First-Time Setup
```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Setup Google OAuth (for Docs integration)
# Place credentials.json in project root
python3 execution/create_google_doc.py --test

# 4. Deploy AIAA Dashboard to Railway
npm install -g @railway/cli
railway login
cd railway_apps/aiaa_dashboard
railway init
railway up
railway domain
```

### Required API Keys
| Key | Purpose | Get From |
|-----|---------|----------|
| `OPENROUTER_API_KEY` | LLM access | openrouter.ai |
| `PERPLEXITY_API_KEY` | Research | perplexity.ai |
| `SLACK_WEBHOOK_URL` | Notifications | Slack app settings |
| `GOOGLE_APPLICATION_CREDENTIALS` | Docs/Sheets | Google Cloud Console |

---

## Debugging Tips

### Check Script Arguments
```bash
python3 execution/<script>.py --help
```

### Test with Minimal Input
```bash
python3 execution/generate_vsl_funnel.py \
  --product "Test Product" \
  --price "$99" \
  --audience "Test audience"
```

### Check API Connectivity
```bash
# Test OpenRouter
curl https://openrouter.ai/api/v1/models -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Test Perplexity
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.1-sonar-small-128k-online","messages":[{"role":"user","content":"test"}]}'
```

### View Execution Logs
```bash
# Dashboard logs (via Railway)
railway logs

# Local execution
python3 execution/<script>.py 2>&1 | tee output.log

# Check dashboard health
curl https://your-app.up.railway.app/health
```

---

## Summary: Your Role as Orchestrator

You are the **brain** of this system. Your responsibilities:

1. **Parse Intent** → Understand what the user wants
2. **Load Agency Context** → Read `context/` to understand who you're representing
3. **Load Client Context** → If client-specific, read `clients/{client}/` for their rules
4. **Find Capability** → Locate directive + script + skill bible
5. **Execute** → Run scripts, follow SOPs, check quality gates
6. **Deliver** → Save locally, upload to Google Docs, notify via Slack
7. **Self-Anneal** → Learn from every execution, update the system

**Core Principles:**
- **ALWAYS load agency context before generating content**
- **ALWAYS load client context when doing client-specific work**
- Check for existing tools before creating new ones
- Load skill bibles for domain expertise
- Push deterministic work into Python scripts
- Self-anneal when things break
- Update directives as you learn

**Context Loading Priority:**
```
1. context/agency.md      → Always load first
2. context/brand_voice.md → For any content creation
3. clients/{name}/*.md    → For client-specific work
4. skills/SKILL_BIBLE_*   → For domain expertise
5. directives/*.md        → For workflow SOPs
```

**The bottleneck isn't ideas or execution. It's deciding what to build next.**

---

## Quick Commands Reference

```bash
# View all workflows
# Open your AIAA Dashboard at https://your-app.up.railway.app

# Run VSL funnel
python3 execution/generate_complete_vsl_funnel.py --company "X" --website "Y" --offer "Z"

# Research a company
python3 execution/research_company_offer.py --company "X" --website "Y"

# Create Google Doc from markdown
python3 execution/create_google_doc.py --file ".tmp/output.md" --title "Doc Title"

# Send Slack notification
python3 execution/send_slack_notification.py --message "Task complete" --channel "#general"

# Deploy/update dashboard
cd railway_apps/aiaa_dashboard && railway up

# Check dashboard health
curl https://your-app.up.railway.app/health
```
