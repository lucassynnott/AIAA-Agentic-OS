# SKILL BIBLE: DO Framework Fundamentals (Directive-Orchestration-Execution)

## Executive Summary

The Directive-Orchestration-Execution (DO) framework solves the fundamental mismatch between probabilistic AI and deterministic business requirements. LLMs are flexible but unreliable for business operations. Traditional automation is rigid but consistent. DO combines both: natural language directives define what to do, AI orchestrates decisions, and Python scripts handle deterministic execution. This separation of concerns achieves 97%+ accuracy on multi-step business workflows where raw LLMs fail catastrophically.

**Core Insight**: "We're asking probabilistic systems to do deterministic work. The solution isn't making LLMs smarter—we build a framework that turns rickety outputs into something usable despite the variability. We wrap galaxy brain intelligence in a structure that controls it for beneficial business purposes."

This skill bible documents the complete DO framework from Nick Saraev's 6-hour Agentic Workflows course, covering theoretical foundations through practical implementation.

---

## 1. The Probabilistic vs Deterministic Problem

### Why Raw LLMs Fail in Business

**The Math of Compounding Errors**:

```
Single step success rate: 90%
5-step workflow success rate: 59%
10-step workflow success rate: 35%
20-step workflow success rate: 12%

Formula: Total Success = (Step Success Rate)^Number_of_Steps
Example: 0.90^5 = 0.59 (59%)
```

**Why This Destroys Business Viability**:

```
Scenario: Invoice generation workflow (5 steps)
Success rate: 59%
Error rate: 41%

Impact: Wrong invoice sent 41% of the time
Business result: Clients leave after 1-2 errors
Conclusion: Completely unusable
```

**The Business Standard**: 95%+ success rate required. Raw LLMs can't achieve this on multi-step workflows.

### How LLMs Actually Work (Under the Hood)

**The Distribution Model**:

LLMs don't predict the single best next word. They predict a statistical distribution of possibilities.

```
Input: "Hi, how are"
       ↓
LLM generates probability distribution:
- "you" (98% probability)
- "things" (1.5% probability)
- "your" (0.3% probability)
- [other options] (0.2% probability)

With temperature/top-p:
- Doesn't always pick highest probability
- Introduces randomness for flexibility
- Result: Same input → different outputs
```

**Why Randomness Exists**: Without it, LLMs would be deterministic lookup tables with zero reasoning ability. Randomness enables problem-solving.

**The Problem for Business**: Randomness at every token → unpredictable outputs → can't use for invoices, receipts, processes.

### Compound Probabilities (The Death Spiral)

**How Errors Stack**:

```
Step 1: Fetch email (90% success)
Step 2: Summarize email (90% success)
Step 3: Feed to another model (90% success)
Step 4: Combine summaries (90% success)
Step 5: Generate daily digest (90% success)

Individual steps: All 90%
Total workflow: 0.90 × 0.90 × 0.90 × 0.90 × 0.90 = 59%

Error range expands:
- Step 1: ±10% variance
- Step 5: ±41% variance (catastrophic)
```

**Business Implication**: More steps = exponentially lower reliability. 20-step workflows become unusable lotteries.

### The Traditional Solution (Deterministic Automation)

**How N8N/Zapier/Make Work**:

```
Drag-and-drop nodes:
[Trigger] → [HTTP Request] → [Data Transform] → [Google Sheets] → [Email]

Characteristics:
✅ 100% deterministic (same input = same output always)
✅ Reliable for business
✅ Interpretable
❌ Inflexible (can't handle edge cases)
❌ Requires manual configuration for every scenario
❌ Breaks on unexpected inputs
```

**The Limitation**: You must anticipate every possible scenario when building. Real world is messy.

---

## 2. The DO Framework Solution (Best of Both Worlds)

### The Three-Layer Architecture

```
┌─────────────────────────────────────┐
│  LAYER 1: DIRECTIVE (What to do)    │
│  - Natural language SOPs             │
│  - Markdown files in directives/     │
│  - No code, just instructions        │
│  - Example: scrape_leads.md          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  LAYER 2: ORCHESTRATION (Decisions) │
│  - AI agent (Claude/GPT/Gemini)      │
│  - Reads directives                  │
│  - Chooses which tools to call       │
│  - Routes data between steps         │
│  - Handles errors flexibly           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  LAYER 3: EXECUTION (How to do it)  │
│  - Python scripts in execution/      │
│  - One script = one job              │
│  - Deterministic, reliable           │
│  - Example: upload_to_sheet.py       │
└─────────────────────────────────────┘
```

### Why Separation Works

