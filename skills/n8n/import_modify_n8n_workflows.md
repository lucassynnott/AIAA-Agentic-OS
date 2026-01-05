# Import & Modify N8N Workflows - Template Customization Guide

## Purpose
This skill teaches you how to import existing N8N workflow templates and customize them for your specific needs. This is the FASTEST way to deploy production-ready automations without building from scratch.

## When to Use This Skill
- When you find a template that's 80% of what you need
- When building common automations (lead capture, email sequences, etc.)
- When you want to learn by example (see how others built workflows)
- When you need to deliver client automations quickly
- When migrating workflows between N8N instances

## Prerequisites
- N8N instance running (Cloud or Self-Hosted)
- Basic understanding of N8N workflows (see build_n8n_workflow.md)
- Source of workflow template (JSON file, URL, or clipboard)
- Credentials ready for any services the workflow uses

## Import Methods Overview

### Method 1: Import from JSON File
**Best for:** Downloaded templates, shared workflows, backups
**Format:** `.json` file
**Success rate:** 100% (if file is valid N8N workflow)

### Method 2: Import from Clipboard
**Best for:** Copy-paste from online sources, Claude AI-generated workflows
**Format:** Raw JSON text
**Success rate:** 95% (occasionally formatting issues)

### Method 3: Import from URL
**Best for:** N8N Cloud templates, shared workflows via link
**Format:** N8N share URL
**Success rate:** 90% (requires internet connection)

## Step-by-Step Execution Instructions

### Phase 1: Import Workflow from JSON File (5 minutes)

#### Step 1.1: Download Workflow Template

**From n8nworkflows.xyz:**
1. Navigate to https://n8nworkflows.xyz
2. Browse or search for workflow
3. Click on workflow card
4. Click "Download Workflow" button (right side)
5. JSON file downloads (e.g., `workflow_name.json`)

**From N8N official site:**
1. Go to https://n8n.io/workflows
2. Find desired workflow
3. Click "Use workflow" button
4. Click "Download" (if self-hosted) OR "Copy to Clipboard"

**From GitHub repositories:**
1. Navigate to repository with N8N workflows
2. Find `.json` workflow file
3. Click "Raw" button
4. Right-click → Save As → Save as `.json` file

#### Step 1.2: Import into N8N

**Method A: Import Menu**
1. Open N8N dashboard
2. Click workflow name "Untitled" at top (if in new workflow)
3. OR click three dots (⋮) next to workflow name
4. Select "Import from File"
5. File picker opens
6. Navigate to downloaded `.json` file
7. Select file, click "Open"
8. Workflow appears on canvas

**Method B: Create New from Import**
1. N8N dashboard main page (workflows list)
2. Click three dots (⋮) top-right OR click "+  Create Workflow"
3. Select "Import from File"
4. Choose `.json` file
5. Workflow opens in new tab

#### Step 1.3: First Look at Imported Workflow

After import, you'll see:

**Green Nodes:** Ready to use (no configuration needed)
**Orange/Yellow Nodes:** Warnings (check these)
**Red Nodes:** Errors (MUST fix before workflow works)

**Common Red Node Causes:**
- Missing credentials (Google, Slack, API keys)
- Hardcoded values that need your input
- Nodes not available in your N8N version
- Invalid expressions or references

### Phase 2: Import from Clipboard (5 minutes)

#### Step 2.1: Copy Workflow JSON

**From website:**
1. Find workflow JSON (usually displayed in code block)
2. Look for text starting with: `{"nodes":[...`
3. Select ALL JSON text (starts with `{`, ends with `}`)
4. Copy to clipboard (Ctrl+C / Cmd+C)

**From Claude/ChatGPT:**
1. Ask AI to generate N8N workflow
2. AI outputs JSON in code block
3. Click "Copy" button on code block
4. OR manually select and copy

**From messaging apps (Slack, Discord):**
1. Workflow shared as JSON
2. Copy entire message containing JSON
3. Make sure you got the complete JSON (starts `{`, ends `}`)

#### Step 2.2: Paste into N8N

1. Open N8N, create new workflow OR open existing
2. Click anywhere on canvas to focus it
3. Paste: Ctrl+V (Windows) / Cmd+V (Mac)
4. Workflow appears on canvas automatically

