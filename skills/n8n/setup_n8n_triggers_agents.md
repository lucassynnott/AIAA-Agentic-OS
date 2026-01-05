# Setup N8N Triggers & Agents - Complete Guide to Workflow Automation

## Purpose
This skill provides comprehensive coverage of N8N triggers, HTTP requests, authorization methods, and AI agent implementation. Master these concepts to build sophisticated automations that respond to events, call external APIs securely, and leverage AI for intelligent workflow decisions.

## When to Use This Skill
- When you need to understand all trigger types in N8N
- When building workflows that respond to external events (webhooks, schedules, emails)
- When connecting to external APIs with various authentication methods
- When implementing AI agents for content generation, decision-making, or data processing
- When building automated systems that need to interact with multiple platforms
- Before creating production workflows that require reliable triggering mechanisms

## Prerequisites

### Required Setup
- N8N instance running (Cloud or Self-Hosted - see setup_n8n_self_hosted.md)
- Access to N8N dashboard with ability to create workflows
- Basic understanding of N8N workflow building (see build_n8n_workflow.md)

### Recommended Knowledge
- Understanding of HTTP protocols (GET, POST, PUT, DELETE)
- Basic authentication concepts (API keys, OAuth)
- JSON data structure familiarity
- Understanding of cron expressions (for scheduling)

### Required Accounts for Examples
- Telegram account (for Telegram bot trigger examples)
- API keys for services you want to integrate
- OpenAI API key (for AI agent examples - optional)

## Trigger Types Deep Dive

### Understanding Triggers
Triggers are the entry points that start workflow execution. N8N supports multiple trigger types to accommodate different automation scenarios.

**Trigger Categories:**
1. **Manual Triggers** - User-initiated execution (testing, on-demand)
2. **Schedule Triggers** - Time-based execution (cron jobs)
3. **Webhook Triggers** - HTTP endpoint that external services call
4. **Platform Triggers** - Service-specific (Telegram, Email, Slack, etc.)
5. **Event Triggers** - Database changes, file system events

---

## Phase 1: Manual & Schedule Triggers (15 minutes)

### Manual Trigger - Testing & Development

**When to Use:**
- Testing workflows during development
- Running workflows on-demand
- Creating utility workflows that don't need automatic triggers

**Setup Instructions:**
1. Create new workflow
2. Add node: Search "Manual"
3. Select "Manual Trigger" (also called "On clicking 'execute'")
4. This trigger is automatically added to new workflows

**Configuration:**
```
Manual Trigger Node
├── No configuration needed
├── Execution: Click "Execute workflow" button
└── Use Case: Development, testing, manual operations
```

**Example Use Cases:**
- Generate reports when needed
- Data migration/cleanup scripts
- Test workflow logic before adding real trigger
- Administrative tasks

**Best Practices:**
- Use for initial development of all workflows
- Test with sample data before switching to automatic triggers
- Keep manual trigger nodes for testing even after adding automatic triggers
- Document what the manual trigger should simulate

---

### Schedule Trigger - Time-Based Automation

**When to Use:**
- Daily/weekly/monthly reports
- Regular data synchronization
- Scheduled content posting
- Database cleanup jobs
- Automated backups
- Time-sensitive operations

#### Basic Configuration

**Step 1.1: Add Schedule Trigger**
1. Create new workflow or click "+" to add node
2. Search "Schedule Trigger"
3. Select "Schedule Trigger" from results

**Step 1.2: Configure Interval**

**Option A: Simple Intervals**
```
Trigger Times: Interval
Mode: Days
Days Between Triggers: 1
Trigger at Hour: 9
Trigger at Minute: 0

Result: Runs every day at 9:00 AM
```

**Common Simple Intervals:**
```yaml
Every 15 minutes:
  Trigger Times: Minutes
  Minutes Between Triggers: 15

Every Hour:
  Trigger Times: Hours
  Hours Between Triggers: 1

Every Day at 8 AM:
  Trigger Times: Days
  Days Between Triggers: 1
  Trigger at Hour: 8
  Trigger at Minute: 0

Every Week on Monday at 9 AM:
  Trigger Times: Weeks
  Weeks Between Triggers: 1
  Trigger on Weekday: Monday
  Trigger at Hour: 9
  Trigger at Minute: 0
```

**Option B: Custom Cron Expression** (Advanced)

```
Trigger Times: Custom (Cron)
Expression: 0 9 * * 1-5
```

**Cron Expression Breakdown:**
```
* * * * * *
│ │ │ │ │ │
│ │ │ │ │ └─── Day of Week (0-6, Sunday=0)
│ │ │ │ └───── Month (1-12)
│ │ │ └─────── Day of Month (1-31)
│ │ └───────── Hour (0-23)
│ └─────────── Minute (0-59)
└───────────── Second (0-59) - Optional
```

**Common Cron Patterns:**

```bash
# Every 15 minutes
*/15 * * * *

# Every hour at minute 30
30 * * * *

# Every day at 9 AM
0 9 * * *

# Every weekday at 8 AM (Mon-Fri)
0 8 * * 1-5

# Every Monday at 9 AM
0 9 * * 1

# First day of every month at midnight
0 0 1 * *

# Every 6 hours
0 */6 * * *

# Multiple times: 9 AM, 1 PM, 5 PM
0 9,13,17 * * *

# Every 5 minutes between 9 AM and 5 PM on weekdays
*/5 9-17 * * 1-5

# Last day of month at 11:59 PM (use code node to calculate)
59 23 28-31 * *
```

**Step 1.3: Test Schedule Trigger**
```javascript
// IMPORTANT: Schedule triggers don't execute when you click "Execute workflow"
// They only execute at scheduled times or when workflow is first activated

Testing Method:
1. Save workflow
2. Toggle workflow to "Active"
3. Set schedule to "Every 1 minute" for testing
4. Wait 1 minute
5. Check "Executions" tab for automatic execution
6. Change back to desired schedule when testing complete
```

#### Real-World Schedule Examples

**Example 1: Daily Sales Report**
```
Workflow: Daily Sales Email Report
Trigger: Schedule Trigger
  - Expression: 0 9 * * 1-5 (Weekdays at 9 AM)
  - Timezone: America/New_York

Flow:
1. Schedule Trigger
2. HTTP Request → Fetch yesterday's sales data
3. Code Node → Calculate totals, averages
4. Gmail → Send formatted report to team
```

**Example 2: Social Media Queue Processor**
```
Workflow: Post Scheduled Content
Trigger: Schedule Trigger
  - Expression: 0 8,12,17 * * * (3 times daily)

Flow:
1. Schedule Trigger
2. Google Sheets → Get next post from content calendar
3. IF Node → Check if post is scheduled for now
4. LinkedIn/Twitter/Facebook → Post content
5. Google Sheets → Mark post as published
```

**Example 3: Database Cleanup**
```
Workflow: Delete Old Records
Trigger: Schedule Trigger
  - Expression: 0 2 * * 0 (Sundays at 2 AM)

Flow:
1. Schedule Trigger
2. HTTP Request → Database API
3. Code Node → Filter records older than 90 days
4. HTTP Request → Delete old records
5. Slack → Send deletion summary to admin channel
```

**Schedule Trigger Best Practices:**

1. **Timezone Awareness**
```javascript
// CRITICAL: Set TZ environment variable in N8N
// Railway: Add TZ variable (see setup_n8n_self_hosted.md)
TZ=America/New_York
TZ=Europe/London
TZ=Australia/Sydney

// Verify timezone in workflow:
{{ $now.toFormat('yyyy-MM-dd HH:mm:ss ZZZZ') }}
```

2. **Avoid Peak Hours**
```yaml
Bad: 0 0 * * * (Midnight - when many crons run)
Good: 0 3 * * * (3 AM - off-peak)

Bad: 0 9,12,15,18 * * * (On the hour)
Good: 15 9,12,15,18 * * * (15 minutes past)
```

3. **Error Handling**
```
Always add error handling to scheduled workflows:
1. Set error workflow (see setup_n8n_error_handling.md)
2. Add Slack/Email notification on failure
3. Log execution results for audit trail
```