**The Rule**: Push deterministic work to code, reserve AI for judgment.

```
Task: Sort a list of 1000 items

Without DO:
- LLM sorts via reasoning
- Time: 30 seconds
- Accuracy: 90% (100 errors)
- Cost: High (many tokens)
- Result: UNUSABLE

With DO:
- AI calls sort_list.py
- Time: 0.05 seconds
- Accuracy: 100% (0 errors)
- Cost: Free (local execution)
- Result: PERFECT
```

**Demonstration** (from course):

Nick shows sorting a demo list:
- LLM native: 15-30 seconds, probabilistic accuracy
- Python script: 53 milliseconds, 100% accurate
- **Speed difference**: 300-500× faster
- **Cost difference**: Several hundred times cheaper

### The Bowling Alley Analogy

**Without DO** (Raw LLM):
```
[Bowler] ----→ ??? → Maybe hits pins, maybe gutter

Wide error bars = unpredictable results
```

**With DO** (Guardrails):
```
[Bowler] ----→ [Bumpers] → Always hits something

Constrained range of outcomes = reliable business use
```

DO framework = guardrails for AI. Reduces stochasticity (randomness) to acceptable business levels.

---

## 3. Layer 1: Directives (Natural Language SOPs)

### What Directives Are

**Definition**: Natural language instructions stored as Markdown files that define workflow goals, inputs, tools, outputs, and edge cases.

**Location**: `directives/` folder in workspace

**Format**: One Markdown file per workflow

**Example Names**:
```
directives/
├── scrape_leads.md
├── upwork_apply_bot.md
├── proposal_generator.md
├── email_enrichment.md
└── create_social_post.md
```

### Directive Structure Template

```markdown
# [Workflow Name]

## Description
[One-sentence: what this workflow does]

## Inputs
- input_1: Description (e.g., "Company name")
- input_2: Description (e.g., "Industry filter")

## Steps
1. Ask user for required inputs
2. Load execution script: execution/scraper.py
3. Call script with parameters
4. Validate output
5. Upload results to Google Sheet
6. Send notification email

## Tools/Scripts
- execution/scraper.py - Scrapes data from platform
- execution/upload_to_sheet.py - Uploads to Google Sheets
- execution/send_email.py - Sends notification

## Outputs
- Google Sheet URL with scraped data
- Email confirmation to user

## Edge Cases
- If no data found: Return empty sheet, notify user
- If API rate limit hit: Wait 60 seconds, retry
- If invalid input: Ask user to clarify
```

### Key Directive Principles

**1. No Code in Directives**

```
❌ WRONG:
"Run this Python: import requests; response = requests.get(url)"

✅ RIGHT:
"Call execution/fetch_url.py with the provided URL"
```

**Why**: Directives must be readable by ANY human in organization, not just technical staff.

**2. Write for Competent Employees, Not Robots**

```
❌ Too vague: "Get some leads"
❌ Too specific: "Initialize HTTP client, set headers to {...}, make GET request..."

✅ Just right: "Call scraper.py to get 100 HVAC leads in Texas. Store results in Google Sheet."
```

**3. Reference Execution Scripts by Name**

```
Step 3: Call execution/scrape_apify.py
Step 5: Call execution/enrich_emails.py
Step 7: Call execution/upload_to_sheet.py
```

Agent reads directive, sees script name, loads and executes script.

### Converting Business SOPs to Directives

**Case Study**: $2M/year dental marketing company

**Existing SOP** (internal knowledge base):
```
"When client onboards:
1. Send welcome email
2. Create project folder
3. Schedule kickoff call
4. Add to CRM
5. Assign account manager"
```

**Converted to Directive** (15 minutes with AI):
```markdown
# Client Onboarding

## Description
Automate complete client onboarding process from contract signature.

## Inputs
- client_name
- client_email
- service_tier (bronze/silver/gold)

## Steps
1. Send welcome email using execution/send_template_email.py
2. Create Google Drive folder via execution/create_project_folder.py
3. Check account manager availability via execution/query_calendar.py
4. Schedule kickoff call using execution/schedule_meeting.py
5. Add to HubSpot CRM via execution/add_to_crm.py
6. Send assignment notification to account manager

## Edge Cases
- If account manager unavailable: Escalate to director
- If email bounces: Flag for manual follow-up
```

**Result**: 90% of onboarding work now automated. 15-minute setup.

---

## 4. Layer 2: Orchestration (The AI Decision Maker)

### What Orchestration Does

**The Project Manager Analogy**:

```
Project Manager receives:
- High-level instructions (directives)
- Available tools (execution scripts)
- Current context (data from previous steps)

Project Manager decides:
- Which tool to use when
- How to route data between steps
- What to do if errors occur
- When to ask for human input
```

AI orchestrator does exactly this, but in milliseconds.

### The PTMRO Loop

Every agent message follows this cycle:

```
P = PLANNING
    ↓
T = TOOLS (take actions)
    ↓
M = MEMORY (store context)
    ↓
R = REFLECTION (evaluate results)
    ↓
O = ORCHESTRATION (coordinate next loop)
    ↓
[Repeat until task complete]
```

**Example** (scraping 200 HVAC leads):

```
Planning:
"I need to scrape HVAC companies. I'll use the scraper.py script,
verify industry match, then upload to Google Sheets."

Tools:
- Execute execution/scraper.py with filters
- Call returned 200 leads but only 150 match industry

Memory:
- Stores: "Initial scrape returned 200, filtered to 150"
- Keeps context for next steps

Reflection:
"Match rate is 75%. Below 80% threshold in directive.
Need to adjust filters."

Orchestration:
"I'll adjust the filter parameters and retry the scrape."
[Loops back to Planning with new approach]
```

### Old vs New Orchestration

**Traditional Automation** (N8N):
```
You orchestrate ONCE when building:
Node A → Node B → Node C → Node D

Fixed forever. Can't adapt to edge cases.
```

**DO Framework** (AI Orchestration):
```
AI orchestrates AT RUNTIME:
- Reads available tools
- Decides routing based on current context
- Adapts when things break
- Can try alternative approaches

Dynamic. Handles unexpected situations.
```

### The Flexibility Advantage

**Example**: Email response workflow

**Fixed automation**:
```
New email → Check if positive → Send template A
             Check if negative → Send template B

Breaks when: Email is neutral, mixed sentiment, or unclear
```

**AI orchestration**:
```
New email → AI reads context
          → AI determines sentiment (handles nuance)
          → AI chooses appropriate response
          → AI customizes template
          → If unsure: Ask human

Handles: Any sentiment, context-specific responses, edge cases
```

---

## 5. Layer 3: Execution (Deterministic Python Scripts)

### What Execution Scripts Are

**Definition**: Single-purpose Python scripts that perform one specific, deterministic task reliably.

**Location**: `execution/` folder in workspace

**Characteristics**:
- One script = one job
- Same input → always same output
- No AI, no flexibility
- Fast, cheap, reliable

### Example Scripts

**execution/sort_list.py**:
```python
import json

# Load data
data = json.load(open('items.json'))

# Sort alphabetically
data['items'] = sorted(data['items'], key=lambda x: x['name'])

# Save
json.dump(data, open('items.json', 'w'))
```

**Purpose**: Sort a list reliably in 53 milliseconds.

**execution/upload_to_sheet.py**:
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Authenticate
creds = service_account.Credentials.from_service_account_file('creds.json')
service = build('sheets', 'v4', credentials=creds)

# Upload data
sheet_id = os.environ['SHEET_ID']
range_name = 'Sheet1!A1'
values = [[row['name'], row['email'], row['phone']] for row in data]

body = {'values': values}
result = service.spreadsheets().values().update(
    spreadsheetId=sheet_id,
    range=range_name,
    valueInputOption='RAW',
    body=body
).execute()

print(f"Updated {result.get('updatedCells')} cells")
```

**Purpose**: Upload data to Google Sheets with 100% reliability, zero token cost.

### Why Scripts Over LLM Execution

**LLMs are terrible at basic operations**:

```
Task: Count letters in "strawberry"

LLM approach:
- Reasons through each letter
- Sometimes miscounts
- Takes several tokens
- Occasionally wrong

Python:
len("strawberry") = 10
- Always correct
- Instant
- Free
```

**Task**: Sort 10,000 numbers

```
LLM:
- Would need billions of operations
- Takes minutes
- Costs hundreds of tokens
- Probabilistic accuracy

Python:
sorted(numbers)
- One function call
- Milliseconds
- Free
- 100% accurate
```

**The 10,000-100,000× Performance Difference**:

Mathematical operations, file handling, API calls, data transformations—all 10,000-100,000× faster with deterministic code.

### The One Script = One Job Rule

**Bad** (monolithic):
```python
# scrape_and_upload.py
def do_everything():
    leads = scrape_leads()
    enriched = enrich_emails(leads)
    uploaded = upload_to_sheet(enriched)
    sent = send_notification(uploaded)
    return sent