**If paste doesn't work:**
1. Three dots (⋮) → "Import from URL"
2. This opens text box
3. Paste JSON there
4. Click "Import"

**Troubleshooting paste issues:**
- JSON must be valid (use jsonlint.com to validate)
- Workflow canvas must be focused (click canvas first)
- Some browsers block clipboard access - use import menu instead

### Phase 3: Understanding Imported Workflow Structure (10 minutes)

#### Step 3.1: Identify Workflow Components

**Read the Sticky Notes first (if present):**
- Yellow notes explain workflow logic
- Often contain setup instructions
- May list required credentials
- Document API requirements

**Map the workflow flow:**
```
Trigger (START)
    ↓
Data Collection/Input
    ↓
Processing/Transformation
    ↓
Decision Points (IF nodes)
    ↓
Actions (API calls, notifications)
    ↓
Output/Response
```

#### Step 3.2: Check Required Credentials

1. Look for red nodes (these need credentials)
2. Common credential types:
   - **OAuth2:** Google, Slack, LinkedIn (must authorize)
   - **API Key:** OpenAI, SendGrid, custom APIs
   - **Basic Auth:** Simple username/password
   - **Header Auth:** Custom authentication headers

**To see what credential is needed:**
1. Double-click red node
2. Top of panel shows: "Credential: [Type] - ⚠️ Not configured"
3. Click "Create new credential" button
4. Follow authentication flow

#### Step 3.3: Identify Hardcoded Values

Look for values that are specific to original creator:

**In Set nodes:**
- Email addresses: `john@example.com` → Change to your email
- Phone numbers: `+1234567890` → Change to your number
- URLs: `https://mysite.com` → Change to your site

**In HTTP Request nodes:**
- API endpoints: May have creator's account ID in URL
- Headers: API keys visible in header fields (SECURITY RISK!)

**In Code nodes:**
- Hardcoded IDs: User IDs, product IDs specific to their system
- File paths: Local file paths that don't exist on your system

**How to find hardcoded values quickly:**
1. Use browser search: Ctrl+F / Cmd+F
2. Search for common patterns:
   - `example.com`
   - `@gmail.com`, `@outlook.com`
   - `test`, `demo`, `placeholder`
   - Numbers that look like IDs: `12345`, `67890`

### Phase 4: Customizing the Workflow (20 minutes)

#### Step 4.1: Replace Credentials

**For each red node:**

1. Double-click node to open
2. Find "Credential" dropdown at top
3. Options you'll see:
   - **Existing credential:** If you already set this up before
   - **Create new credential:** First time using this service

**Creating new credential:**

**Example: Gmail**
1. Click "Create new credential"
2. Select authentication method (OAuth2 recommended)
3. Click "Connect my account"
4. Browser window opens → Log in to Gmail
5. Allow N8N access
6. Window closes, credential saved
7. **IMPORTANT:** Give credential a descriptive name
   - Bad: "Gmail Account", "Gmail 1"
   - Good: "Agency Gmail (support@agency.com)", "Client John Doe Gmail"

**Example: API Key (OpenAI, SendGrid)**
1. Click "Create new credential"
2. Find "API Key" field
3. Get API key from service:
   - OpenAI: https://platform.openai.com/api-keys
   - SendGrid: https://app.sendgrid.com/settings/api_keys
4. Paste API key into field
5. Click "Save"
6. Name credential: "OpenAI - Agency Account"

**Example: Basic Auth**
1. Click "Create new credential"
2. Enter username and password
3. Save with descriptive name

#### Step 4.2: Update Hardcoded Values

**Pattern 1: Email addresses**
Find all nodes sending emails:
1. Search workflow for "Email", "Gmail", "Send" node types
2. Open each
3. Update "To" field: Change `{{ $json.email }}` is fine (dynamic)
4. Change hardcoded: `john@example.com` → `your@email.com`

**Pattern 2: Webhook URLs**
If workflow calls your own APIs:
1. Find HTTP Request nodes
2. Update URL from: `https://creator-site.com/api/endpoint`
3. To your URL: `https://your-site.com/api/endpoint`