4. **Prevent Overlapping Executions**
```javascript
// For long-running scheduled workflows:
// Add execution time check at start

// Code Node at beginning:
const lastExecution = $('Get Last Execution Time').first().json.timestamp;
const now = Date.now();
const timeSinceLastRun = now - lastExecution;

// If less than 50 minutes (for hourly job), skip
if (timeSinceLastRun < 50 * 60 * 1000) {
  throw new Error('Previous execution still running or too recent');
}

return [{ json: { timestamp: now } }];
```

---

## Phase 2: Webhook Triggers (30 minutes)

### Understanding Webhooks

**What is a Webhook?**
A webhook is a user-defined HTTP callback. When an event occurs in an external system, it sends an HTTP request to your N8N webhook URL, triggering your workflow.

**Use Cases:**
- Form submissions from websites
- Payment notifications (Stripe, PayPal)
- CRM updates (new lead, status change)
- GitHub events (push, pull request)
- Third-party service integrations
- Custom application events

### Basic Webhook Setup

**Step 2.1: Add Webhook Trigger**
1. Create new workflow
2. Search "Webhook"
3. Select "Webhook" trigger node

**Step 2.2: Configure Webhook**

```yaml
HTTP Method: POST
Path: contact-form
Authentication: None (for public webhooks)
Respond: Immediately
Response Code: 200
Response Mode: Last Node
```

**Understanding Configuration:**

**HTTP Methods:**
- **GET** - Retrieve data (query parameters in URL)
- **POST** - Submit data (JSON/form data in body)
- **PUT** - Update existing resource
- **DELETE** - Remove resource
- **PATCH** - Partial update

**Path:**
```
Custom path for your webhook
Examples:
  - contact-form
  - stripe-payment
  - new-lead
  - github-push

Results in URL:
https://your-domain.up.railway.app/webhook/contact-form
```

**Authentication Options:**

**Option 1: None (Public)**
```yaml
Authentication: None
Use Case: Public forms, publicly accessible endpoints
Security: Validate data in workflow, not production-ready for sensitive data
```

**Option 2: Basic Auth**
```yaml
Authentication: Basic Auth
User: webhook_user
Password: your-secure-password-here

Use Case: Simple protection, partner integrations
Security Level: Medium
```

**Option 3: Header Auth**
```yaml
Authentication: Header Auth
Name: X-API-Key
Value: your-secret-api-key-here

Use Case: API integrations, service-to-service
Security Level: Medium-High

Usage:
curl -X POST https://your-n8n.com/webhook/endpoint \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"data": "value"}'
```

**Option 4: Token Auth (Custom Implementation)**
```javascript
// Add Code node after webhook to validate token
const receivedToken = $json.headers['authorization']?.replace('Bearer ', '');
const validToken = $env.WEBHOOK_SECRET_TOKEN;

if (receivedToken !== validToken) {
  throw new Error('Invalid authentication token');
}

return $input.all();
```

**Step 2.3: Get Webhook URL**
1. After adding webhook trigger, save workflow
2. Toggle workflow to "Active"
3. Webhook URL appears in node:
```
Production URL:
https://your-domain.up.railway.app/webhook/contact-form

Test URL (visible when workflow inactive):
https://your-domain.up.railway.app/webhook-test/contact-form
```

**CRITICAL:** Test URL only works when workflow is INACTIVE. Production URL only works when workflow is ACTIVE.

### Testing Webhooks

**Method 1: Using curl (Command Line)**
```bash
# Test POST request with JSON data
curl -X POST https://your-n8n.com/webhook/contact-form \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Test message"
  }'

# Expected response:
{"success": true}

# Test with authentication
curl -X POST https://your-n8n.com/webhook/protected \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"data": "value"}'

# Test GET request with query parameters
curl -X GET "https://your-n8n.com/webhook/test?name=John&email=test@example.com"
```

**Method 2: Using Postman/Insomnia**
```
1. Open Postman
2. Create new request
3. Method: POST
4. URL: https://your-n8n.com/webhook/contact-form
5. Headers:
   Content-Type: application/json
6. Body → Raw → JSON:
   {
     "name": "Test User",
     "email": "test@example.com",
     "message": "Hello from Postman"
   }
7. Click Send
8. Check N8N execution history
```

**Method 3: HTML Form Testing**
```html
<!DOCTYPE html>
<html>
<body>
  <form id="testForm">
    <input name="name" placeholder="Name" required>
    <input name="email" type="email" placeholder="Email" required>
    <textarea name="message" placeholder="Message"></textarea>
    <button type="submit">Submit</button>
  </form>

  <script>
    document.getElementById('testForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const data = Object.fromEntries(formData);

      const response = await fetch('https://your-n8n.com/webhook/contact-form', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();
      alert('Form submitted! ' + JSON.stringify(result));
    });
  </script>
</body>
</html>
```

### Webhook Response Configuration

**Understanding Response Modes:**

**Mode 1: Immediately**
```yaml
Respond: Immediately
Response Code: 200
Response Data: Using 'Respond to Webhook' Node

Use Case: When workflow is fast (<3 seconds)
Behavior: Sends response immediately, workflow continues in background
```

**Mode 2: When Last Node Finishes**
```yaml
Respond: When Last Node Finishes
Response Mode: Last Node

Use Case: When you want to return processed data
Behavior: Waits for entire workflow to complete before responding
Warning: If workflow takes >30 seconds, requester may timeout
```

**Mode 3: Using Expression**
```yaml
Respond: Using 'Respond to Webhook' Node
Place node anywhere in workflow

Configuration in 'Respond to Webhook' node:
Response Code: 200
Response Body:
  {
    "success": true,
    "message": "Data received and processing started",
    "id": "{{ $json.submissionId }}"
  }
```

### Real-World Webhook Examples

**Example 1: Contact Form Submission**
```
Workflow: Website Contact Form Handler

1. Webhook Trigger
   - Method: POST
   - Path: contact-form
   - Auth: None (public form)

2. Set Node (Validate & Format Data)
   - fullName: {{ $json.body.name }}
   - email: {{ $json.body.email }}
   - message: {{ $json.body.message }}
   - submittedAt: {{ $now.toISO() }}
   - ip: {{ $json.headers['x-forwarded-for'] }}

3. IF Node (Validate Email)
   - Condition: {{ $json.email.includes('@') && $json.email.includes('.') }}
   - True → Continue
   - False → Respond with error

4. Google Sheets (Append Row)
   - Spreadsheet: Contact Form Submissions
   - Data: Map from Set node

5. Gmail (Send to Team)
   - To: team@company.com
   - Subject: New Contact Form: {{ $json.fullName }}
   - Body: [Details]

6. Gmail (Auto-reply to Submitter)
   - To: {{ $json.email }}
   - Subject: Thanks for contacting us!
   - Body: We received your message and will respond within 24 hours.

7. Respond to Webhook
   - Response Code: 200
   - Body:
     {
       "success": true,
       "message": "Thank you! We'll be in touch soon."
     }

Error Handling:
- On false email validation:
  Respond to Webhook:
    Response Code: 400
    Body: {"success": false, "error": "Invalid email address"}
```

**Example 2: Stripe Payment Webhook**
```
Workflow: Process Stripe Payment Events

1. Webhook Trigger
   - Method: POST
   - Path: stripe-payment
   - Auth: Header Auth (X-Stripe-Signature)

2. Code Node (Verify Stripe Signature)
   ```javascript
   const crypto = require('crypto');
   const signature = $json.headers['stripe-signature'];
   const payload = $json.body;
   const secret = $env.STRIPE_WEBHOOK_SECRET;

   // Stripe signature verification logic
   const expectedSignature = crypto
     .createHmac('sha256', secret)
     .update(JSON.stringify(payload))
     .digest('hex');

   if (signature !== expectedSignature) {
     throw new Error('Invalid Stripe signature');
   }

   return [{ json: payload }];
   ```

3. Switch Node (Route by Event Type)
   - payment_intent.succeeded → Process Successful Payment
   - payment_intent.failed → Handle Failed Payment
   - customer.subscription.created → New Subscription
   - customer.subscription.deleted → Cancelled Subscription

4a. Process Successful Payment Branch:
   - HTTP Request → Update order status in database
   - Gmail → Send receipt to customer
   - Slack → Notify sales team

4b. Handle Failed Payment Branch:
   - Gmail → Send payment failed notice to customer
   - HTTP Request → Mark order as payment pending
   - Slack → Alert finance team

5. Respond to Webhook
   - Response Code: 200
   - Body: {"received": true}
```