```

**Good** (modular):
```
execution/
├── scrape_leads.py - Just scrapes
├── enrich_emails.py - Just enriches
├── upload_to_sheet.py - Just uploads
└── send_notification.py - Just notifies
```

**Why Modular**:
- Easy to test individually
- Easy to debug (know exactly which script failed)
- Easy to replace/improve one piece
- Reusable across workflows

### How Orchestration Calls Scripts

**User says**: "Scrape leads"

**Orchestration process**:
```
1. AI reads all directives
2. Finds: directives/scrape_leads.md
3. Reads directive step-by-step
4. Sees: "Step 3: Call execution/scrape_apify.py"
5. Loads execution/scrape_apify.py
6. Executes script
7. Script returns JSON with leads
8. AI evaluates: Success or error?
9. If success: Continue to next directive step
10. If error: Diagnose and fix or retry
```

**User never touches code**. Just: "Scrape leads" → System handles everything.

---

## 6. Workspace Setup & File Structure

### The Complete Workspace

```
my_agentic_workspace/
│
├── directives/               # Natural language instructions
│   ├── scrape_leads.md
│   ├── proposal_generator.md
│   ├── upwork_apply.md
│   └── email_enrichment.md
│
├── execution/                # Python scripts (one job each)
│   ├── scrape_apify.py
│   ├── enrich_with_anymailfinder.py
│   ├── upload_to_sheet.py
│   ├── generate_proposal.py
│   └── send_email.py
│
├── .tmp/                     # Temporary files (scratch pad)
│   └── [agent creates files here during execution]
│
├── resources/                # Optional: static files
│   ├── templates/
│   └── reference_docs/
│
├── .env                      # API keys and secrets
│   └── OPENAI_API_KEY=sk-...
│      APIFY_TOKEN=...
│      GOOGLE_SHEET_ID=...
│
├── AGENTS.md                 # System prompt (framework instructions)
├── CLAUDE.md                 # Claude-specific system prompt
├── GEMINI.md                 # Gemini-specific system prompt
└── cursor.md                 # Cursor IDE system prompt
```

### Why This Structure

**directives/** = What humans understand
**execution/** = What computers execute reliably
**System prompts** = How AI understands the framework

Separation = Different stakeholders can work in their domains.

### System Prompt (The Framework Explainer)

**CLAUDE.md** (or AGENTS.md):

```markdown
You operate within a 3-layer architecture that separates concerns
to maximize reliability. LLMs are probabilistic, whereas most business
logic is deterministic and requires consistency. This system fixes
that mismatch.

Layer 1: Directives (What to do)
- Natural language SOPs in directives/
- Define goals, inputs, tools, outputs, edge cases

Layer 2: Orchestration (Decision making)
- This is you. Your job: intelligent routing.
- Read directives, call execution tools, handle errors

Layer 3: Execution (Doing the work)
- Deterministic Python scripts in execution/
- Handle API calls, data processing, validation
- Reliable, testable, fast

Your job:
1. Parse user intent → Identify relevant directive
2. Load directive → Understand steps
3. Execute steps → Call appropriate scripts
4. Handle errors → Retry or diagnose
5. Return results → Report to user
```

**Critical**: This system prompt is injected into EVERY conversation. Agent always knows the framework.

### Naming Conventions

**Descriptive > Concise**:

```
❌ Bad: s_l.md, proc_data.py, x.md
✅ Good: scrape_leads.md, process_customer_data.py, email_enrichment.md
```

**Why**: Agent uses filenames to determine which workflow to run. Clear names = correct routing.

**Markdown Files** (.md):
- All directives use .md extension
- Markdown allows formatting (headers, bullets, code blocks)
- More information per token than plain text

**Python Files** (.py):
- All execution scripts use .py extension
- Could use other languages (JavaScript, Ruby, etc.)
- Python chosen for AI coding proficiency

---

## 7. Building Your First DO Workflow

### Step-by-Step: Lead Scraping Workflow

**Goal**: Scrape 100 HVAC leads from Apify, upload to Google Sheets.

**Phase 1: Create Directive**

```
User to Claude Code:
"I want to build a lead scraping workflow. It should scrape HVAC
companies from Apify, get 100 leads, and upload to a Google Sheet.
Create the directive for me."
```

**Claude Code creates**: `directives/scrape_hvac_leads.md`

```markdown
# Scrape HVAC Leads

## Description
Scrapes HVAC company leads from Apify and uploads to Google Sheets.

## Inputs
- industry: "HVAC" (default)
- location: User specifies (e.g., "Texas")
- limit: Number of leads (default: 100)

## Steps
1. Ask user for location if not provided
2. Call execution/scrape_apify.py with parameters:
   - industry: HVAC
   - location: {user input}
   - limit: {user input or 100}
