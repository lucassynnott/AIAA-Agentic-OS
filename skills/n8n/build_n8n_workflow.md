# Build N8N Workflow - Complete Workflow Construction Guide

## Purpose
This skill teaches you how to build production-ready N8N workflows from scratch, covering all essential node types, data manipulation, and workflow design patterns. This is your comprehensive guide to creating automated workflows that actually work reliably.

## When to Use This Skill
- When starting a new automation project
- When you need to understand how N8N workflows function
- When building client deliverables that must be reliable
- When you want to learn workflow best practices
- Before modifying existing workflows (understand the building blocks first)

## Prerequisites
### Required Setup
- N8N instance running (Cloud or Self-Hosted - see setup_n8n_self_hosted.md)
- Access to N8N dashboard with ability to create workflows
- Basic understanding of automation concepts (triggers, actions, data flow)

### Recommended Knowledge
- Basic JSON understanding (data structure)
- Familiarity with API concepts (helpful but not required)
- Understanding of conditional logic (if/then)

## Workflow Architecture Fundamentals

### The N8N Execution Model
```
Trigger Node (START)
    ↓
Processing Nodes (MIDDLE)
    ↓
Action Nodes (END)
```

**Key Concepts:**
1. **Trigger Nodes:** Start the workflow (webhook, schedule, manual)
2. **Processing Nodes:** Transform, filter, route data
3. **Action Nodes:** Perform actions (send email, update database, API calls)
4. **Data Flow:** Items flow from left to right through nodes
5. **Execution:** Each node receives items from previous node, processes, outputs to next

### Data Structure in N8N
Every node outputs data in this format:
```json
[
  {
    "json": {
      "field1": "value1",
      "field2": "value2"
    },
    "binary": {}  // Optional: for file data
  }
]
```

**Understanding Items:**
- N8N processes arrays of items
- Each item is an object with `json` property containing your data
- Nodes can output multiple items (array of objects)
- Subsequent nodes process ALL items from previous node

## Step-by-Step Workflow Building

### Phase 1: Create Your First Workflow (10 minutes)

#### Step 1.1: Create New Workflow
1. Log into N8N dashboard
2. Click "Create Workflow" button (top-right or center)
3. You'll see empty canvas with one node: "On clicking 'execute'"
4. This is a Manual Trigger node (for testing)

#### Step 1.2: Understanding the Interface
**Left Sidebar:**
- Workflows: List of all your workflows
- Executions: History of workflow runs
- Credentials: Saved API keys, OAuth tokens