**Example 3: GitHub Webhook (Push Event)**
```
Workflow: Auto-Deploy on Git Push

1. Webhook Trigger
   - Method: POST
   - Path: github-push
   - Auth: Header Auth (X-Hub-Signature-256)

2. Code Node (Verify GitHub Signature)
   ```javascript
   const crypto = require('crypto');
   const signature = $json.headers['x-hub-signature-256'];
   const payload = JSON.stringify($json.body);
   const secret = $env.GITHUB_WEBHOOK_SECRET;

   const hash = 'sha256=' + crypto
     .createHmac('sha256', secret)
     .update(payload)
     .digest('hex');

   if (signature !== hash) {
     throw new Error('Invalid GitHub signature');
   }

   return [{
     json: {
       repo: $json.body.repository.name,
       branch: $json.body.ref.split('/').pop(),
       author: $json.body.pusher.name,
       commits: $json.body.commits.length
     }
   }];
   ```

3. IF Node (Check Branch)
   - Condition: {{ $json.branch === 'main' }}
   - True → Deploy
   - False → Notify only

4. HTTP Request (Trigger Deployment)
   - URL: https://api.railway.app/deploy
   - Method: POST
   - Headers: Authorization: Bearer {{ $env.RAILWAY_API_TOKEN }}

5. Slack (Deployment Notice)
   - Channel: #deployments
   - Message:
     "Deployment started for {{ $json.repo }}
     Branch: {{ $json.branch }}
     Author: {{ $json.author }}
     Commits: {{ $json.commits }}"

6. Respond to Webhook
   - Response Code: 200
   - Body: {"status": "deployment_triggered"}
```

### Webhook Security Best Practices

**1. Always Validate Signatures for Payment/Critical Webhooks**
```javascript
// Template for webhook signature validation
const receivedSignature = $json.headers['x-signature-header'];
const payload = JSON.stringify($json.body);
const secret = $env.WEBHOOK_SECRET;

const expectedSignature = crypto
  .createHmac('sha256', secret)
  .update(payload)
  .digest('hex');

if (receivedSignature !== expectedSignature) {
  throw new Error('Invalid webhook signature - possible security threat');
}
```

**2. Rate Limiting (Using Code Node)**
```javascript
// Simple rate limiting implementation
const redis = require('redis'); // If available
const ip = $json.headers['x-forwarded-for'] || $json.headers['x-real-ip'];
const key = `ratelimit:${ip}`;

// Check request count (pseudo-code - implement with database/redis)
const requestCount = await getRequestCount(key);

if (requestCount > 100) { // 100 requests per hour
  throw new Error('Rate limit exceeded');
}

await incrementRequestCount(key);
return $input.all();
```

**3. Input Validation**
```javascript
// Always validate expected data structure
const requiredFields = ['email', 'name', 'message'];
const data = $json.body;

for (const field of requiredFields) {
  if (!data[field] || data[field].trim() === '') {
    throw new Error(`Missing required field: ${field}`);
  }
}

// Validate email format
if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
  throw new Error('Invalid email format');
}

// Sanitize inputs
const sanitized = {
  email: data.email.toLowerCase().trim(),
  name: data.name.trim().substring(0, 100),
  message: data.message.trim().substring(0, 1000)
};

return [{ json: sanitized }];
```

**4. IP Whitelisting (For Partner Integrations)**
```javascript
// Code node at start of workflow
const allowedIPs = [
  '192.168.1.100',
  '10.0.0.50',
  // Add partner IPs
];

const clientIP = $json.headers['x-forwarded-for'] || $json.headers['x-real-ip'];

if (!allowedIPs.includes(clientIP)) {
  throw new Error(`Unauthorized IP: ${clientIP}`);
}

return $input.all();
```

---

## Phase 3: Platform-Specific Triggers (25 minutes)

### Telegram Trigger - Chatbot & Messaging

**Use Cases:**
- Customer support bots
- Internal team notifications and commands
- Content idea capture (send message → create LinkedIn post)
- Personal automation triggers
- Alert acknowledgment systems

#### Setup Telegram Trigger

**Step 3.1: Create Telegram Bot**

1. Open Telegram app
2. Search for "BotFather" (official Telegram bot)
3. Start chat and send `/newbot`
4. Follow prompts:
```
BotFather: Alright, a new bot. How are we going to call it?
You: My N8N Bot

BotFather: Good. Now let's choose a username for your bot.
You: my_n8n_bot (must end in 'bot')

BotFather: Done! Your token is: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

5. SAVE THIS TOKEN - you'll need it for N8N

**Step 3.2: Configure N8N Telegram Trigger**

1. Add node: Search "Telegram Trigger"
2. Create new credential:
```yaml
Access Token: [Paste token from BotFather]
Base URL: https://api.telegram.org (default, don't change)
```
3. Save credential

**Step 3.3: Configure Trigger Settings**

```yaml
Updates: Message
Additional Fields:
  ├── Download Images: Yes (if you need to process images)
  └── Download Videos: Yes (if you need to process videos)
```

**Step 3.4: Activate & Test**

1. Save workflow
2. Toggle to "Active"
3. Open Telegram bot (click link from BotFather or search bot username)
4. Click "Start"
5. Send test message: "Hello Bot!"
6. Check N8N Executions - should see new execution triggered

#### Telegram Trigger Examples

**Example 1: Simple Echo Bot**
```
Workflow: Echo Bot

1. Telegram Trigger
   - Updates: Message

2. Telegram Node (Send Message)
   - Resource: Message
   - Operation: Send Message
   - Chat ID: {{ $json.message.chat.id }}
   - Text: You said: {{ $json.message.text }}
```

**Example 2: AI-Powered LinkedIn Post Generator**
```
Workflow: Telegram → LinkedIn Post Creator

1. Telegram Trigger
   - Updates: Message

2. Code Node (Extract Idea)
   ```javascript
   return [{
     json: {
       chatId: $json.message.chat.id,
       userId: $json.message.from.id,
       userName: $json.message.from.first_name,
       idea: $json.message.text,
       timestamp: new Date().toISOString()
     }
   }];
   ```

3. AI Agent (OpenAI) - Generate Post
   - System Message: "You are a LinkedIn content expert..."
   - User Message: "Create a LinkedIn post about: {{ $json.idea }}"

4. Google Docs (Create Draft)
   - Title: "LinkedIn Post - {{ $json.idea }}"
   - Content: {{ $json.aiResponse }}

5. Telegram (Send Approval Request)
   - Chat ID: {{ $json.chatId }}
   - Text: "Post created! Preview: {{ $json.aiResponse.substring(0, 200) }}..."
   - Reply Markup:
     {
       "inline_keyboard": [[
         {"text": "✅ Approve", "callback_data": "approve"},
         {"text": "❌ Reject", "callback_data": "reject"}
       ]]
     }

6. Wait for Telegram Callback

7. Switch Node (Handle Response)
   - approve → Post to LinkedIn
   - reject → Archive draft

8. LinkedIn Node (Post)
   - Text: {{ $('AI Agent').item.json.aiResponse }}

9. Telegram (Confirmation)
   - Chat ID: {{ $json.chatId }}
   - Text: "✅ Posted to LinkedIn!"
```

**Example 3: Team Command Bot**
```
Workflow: Admin Commands Bot

1. Telegram Trigger
   - Updates: Message

2. Code Node (Parse Command)
   ```javascript
   const message = $json.message.text;
   const chatId = $json.message.chat.id;
   const userId = $json.message.from.id;

   // Authorized admin user IDs
   const adminUsers = [123456789, 987654321];

   if (!adminUsers.includes(userId)) {
     return [{
       json: {
         authorized: false,
         chatId,
         response: 'Sorry, you are not authorized to use this bot.'
       }
     }];
   }

   // Parse command
   const [command, ...args] = message.trim().split(' ');

   return [{
     json: {
       authorized: true,
       chatId,
       command: command.toLowerCase(),
       args: args,
       userId
     }
   }];
   ```