3. Verify results contain required fields
4. Call execution/upload_to_sheet.py with scraped data
5. Return Google Sheet URL to user

## Tools
- execution/scrape_apify.py
- execution/upload_to_sheet.py

## Outputs
- Google Sheet URL with columns: company_name, location, phone, website

## Edge Cases
- If scrape returns < 10 leads: Warn user, broaden search
- If API fails: Retry 3x, then report error
- If Sheet upload fails: Save to local CSV as backup
```

**Phase 2: Build Execution Scripts**

```
User: "Build the execution scripts for this directive."
```

**Claude Code creates**:

**execution/scrape_apify.py**:
```python
#!/usr/bin/env python3
import os
import sys
import json
import requests

def scrape_leads(industry, location, limit):
    """Scrape leads from Apify"""
    api_token = os.environ['APIFY_TOKEN']
    actor_id = 'curious-coder~business-scraper'

    url = f'https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items'

    payload = {
        'industry': industry,
        'location': location,
        'maxResults': limit
    }

    headers = {'Authorization': f'Bearer {api_token}'}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    leads = response.json()
    return leads

if __name__ == '__main__':
    industry = sys.argv[1] if len(sys.argv) > 1 else 'HVAC'
    location = sys.argv[2] if len(sys.argv) > 2 else 'United States'
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    results = scrape_leads(industry, location, limit)
    print(json.dumps(results))
```

**execution/upload_to_sheet.py**:
```python
#!/usr/bin/env python3
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def upload_to_sheet(data):
    """Upload leads to Google Sheets"""
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )

    service = build('sheets', 'v4', credentials=creds)
    sheet_id = os.environ['GOOGLE_SHEET_ID']

    # Prepare data
    values = [[
        lead['company_name'],
        lead['location'],
        lead['phone'],
        lead['website']
    ] for lead in data]

    # Upload
    body = {'values': values}
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='Leads!A2',
        valueInputOption='RAW',
        body=body
    ).execute()

    sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}'
    return sheet_url

if __name__ == '__main__':
    data = json.loads(sys.stdin.read())
    url = upload_to_sheet(data)
    print(url)
```

**Phase 3: Test the Workflow**

```
User: "Scrape 100 HVAC leads in Texas"

Claude Code execution:
1. Reads directives/scrape_hvac_leads.md
2. Sees Step 2: Call scraper.py
3. Executes: python execution/scrape_apify.py HVAC Texas 100
4. Script returns JSON with 100 leads
5. Sees Step 4: Call upload_to_sheet.py
6. Executes: cat leads.json | python execution/upload_to_sheet.py
7. Returns: "https://docs.google.com/spreadsheets/d/{id}"

User receives: Google Sheet URL with 100 leads
```

**Time**: 2-3 minutes (mostly API calls)

**User effort**: One sentence

---

## 8. IDE Integration (Where DO Lives)

### What is an IDE?

**IDE** = Integrated Development Environment

**Think**: Microsoft Word, but for code (and now, for AI workflows).

**Three Main Areas**:

```
┌────────────┬──────────────────┬────────────────┐
│  File      │     Editor       │   Agent Chat   │
│  Explorer  │     Panel        │     Panel      │
│  (Left)    │    (Center)      │    (Right)     │
├────────────┼──────────────────┼────────────────┤
│            │                  │                │
│ directives/│  [File contents  │ User: "Scrape  │
│ execution/ │   displayed      │ leads"         │
│ .env       │   here when      │                │
│ CLAUDE.md  │   clicked]       │ Agent: "I'll   │
│            │                  │ use scrape_    │
│            │                  │ leads.md"      │
│            │                  │                │
│            │                  │ [Executes...]  │
└────────────┴──────────────────┴────────────────┘
```

### Popular IDEs for Agentic Workflows

**1. Anti-Gravity** (Google, newest)
- **Best for**: Beginners
- **Interface**: Minimal, agent-focused
- **Unique feature**: Auto-hides complexity
- **Model**: Gemini (default), supports others

**2. VS Code** (Microsoft, established)
- **Best for**: Those with existing VS Code experience
- **Interface**: Traditional, lots of extensions
- **Unique feature**: Massive extension library
- **Model**: Any (via extensions like Claude Code, GitHub Copilot)

**3. Cursor** (AI-native)
- **Best for**: Early AI IDE adopters
- **Interface**: Similar to VS Code
- **Unique feature**: Built-in composer mode
- **Model**: Multiple supported

### You Don't Need to Know Coding

**The New Reality**:

```
Old world: You write code
New world: You direct AI to write code