**Top Bar:**
- Workflow name: Click "Untitled" to rename
- Save button: ALWAYS save your work (N8N doesn't auto-save!)
- Execute button: Run workflow manually
- Active toggle: Enable/disable workflow for automatic execution

**Canvas:**
- Nodes: The building blocks
- Connections: Lines showing data flow
- Zoom controls: Bottom-right corner

#### Step 1.3: Add Your First Processing Node
1. Click the **+** button on the right side of the Manual Trigger node
2. Search bar appears with all available nodes
3. Type "Set" and select "Set" node
4. Click to add it to canvas
5. Node appears connected to Manual Trigger

#### Step 1.4: Configure the Set Node
1. Double-click the "Set" node to open configuration
2. Click "Add Value" button
3. Select "String" from dropdown
4. Configure:
   - **Name:** `message`
   - **Value:** `Hello from my first N8N workflow!`
5. Click "Add Value" again
6. Select "Number"
7. Configure:
   - **Name:** `timestamp`
   - **Value:** `{{ $now.toUnixInteger() }}` (this is an expression)
8. Click outside node or press ESC to close

#### Step 1.5: Execute and View Results
1. Click "Execute workflow" button (top-right)
2. Workflow runs
3. Nodes show green checkmark ✓ (success)
4. Click on "Set" node to view output
5. You'll see:
```json
{
  "message": "Hello from my first N8N workflow!",
  "timestamp": 1702999999
}
```

**🎉 Congratulations!** You've built your first N8N workflow.

### Phase 2: Essential Node Types (30 minutes)

#### Node Type 1: Trigger Nodes (START workflows)

**A. Manual Trigger**
- **When to use:** Testing workflows, manual execution
- **Configuration:** None needed
- **Execution:** Click "Execute" button
- **Use case:** Development and testing

**B. Schedule Trigger**
1. Add node: Search "Schedule Trigger"
2. Configuration options:
   - **Trigger Interval:** How often to run
     - Every X minutes/hours/days
     - Cron expression (advanced)
   - **Examples:**
     - Every 15 minutes: `*/15 * * * *`
     - Every day at 9 AM: `0 9 * * *`
     - Every Monday at 8 AM: `0 8 * * 1`
3. Save and activate workflow (toggle to "Active")

**C. Webhook Trigger**
1. Add node: Search "Webhook"
2. Configuration:
   - **HTTP Method:** GET, POST, PUT, DELETE
   - **Path:** Custom URL path (e.g., `my-webhook`)
   - **Authentication:** None, Basic Auth, Header Auth
3. Copy webhook URL (shown in node)
4. Use this URL in external services (forms, Zapier replacement, etc.)
5. **Testing:**
   ```bash
   curl -X POST https://your-n8n-domain.com/webhook/my-webhook \
     -H "Content-Type: application/json" \
     -d '{"name": "John", "email": "john@example.com"}'
   ```

**D. Email Trigger (IMAP)**
1. Add node: Search "Email Trigger (IMAP)"
2. Create credential:
   - **Gmail:** Use App Password (not regular password)
   - **Other:** IMAP server settings
3. Configuration:
   - **Mailbox:** INBOX, specific folder
   - **Check Interval:** How often to check (minutes)
   - **Options:** Mark as read, download attachments
4. Use case: Auto-respond to emails, process order confirmations

#### Node Type 2: Data Processing Nodes

**A. Set Node (Most Common)**
- **Purpose:** Create or modify data fields
- **When to use:** Adding new fields, renaming fields, hardcoding values

**Example Configuration:**
```
Add Value → String → Name: fullName, Value: {{ $json.firstName }} {{ $json.lastName }}
Add Value → Boolean → Name: isActive, Value: true
Add Value → Number → Name: total, Value: {{ $json.quantity * $json.price }}
```

**Best Practices:**
- Use Set for simple field creation
- Keep field names consistent (camelCase recommended)
- Don't use Set for complex logic (use Code node instead)

**B. Code Node (Most Powerful)**
- **Purpose:** Custom JavaScript/Python for complex operations
- **When to use:** Complex data transformations, loops, conditional logic

**Basic Structure:**
```javascript
// Access input data
const items = $input.all();

// Process each item
const outputItems = items.map(item => {
  // Your logic here
  return {
    json: {
      // Your output fields
      originalData: item.json,
      newField: 'new value',
      calculated: item.json.value * 2
    }
  };
});

// Return processed items
return outputItems;
```

**Common Patterns:**

**Pattern 1: Filter Items**
```javascript
// Only return items where status is "active"
return $input.all().filter(item => item.json.status === 'active');
```

**Pattern 2: Transform Data**
```javascript
return $input.all().map(item => ({
  json: {
    id: item.json.user_id,
    name: item.json.full_name.toUpperCase(),
    email: item.json.email.toLowerCase()
  }
}));
```

**Pattern 3: Aggregate Data**
```javascript
const items = $input.all();
const total = items.reduce((sum, item) => sum + item.json.amount, 0);

return [{
  json: {
    totalAmount: total,
    itemCount: items.length,
    averageAmount: total / items.length
  }
}];
```

**Pattern 4: Generate Multiple Items**
```javascript
const items = [];
for (let i = 0; i < 10; i++) {
  items.push({
    json: {
      index: i,
      value: `Item ${i}`,
      timestamp: new Date().toISOString()
    }
  });
}
return items;
```

**C. IF Node (Conditional Routing)**
- **Purpose:** Route data based on conditions
- **When to use:** Different actions for different data

**Configuration:**
1. Add IF node
2. Set condition type:
   - **Boolean:** True/False
   - **Number:** Greater than, less than, equal
   - **String:** Contains, equals, starts with
   - **Date & Time:** Before, after
3. Reference previous node data:
   - Expression: `{{ $json.fieldName }}`
   - Example: `{{ $json.status }}` equals `active`

**Example Flow:**
```
Webhook Trigger
    ↓
IF: status equals "paid"
    ↓                  ↓
   true              false
    ↓                  ↓
Send Receipt      Send Reminder
```

**D. Switch Node (Multiple Routes)**
- **Purpose:** Route to multiple paths based on value
- **When to use:** More than 2 possible outcomes

**Configuration:**
```
Mode: Rules
Rules:
  Rule 1: {{ $json.category }} equals "urgent" → Output 0
  Rule 2: {{ $json.category }} equals "normal" → Output 1
  Rule 3: {{ $json.category }} equals "low" → Output 2
Fallback Output: 3 (for unmatched items)
```

**E. Merge Node (Combine Data)**
- **Purpose:** Combine data from multiple branches
- **Modes:**
  - **Append:** Add items from both inputs together
  - **Merge by Fields:** Combine items with matching field values
  - **Merge by Position:** Combine items at same array index

**Use Case Example:**
```
Get User Data (ID, Name)
                        ↘
                         Merge (by User ID)
                        ↗
Get Order Data (User ID, Order Total)
```

**F. Loop Over Items Node**
- **Purpose:** Process items one at a time (not in batch)
- **When to use:** API rate limiting, sequential processing required

#### Node Type 3: Action Nodes (DO Things)

**A. HTTP Request Node**
- **Purpose:** Call external APIs
- **Most versatile action node**

**Basic Configuration:**
1. Method: GET, POST, PUT, DELETE, PATCH
2. URL: API endpoint
3. Authentication:
   - None
   - Basic Auth
   - Header Auth (API Key)
   - OAuth2
4. Headers: Content-Type, Authorization, custom headers
5. Body (for POST/PUT): JSON, Form Data, Raw

**Example: Call OpenAI API**
```
HTTP Request Node Config:
  Method: POST
  URL: https://api.openai.com/v1/chat/completions
  Authentication: Header Auth
    Name: Authorization
    Value: Bearer {{ $credentials.openAIKey }}
  Headers:
    Content-Type: application/json
  Body (JSON):
    {
      "model": "gpt-4",
      "messages": [
        {
          "role": "user",
          "content": "{{ $json.userQuestion }}"
        }
      ]
    }
```

**B. Gmail Node**
- **Purpose:** Send emails via Gmail
- **Prerequisites:** Google OAuth setup (see setup_n8n_google_oauth.md)

**Send Email Configuration:**
1. Resource: Message
2. Operation: Send
3. To: `{{ $json.email }}`
4. Subject: Dynamic via expression
5. Message (HTML):
```html
<h1>Hello {{ $json.firstName }}!</h1>
<p>Your order #{{ $json.orderId }} has been confirmed.</p>
```

**C. Google Sheets Node**
- **Purpose:** Read/write spreadsheet data
- **Common Operations:**

**Append Row:**
```
Resource: Sheet
Operation: Append
Sheet ID: [Your Sheet ID]
Range: Sheet1!A:E
Values to Send: Manual Mapping
  Column A: {{ $json.name }}
  Column B: {{ $json.email }}
  Column C: {{ $json.phone }}
```

**Read Rows:**
```
Resource: Sheet
Operation: Get All
Sheet ID: [Your Sheet ID]
Range: Sheet1!A:E
Returns array of objects with column headers as keys
```

**D. Slack Node**
- **Purpose:** Send messages to Slack
- **Setup:** Create Slack app, add to workspace

**Post Message:**
```
Resource: Message
Operation: Post
Channel: #general (or channel ID)
Text: Workflow completed successfully!
Attachments: Can add rich formatting
```

**E. Telegram Node**
- **Purpose:** Send/receive Telegram messages
- **Setup:** Create bot via BotFather

**Send Message:**
```
Resource: Message
Operation: Send Text
Chat ID: {{ $json.chatId }} (from trigger)
Text: Your message here
Parse Mode: Markdown or HTML
```

### Phase 3: Data Manipulation Techniques (20 minutes)

#### Technique 1: Expressions
Expressions allow dynamic data references using `{{ }}` syntax.

**Basic Field Reference:**
```
{{ $json.fieldName }}
{{ $json.user.email }}  // Nested object
{{ $json.items[0].name }}  // Array access
```

**Common Expression Functions:**

**String Manipulation:**
```
{{ $json.name.toUpperCase() }}
{{ $json.email.toLowerCase() }}
{{ $json.text.trim() }}
{{ $json.fullName.split(' ')[0] }}  // Get first name
```

**Number Operations:**
```
{{ $json.price * 1.1 }}  // Add 10%
{{ Math.round($json.value) }}
{{ Math.floor($json.rating) }}
```

**Date/Time:**
```
{{ $now }}  // Current datetime
{{ $now.toFormat('yyyy-MM-dd') }}  // Format date
{{ $now.plus({ days: 7 }) }}  // 7 days from now
{{ DateTime.fromISO($json.createdDate) }}  // Parse date
```

**Conditional Expressions:**
```
{{ $json.status === 'paid' ? 'Complete' : 'Pending' }}
{{ $json.amount > 100 ? 'High' : 'Low' }}
```

**String Concatenation:**
```
{{ $json.firstName + ' ' + $json.lastName }}
{{ 'Hello, ' + $json.name + '!' }}
```

#### Technique 2: Accessing Previous Node Data
```
{{ $('Node Name').item.json.fieldName }}  // Specific node
{{ $('Node Name').all() }}  // All items from node
{{ $('Node Name').first().json.id }}  // First item only
```

#### Technique 3: Environment Variables
```
{{ $env.API_KEY }}  // Access environment variable
{{ $env.WEBHOOK_URL }}
```

#### Technique 4: Credentials Access
```
{{ $credentials.apiKey }}  // Access saved credential
{{ $credentials.oauth2.accessToken }}
```

### Phase 4: Real-World Workflow Examples

#### Example 1: Contact Form to Google Sheets
**Use Case:** Save website form submissions to spreadsheet

**Workflow Structure:**
```
1. Webhook Trigger (POST)
   - Path: contact-form
   - Authentication: None

2. Set Node (Clean Data)
   - fullName: {{ $json.body.firstName }} {{ $json.body.lastName }}
   - email: {{ $json.body.email.toLowerCase() }}
   - phone: {{ $json.body.phone }}
   - message: {{ $json.body.message }}
   - submittedAt: {{ $now.toFormat('yyyy-MM-dd HH:mm:ss') }}

3. Google Sheets (Append Row)
   - Sheet: Contacts
   - Values: Map from Set node

4. Gmail (Send Confirmation)
   - To: {{ $json.email }}
   - Subject: Thanks for contacting us!
   - Body: We received your message and will respond soon.

5. Slack (Notify Team)
   - Channel: #leads
   - Message: New contact form submission from {{ $json.fullName }}

6. Respond to Webhook
   - Response Code: 200
   - Body: {"success": true, "message": "Form submitted successfully!"}
```

**Implementation Steps:**
1. Create workflow, add Webhook trigger
2. Add Set node, configure data mapping
3. Add Google Sheets node, authenticate, select sheet
4. Add Gmail node, authenticate, configure email template
5. Add Slack node, authenticate, set channel
6. Add "Respond to Webhook" node at end
7. Save workflow, set to Active
8. Test with curl or Postman
9. Integrate webhook URL into website form

#### Example 2: Daily Report Generation
**Use Case:** Email daily summary of orders from database

**Workflow Structure:**
```
1. Schedule Trigger
   - Cron: 0 9 * * * (every day at 9 AM)

2. HTTP Request (Get Yesterday's Orders)
   - Method: GET
   - URL: https://api.yourstore.com/orders
   - Query Parameters:
     - startDate: {{ $now.minus({ days: 1 }).startOf('day').toISO() }}
     - endDate: {{ $now.minus({ days: 1 }).endOf('day').toISO() }}

3. Code Node (Calculate Stats)
   ```javascript
   const orders = $input.all();
   const totalRevenue = orders.reduce((sum, order) =>
     sum + order.json.total, 0);
   const averageOrder = totalRevenue / orders.length;

   return [{
     json: {
       date: $now.minus({ days: 1 }).toFormat('yyyy-MM-dd'),
       orderCount: orders.length,
       totalRevenue: totalRevenue.toFixed(2),
       averageOrder: averageOrder.toFixed(2),
       orders: orders.map(o => o.json)
     }
   }];
   ```

4. Gmail (Send Report)
   - To: team@company.com
   - Subject: Daily Sales Report - {{ $json.date }}
   - Body HTML:
   ```html
   <h2>Sales Report for {{ $json.date }}</h2>
   <p><strong>Total Orders:</strong> {{ $json.orderCount }}</p>
   <p><strong>Total Revenue:</strong> ${{ $json.totalRevenue }}</p>
   <p><strong>Average Order:</strong> ${{ $json.averageOrder }}</p>
   ```
```

#### Example 3: AI-Powered Email Response
**Use Case:** Automatically generate email responses using AI

**Workflow Structure:**
```
1. Email Trigger (IMAP)
   - Mailbox: support@company.com
   - Check every: 5 minutes
   - Mark as read: Yes

2. IF Node (Check for Auto-Reply Keyword)
   - Condition: {{ $json.subject }} contains "[Auto]"
   - true → Stop (don't auto-reply to auto-replies)
   - false → Continue

3. Code Node (Prepare AI Prompt)
   ```javascript
   return [{
     json: {
       prompt: `You are a helpful customer support agent.

       Customer Email:
       From: ${$json.from}
       Subject: ${$json.subject}
       Body: ${$json.body}

       Generate a professional, helpful response.
       Be concise and friendly.`,
       customerEmail: $json.from,
       originalSubject: $json.subject
     }
   }];
   ```

4. HTTP Request (Call OpenAI)
   - Method: POST
   - URL: https://api.openai.com/v1/chat/completions
   - Headers: Authorization, Content-Type
   - Body:
   ```json
   {
     "model": "gpt-4",
     "messages": [{"role": "user", "content": "{{ $json.prompt }}"}],
     "max_tokens": 500
   }
   ```

5. Set Node (Extract AI Response)
   - aiResponse: {{ $json.choices[0].message.content }}
   - customerEmail: {{ $('Code').item.json.customerEmail }}
   - subject: Re: {{ $('Code').item.json.originalSubject }}

6. Gmail (Send Response)
   - To: {{ $json.customerEmail }}
   - Subject: {{ $json.subject }}
   - Body: {{ $json.aiResponse }}
```

### Phase 5: Workflow Best Practices

#### Best Practice 1: Name Your Nodes Descriptively
**Bad:** "Set", "HTTP Request", "Code"
**Good:** "Format Customer Data", "Get User from API", "Calculate Order Total"

**Why:** Makes workflows self-documenting, easier to debug

#### Best Practice 2: Add Sticky Notes for Documentation
1. Right-click canvas → Add Sticky Note
2. Use for:
   - Explaining complex logic
   - Documenting API requirements
   - Noting credentials needed
   - Warning about dependencies

#### Best Practice 3: Use Try/Catch in Code Nodes
```javascript
try {
  const result = complexOperation($json.data);
  return [{ json: { result } }];
} catch (error) {
  return [{
    json: {
      error: true,
      message: error.message,
      originalData: $json
    }
  }];
}
```

#### Best Practice 4: Validate Input Data
```javascript
const requiredFields = ['email', 'name', 'orderId'];
const missingFields = requiredFields.filter(field => !$json[field]);

if (missingFields.length > 0) {
  throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
}

// Continue with processing...
```

#### Best Practice 5: Use Set Node Before Action Nodes
**Why:** Ensures data is in correct format, easier to debug

**Pattern:**
```
HTTP Request (Get Data)
    ↓
Set Node (Format for Email)
    ↓
Gmail (Send Email)
```

Instead of trying to format data directly in Gmail node.

#### Best Practice 6: Test with Sample Data
1. Use Manual Trigger for development
2. Add "Set" node at start with sample data:
```
{
  "email": "test@example.com",
  "name": "Test User",
  "amount": 99.99,
  "status": "paid"
}
```
3. Test workflow end-to-end before activating trigger
4. Remove sample data Set node when ready for production

#### Best Practice 7: Handle Empty Results
```javascript
const items = $input.all();

if (items.length === 0) {
  return [{
    json: {
      status: 'no_data',
      message: 'No items to process'
    }
  }];
}

// Process items...
```

#### Best Practice 8: Use Error Workflow (See setup_n8n_error_handling.md)
Every production workflow should have error handling configured.

### Phase 6: Debugging Workflows

#### Debugging Technique 1: Execute Node
1. Click on any node
2. Click "Execute node" in node panel
3. See output of just that node
4. Verify data is correct before next node

#### Debugging Technique 2: View Input/Output
1. After executing workflow
2. Click on any node
3. Toggle between "Input" and "Output" tabs
4. See exactly what data entered and left the node

#### Debugging Technique 3: Use Console.log in Code Nodes
```javascript
console.log('Debug: Processing item', $json);
console.log('Debug: Calculated value', calculatedValue);
return $input.all();
```

View logs in:
- Execution view → Click execution → "Logs" tab
- Self-hosted: Check Railway logs or Docker logs

#### Debugging Technique 4: Simplify and Test
If workflow failing:
1. Disconnect nodes after problem point
2. Execute up to problem node
3. Verify data is correct
4. Reconnect one node at a time
5. Identify exactly which node causes issue

#### Debugging Technique 5: Check Execution History
1. Click "Executions" in left sidebar
2. Filter by:
   - Failed executions
   - Specific workflow
   - Date range
3. Click execution to see full flow and error details

## Common Mistakes to Avoid

### Mistake 1: Not Saving Workflows
**Problem:** N8N doesn't auto-save. Close tab = lose work.
**Solution:** Save after every significant change. Keyboard shortcut: Ctrl+S / Cmd+S

### Mistake 2: Forgetting to Activate Workflows
**Problem:** Schedule/Webhook triggers won't work if workflow inactive
**Solution:** After testing, toggle workflow to "Active" (top-right)

### Mistake 3: Incorrect Expression Syntax
**Problem:** `$json.name` instead of `{{ $json.name }}`
**Solution:** Always wrap expressions in `{{ }}`

### Mistake 4: Not Handling Empty Arrays
**Problem:** Workflows fail when API returns no results
**Solution:** Always check `if (items.length === 0)` in Code nodes

### Mistake 5: Hardcoding Values That Should Be Dynamic
**Problem:** Email always goes to "john@example.com" instead of dynamic recipient
**Solution:** Use expressions: `{{ $json.recipientEmail }}`

### Mistake 6: Processing Too Much Data at Once
**Problem:** Workflow times out or crashes with 10,000 records
**Solution:**
- Use pagination in API calls
- Process in batches with Loop node
- Use "Limit" parameter in data source nodes

### Mistake 7: Not Testing Edge Cases
**Problem:** Workflow works with sample data but fails in production
**Solution:** Test with:
- Empty data
- Missing fields
- Invalid formats
- Maximum data volumes

### Mistake 8: Complex Logic in Single Code Node
**Problem:** 200-line Code node that's impossible to debug
**Solution:** Split into multiple Code nodes, each doing one thing well

### Mistake 9: Not Using Error Handling
**Problem:** One failure stops entire workflow
**Solution:** See setup_n8n_error_handling.md for comprehensive error handling

### Mistake 10: Ignoring Rate Limits
**Problem:** API blocks your requests
**Solution:**
- Add "Wait" nodes between requests
- Use "Loop Over Items" for rate-limited APIs
- Implement retry logic with exponential backoff

## Troubleshooting

### Issue: "Cannot read property 'json' of undefined"
**Cause:** Trying to access data from node that didn't execute or has no data
**Solution:**
```javascript
// Check if data exists before accessing
if ($input.first()?.json) {
  const data = $input.first().json;
  // Process data
}
```

### Issue: "Workflow execution timed out"
**Cause:** Processing too much data or slow external API
**Solutions:**
- Increase execution timeout in workflow settings
- Process data in smaller batches
- Use queue mode for long-running workflows (advanced)

### Issue: "Invalid expression"
**Cause:** Syntax error in `{{ }}` expression
**Solutions:**
- Check for typos in field names
- Verify bracket matching
- Use Expression Editor (click field, then expression icon)
- Test expressions: `{{ $json.fieldName }}` should show preview

### Issue: Webhook returns 404
**Cause:** Workflow not active or incorrect URL
**Solutions:**
- Ensure workflow is toggled to "Active"
- Copy webhook URL directly from node
- Check WEBHOOK_URL environment variable is set correctly

### Issue: Gmail node fails with "Invalid credentials"
**Cause:** OAuth token expired or incorrect setup
**Solutions:**
- Reconnect Google account: Credentials → Edit → Reconnect
- For self-hosted: Verify OAuth setup (see setup_n8n_google_oauth.md)
- Check Google account has Gmail API enabled

## Success Metrics
- ✅ Can create workflow from scratch in under 10 minutes
- ✅ Can add and configure any node type
- ✅ Can write expressions to reference data dynamically
- ✅ Can debug failed workflows using execution history
- ✅ Can build complete workflow with trigger, processing, and action
- ✅ Workflows execute successfully 95%+ of the time
- ✅ Can explain data flow through workflow to non-technical person

## Related Skills
- **setup_n8n_error_handling.md** - Add robust error handling to workflows
- **import_modify_n8n_workflows.md** - Import and customize existing workflows
- **setup_n8n_triggers_agents.md** - Advanced trigger configuration and AI agents
- **setup_n8n_gohighlevel_integration.md** - Connect Go High Level CRM

## Quick Reference: Node Cheat Sheet

| Node | Purpose | Common Use |
|------|---------|-----------|
| Manual Trigger | Start workflow manually | Testing |
| Schedule Trigger | Run on schedule | Daily reports, cleanup jobs |
| Webhook | HTTP endpoint | Forms, external integrations |
| Set | Create/modify fields | Data formatting |
| Code | Custom logic | Complex transformations |
| IF | Conditional routing | Different actions based on data |
| Switch | Multi-way routing | Route by category/status |
| HTTP Request | API calls | Any external service |
| Gmail | Send emails | Notifications, confirmations |
| Google Sheets | Read/write spreadsheets | Data storage, reports |
| Slack | Team notifications | Alerts, status updates |
| Merge | Combine data | Join data from multiple sources |
| Wait | Pause execution | Rate limiting, delays |

## Expression Quick Reference

```javascript
// Current date/time
{{ $now }}
{{ $now.toFormat('yyyy-MM-dd') }}

// Access data
{{ $json.fieldName }}
{{ $json.nested.field }}
{{ $json.array[0] }}

// String manipulation
{{ $json.text.toUpperCase() }}
{{ $json.text.toLowerCase() }}
{{ $json.text.trim() }}
{{ $json.text.split(',') }}

// Number operations
{{ $json.price * 1.1 }}
{{ Math.round($json.value) }}

// Conditional
{{ $json.status === 'active' ? 'Yes' : 'No' }}

// Previous node data
{{ $('Node Name').item.json.field }}

// Environment variables
{{ $env.VARIABLE_NAME }}

// Credentials
{{ $credentials.apiKey }}
```

---

**Skill Version:** 1.0
**Last Updated:** 2024
**Estimated Execution Time:** 60-90 minutes for first workflow, 15-30 minutes after practice
**Difficulty:** Beginner to Intermediate
**Prerequisites:** N8N instance running, basic understanding of automation concepts