3. Switch Node (Route by Command)
   - /status → System Status Check
   - /deploy → Trigger Deployment
   - /report → Generate Report
   - /backup → Start Backup Process
   - default → Unknown Command

4a. Status Branch:
   - HTTP Request → Health check endpoint
   - Telegram → Send status report

4b. Deploy Branch:
   - HTTP Request → Railway deployment API
   - Telegram → Deployment started message

4c. Report Branch:
   - Google Sheets → Fetch data
   - Code Node → Generate summary
   - Telegram → Send report with file

4d. Unknown Command:
   - Telegram → Send help message with available commands
```

**Telegram Button Interactions:**

```javascript
// Creating inline keyboard with buttons
{
  "inline_keyboard": [
    [
      {"text": "Option 1", "callback_data": "opt1"},
      {"text": "Option 2", "callback_data": "opt2"}
    ],
    [
      {"text": "Cancel", "callback_data": "cancel"}
    ]
  ]
}

// Handling button responses - use Telegram Trigger with:
// Updates: Callback Query
```

### Email Trigger (IMAP) - Email Automation

**Use Cases:**
- Auto-reply to support emails
- Parse order confirmations
- Process attachments (invoices, documents)
- Email-to-task systems
- Newsletter processing

#### Setup Email Trigger

**Step 3.1: Add IMAP Email Trigger**
1. Add node: Search "Email Trigger (IMAP)"
2. Create credential

**For Gmail:**
```yaml
Authentication: Password
User: your-email@gmail.com
Password: [App Password - NOT regular password]
Host: imap.gmail.com
Port: 993
Security: SSL/TLS
```

**Getting Gmail App Password:**
1. Go to Google Account settings
2. Security → 2-Step Verification (must be enabled)
3. App Passwords → Generate new password
4. Select "Mail" and device type
5. Copy generated password (16 characters)
6. Use this password in N8N credential

**For Other Providers:**
```yaml
# Outlook/Office365
Host: outlook.office365.com
Port: 993

# Yahoo
Host: imap.mail.yahoo.com
Port: 993

# Custom IMAP Server
Host: mail.yourdomain.com
Port: 993
```

**Step 3.2: Configure Trigger Settings**

```yaml
Mailbox: INBOX
Action: Mark as Read
Check Interval: 5 (minutes)

Options:
  ├── Download Attachments: Yes (if needed)
  ├── Force Reconnect: 60 (minutes)
  └── Simple: Yes (for easier data access)
```

#### Email Trigger Examples

**Example 1: Auto-Respond to Support Emails**
```
Workflow: Support Email Auto-Reply

1. Email Trigger (IMAP)
   - Mailbox: support@company.com
   - Action: Mark as Read
   - Interval: 5 minutes

2. IF Node (Check for "urgent" in subject)
   - Condition: {{ $json.subject.toLowerCase().includes('urgent') }}

3a. Urgent Branch:
   - Slack → Notify support team immediately
   - Priority: High

3b. Normal Branch:
   - Continue to auto-reply

4. OpenAI Agent (Generate Response)
   - System: "You are a customer support agent..."
   - User:
     "Customer Email:
     From: {{ $json.from }}
     Subject: {{ $json.subject }}
     Body: {{ $json.text }}

     Generate a helpful, professional response."

5. Gmail (Send Reply)
   - To: {{ $json.from }}
   - Subject: Re: {{ $json.subject }}
   - Body: {{ $('OpenAI Agent').item.json.response }}
   - In-Reply-To: {{ $json.messageId }}

6. Google Sheets (Log Interaction)
   - Spreadsheet: Support Tickets
   - Append: [Email data + AI response]
```

**Example 2: Invoice Processing**
```
Workflow: Extract & Store Invoice Data

1. Email Trigger (IMAP)
   - Mailbox: invoices@company.com
   - Download Attachments: Yes

2. IF Node (Has PDF Attachment)
   - Condition: {{ $json.attachments.length > 0 }}

3. Loop Over Items (Process Each Attachment)

4. Switch Node (Check File Type)
   - PDF → Extract data
   - Other → Skip

5. HTTP Request (OCR API - Extract Text)
   - Service: OCR.space or Google Vision API
   - Upload PDF attachment

6. Code Node (Parse Invoice Data)
   ```javascript
   const text = $json.ocrResult;

   // Extract invoice details using regex
   const invoiceNumber = text.match(/Invoice #?:?\s*(\w+)/i)?.[1];
   const amount = text.match(/Total:?\s*\$?([\d,]+\.?\d*)/i)?.[1];
   const date = text.match(/Date:?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i)?.[1];
   const vendor = $json.from; // Email sender

   return [{
     json: {
       invoiceNumber,
       amount: parseFloat(amount?.replace(',', '') || 0),
       date,
       vendor,
       emailSubject: $('Email Trigger').item.json.subject,
       processedAt: new Date().toISOString()
     }
   }];
   ```

7. Google Sheets (Append Invoice Data)
   - Spreadsheet: Invoice Tracker
   - Map extracted data

8. Google Drive (Save PDF)
   - Folder: Invoices/{{ new Date().getFullYear() }}
   - File Name: {{ $json.invoiceNumber }}_{{ $json.vendor }}.pdf

9. Gmail (Confirmation Reply)
   - To: {{ $('Email Trigger').item.json.from }}
   - Subject: Invoice Processed: {{ $json.invoiceNumber }}
   - Body: Thank you! Your invoice has been received and processed.
```

---

## Phase 4: HTTP Request Node - API Integration (40 minutes)

### Understanding HTTP Requests

The HTTP Request node is the most powerful and versatile node in N8N. It allows you to connect to virtually any service with an API.

**Common Use Cases:**
- Call REST APIs
- Integrate with services without native N8N nodes
- Custom authentication flows
- Database operations via API
- Microservice communication

### Basic HTTP Request Configuration

**Step 4.1: Add HTTP Request Node**
1. Click "+" or search "HTTP Request"
2. Select "HTTP Request"

**Step 4.2: Configure Request**

```yaml
Method: POST
URL: https://api.example.com/endpoint

Authentication:
  Type: Generic Credential Type → API Key Auth

Headers:
  Content-Type: application/json

Body:
  Content Type: JSON
  JSON/RAW:
    {
      "key": "value",
      "data": "{{ $json.dynamicField }}"
    }
```

### HTTP Methods Explained

**GET - Retrieve Data**
```yaml
Method: GET
URL: https://api.example.com/users/123
Use Case: Fetch user data, retrieve records

No Body (data in URL parameters)
```

**POST - Create New Resource**
```yaml
Method: POST
URL: https://api.example.com/users
Body:
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
Use Case: Create new user, submit form data
```

**PUT - Replace Entire Resource**
```yaml
Method: PUT
URL: https://api.example.com/users/123
Body:
  {
    "name": "John Updated",
    "email": "john@example.com",
    "status": "active"
  }
Use Case: Complete update of existing record
```

**PATCH - Partial Update**
```yaml
Method: PATCH
URL: https://api.example.com/users/123
Body:
  {
    "status": "inactive"
  }
Use Case: Update only specific fields
```

**DELETE - Remove Resource**
```yaml
Method: DELETE
URL: https://api.example.com/users/123
Use Case: Delete record
```

### Authentication Methods

#### Method 1: API Key (Header)

**Most Common Method**

```yaml
Authentication: Header Auth
Name: X-API-Key
Value: your-api-key-here

Or using credentials:
Authentication: Generic Credential Type → API Key Auth
API Key: your-api-key
Add To: Header
Key: X-API-Key
```

**Example: OpenAI API**
```yaml
Method: POST
URL: https://api.openai.com/v1/chat/completions
Authentication: Header Auth
  Name: Authorization
  Value: Bearer sk-your-openai-api-key

Headers:
  Content-Type: application/json

Body:
  {
    "model": "gpt-4",
    "messages": [
      {
        "role": "user",
        "content": "{{ $json.userMessage }}"
      }
    ]
  }