Old: "How do I write a Python script to scrape Apify?"
New: "Create a script that scrapes Apify for HVAC leads"
      → AI writes script for you
```

**You become CEO of your agent company**: Give high-level instructions, AI handles implementation.

---

## 9. How DO Reduces Error Rates

### The Guardrail Effect

**Without DO**:
```
Possible outcomes: [-----very wide range-----]
                   Failure ← → → → → → Success

Error rate: 40-50% on complex workflows
```

**With DO**:
```
Possible outcomes: [--narrow range--]
                        Success zone

Error rate: 2-3% on same workflows
```

**Real Example** (dental marketing company):

```
Before DO:
- Raw LLM generating client emails
- Error rate: 35% (wrong tone, missing info, etc.)
- Unusable for business

After DO (15-minute setup):
- Directive defines email template requirements
- Scripts handle data insertion
- AI only makes routing decisions
- Error rate: 2.5%
- Now handling 90% of client communication
```

### The Reliability Formula

```
Reliability = (Deterministic %) + (AI Judgment Quality × Probabilistic %)

Example workflow:
- 80% deterministic (API calls, data transforms)
- 20% requires judgment (which customer segment?)

With DO:
- 80% at 100% reliability (scripts)
- 20% at 95% reliability (AI decisions)
- Total: 99% reliable

Without DO:
- 100% probabilistic
- Each step 90% reliable
- 5 steps: 59% reliable
```

**The Lever**: Push as much as possible to deterministic layer.

---

## 10. Real-World Implementation Examples

### Example 1: Proposal Generation from Sales Calls

**Directive**: `directives/create_proposal.md`

```markdown
# Create Proposal from Sales Call

## Description
Generates customized proposal document from sales call transcript.

## Inputs
- transcript: Sales call transcript (text)
- client_email: Where to send proposal

## Steps
1. Read transcript
2. Extract: client pain points, budget mentioned, timeline, requirements
3. Call execution/generate_proposal.py with extracted data
4. Upload to Google Docs
5. Call execution/send_email.py to send proposal to client

## Tools
- execution/extract_sales_info.py
- execution/generate_proposal.py
- execution/upload_to_docs.py
- execution/send_email.py
```

**User experience**:
```
User: "Generate a proposal using the below transcript: [paste]"

15 seconds later: "Proposal created and emailed to client@email.com.
Link: [Google Doc URL]"
```

**What happened under the hood**:
- AI extracted key information
- Scripts generated formatted proposal
- Google Docs API created document
- Email API sent notification

**Time saved**: 30-45 minutes per proposal

### Example 2: Upwork Job Application Bot

**Directive**: `directives/upwork_scrape_apply.md`

```markdown
# Upwork Scrape & Apply System

## Description
Scrapes Upwork jobs matching AI automation keywords, generates
personalized cover letters, outputs to Google Sheet with one-click apply links.

## Inputs
- keywords: Job search terms
- limit: Number of jobs to process

## Steps
1. Ask user for keywords and limit
2. Call execution/scrape_upwork.py
3. For each job:
   a. Call execution/analyze_job_fit.py (AI filters non-matches)
   b. If match: Call execution/generate_cover_letter.py
   c. Call execution/create_apply_link.py
4. Upload all results to Google Sheet
5. Return sheet URL

## Tools
- execution/scrape_upwork.py
- execution/analyze_job_fit.py
- execution/generate_cover_letter.py
- execution/create_apply_link.py
- execution/upload_to_sheet.py
```

**Result**: Apply to 100+ jobs in 10 minutes (vs 20+ hours manually).

### Example 3: YouTube Outlier Detector

**Directive**: `directives/cross_niche_outlier.md`

```markdown
# Cross-Niche YouTube Outlier Detector

## Description
Finds high-performing videos in related niches for content inspiration.

## Inputs
- niche: Related content area (e.g., "business but not AI")
- limit: Number of videos to analyze

## Steps
1. Ask user for niche and limit
2. Call execution/tubelab_scraper.py to get videos
3. For each video:
   a. Calculate outlier score (views / channel average)
   b. Apply recency boost
   c. Fetch transcript
   d. Call execution/summarize_with_ai.py
   e. Generate 3 title variants
4. Upload to Google Sheet with thumbnails
5. Return sheet URL