**Pattern 3: Slack Channels**
1. Find Slack nodes
2. Update channel from: `#creator-channel`
3. To your channel: `#your-channel`
4. OR update to dynamic: `{{ $json.channel }}`

**Pattern 4: Google Sheets / Docs**
1. Find Google Sheets/Docs nodes
2. Update Sheet ID from creator's sheet
3. To your sheet ID:
   - Open your Google Sheet
   - URL: `https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`
   - Copy `[SHEET_ID]` part
   - Paste in node configuration

#### Step 4.3: Adjust Workflow Logic for Your Use Case

**Common Customizations:**

**A. Change Trigger Type**
Template uses: Schedule Trigger (runs daily)
You need: Webhook (runs on form submission)

**Solution:**
1. Delete Schedule Trigger node
2. Add Webhook node
3. Connect webhook to next node in chain
4. Configure webhook path: `/your-endpoint`

**B. Modify Data Transformation**
Template: Formats name as "First Last"
You need: "LAST, First" format

**Solution:**
1. Find Set node or Code node handling name
2. Modify expression:
   ```
   Original: {{ $json.firstName }} {{ $json.lastName }}
   Updated: {{ $json.lastName }}, {{ $json.firstName }}
   ```

**C. Add Additional Actions**
Template: Sends Slack notification
You need: Slack + Email notification

**Solution:**
1. After Slack node, click "+" button
2. Add Gmail node
3. Configure email settings
4. Both notifications now send

**D. Change Conditional Logic**
Template: IF status equals "paid" → send receipt
You need: IF status equals "paid" AND amount > 100 → send receipt

**Solution:**
1. Open IF node
2. Click "Add Condition"
3. Add second condition:
   - `{{ $json.amount }}` greater than `100`
4. Both conditions must be true (AND logic)

#### Step 4.4: Test Modified Workflow

**Step 1: Use Manual Trigger for Testing**
1. Temporarily disconnect original trigger
2. Add Manual Trigger at start
3. Click "Execute Workflow"
4. Verify each node executes correctly

**Step 2: Check Each Node Output**
1. After execution, nodes show green checkmarks
2. Click each node
3. Review "Output" tab
4. Verify data is correct

**Step 3: Test Error Scenarios**
1. Try with missing data (if applicable)
2. Try with invalid data
3. Verify error handling works (see setup_n8n_error_handling.md)

**Step 4: Test with Real Trigger**
1. Remove Manual Trigger
2. Reconnect original trigger (or your new trigger)
3. Test actual trigger:
   - Webhook: Send test POST request
   - Schedule: Wait for scheduled time OR manually execute
   - Email Trigger: Send test email

### Phase 5: Advanced Modifications (30 minutes)

#### Technique 1: Merge Multiple Workflows

You have:
- Workflow A: Captures leads from form
- Workflow B: Sends welcome email sequence

**Combine them:**
1. Open Workflow A
2. At the end, instead of stopping, continue
3. Import Workflow B nodes:
   - Open Workflow B
   - Select all nodes (Ctrl+A / Cmd+A)
   - Copy (Ctrl+C / Cmd+C)
4. Go back to Workflow A
5. Paste at end (Ctrl+V / Cmd+V)
6. Connect last node of A to first node of B

**Why:** Single workflow is easier to manage than two separate workflows

#### Technique 2: Convert to Sub-Workflow

Large workflow too complex? Split it:

**Original:** One 50-node workflow
**New Structure:**
- Main workflow (10 nodes)
- Sub-workflow 1: Data processing (20 nodes)
- Sub-workflow 2: Notifications (20 nodes)

**How:**
1. Identify section to extract (e.g., all notification nodes)
2. Create new workflow
3. Add "Execute Workflow Trigger"
4. Move nodes to new workflow
5. In main workflow:
   - Delete moved nodes
   - Add "Execute Workflow" node
   - Select sub-workflow
   - Data passes between workflows automatically

#### Technique 3: Parameterize Workflow

Template has hardcoded values. Make them configurable:

**Step 1: Identify all hardcoded values**
- Email: `support@example.com`
- Slack channel: `#alerts`
- API URL: `https://api.example.com`