```

#### Method 2: Basic Auth

**Username + Password**

```yaml
Authentication: Basic Auth
User: api_user
Password: api_password
```

**How it works:**
```
Encoded as Base64: username:password
Sent in header: Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Example: Simple API**
```yaml
Method: GET
URL: https://api.example.com/protected-data
Authentication: Basic Auth
  User: my_username
  Password: my_secure_password
```

#### Method 3: OAuth2

**For Google, Facebook, LinkedIn, etc.**

**Step-by-Step OAuth Setup:**

1. Create OAuth credential in N8N credentials section
2. Get Client ID and Client Secret from service
3. Configure redirect URL
4. Authorize account

**Example: Google Sheets API**
```yaml
Authentication: OAuth2
Grant Type: Authorization Code
Authorization URL: https://accounts.google.com/o/oauth2/v2/auth
Access Token URL: https://oauth2.googleapis.com/token
Client ID: [From Google Cloud Console]
Client Secret: [From Google Cloud Console]
Scope: https://www.googleapis.com/auth/spreadsheets
```

**Using OAuth in HTTP Request:**
```yaml
Method: GET
URL: https://sheets.googleapis.com/v4/spreadsheets/SHEET_ID/values/Sheet1
Authentication: Predefined Credential Type → Google OAuth2 API
```

#### Method 4: Bearer Token

**Common for JWT Authentication**

```yaml
Authentication: Generic Credential Type → Header Auth
Name: Authorization
Value: Bearer {{ $json.accessToken }}
```

**Example: Custom API with JWT**
```yaml
# Step 1: Login to get token
Method: POST
URL: https://api.example.com/auth/login
Body:
  {
    "username": "{{ $env.API_USERNAME }}",
    "password": "{{ $env.API_PASSWORD }}"
  }

# Extract token from response
# Next HTTP Request node:
Method: GET
URL: https://api.example.com/user/profile
Headers:
  Authorization: Bearer {{ $('Login').item.json.accessToken }}
```

#### Method 5: Query Parameters (API Key in URL)

```yaml
Method: GET
URL: https://api.example.com/data

Query Parameters:
  api_key: your-api-key-here
  format: json

Results in: https://api.example.com/data?api_key=your-api-key-here&format=json
```

### Working with API Responses

**Parsing JSON Responses:**
```javascript
// Code node after HTTP Request
const response = $json;

// Access nested data
const userData = response.data.user;
const items = response.results.map(item => ({
  id: item.id,
  name: item.name,
  status: item.status
}));

return items.map(item => ({ json: item }));
```

**Handling Pagination:**
```javascript
// Get all pages of results
let allItems = [];
let page = 1;
let hasMore = true;

while (hasMore) {
  const response = await fetch(
    `https://api.example.com/items?page=${page}&limit=100`,
    {
      headers: { 'Authorization': `Bearer ${$env.API_TOKEN}` }
    }
  );

  const data = await response.json();
  allItems = allItems.concat(data.items);

  hasMore = data.pagination.hasNext;
  page++;
}

return allItems.map(item => ({ json: item }));
```

### Real-World HTTP Request Examples

**Example 1: Notion Database Integration**
```
Workflow: Add Task to Notion

1. Webhook Trigger
   - Receives task data

2. HTTP Request (Create Notion Page)
   - Method: POST
   - URL: https://api.notion.com/v1/pages
   - Authentication: Bearer Token
   - Headers:
     Authorization: Bearer {{ $env.NOTION_API_KEY }}
     Notion-Version: 2022-06-28
     Content-Type: application/json
   - Body:
     {
       "parent": { "database_id": "{{ $env.NOTION_DATABASE_ID }}" },
       "properties": {
         "Name": {
           "title": [
             {
               "text": {
                 "content": "{{ $json.taskName }}"
               }
             }
           ]
         },
         "Status": {
           "select": {
             "name": "To Do"
           }
         },
         "Due Date": {
           "date": {
             "start": "{{ $json.dueDate }}"
           }
         }
       }
     }

3. Respond to Webhook
   - Body: {"success": true, "notionPageId": "{{ $json.id }}"}
```

**Example 2: Airtable Integration**
```
Workflow: Sync Google Sheets to Airtable

1. Schedule Trigger
   - Cron: 0 */6 * * * (every 6 hours)

2. Google Sheets (Read All Rows)
   - Spreadsheet: Sales Data
   - Sheet: Current Month

3. Code Node (Transform Data for Airtable)
   ```javascript
   const items = $input.all();

   const records = items.map(item => ({
     fields: {
       "Customer Name": item.json.customerName,
       "Amount": parseFloat(item.json.amount),
       "Date": item.json.date,
       "Status": item.json.status,
       "Product": item.json.product
     }
   }));

   // Airtable requires max 10 records per request
   const batches = [];
   for (let i = 0; i < records.length; i += 10) {
     batches.push(records.slice(i, i + 10));
   }

   return batches.map(batch => ({
     json: { records: batch }
   }));
   ```

4. Loop Over Items (Process Each Batch)

5. HTTP Request (Airtable Create Records)
   - Method: POST
   - URL: https://api.airtable.com/v0/{{ $env.AIRTABLE_BASE_ID }}/Sales
   - Headers:
     Authorization: Bearer {{ $env.AIRTABLE_API_KEY }}
     Content-Type: application/json
   - Body: {{ $json.records }}

6. Slack (Completion Notice)
   - Message: "Synced {{ $('Code Node').item.json.totalRecords }} records to Airtable"
```

**Example 3: OpenAI Content Generation**
```
Workflow: AI Content Writer

1. Manual Trigger (or Webhook)

2. HTTP Request (OpenAI API)
   - Method: POST
   - URL: https://api.openai.com/v1/chat/completions
   - Headers:
     Authorization: Bearer {{ $env.OPENAI_API_KEY }}
     Content-Type: application/json
   - Body:
     {
       "model": "gpt-4",
       "messages": [
         {
           "role": "system",
           "content": "You are an expert blog writer."
         },
         {
           "role": "user",
           "content": "Write a 500-word blog post about: {{ $json.topic }}"
         }
       ],
       "temperature": 0.7,
       "max_tokens": 1000
     }

3. Set Node (Extract Content)
   - generatedContent: {{ $json.choices[0].message.content }}
   - topic: {{ $('Manual Trigger').item.json.topic }}
   - wordCount: {{ $json.choices[0].message.content.split(' ').length }}
   - timestamp: {{ $now.toISO() }}

4. Google Docs (Create Document)
   - Title: {{ $json.topic }} - {{ $now.toFormat('yyyy-MM-dd') }}
   - Content: {{ $json.generatedContent }}

5. Slack (Notification)
   - Message: "New blog post created: {{ $json.topic }}"
```

### Error Handling for HTTP Requests

**Method 1: Continue on Fail**
```yaml
HTTP Request Node Settings:
  Continue on Fail: Yes (toggle on)

Behavior: Node won't stop workflow on error
Use: When you want to handle errors gracefully

Check for errors in next node:
IF Node:
  Condition: {{ $json.error === undefined }}
  True → Success path
  False → Error handling path
```

**Method 2: Retry on Fail**
```yaml
HTTP Request Node Settings:
  Options → Add Option → Retry on Fail
  Max Tries: 3
  Wait Between Tries: 1000 (ms)