## Tools
- execution/tubelab_scraper.py
- execution/calculate_outlier_score.py
- execution/fetch_transcript.py
- execution/summarize_with_ai.py
- execution/generate_title_variants.py
- execution/upload_to_sheet.py
```

**Usage**: "Find 50 outliers in business niche" → Google Sheet with ranked ideas ready in 5 minutes.

---

## 11. Advanced Concepts

### Self-Annealing (Workflows That Heal Themselves)

**The Concept**: When errors occur, agent fixes the script and documents the fix for future runs.

**How It Works**:

```
Run 1: Script fails with error
       ↓
    AI reads error message
       ↓
    AI fixes script
       ↓
    Tests fix
       ↓
    Updates directive with new edge case handling
       ↓
Run 2: Same error doesn't occur
       ↓
    System is now stronger
```

**Example**:

```
Initial directive:
"Step 3: Call execution/scrape.py"

Error occurs: "API rate limit exceeded"

AI updates directive:
"Step 3: Call execution/scrape.py
If rate limit error: Wait 60 seconds, retry up to 3 times"

Also updates scrape.py to handle rate limits gracefully

Future runs: No more rate limit failures
```

**The Learning Loop**: Each error makes the system more robust.

### Sub-Agents (Multiple Agents Working Together)

**Concept**: Complex workflows split across multiple specialized agents.

```
Main Agent (Orchestrator)
├─→ Research Agent (finds information)
├─→ Writing Agent (creates content)
├─→ Quality Agent (reviews output)
└─→ Delivery Agent (sends to client)

Each has own directives + tools
Orchestrator coordinates them all
```

**Example**: Content creation pipeline

```
User: "Create a blog post about AI automation"

Main Agent:
1. Calls Research Agent → "Find 5 recent AI automation trends"
2. Waits for results
3. Calls Writing Agent → "Write 1500-word post using these trends"
4. Calls Quality Agent → "Review for clarity and accuracy"
5. Calls Delivery Agent → "Upload to WordPress, schedule for tomorrow"

Each agent specialized, all coordinated by main agent
```

**Benefits**:
- Parallel processing (faster)
- Specialized prompts (higher quality)
- Modular (easy to swap agents)

### Horizontal Leverage (The 90% of 10,000 Concept)

**The Shift**:

```
Traditional automation: Automate 100% of 1 role
Agentic workflows: Automate 90% of 10,000 roles

Math:
- 100% of 1 = 1 unit of value
- 90% of 10,000 = 9,000 units of value
```

**Why 90% Not 100%**:
- Humans have slightly more context
- Edge cases require judgment
- Final review often needed

**But**: 90% of 10,000 > 100% of 1 by orders of magnitude.

**Real Application**:

```
Marketing agency (20 employees):
Instead of replacing 1 employee completely,
Automate 90% of all 20 employees' work

Results:
- 18 FTE worth of work automated
- 20 employees become managers/strategists
- 10× output with same headcount
```

### The Industrial Revolution Analogy

**Before** (manual labor):
- 1 seamstress = 10 garments/day
- 100 seamstresses = 1,000 garments/day

**After** (machines):
- 1 loom operator = 10,000 garments/day
- 100 loom operators = 1,000,000 garments/day

**Now** (agentic workflows):
- 1 knowledge worker + AI = 10-100× output
- Can reconfigure "loom" (workflow) in seconds via natural language

**This is a phase change in automation capability**.

---

## 12. Common Pitfalls & Solutions

### Pitfall 1: Putting Code in Directives

**Mistake**:
```markdown
# My Workflow

## Steps
1. Run this code:
   ```python
   import requests
   requests.get('https://api.example.com')
   ```
```

**Why Bad**:
- Non-technical team members can't read it
- Hard to maintain
- Defeats purpose of DO separation

**Fix**:
```markdown
# My Workflow

## Steps
1. Call execution/fetch_api_data.py
2. API endpoint: https://api.example.com
```

### Pitfall 2: Monolithic Scripts

**Mistake**:
```
execution/
└── do_everything.py (500 lines, does scraping + enrichment + upload + email)
```

**Why Bad**:
- Can't test pieces individually
- One bug breaks entire flow
- Can't reuse across workflows

**Fix**:
```
execution/
├── scrape.py (50 lines)
├── enrich.py (30 lines)
├── upload.py (40 lines)
└── send_email.py (25 lines)

Each tested independently
Combined in directive
```

### Pitfall 3: Vague Directives

**Mistake**:
```markdown
# Do Marketing Stuff

## Steps
1. Do some research
2. Make content
3. Post it
```

**Why Bad**:
- AI doesn't know which scripts to call
- Too ambiguous to execute reliably
- No quality standards

**Fix**:
```markdown
# Create LinkedIn Post from Blog