**Step 2: Create variables at workflow start**
Add Set node at very beginning:
```
Set Node: "Configuration"
Fields:
  - supportEmail (String): support@youragency.com
  - slackChannel (String): #your-alerts
  - apiUrl (String): https://your-api.com
```

**Step 3: Reference variables throughout**
Everywhere you had hardcoded value:
```
Old: support@example.com
New: {{ $('Configuration').item.json.supportEmail }}
```

**Benefit:** Change config in ONE place, affects entire workflow

#### Technique 4: Add Logging for Debugging

Template works but you don't understand how:

**Add logging nodes:**
```
[After each major step]
    ↓
[Set: Log Step]
Fields:
  - step: "Step 1: Data Retrieved"
  - timestamp: {{ $now }}
  - dataPreview: {{ $json }}
    ↓
[Continue workflow]
```

**Send logs to Google Sheets:**
```
[After each Set: Log Step]
    ↓
[Google Sheets: Append Log]
Sheet: Workflow Logs
Row: Timestamp, Step, Data
```

**Benefit:** See exactly what happens at each step, helps with debugging

#### Technique 5: Optimize Performance

Template works but slow:

**Optimization 1: Remove unnecessary nodes**
- Look for duplicate Set nodes
- Combine multiple Set operations into one

**Optimization 2: Parallel execution**
Original (sequential):
```
Get User Data
    ↓
Send Email
    ↓
Post to Slack
```

Optimized (parallel):
```
Get User Data
    ↓ (splits to both)
Send Email
AND
Post to Slack
```

Both email and Slack happen simultaneously, saving time.

**How to implement:**
1. From single node, click "+" button
2. Add first action node
3. Go BACK to original node, click "+" again
4. Add second action node
5. Both execute in parallel

**Optimization 3: Filter early**
Original:
```
Get 1000 records
    ↓
Process all 1000
    ↓
Filter to 10 needed records
```

Optimized:
```
Get 1000 records
    ↓
Filter to 10 needed records
    ↓
Process only 10 records
```

Move IF/Filter nodes as early as possible in workflow.

### Phase 6: Common Template Modifications (20 minutes)

#### Modification 1: Change from Airtable to Google Sheets

Template uses Airtable, you use Google Sheets:

**Steps:**
1. Find all Airtable nodes
2. Note what they do (create record, update, read, etc.)
3. Replace with Google Sheets equivalent:

**Airtable "Create Record" → Google Sheets "Append Row"**
```
Airtable config:
  Base: MyBase
  Table: Contacts
  Fields:
    Name: {{ $json.name }}
    Email: {{ $json.email }}

Becomes Google Sheets:
  Operation: Append
  Sheet: Contacts
  Values:
    Column A (Name): {{ $json.name }}
    Column B (Email): {{ $json.email }}
```

**Airtable "Search" → Google Sheets "Lookup"**
```
Airtable:
  Filter by Formula: Email = "john@example.com"

Becomes Google Sheets:
  Operation: Lookup
  Lookup Column: Email
  Lookup Value: john@example.com
```

#### Modification 2: Replace OpenAI with Anthropic Claude

Template uses OpenAI, you prefer Claude:

**OpenAI HTTP Request:**
```
Method: POST
URL: https://api.openai.com/v1/chat/completions
Headers:
  Authorization: Bearer {{ $credentials.openaiKey }}
  Content-Type: application/json
Body:
{
  "model": "gpt-4",
  "messages": [{"role": "user", "content": "{{ $json.prompt }}"}]
}
```

**Replace with Claude:**
```
Method: POST
URL: https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {{ $credentials.claudeKey }}
  anthropic-version: 2023-06-01
  Content-Type: application/json
Body:
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [{"role": "user", "content": "{{ $json.prompt }}"}]
}
```

**Then update response parsing:**
```
OpenAI response: {{ $json.choices[0].message.content }}
Claude response: {{ $json.content[0].text }}
```

#### Modification 3: Add Multi-Language Support

Template in English, you need Spanish:

**Find all user-facing text:**
- Email subject lines
- Email body
- Slack messages
- SMS text