Use Case: Temporary network issues, rate limits
```

**Method 3: Custom Error Handling**
```javascript
// Code node after HTTP Request
try {
  const response = $input.first().json;

  // Check for API-specific error codes
  if (response.status === 'error') {
    throw new Error(`API Error: ${response.message}`);
  }

  if (response.code === 429) {
    throw new Error('Rate limit exceeded - wait and retry');
  }

  return [{ json: response }];

} catch (error) {
  // Log error and return formatted error object
  return [{
    json: {
      error: true,
      message: error.message,
      timestamp: new Date().toISOString(),
      originalData: $input.first().json
    }
  }];
}
```

---

## Phase 5: AI Agents in N8N (45 minutes)

### Understanding AI Agents

AI agents in N8N are nodes that use language models (like GPT-4) to make intelligent decisions, generate content, or process data. They can call tools, make decisions, and chain multiple operations.

**Key Concepts:**
- **Agent**: Orchestrator that decides which tools to use
- **Tools**: Functions the agent can call (HTTP requests, database queries, etc.)
- **System Message**: Instructions for how the agent should behave
- **User Message**: The specific request or input

### AI Agent Types in N8N

**1. Tools Agent** (Most Common)
- Can use multiple tools
- Makes decisions about which tool to use
- Iterative: Can call multiple tools in sequence

**2. Conversational Agent**
- Maintains conversation context
- Good for chatbots
- Can remember previous messages

**3. OpenAI Functions Agent**
- Uses OpenAI's function calling
- Structured outputs
- Best for API integrations

### Setting Up Basic AI Agent

**Step 5.1: Prerequisites**
```
Required:
- OpenAI API Key (get from platform.openai.com)
- Or: Anthropic API Key for Claude
- Or: Other LLM API access

Add API key to N8N:
1. Credentials → Add Credential
2. Search "OpenAI"
3. Paste API key
4. Save
```

**Step 5.2: Add AI Agent Node**
1. Search "AI Agent"
2. Select "AI Agent" node
3. Select agent type: "Tools Agent"

**Step 5.3: Configure Agent**

```yaml
Agent Type: Tools Agent

Chat Model:
  Model: OpenAI Chat Model
  Model: gpt-4 (or gpt-3.5-turbo for speed/cost)
  Credential: [Select saved OpenAI credential]

Text:
  Use as System Message
  Message:
    "You are a helpful assistant that helps users create LinkedIn posts.
    Write engaging, professional content.
    Keep posts between 100-150 words.
    Use relevant hashtags.
    Maintain a friendly yet professional tone."

Prompt:
  Type: Define below
  Text: "Create a LinkedIn post about: {{ $json.topic }}"
```

### Simple AI Agent Example

**Example 1: Content Generator**
```
Workflow: AI Blog Title Generator

1. Manual Trigger (with test data)
   {"keyword": "productivity tips", "targetAudience": "remote workers"}

2. AI Agent
   - Agent Type: Tools Agent
   - Model: GPT-4
   - System Message:
     "You are an expert content strategist.
     Generate compelling blog titles that:
     - Include the provided keyword
     - Appeal to the target audience
     - Are 50-70 characters long
     - Use power words
     - Are SEO-friendly"

   - User Message:
     "Generate 5 blog title options.
     Keyword: {{ $json.keyword }}
     Target Audience: {{ $json.targetAudience }}"

3. Code Node (Parse Titles)
   ```javascript
   const response = $json.output;

   // Extract titles (assuming AI returns numbered list)
   const titles = response
     .split('\n')
     .filter(line => line.match(/^\d+\./))
     .map(line => line.replace(/^\d+\.\s*/, '').trim());

   return titles.map((title, index) => ({
     json: {
       title,
       position: index + 1,
       keyword: $('Manual Trigger').item.json.keyword,
       length: title.length
     }
   }));
   ```

4. Google Sheets (Save Options)
   - Append each title option to sheet for review
```

### AI Agent with Tools

Tools allow the agent to take actions, not just generate text.

**Example 2: AI Research Assistant**
```
Workflow: AI-Powered Fact Checker

1. Telegram Trigger
   - User sends claim to verify

2. AI Agent (Tools Agent)
   - System Message:
     "You are a fact-checking assistant.
     Search the web for information about claims.
     Provide sources and assess credibility.
     Be objective and cite your sources."

   - User Message: "Verify this claim: {{ $json.message.text }}"

   - Tools:
     → Connected to HTTP Request node (web search)
     → Connected to Code node (parse results)

3. HTTP Request Tool (Web Search)
   - Method: GET
   - URL: https://api.serpapi.com/search
   - Params:
     q: {{ $json.query }}
     api_key: {{ $env.SERPAPI_KEY }}

   Returns: Search results with sources

4. Code Node Tool (Analyze Results)
   ```javascript
   const results = $json.results;

   // Extract relevant information
   const facts = results.map(result => ({
     title: result.title,
     snippet: result.snippet,
     source: result.source,
     url: result.link
   }));

   return [{ json: { facts } }];
   ```

5. AI Agent processes tool results and formulates answer

6. Telegram (Send Response)
   - Chat ID: {{ $('Telegram Trigger').item.json.message.chat.id }}
   - Text: {{ $('AI Agent').item.json.output }}
   - Parse Mode: Markdown (for formatted response)
```

### Advanced AI Agent Patterns

**Pattern 1: Multi-Step AI Workflow**
```
Use multiple AI agents in sequence, each specialized:

1. AI Agent 1: Research & Outline
   - Input: Topic
   - Output: Detailed outline with key points

2. AI Agent 2: Content Writing
   - Input: Outline from Agent 1
   - Output: Full draft content

3. AI Agent 3: Editing & Polish
   - Input: Draft from Agent 2
   - Output: Final polished content

4. AI Agent 4: SEO Optimization
   - Input: Final content
   - Output: Meta description, title tag, keywords
```

**Implementation:**
```
Workflow: AI Content Production Pipeline

1. Webhook Trigger
   {"topic": "Remote Work Benefits", "targetLength": "1000 words"}

2. AI Agent (Researcher)
   - System: "You are a research assistant..."
   - User: "Research {{ $json.topic }} and create a detailed outline"
   - Output: Structured outline

3. AI Agent (Writer)
   - System: "You are a professional writer..."
   - User: "Write {{ $json.targetLength }} words based on this outline:
           {{ $('AI Agent (Researcher)').item.json.output }}"
   - Output: Draft article

4. AI Agent (Editor)
   - System: "You are an editor. Improve clarity, flow, and grammar..."
   - User: "Edit this article: {{ $('AI Agent (Writer)').item.json.output }}"
   - Output: Edited article

5. AI Agent (SEO Specialist)
   - System: "You are an SEO expert..."
   - User: "Generate SEO meta data for: {{ $('AI Agent (Editor)').item.json.output }}"
   - Output: SEO metadata

6. Code Node (Combine Results)
   ```javascript
   return [{
     json: {
       topic: $('Webhook').item.json.topic,
       outline: $('AI Agent (Researcher)').item.json.output,
       draft: $('AI Agent (Writer)').item.json.output,
       finalArticle: $('AI Agent (Editor)').item.json.output,
       seoTitle: $('AI Agent (SEO)').item.json.title,
       seoDescription: $('AI Agent (SEO)').item.json.description,
       keywords: $('AI Agent (SEO)').item.json.keywords,
       wordCount: $('AI Agent (Editor)').item.json.output.split(' ').length,
       createdAt: new Date().toISOString()
     }
   }];
   ```

7. Google Docs (Create Document)

8. WordPress (Publish - via HTTP Request)
```

**Pattern 2: AI Decision Router**
```
Use AI to intelligently route workflow based on content:

1. Email Trigger (Support Email)

2. AI Agent (Classifier)
   - System: "Classify the email intent into one of these categories:
              - bug_report
              - feature_request
              - billing_question
              - technical_support
              - general_inquiry

              Respond with just the category name."

   - User: "Classify this email:
            Subject: {{ $json.subject }}
            Body: {{ $json.text }}"

3. Switch Node
   - Route by AI classification
   - bug_report → Engineering Team
   - feature_request → Product Team
   - billing_question → Finance Team
   - technical_support → Support Team
   - general_inquiry → General Queue

4a-4e. Different handling for each category
```

**Pattern 3: AI Data Extraction**
```
Extract structured data from unstructured text:

1. Webhook Trigger (Receives invoice image or text)

2. HTTP Request (OCR if image)
   - Extract text from image

3. AI Agent (Data Extractor)
   - System: "You are a data extraction specialist.
              Extract the following information from invoices:
              - Invoice number
              - Date
              - Vendor name
              - Total amount
              - Line items with quantities and prices

              Respond in JSON format only."

   - User: "Extract data from: {{ $json.invoiceText }}"