## Steps
1. Call execution/fetch_blog_post.py with URL
2. Call execution/summarize_for_linkedin.py (max 1300 chars)
3. Call execution/generate_image.py for visual
4. Call execution/post_to_linkedin.py
5. Verify post live, return URL
```

### Pitfall 4: Not Using .env for Secrets

**Mistake**:
```python
# execution/scraper.py
API_KEY = "sk-1234567890abcdef"  # Hardcoded API key
```

**Why Bad**:
- Can't share code (exposes secrets)
- Hard to update keys (must edit every script)
- Security risk

**Fix**:
```python
# execution/scraper.py
import os
API_KEY = os.environ['APIFY_TOKEN']  # From .env file
```

**.env file**:
```
APIFY_TOKEN=your_token_here
OPENAI_API_KEY=sk-your_key_here
GOOGLE_SHEET_ID=your_sheet_id
```

Never commit .env to version control.

---

## AI PARSING GUIDE

### Primary Objective
When building business automation workflows, use the DO framework to separate natural language instructions (directives) from deterministic code execution (scripts), with AI orchestrating decisions between them.

### Critical Decision Points

**If User Says**: "I want to automate [business process]"
**Action Sequence**:
1. Create directive describing workflow in natural language
2. Identify which steps are deterministic (→ scripts)
3. Identify which steps require judgment (→ AI orchestration)
4. Build execution scripts for deterministic steps
5. Test workflow end-to-end
6. Iterate based on errors

**If User Says**: "The workflow keeps making mistakes"
**Diagnose**:
1. Is error in deterministic step? → Fix script
2. Is error in AI judgment? → Improve directive instructions
3. Is error in orchestration? → Adjust system prompt

**If User Says**: "Can I use my existing N8N/Make workflows?"
**Answer**: Yes, via Hybrid Directives approach:
1. Keep N8N/Make workflow as-is
2. Create directive that calls it via webhook
3. Agent orchestrates when to trigger
4. Best of both worlds

### Integration Points

**Connects to**:
- Workflow Automation (N8N, Make, Zapier)
- AI Development (Claude Code, GPT, Gemini)
- Business Process Optimization (SOPs → Directives)
- Cloud Deployment (Modal, local servers)
- No-Code Tools (hybrid integration)

### Output Quality Standards

When helping build DO framework workflows:
1. ✅ Directives in natural language (no code)
2. ✅ One script = one job (modular)
3. ✅ Deterministic work pushed to scripts
4. ✅ AI reserved for judgment/routing
5. ✅ System prompts explain framework
6. ✅ Clear naming conventions

### Red Flags (Anti-Patterns)

❌ Code mixed into directive files
❌ AI doing math/sorting/basic operations
❌ Monolithic scripts (500+ lines, multiple jobs)
❌ Hardcoded API keys in scripts
❌ Vague directives ("do marketing stuff")
❌ No error handling in scripts

---

## SOURCE ATTRIBUTION

**Primary Source**: Nick Saraev - "AGENTIC WORKFLOWS 6 HOUR COURSE: Beginner to Pro (2026)"
- **Video ID**: MxyRjL7NG18
- **Duration**: 5 hours 42 minutes (excerpts from first 3 sections analyzed)
- **Context**: Comprehensive course on agentic workflows covering theory through advanced implementation
- **Key Contribution**: Complete DO framework methodology with mathematical foundations of why LLMs fail in business
- **Authority Basis**: Built two AI agencies to $160K/month combined revenue, consulted for billion-dollar businesses, leads 3,000-member AI automation community
- **Technical Depth**: From probability theory through IDE configuration, API integration, deployment strategies
- **Unique Value**: Explains WHY frameworks are necessary (probabilistic vs deterministic mismatch) before showing HOW to build them
- **Teaching Philosophy**: "Building is the most effective way to learn. When you get your hands dirty, you're forced to deal with concepts you never would if you just passively listened."
- **Capture Date**: January 2026 (via MCP YouTube Transcript)

**Supporting Sources**:
- Live demonstrations of meal prep automation, lead scraping, video editing workflows
- Real business examples: dental marketing company ($2M/year), various client implementations
- Mathematical proofs of error rate compounding
- IDE comparisons (Anti-Gravity, VS Code, Cursor)

**Synthesis Approach**: This skill bible extracts the foundational DO framework from the first 3 sections of a 6-hour comprehensive course. Focus is on theoretical understanding (why frameworks exist) combined with practical implementation (how to build them), with emphasis on the separation of concerns principle that makes agentic workflows viable for business use.

---

**END SKILL BIBLE: DO Framework Fundamentals (Directive-Orchestration-Execution)**