**Add language detection:**
```
[After getting user data]
    ↓
[IF: Detect Language]
{{ $json.language }} equals "es"
    ↓                ↓
  Spanish         English
    ↓                ↓
[Set: Spanish     [Set: English
Message]         Message]
    ↓                ↓
    (merge back)
    ↓
[Send Email]
```

**Or use translation API:**
```
[Get template text in English]
    ↓
[IF: User language not English]
    ↓
[HTTP Request: Google Translate API]
Translate text to {{ $json.userLanguage }}
    ↓
[Use translated text in email]
```

#### Modification 4: Convert to White-Label for Clients

Template has your branding, client needs theirs:

**Parameterize all branding:**
At workflow start:
```
Set Node: "Client Branding"
Fields:
  - companyName: {{ $json.clientName }}
  - logoUrl: {{ $json.clientLogoUrl }}
  - supportEmail: {{ $json.clientSupportEmail }}
  - primaryColor: {{ $json.clientColor }}
```

**Use throughout workflow:**
```
Email body:
<img src="{{ $('Client Branding').item.json.logoUrl }}" />
<h1>Welcome to {{ $('Client Branding').item.json.companyName }}!</h1>
<p>Questions? Contact us: {{ $('Client Branding').item.json.supportEmail }}</p>
```

**Store client configs:**
Option 1: Google Sheets with client configs
Option 2: Database with client ID → config mapping
Option 3: Separate workflow per client (less scalable)

### Phase 7: Troubleshooting Imported Workflows (15 minutes)

#### Issue 1: "Node type not found"
**Symptom:** Node shows as unknown type, can't configure

**Causes:**
- Template uses custom/community node not installed
- Template created with newer N8N version
- Node was renamed in newer N8N versions

**Solutions:**
1. Check N8N version:
   - Settings → About N8N → Version
2. Update N8N to latest (if self-hosted)
3. Install community node:
   - Settings → Community Nodes
   - Search for missing node
   - Install
4. Replace with equivalent node:
   - Delete unknown node
   - Add similar built-in node
   - Reconfigure

#### Issue 2: Expressions not resolving
**Symptom:** `{{ $json.field }}` shows literally in output instead of value

**Causes:**
- Expression not in correct field type
- Referencing node that doesn't exist in your workflow
- Typo in field name

**Solutions:**
1. Check field type: Must be set to "Expression" not "Fixed"
2. Verify referenced node exists:
   - `{{ $('Node Name').item.json.field }}`
   - Node Name must match exactly (case-sensitive)