4. Code Node (Parse JSON)
   ```javascript
   // AI should return JSON string
   let extracted;
   try {
     extracted = JSON.parse($json.output);
   } catch (e) {
     // If AI didn't return perfect JSON, try to extract it
     const jsonMatch = $json.output.match(/\{[\s\S]*\}/);
     extracted = JSON.parse(jsonMatch[0]);
   }

   return [{
     json: {
       invoiceNumber: extracted.invoiceNumber,
       date: extracted.date,
       vendor: extracted.vendor,
       totalAmount: parseFloat(extracted.totalAmount),
       lineItems: extracted.lineItems,
       extractedAt: new Date().toISOString()
     }
   }];
   ```

5. Google Sheets (Append Extracted Data)

6. QuickBooks API (Create Invoice - via HTTP Request)
```

### Real-World AI Agent Examples

**Example 3: LinkedIn Post Generator (Complete)**
```
Workflow: Telegram → AI LinkedIn Post → Google Docs → Approval → Post

1. Telegram Trigger
   - User sends idea via message

2. Set Node (Prepare Data)
   - chatId: {{ $json.message.chat.id }}
   - userId: {{ $json.message.from.id }}
   - userFirstName: {{ $json.message.from.first_name }}
   - postIdea: {{ $json.message.text }}
   - timestamp: {{ $now.toISO() }}

3. AI Agent (LinkedIn Post Writer)
   - Agent Type: Tools Agent
   - Model: GPT-4

   - System Message:
     "You are Lucas Nolan, a marketing automation expert.

     Writing Style:
     - First person perspective
     - Professional but conversational
     - Use short paragraphs (2-3 sentences)
     - Include practical insights
     - End with a question to encourage engagement

     Format Requirements:
     - 100-150 words
     - Include 3-5 relevant hashtags at end
     - Use line breaks for readability
     - No emojis unless specifically requested"

   - User Message:
     "Write a LinkedIn post about this topic: {{ $json.postIdea }}

     Context: This is for a professional audience interested in
     marketing automation, AI tools, and agency operations."

4. AI Agent (Title Generator)
   - System: "Generate a short, catchy title (5-7 words) for a LinkedIn post."
   - User: "Title for: {{ $('AI Agent').item.json.output }}"

5. Set Node (Combine Results)
   - title: {{ $('AI Agent (Title Generator)').item.json.output }}
   - content: {{ $('AI Agent (LinkedIn Post Writer)').item.json.output }}
   - postIdea: {{ $('Set Node').item.json.postIdea }}
   - chatId: {{ $('Set Node').item.json.chatId }}

6. Google Docs (Create Draft)
   - Document Title: {{ $json.title }}
   - Content:
     "Title: {{ $json.title }}

     Original Idea: {{ $json.postIdea }}
     Generated: {{ $now.toFormat('yyyy-MM-dd HH:mm') }}

     ---

     {{ $json.content }}"

7. Google Drive (Move to Folder)
   - File ID: {{ $json.documentId }}
   - Folder: LinkedIn Posts/Drafts

8. Telegram (Approval Request)
   - Chat ID: {{ $('Set Node').item.json.chatId }}
   - Text:
     "✅ LinkedIn post created!

     Title: {{ $json.title }}

     Preview:
     {{ $json.content.substring(0, 200) }}...

     Full post in Google Docs: {{ $json.documentUrl }}

     Do you want to post this to LinkedIn?"

   - Reply Markup:
     {
       "inline_keyboard": [[
         {"text": "✅ Yes, Post It", "callback_data": "approve:{{ $json.documentId }}"},
         {"text": "❌ No, Discard", "callback_data": "reject:{{ $json.documentId }}"}
       ]]
     }

9. Wait Node (Wait for Telegram Callback)
   - Resume On: Webhook (Telegram callback query)
   - Webhook URL: /telegram-callback
   - Timeout: 24 hours

10. Switch Node (Handle Response)
    - {{ $json.callback_query.data.startsWith('approve') }} → Approve Branch
    - {{ $json.callback_query.data.startsWith('reject') }} → Reject Branch

11a. Approve Branch:
    - HTTP Request → LinkedIn API (Post Content)
      Method: POST
      URL: https://api.linkedin.com/v2/ugcPosts
      Headers:
        Authorization: Bearer {{ $credentials.linkedInToken }}
      Body:
        {
          "author": "urn:li:person:{{ $env.LINKEDIN_PERSON_ID }}",
          "lifecycleState": "PUBLISHED",
          "specificContent": {
            "com.linkedin.ugc.ShareContent": {
              "shareCommentary": {
                "text": "{{ $('Set Node (Combine)').item.json.content }}"
              },
              "shareMediaCategory": "NONE"
            }
          },
          "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
          }
        }

    - Telegram (Success Notification)
      Chat ID: {{ $('Set Node').item.json.chatId }}
      Text: "🎉 Posted to LinkedIn! {{ $json.postUrl }}"

    - Google Drive (Move to Posted Folder)
      File ID: {{ $('Google Docs').item.json.documentId }}
      Folder: LinkedIn Posts/Posted

11b. Reject Branch:
    - Google Drive (Move to Rejected Folder)
      File ID: {{ $('Google Docs').item.json.documentId }}
      Folder: LinkedIn Posts/Rejected

    - Telegram (Confirmation)
      Chat ID: {{ $('Set Node').item.json.chatId }}
      Text: "Post discarded. Send me a new idea anytime!"
```

### AI Agent Best Practices

**1. Craft Specific System Messages**
```
❌ Bad:
"You are a helpful assistant."

✅ Good:
"You are a LinkedIn content expert specializing in B2B SaaS marketing.
Your writing style is:
- Professional yet approachable
- Data-driven with specific examples
- Action-oriented with clear takeaways
- Optimized for engagement (questions, hooks)

Constraints:
- Posts must be 100-150 words
- Include 3-5 relevant hashtags
- Use 2-3 line breaks for readability
- Avoid corporate jargon
- Write in first person"
```

**2. Provide Examples (Few-Shot Learning)**
```
System Message:
"You extract invoice data and return JSON.

Example Input:
'Invoice #12345
Date: 2024-01-15
Amount: $499.99
Vendor: Acme Corp'

Example Output:
{
  "invoiceNumber": "12345",
  "date": "2024-01-15",
  "amount": 499.99,
  "vendor": "Acme Corp"
}

Now extract from the provided invoice."
```

**3. Handle AI Errors Gracefully**
```javascript
// Code node after AI Agent
try {
  const aiOutput = $json.output;

  // Validate AI returned something
  if (!aiOutput || aiOutput.trim().length === 0) {
    throw new Error('AI returned empty response');
  }

  // Check for common AI error messages
  if (aiOutput.includes('I cannot') || aiOutput.includes('I apologize')) {
    throw new Error('AI refused the request');
  }

  return [{ json: { content: aiOutput, success: true } }];

} catch (error) {
  // Log and notify
  return [{
    json: {
      error: true,
      message: error.message,
      originalPrompt: $('AI Agent').item.json.prompt,
      timestamp: new Date().toISOString()
    }
  }];
}
```

**4. Cost Management**
```javascript
// Monitor token usage
const systemMessage = "Your system message here";
const userMessage = $json.userInput;

// Rough token estimate (1 token ≈ 4 characters)
const estimatedTokens = (systemMessage + userMessage).length / 4;

// GPT-4 pricing (as of 2024):
// Input: $0.03 per 1K tokens
// Output: $0.06 per 1K tokens

if (estimatedTokens > 4000) {
  // Consider using GPT-3.5-turbo instead
  // Or split into multiple smaller requests
  throw new Error('Prompt too large - optimize to reduce costs');
}

// Log for monitoring
console.log(`Estimated tokens: ${estimatedTokens}, Estimated cost: $${(estimatedTokens / 1000 * 0.03).toFixed(4)}`);
```

**5. Temperature and Model Selection**
```yaml
Creative Tasks (Content Writing):
  Model: gpt-4
  Temperature: 0.7-0.9
  Max Tokens: 500-1000

Factual/Structured Tasks (Data Extraction):
  Model: gpt-4
  Temperature: 0.1-0.3
  Max Tokens: 200-500

Cost-Effective (Simple Tasks):
  Model: gpt-3.5-turbo
  Temperature: 0.5
  Max Tokens: 300