3. Execute workflow, click node before problem node
4. Check field names in output (they're case-sensitive)

#### Issue 3: Workflow executes but no output
**Symptom:** All nodes green, but nothing happens (no email sent, no data saved)

**Causes:**
- Action nodes have "dry run" or "test mode" enabled
- Credentials are test credentials (not production)
- Filtering removed all items before reaching action

**Solutions:**
1. Check each action node's "Options":
   - Gmail: "Send Mode" should be "Send"
   - HTTP Request: No "test" parameters
2. Verify credentials are production:
   - Credentials → Check name (shouldn't have "test" or "dev")
3. Add Set node before action to verify data reaching it:
   ```
   [Before action node]
       ↓
   [Set: Debug]
   Field: itemCount
   Value: {{ $input.all().length }}
   ```
   If itemCount = 0, problem is earlier in workflow

#### Issue 4: Rate limit errors
**Symptom:** Workflow fails with "Too many requests" or 429 error

**Causes:**
- Template processes more items than your API allows
- Template doesn't have rate limiting

**Solutions:**
1. Add "Wait" node between API calls:
   ```
   [Loop Over Items]
       ↓ (for each item)
   [HTTP Request: API Call]
       ↓
   [Wait: 1 second]
   ```
2. Reduce batch size:
   - Add "Limit" node after data source
   - Process 10 items at a time instead of 1000
3. Upgrade API plan (if available)

#### Issue 5: Webhook not receiving data
**Symptom:** Webhook trigger waiting, never executes

**Causes:**
- Webhook URL incorrect
- Workflow not active
- External service not configured correctly

**Solutions:**
1. Verify webhook URL:
   - Double-click Webhook node
   - Copy "Test URL" or "Production URL"
   - Make sure using correct one (Test during development, Production when active)
2. Ensure workflow is Active (toggle top-right)
3. Test with curl:
   ```bash
   curl -X POST https://your-n8n-domain.com/webhook/test-path \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```
4. Check external service configuration:
   - Is webhook URL saved there?
   - Is webhook enabled?
   - Check service's webhook logs for errors

## Common Mistakes to Avoid

### Mistake 1: Not Checking Node Versions
**Problem:** Import old template, nodes behave differently in your newer N8N
**Solution:** Check template creation date, update nodes to use new parameters

### Mistake 2: Trusting Hardcoded API Keys
**Problem:** Template has API key visible - creator can see your data!
**Solution:** ALWAYS replace API keys, never use keys from templates

### Mistake 3: Not Testing Before Activating
**Problem:** Activate workflow immediately, sends 1000 emails to wrong addresses
**Solution:** Test with Manual Trigger, verify output, THEN activate

### Mistake 4: Ignoring Sticky Notes
**Problem:** Template doesn't work, instructions were in sticky note you didn't read
**Solution:** Read all sticky notes first, they contain setup instructions

### Mistake 5: Not Renaming Imported Workflow
**Problem:** Have 5 workflows all named "Untitled Workflow"
**Solution:** Rename immediately after import: Click name → Type new name

### Mistake 6: Keeping Test Data in Production
**Problem:** Template has Set node with test data at start, real trigger is ignored
**Solution:** Delete test Set nodes before activating with real trigger

### Mistake 7: Not Understanding What Workflow Does
**Problem:** Workflow running, no idea what it's actually doing
**Solution:** Add sticky notes explaining each section as you customize

### Mistake 8: Partial Customization
**Problem:** Changed email address but forgot to update Slack channel - notifications go to template creator!
**Solution:** Use checklist - verify EVERY node has been customized

### Mistake 9: No Backup Before Modifying
**Problem:** Template worked, you modified it, now it's broken and can't undo
**Solution:** Before major changes:
1. Three dots → "Download"
2. Save original JSON
3. Now modify safely - can always re-import original

### Mistake 10: Credentials Not Matching Environment
**Problem:** Use production credentials in test workflow, accidentally send real emails to customers
**Solution:** Create separate credentials named "Service - Test" and "Service - Production"

## Success Metrics
- ✅ Can import workflow in under 2 minutes
- ✅ Can identify all nodes needing customization
- ✅ Can replace credentials without errors
- ✅ Can test imported workflow successfully
- ✅ Can modify workflow logic for specific use case
- ✅ Imported workflows execute with 95%+ success rate
- ✅ Can merge multiple templates into one workflow
- ✅ Can troubleshoot import errors independently

## Import Workflow Checklist

Use this checklist for EVERY imported workflow:

- [ ] Workflow imported successfully (all nodes visible)
- [ ] Read all sticky notes and documentation
- [ ] Identified all red nodes (credentials needed)
- [ ] Created/assigned credentials for all services
- [ ] Updated all hardcoded email addresses
- [ ] Updated all hardcoded phone numbers
- [ ] Updated all hardcoded URLs
- [ ] Updated Google Sheets/Docs IDs (if applicable)
- [ ] Updated Slack channels
- [ ] Verified API keys are YOUR keys, not template creator's
- [ ] Renamed workflow to descriptive name
- [ ] Added error workflow (see setup_n8n_error_handling.md)
- [ ] Tested with Manual Trigger
- [ ] Verified output of each node
- [ ] Tested error scenarios
- [ ] Downloaded backup of customized workflow
- [ ] Documented customizations in sticky notes
- [ ] Set workflow to Active (if ready for production)

## Related Skills
- **build_n8n_workflow.md** - Understand workflow fundamentals before modifying
- **setup_n8n_error_handling.md** - Add error handling to imported workflows
- **find_n8n_templates.md** - Where to find templates to import
- **setup_n8n_triggers_agents.md** - Customize trigger types in imported workflows

---

**Skill Version:** 1.0
**Last Updated:** 2024
**Estimated Execution Time:** 20-30 minutes per imported workflow
**Difficulty:** Beginner to Intermediate
**Prerequisites:** N8N instance running, basic workflow understanding