Fast Response (Chatbots):
  Model: gpt-3.5-turbo
  Temperature: 0.7
  Max Tokens: 150
```

---

## Common Mistakes to Avoid

### Mistake 1: Not Activating Workflows
```
Problem: Schedule/Webhook triggers don't fire
Reason: Workflow is not toggled to "Active"

Solution:
1. Save workflow
2. Toggle switch to "Active" (top right)
3. Verify active workflows in workflow list (green dot)
```

### Mistake 2: Incorrect Webhook Testing
```
Problem: Testing webhook with workflow active or inactive at wrong times

Understanding:
- Test URL: Only works when workflow is INACTIVE
- Production URL: Only works when workflow is ACTIVE

Testing Process:
1. Keep workflow INACTIVE during development
2. Use Test URL for testing
3. Activate workflow for production
4. Use Production URL
```

### Mistake 3: Timezone Issues with Schedule Triggers
```
Problem: Workflow runs at wrong time

Solution:
1. Set TZ environment variable (Railway or server)
2. Verify timezone: {{ $now.toFormat('yyyy-MM-dd HH:mm:ss ZZZZ') }}
3. Test schedule trigger with 1-minute interval first
4. Check execution history for actual run times
```

### Mistake 4: Not Handling Rate Limits
```
Problem: API blocks requests due to too many calls

Solution:
1. Add Wait node between API calls
   - Wait Amount: 1000ms (1 second)

2. Use "Loop Over Items" node for API calls
   - Processes one item at a time

3. Implement retry with exponential backoff:
   HTTP Request Options:
   - Retry on Fail: Yes
   - Max Tries: 3
   - Wait Between Tries: Starts at 1000ms, doubles each time
```

### Mistake 5: Insecure Webhook Endpoints
```
Problem: Public webhooks with no authentication

Solutions:
1. Add authentication (Basic Auth, Header Auth)
2. Validate webhook signatures (Stripe, GitHub, etc.)
3. Implement IP whitelisting in Code node
4. Use Header Auth with secret token stored in environment variable

Never:
- Use no authentication for production webhooks handling sensitive data
- Store API keys directly in workflow (use credentials/env vars)
```

### Mistake 6: Poor AI Agent Prompts
```
❌ Bad Prompt:
"Write a post"

❌ Also Bad:
"You are helpful. Write a LinkedIn post about the topic."

✅ Good Prompt:
"You are [specific role with context].

Task: [Clear, specific instruction]

Requirements:
- [Specific constraint 1]
- [Specific constraint 2]
- [Specific constraint 3]

Style: [Tone, voice, perspective]

Example Output: [Show what you want]

Now generate for: {{ $json.topic }}"
```

### Mistake 7: Not Testing with Real Data
```
Problem: Workflow works with test data, fails in production

Solution:
1. Test with actual data samples
2. Test edge cases:
   - Empty strings
   - Null values
   - Very long strings
   - Special characters
   - Maximum data volumes

3. Add validation:
   ```javascript
   if (!$json.email || !$json.email.includes('@')) {
     throw new Error('Invalid email');
   }
   ```
```

### Mistake 8: Overlooking Error Handling
```
Problem: Workflow fails silently, no notification

Solution:
1. Set error workflow for all production workflows
2. Add Slack/Email notification on failure
3. Use "Continue on Fail" for non-critical nodes
4. Log errors to database/spreadsheet for audit trail
```

---

## Troubleshooting

### Issue 1: Telegram Trigger Not Receiving Messages
**Symptoms:** Sending messages to bot but workflow doesn't execute

**Solutions:**
1. Verify workflow is ACTIVE (toggle on)
2. Check bot token is correct (test in BotFather)
3. Send "/start" command to bot first
4. Check execution history - might be receiving but failing later
5. Verify webhook is not set elsewhere:
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo
   ```
6. Clear webhook if set:
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/deleteWebhook
   ```

### Issue 2: Schedule Trigger Not Running
**Symptoms:** Workflow should run automatically but doesn't

**Solutions:**
1. Verify workflow is ACTIVE
2. Check cron expression is valid (use crontab.guru)
3. Verify timezone setting (TZ environment variable)
4. Test with "Every 1 minute" first
5. Check Railway/server isn't restarting during schedule time
6. View execution history for error messages
7. Ensure no infinite execution prevention is blocking

### Issue 3: HTTP Request Authentication Fails
**Symptoms:** 401 Unauthorized or 403 Forbidden

**Solutions:**
1. Verify API key/token is correct
2. Check authentication method matches API docs:
   - Header Auth: Header name matters (X-API-Key vs api-key)
   - Bearer token needs "Bearer " prefix
   - Basic Auth needs proper format
3. Check credential is saved and selected in node
4. Test API call with curl first:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://api.example.com/endpoint
   ```
5. Verify token hasn't expired (OAuth tokens expire)
6. Check API endpoint URL is correct (trailing slash matters)

### Issue 4: Webhook Returns Immediately But Workflow Fails Later
**Symptoms:** Webhook responds successfully but workflow doesn't complete

**Solutions:**
1. Check execution history for error details
2. Use "Respond to Webhook" node early in workflow
3. For long workflows (>30s), respond immediately:
   ```
   Webhook Settings: Respond Immediately
   Add "Respond to Webhook" node after initial validation
   ```
4. Check for nodes that timeout
5. Verify all credentials are configured
6. Test workflow with manual trigger first

### Issue 5: AI Agent Returns Unexpected Format
**Symptoms:** AI doesn't follow instructions or returns wrong format

**Solutions:**
1. Make system message more specific:
   ```
   "Return ONLY valid JSON. No explanations.
   Format: {"field": "value"}"
   ```
2. Add examples (few-shot learning)
3. Lower temperature (0.1-0.3 for structured tasks)
4. Use GPT-4 instead of GPT-3.5 for complex formatting
5. Parse AI response defensively:
   ```javascript
   let result;
   try {
     result = JSON.parse($json.output);
   } catch {
     // Try to extract JSON from text
     const match = $json.output.match(/\{[\s\S]*\}/);
     if (match) {
       result = JSON.parse(match[0]);
     } else {
       throw new Error('AI did not return valid JSON');
     }
   }
   ```

### Issue 6: OAuth Connection Keeps Disconnecting
**Symptoms:** OAuth credentials stop working periodically

**Solutions:**
1. Google OAuth: Ensure app is published (not testing mode)
2. Check token expiration settings
3. Enable refresh token:
   - OAuth2 credential settings
   - Request refresh token: Yes
4. Re-authenticate if app was in testing mode initially
5. For Google: Verify redirect URL matches Railway domain

---

## Success Metrics

### Immediate Success (Day 1)
- ✅ Can create and test webhook triggers
- ✅ Schedule trigger executes at correct time
- ✅ HTTP Request successfully calls external API
- ✅ Telegram bot receives and processes messages
- ✅ AI agent generates expected output
- ✅ Understanding of authentication methods

### Short-Term Success (Week 1)
- ✅ Built 3+ workflows with different trigger types
- ✅ Successfully integrated with 2+ external APIs
- ✅ Implemented AI agent in production workflow
- ✅ All triggers working reliably without manual intervention
- ✅ Proper error handling on all workflows
- ✅ Can debug and troubleshoot failed executions

### Long-Term Success (Month 1+)
- ✅ 10+ production workflows running automatically
- ✅ 99%+ success rate on scheduled/webhook triggers
- ✅ AI agents providing consistent, quality outputs
- ✅ Complex multi-step automations working reliably
- ✅ Can integrate any API with HTTP Request node
- ✅ Building custom solutions not available in templates

---

## Related Skills
- **build_n8n_workflow.md** - Foundational workflow building concepts
- **setup_n8n_error_handling.md** - Comprehensive error handling strategies
- **setup_n8n_gohighlevel_integration.md** - CRM integration specifics
- **setup_n8n_google_oauth.md** - Google services OAuth configuration

---

**Skill Version:** 1.0
**Last Updated:** 2024
**Estimated Execution Time:** 2-3 hours first time, 30-45 minutes after mastery
**Difficulty:** Intermediate to Advanced
**Prerequisites:** Basic N8N workflow understanding, API concepts
