# Setup N8N GoHighLevel Integration - Complete CRM Automation Guide

## Purpose
This skill provides comprehensive setup and integration instructions for connecting GoHighLevel (GHL) CRM with N8N for complete marketing automation. Learn to automate lead management, opportunity tracking, contact synchronization, and workflow triggers between GHL and other platforms.

## When to Use This Skill
- When you need to automate GoHighLevel operations
- When building agency client automation workflows
- When integrating GHL with other platforms (Google Sheets, email, SMS)
- When creating lead capture and follow-up systems
- When syncing data between GHL and external systems
- Before building production CRM automations for clients

## Prerequisites

### Required Accounts
- **GoHighLevel Account** - Active GHL subscription (Agency or Business plan)
- **GoHighLevel Developer Account** - Separate from regular GHL account (developers.gohighlevel.com)
- **N8N Instance** - Running and accessible (Cloud or Self-Hosted)

### Required Knowledge
- Basic N8N workflow building (see build_n8n_workflow.md)
- Understanding of OAuth2 authentication
- CRM concepts (contacts, opportunities, pipelines)
- HTTP Request node usage (see setup_n8n_triggers_agents.md)

### Recommended Setup
- Self-hosted N8N on Railway.app (see setup_n8n_self_hosted.md)
- Custom domain for consistent OAuth redirects (optional but recommended)

## GoHighLevel Architecture Overview

```
GoHighLevel Structure:
├── Account (Agency Level)
│   ├── Location 1 (Client/Sub-Account)
│   │   ├── Contacts
│   │   ├── Opportunities
│   │   ├── Calendars
│   │   ├── Pipelines
│   │   └── Workflows
│   ├── Location 2 (Another Client)
│   └── Location 3 (Another Client)
```

**Important Concepts:**
- **Agency Account**: Your main GHL account
- **Location/Sub-Account**: Individual client accounts under your agency
- **API Access**: Can be agency-level or location-specific
- **OAuth Scopes**: Permissions for what data you can access

---

## Phase 1: GoHighLevel Developer Account Setup (15 minutes)

### Step 1.1: Create GHL Developer Account

**CRITICAL: This is separate from your regular GoHighLevel account**

1. Navigate to: https://developers.gohighlevel.com
2. Click "Sign Up" (top right)
3. Fill in registration details:
```
Email: your-email@company.com (can be same as GHL account)
Password: [Create strong password]
Company Name: Your Agency Name
```
4. Click "Create Account"
5. Verify email address (check inbox for verification link)
6. Log in to developer portal

**What This Account Does:**
- Manages API applications
- Creates OAuth credentials
- Accesses API documentation
- Monitors API usage

**Note:** This developer account DOES NOT replace your regular GHL account. You still use your regular GHL account for managing clients/locations.

### Step 1.2: Understand Developer Portal

Once logged in, you'll see:

```
Developer Portal Layout:
├── Dashboard - Overview of your apps
├── My Apps - Your created applications
├── Documentation - API reference
├── Webhooks - Event notifications
└── Account - Profile settings
```

---

## Phase 2: Create GHL OAuth Application (20 minutes)

### Step 2.1: Create New Application

1. In Developer Portal, click "My Apps" (left sidebar)
2. Click "Create App" button (top right)
3. You'll see the app creation form

### Step 2.2: Configure Basic Information

Fill in the application details:

```yaml
App Name: N8N Automation
Description: N8N workflow automation integration
Category: Automation & Workflow
App Logo: [Upload 400x400px PNG - minimum requirement]
Tagline: Automate your GoHighLevel workflows
Company: Your Agency Name
```

**App Logo Requirements:**
- Minimum 400x400 pixels
- PNG or JPG format
- Clear, professional design
- Represents your agency/integration

**Quick Logo Tip:**
If you don't have a logo ready, create simple text logo at:
- Canva.com (free)
- Or use N8N logo temporarily from: https://n8n.io/press

### Step 2.3: Configure Application Settings

**Application Type:**
```yaml
App Type: Private
Target User: Sub Account
Who Can Install: Anyone
Listing Type: White Label
```

**Understanding Settings:**

**App Type:**
- **Private**: Only you can use it (recommended for agency use)
- **Public**: Available in GHL marketplace (if you want to sell/distribute)

**Target User:**
- **Sub Account**: Works with individual client locations (most common)
- **Agency**: Works at agency level only

**Who Can Install:**
- **Anyone**: Any GHL user can install (even for private apps, this means anyone in your agency)
- **Specific Agencies**: Restrict to certain agencies only

**Listing Type:**
- **White Label**: Branded as your app
- **Standard**: Shows as third-party integration

### Step 2.4: Add Profile Details

```yaml
Support Email: support@youragency.com
Support Phone: +1-555-123-4567 (format matters)
Website URL: https://youragency.com (optional)
Privacy Policy URL: https://youragency.com/privacy (optional)
Terms of Service URL: https://youragency.com/terms (optional)
```

**Images** (Upload at least 3 screenshots):
- Can be mockups or actual integration screenshots
- Minimum 3 images required
- 1200x800 pixels recommended
- Show what your integration does

**Tip:** For private agency use, these can be simple placeholder images.

### Step 2.5: Configure Pricing (Leave as Free)

```yaml
Pricing Model: Free
Monthly Fee: $0.00
Trial Period: N/A
```

For agency-internal use, always leave as free.

**Click "Save" after each section to preserve changes**

---

## Phase 3: Configure OAuth Settings (25 minutes)

### Step 3.1: Set Up OAuth Scopes

Scopes determine what data your N8N integration can access.

1. In your app settings, go to "Advanced Settings"
2. Click "OAuth" section
3. Scroll to "Scopes"

**Required Scopes for Basic Automation:**

Add these scopes one by one:
```
locations.readonly
contacts.readonly
contacts.write
opportunities.readonly
opportunities.write
users.readonly
users.write
```

**Understanding Scopes:**

```yaml
locations.readonly:
  - View location/sub-account information
  - Essential for multi-client setups

contacts.readonly:
  - Read contact data
  - Search contacts
  - View contact details

contacts.write:
  - Create new contacts
  - Update existing contacts
  - Delete contacts
  - Add tags, notes

opportunities.readonly:
  - View pipeline data
  - Read opportunity details
  - Access deal stages

opportunities.write:
  - Create opportunities
  - Update opportunity status
  - Move deals through pipeline
  - Assign monetary values

users.readonly:
  - View team members
  - Read user assignments
  - Access user details

users.write:
  - Assign contacts to users
  - Update user information
  - Manage team assignments
```

**Additional Useful Scopes:**

```
calendars.readonly - View calendar events
calendars.write - Create/update events
conversations.readonly - Read messages/emails
conversations.write - Send messages
workflows.readonly - View GHL workflows
workflows - Trigger GHL workflows
```

**Add scopes based on your needs. More scopes = more permissions required from users.**

### Step 3.2: Get Your N8N Redirect URL

1. Open N8N in new tab/window
2. Create new workflow (or open existing)
3. Add "GoHighLevel" node (search for it)
4. Click on node, select "GoHighLevel OAuth2 API" credential
5. Click "Create New Credential"
6. **DO NOT FILL ANYTHING YET**
7. Look for "OAuth Redirect URL" at top of credential form
8. **COPY THIS URL** - it looks like:
```
https://your-n8n-domain.up.railway.app/rest/oauth2-credential/callback
```

**CRITICAL:** This URL must match EXACTLY in GHL developer portal.

### Step 3.3: Add Redirect URL to GHL App

1. Back in GHL Developer Portal
2. Your app → Advanced Settings → OAuth
3. Find "Redirect URL" field
4. Paste your N8N OAuth redirect URL:
```
https://your-n8n-domain.up.railway.app/rest/oauth2-credential/callback
```
5. Click "Add" button
6. URL should appear in list below
7. **Click "Save"** at bottom of page

**Common Mistake:** Forgetting to click "Save" after adding redirect URL. Always save!

### Step 3.4: Set Distribution Type

Still in Advanced Settings:

```yaml
Distribution Type: Standard (not White Label for OAuth section)
```

**Why Standard?**
- White Label OAuth requires custom domain setup
- Standard works immediately with Railway/N8N URLs
- For agency-internal use, Standard is sufficient

### Step 3.5: Generate Client Credentials

1. In Advanced Settings, find "Client Keys" section
2. Click "Add New Client Key"
3. Name it: "N8N Integration"
4. Click "Add"
5. You'll see:
   - **Client ID**: Long alphanumeric string
   - **Client Secret**: Another long alphanumeric string

**COPY BOTH - You'll need them for N8N**

Store them temporarily in notepad:
```
Client ID: abc123def456ghi789...
Client Secret: xyz987uvw654rst321...
```

**Security Note:** Treat Client Secret like a password. Never commit to git, never share publicly.

### Step 3.6: Publish Application

**CRITICAL STEP - Easy to miss:**

1. In your app settings, look for "Audience" or "Publishing" section
2. You'll see "Publishing Status": Currently in test mode
3. Click "Publish App" button
4. Confirm publication

**Why This Matters:**
- Test mode apps have limited OAuth functionality
- N8N can't connect to unpublished apps
- Error: "Please log in the serum" = App not published

**Verification:**
- After publishing, status should show "Published" or "Live"
- If you see "Testing" or "Draft", app is not fully published

---

## Phase 4: Configure N8N Credential (15 minutes)

### Step 4.1: Create GHL OAuth2 Credential in N8N

1. In N8N workflow with GoHighLevel node
2. Credential dropdown → "Create New Credential"
3. Select "GoHighLevel OAuth2 API"

### Step 4.2: Enter Credentials

Fill in the credential form:

```yaml
Client ID: [Paste from GHL Developer Portal]
Client Secret: [Paste from GHL Developer Portal]
Scope: [Paste all scopes with spaces]
```

**Scope Field:**
N8N provides a helpful "Copy Scopes" button. If not visible, manually enter:

```
locations.readonly contacts.readonly contacts.write opportunities.readonly opportunities.write users.readonly users.write
```

**Important:** Scopes must be space-separated, not comma-separated.

### Step 4.3: Connect Your Account

1. After entering Client ID, Secret, and Scopes
2. Click "Connect my account" button
3. New browser window opens to GoHighLevel
4. You'll see OAuth consent screen

**OAuth Flow:**

```
Step 1: GHL Login
- Enter your GoHighLevel credentials (regular account, not developer)
- If already logged in, may skip this

Step 2: App Authorization Screen
- Shows your app name: "N8N Automation"
- Lists permissions requested
- Shows which location/sub-account to authorize

Step 3: Choose Location
- Dropdown with all your GHL locations/clients
- Select which client account to connect
- For agency operations, select your main location
- For client automation, select that client's location

Step 4: Authorize
- Click "Authorize" or "Allow"
- Redirects back to N8N

Step 5: Success
- N8N shows "Successfully connected!"
- Credential is now active
```

**If You See Errors:**

**Error: "Please log in the serum"**
```
Cause: App not published
Solution:
1. Go back to GHL Developer Portal
2. Find Publishing section
3. Click "Publish App"
4. Wait 1-2 minutes
5. Try connecting again
```

**Error: "Redirect URI mismatch"**
```
Cause: Redirect URL in GHL doesn't match N8N
Solution:
1. Check N8N OAuth redirect URL
2. Verify exact match in GHL (including https://)
3. Click Save in GHL after changing
4. Try connecting again
```

**Error: "Invalid client"**
```
Cause: Client ID or Secret incorrect
Solution:
1. Verify you copied full Client ID and Secret
2. No extra spaces
3. Regenerate credentials in GHL if needed
```

### Step 4.4: Test Connection

1. After successful authorization
2. In GoHighLevel node, select credential from dropdown
3. Choose a simple operation: "Contact" → "Get All"
4. Click "Execute Node"
5. Should return list of contacts from your GHL account

**Success Indicators:**
- No error messages
- Returns contact data (or empty array if no contacts)
- Green checkmark on node

---

## Phase 5: Basic GoHighLevel Operations (30 minutes)

### Understanding GHL Data Structure

**Contacts** (Leads/Customers)
```javascript
{
  "id": "contact_abc123",
  "firstName": "John",
  "lastName": "Doe",
  "email": "john@example.com",
  "phone": "+15551234567",
  "tags": ["lead", "interested"],
  "customFields": {
    "lead_source": "Website Form"
  },
  "locationId": "location_xyz789"
}
```

**Opportunities** (Deals/Pipeline Items)
```javascript
{
  "id": "opportunity_def456",
  "name": "New Website Project",
  "status": "open",
  "monetaryValue": 5000,
  "pipelineId": "pipeline_123",
  "pipelineStageId": "stage_456",
  "contactId": "contact_abc123",
  "assignedTo": "user_789"
}
```

### Operation 1: Create Contact

**Use Case:** Add new lead from form submission

**Workflow Example:**
```
1. Webhook Trigger (Form Submission)

2. GoHighLevel Node
   - Credential: [Your GHL OAuth2 credential]
   - Resource: Contact
   - Operation: Create

   Configuration:
   Location ID: {{ $env.GHL_LOCATION_ID }}

   Additional Fields:
   - First Name: {{ $json.firstName }}
   - Last Name: {{ $json.lastName }}
   - Email: {{ $json.email }}
   - Phone: {{ $json.phone }}
   - Source: {{ $json.source }}
   - Tags: lead,website
   - Custom Fields:
     {
       "lead_source": "{{ $json.source }}",
       "signup_date": "{{ $now.toISO() }}"
     }

3. Respond to Webhook
   - Response: {"success": true, "contactId": "{{ $json.id }}"}
```

**Getting Location ID:**

Method 1: From GHL URL
```
When logged into GHL, URL shows:
https://app.gohighlevel.com/location/abc123def456/dashboard
                                    ^^^^^^^^^^^^
                                    This is Location ID
```

Method 2: Using N8N
```
1. GoHighLevel Node
2. Resource: Location
3. Operation: Get All
4. Execute node
5. Copy "id" from response
```

Store in environment variable:
```
Railway → N8N service → Variables
GHL_LOCATION_ID = abc123def456
```

### Operation 2: Search for Contact

**Use Case:** Check if contact exists before creating

**Workflow Example:**
```
1. Trigger (Any)

2. GoHighLevel Node (Search Contact)
   - Resource: Contact
   - Operation: Get All
   - Location ID: {{ $env.GHL_LOCATION_ID }}
   - Additional Fields:
     - Filters:
       {
         "email": "{{ $json.email }}"
       }
     - Limit: 1

3. IF Node (Check if Found)
   - Condition: {{ $json.contacts.length > 0 }}
   - True → Contact exists, update it
   - False → Contact doesn't exist, create it

4a. Update Branch:
    - GoHighLevel Node (Update Contact)

4b. Create Branch:
    - GoHighLevel Node (Create Contact)
```

### Operation 3: Update Contact

**Use Case:** Add tags, update custom fields

**Workflow Example:**
```
1. Trigger with Contact ID

2. GoHighLevel Node (Update Contact)
   - Resource: Contact
   - Operation: Update
   - Contact ID: {{ $json.contactId }}
   - Location ID: {{ $env.GHL_LOCATION_ID }}

   Additional Fields:
   - Tags: existing_customer,active
   - Custom Fields:
     {
       "last_purchase_date": "{{ $now.toISO() }}",
       "total_value": "{{ $json.totalSpent }}"
     }
```

### Operation 4: Create Opportunity

**Use Case:** Move qualified lead to sales pipeline

**Workflow Example:**
```
1. Trigger (Contact qualified)

2. GoHighLevel Node (Create Opportunity)
   - Resource: Opportunity
   - Operation: Create
   - Location ID: {{ $env.GHL_LOCATION_ID }}

   Configuration:
   - Name: {{ $json.firstName }} {{ $json.lastName }} - {{ $json.service }}
   - Pipeline ID: {{ $env.GHL_PIPELINE_ID }}
   - Pipeline Stage ID: {{ $env.GHL_INITIAL_STAGE_ID }}
   - Status: open
   - Contact ID: {{ $json.contactId }}
   - Monetary Value: {{ $json.estimatedValue }}
   - Assigned To: {{ $env.GHL_SALES_USER_ID }}

3. Slack Notification
   - Channel: #sales
   - Message: "New opportunity: {{ $json.name }} - ${{ $json.monetaryValue }}"
```

**Getting Pipeline and Stage IDs:**

```
1. GoHighLevel Node
2. Resource: Pipeline
3. Operation: Get All
4. Location ID: {{ $env.GHL_LOCATION_ID }}
5. Execute node
6. Response shows:
   {
     "pipelines": [
       {
         "id": "pipeline_123",
         "name": "Sales Pipeline",
         "stages": [
           {
             "id": "stage_abc",
             "name": "New Lead"
           },
           {
             "id": "stage_def",
             "name": "Qualified"
           },
           {
             "id": "stage_ghi",
             "name": "Proposal Sent"
           }
         ]
       }
     ]
   }

Store these IDs in environment variables
```

### Operation 5: Update Opportunity Status

**Use Case:** Move deal through pipeline stages

**Workflow Example:**
```
1. Trigger (Deal progresses)

2. GoHighLevel Node (Update Opportunity)
   - Resource: Opportunity
   - Operation: Update
   - Opportunity ID: {{ $json.opportunityId }}
   - Location ID: {{ $env.GHL_LOCATION_ID }}

   Fields to Update:
   - Pipeline Stage ID: {{ $json.newStageId }}
   - Status: {{ $json.newStatus }}
   - Monetary Value: {{ $json.updatedValue }}

3. GoHighLevel Node (Add Note to Opportunity)
   - Resource: Opportunity
   - Operation: Upsert
   - Add note about stage change

4. Email Notification to Assigned User
```

---

## Phase 6: Real-World Integration Examples (45 minutes)

### Example 1: Website Form to GHL Contact

**Complete Automation: Form → GHL → Email → Slack**

```
Workflow: Contact Form to GoHighLevel

1. Webhook Trigger
   - Method: POST
   - Path: contact-form
   - Authentication: Header Auth (X-API-Key)

2. Set Node (Format Data)
   ```
   firstName: {{ $json.body.first_name }}
   lastName: {{ $json.body.last_name }}
   email: {{ $json.body.email }}
   phone: {{ $json.body.phone }}
   message: {{ $json.body.message }}
   source: {{ $json.body.utm_source || 'Website' }}
   timestamp: {{ $now.toISO() }}
   ```

3. IF Node (Validate Email)
   - Condition: {{ $json.email && $json.email.includes('@') }}
   - False → Error response

4. GoHighLevel Node (Search Existing Contact)
   - Resource: Contact
   - Operation: Get All
   - Location ID: {{ $env.GHL_LOCATION_ID }}
   - Filters: {"email": "{{ $json.email }}"}
   - Limit: 1

5. IF Node (Contact Exists?)
   - Condition: {{ $json.contacts && $json.contacts.length > 0 }}
   - True → Update existing
   - False → Create new

6a. Create New Contact Branch:
    - GoHighLevel Node (Create Contact)
      - Resource: Contact
      - Operation: Create
      - Location ID: {{ $env.GHL_LOCATION_ID }}
      - First Name: {{ $('Set Node').item.json.firstName }}
      - Last Name: {{ $('Set Node').item.json.lastName }}
      - Email: {{ $('Set Node').item.json.email }}
      - Phone: {{ $('Set Node').item.json.phone }}
      - Source: {{ $('Set Node').item.json.source }}
      - Tags: new_lead,website
      - Custom Fields:
        {
          "initial_message": "{{ $('Set Node').item.json.message }}",
          "lead_date": "{{ $('Set Node').item.json.timestamp }}"
        }

6b. Update Existing Contact Branch:
    - GoHighLevel Node (Update Contact)
      - Contact ID: {{ $json.contacts[0].id }}
      - Tags: returning_visitor
      - Custom Fields:
        {
          "last_contact_date": "{{ $('Set Node').item.json.timestamp }}",
          "contact_count": "{{ parseInt($json.contacts[0].customFields.contact_count || 0) + 1 }}"
        }

7. Merge Node (Combine Branches)
   - Mode: Append
   - Merges both paths back together

8. GoHighLevel Node (Create Task for Sales Team)
   - Resource: Task
   - Operation: Create
   - Contact ID: {{ $json.id || $json.contacts[0].id }}
   - Title: "Follow up with {{ $('Set Node').item.json.firstName }} {{ $('Set Node').item.json.lastName }}"
   - Description: "{{ $('Set Node').item.json.message }}"
   - Due Date: {{ $now.plus({days: 1}).toISO() }}
   - Assigned To: {{ $env.GHL_SALES_TEAM_USER_ID }}

9. Gmail (Auto-Reply to Lead)
   - To: {{ $('Set Node').item.json.email }}
   - Subject: Thanks for contacting {{ $env.COMPANY_NAME }}!
   - Body:
     "Hi {{ $('Set Node').item.json.firstName }},

     Thank you for reaching out! We received your message and a team member will
     respond within 24 hours.

     In the meantime, feel free to check out our resources at {{ $env.WEBSITE_URL }}.

     Best regards,
     {{ $env.COMPANY_NAME }} Team"

10. Slack (Notify Sales Team)
    - Channel: #leads
    - Message:
      "🆕 New lead: *{{ $('Set Node').item.json.firstName }} {{ $('Set Node').item.json.lastName }}*

      Email: {{ $('Set Node').item.json.email }}
      Phone: {{ $('Set Node').item.json.phone }}
      Source: {{ $('Set Node').item.json.source }}

      Message: {{ $('Set Node').item.json.message }}

      <https://app.gohighlevel.com/location/{{ $env.GHL_LOCATION_ID }}/contacts/detail/{{ $json.id }}|View in GHL>"

11. Respond to Webhook
    - Response Code: 200
    - Body:
      {
        "success": true,
        "message": "Thank you! We'll be in touch soon.",
        "contactId": "{{ $json.id || $json.contacts[0].id }}"
      }

Error Handling:
- On any node failure → Error Workflow triggers
- Sends alert to #tech-alerts channel
- Logs failed submission to Google Sheets for manual follow-up
```

### Example 2: Sync Google Sheets to GoHighLevel

**Use Case:** Bulk import contacts from spreadsheet

```
Workflow: Google Sheets → GoHighLevel Contact Sync

1. Schedule Trigger
   - Cron: 0 */6 * * * (Every 6 hours)
   - Or: Manual trigger for one-time import

2. Google Sheets Node (Read Contacts)
   - Operation: Get All Rows
   - Spreadsheet: Lead Import Sheet
   - Sheet: Pending Imports
   - Range: A:J (Columns A through J)

3. Code Node (Validate & Format Data)
   ```javascript
   const rows = $input.all();
   const validated = [];
   const errors = [];

   for (const row of rows) {
     const data = row.json;

     // Skip header row
     if (data.email === 'Email' || !data.email) continue;

     // Validate email
     if (!data.email.includes('@')) {
       errors.push({
         row: data,
         error: 'Invalid email'
       });
       continue;
     }

     // Format phone (remove non-digits, add +1 if US)
     let phone = data.phone?.replace(/\D/g, '') || '';
     if (phone && phone.length === 10) {
       phone = '+1' + phone;
     }

     validated.push({
       firstName: data.first_name?.trim() || '',
       lastName: data.last_name?.trim() || '',
       email: data.email.toLowerCase().trim(),
       phone: phone,
       company: data.company?.trim() || '',
       source: data.source || 'Import',
       tags: data.tags?.split(',').map(t => t.trim()) || [],
       customFields: {
         import_date: new Date().toISOString(),
         sheet_row: data.__rowNum__,
         notes: data.notes || ''
       }
     });
   }

   // Return validated contacts
   return validated.map(contact => ({ json: contact }));
   ```

4. Loop Over Items
   - Process one contact at a time (avoids rate limits)

5. Wait Node (Rate Limiting)
   - Wait: 500ms
   - Prevents API rate limit issues

6. GoHighLevel Node (Search Existing Contact)
   - Resource: Contact
   - Operation: Get All
   - Location ID: {{ $env.GHL_LOCATION_ID }}
   - Filters: {"email": "{{ $json.email }}"}
   - Limit: 1

7. IF Node (Contact Exists?)
   - Condition: {{ $json.contacts && $json.contacts.length > 0 }}
   - True → Skip (already exists)
   - False → Create new

8. GoHighLevel Node (Create Contact)
   - Resource: Contact
   - Operation: Create
   - Location ID: {{ $env.GHL_LOCATION_ID }}
   - Map all fields from validated data

9. Code Node (Aggregate Results)
   ```javascript
   // This runs after loop completes
   const items = $input.all();

   const summary = {
     totalProcessed: items.length,
     created: items.filter(i => i.json.id).length,
     skipped: items.filter(i => !i.json.id).length,
     timestamp: new Date().toISOString()
   };

   return [{ json: summary }];
   ```

10. Google Sheets Node (Update Status)
    - Operation: Update Range
    - Sheet: Pending Imports
    - Range: K:K (Status column)
    - Values: "Imported - {{ $now.toFormat('yyyy-MM-dd HH:mm') }}"

11. Slack (Summary Notification)
    - Channel: #automations
    - Message:
      "📊 GHL Contact Import Complete

      Processed: {{ $json.totalProcessed }}
      Created: {{ $json.created }}
      Skipped (existing): {{ $json.skipped }}

      Timestamp: {{ $json.timestamp }}"
```

### Example 3: Opportunity Pipeline Automation

**Use Case:** Auto-create opportunity when contact tagged as "qualified"**

```
Workflow: Qualified Lead → Sales Pipeline

1. GoHighLevel Trigger (Webhook from GHL)
   - Setup in GHL: Workflow → Webhook → Contact Tag Added
   - Trigger when tag "qualified" added to contact

2. GoHighLevel Node (Get Contact Details)
   - Resource: Contact
   - Operation: Get
   - Contact ID: {{ $json.contactId }}
   - Location ID: {{ $env.GHL_LOCATION_ID }}

3. Code Node (Determine Opportunity Value)
   ```javascript
   const contact = $json;

   // Estimate deal value based on service interest
   let estimatedValue = 1000; // Default

   const serviceField = contact.customFields?.service_interest?.toLowerCase();

   if (serviceField?.includes('enterprise')) {
     estimatedValue = 10000;
   } else if (serviceField?.includes('premium')) {
     estimatedValue = 5000;
   } else if (serviceField?.includes('standard')) {
     estimatedValue = 2500;
   }

   // Round robin assignment to sales team
   const salesTeam = [
     $env.SALES_USER_1_ID,
     $env.SALES_USER_2_ID,
     $env.SALES_USER_3_ID
   ];

   const assignedUser = salesTeam[Math.floor(Math.random() * salesTeam.length)];

   return [{
     json: {
       contact: contact,
       estimatedValue: estimatedValue,
       assignedTo: assignedUser,
       opportunityName: `${contact.firstName} ${contact.lastName} - ${serviceField || 'General'}`
     }
   }];
   ```

4. GoHighLevel Node (Create Opportunity)
   - Resource: Opportunity
   - Operation: Create
   - Location ID: {{ $env.GHL_LOCATION_ID }}
   - Name: {{ $json.opportunityName }}
   - Contact ID: {{ $json.contact.id }}
   - Pipeline ID: {{ $env.GHL_SALES_PIPELINE_ID }}
   - Pipeline Stage ID: {{ $env.GHL_NEW_LEAD_STAGE_ID }}
   - Status: open
   - Monetary Value: {{ $json.estimatedValue }}
   - Assigned To: {{ $json.assignedTo }}

5. GoHighLevel Node (Add Note to Contact)
   - Resource: Note
   - Operation: Create
   - Contact ID: {{ $json.contact.id }}
   - Body: "Opportunity created: {{ $json.opportunityName }}
           Value: ${{ $json.estimatedValue }}
           Assigned to: [User Name]
           Date: {{ $now.toFormat('yyyy-MM-dd HH:mm') }}"

6. HTTP Request (Get Assigned User Details)
   - Method: GET
   - URL: https://rest.gohighlevel.com/v1/users/{{ $json.assignedTo }}
   - Authentication: OAuth2 (GHL credential)

7. Slack (Notify Assigned Salesperson)
   - Channel: @{{ $json.userName }} (DM)
   - Message:
     "🎯 New opportunity assigned to you!

     Contact: {{ $('Code Node').item.json.contact.firstName }} {{ $('Code Node').item.json.contact.lastName }}
     Email: {{ $('Code Node').item.json.contact.email }}
     Phone: {{ $('Code Node').item.json.contact.phone }}
     Est. Value: ${{ $('Code Node').item.json.estimatedValue }}

     <https://app.gohighlevel.com/location/{{ $env.GHL_LOCATION_ID }}/opportunities/{{ $('GoHighLevel Node (Create Opportunity)').item.json.id }}|View Opportunity>

     Next Steps:
     1. Review contact history
     2. Schedule discovery call
     3. Send proposal within 48 hours"

8. Gmail (Auto-Email to Contact)
   - To: {{ $('Code Node').item.json.contact.email }}
   - Subject: Next Steps with {{ $env.COMPANY_NAME }}
   - Body:
     "Hi {{ $('Code Node').item.json.contact.firstName }},

     Thank you for your interest in our {{ $('Code Node').item.json.contact.customFields.service_interest }} services!

     I've assigned {{ $('HTTP Request').item.json.firstName }} from our team to help you.
     You can expect a call or email within 24 hours to discuss your needs and next steps.

     In the meantime, feel free to reply to this email with any questions.

     Best regards,
     {{ $env.COMPANY_NAME }} Team"

9. Google Sheets (Log New Opportunity)
   - Operation: Append
   - Spreadsheet: Sales Pipeline Report
   - Values:
     - Date: {{ $now.toFormat('yyyy-MM-dd') }}
     - Contact Name: {{ $('Code Node').item.json.opportunityName }}
     - Email: {{ $('Code Node').item.json.contact.email }}
     - Value: {{ $('Code Node').item.json.estimatedValue }}
     - Assigned To: {{ $('HTTP Request').item.json.firstName }} {{ $('HTTP Request').item.json.lastName }}
     - Stage: New Lead
     - Opportunity ID: {{ $('GoHighLevel Node (Create Opportunity)').item.json.id }}
```

### Example 4: Two-Way Sync with External CRM

**Use Case:** Sync contacts between GoHighLevel and another system (Airtable example)

```
Workflow: Bi-Directional GHL ↔ Airtable Sync

Part A: GHL → Airtable (When contact updated in GHL)

1. Schedule Trigger
   - Cron: */15 * * * * (Every 15 minutes)
   - Or: GHL Webhook (if available for contact updates)

2. HTTP Request (Get Recent GHL Contacts)
   - Method: GET
   - URL: https://rest.gohighlevel.com/v1/contacts/
   - Authentication: OAuth2 (GHL credential)
   - Query Parameters:
     locationId: {{ $env.GHL_LOCATION_ID }}
     startAfterDate: {{ $now.minus({minutes: 20}).toISO() }}

3. Code Node (Filter Updated Contacts)
   ```javascript
   const contacts = $json.contacts || [];
   const recentlyUpdated = contacts.filter(contact => {
     const updatedAt = new Date(contact.dateUpdated);
     const fifteenMinAgo = new Date(Date.now() - 15 * 60 * 1000);
     return updatedAt > fifteenMinAgo;
   });

   return recentlyUpdated.map(contact => ({ json: contact }));
   ```

4. Loop Over Items (Process Each Contact)

5. HTTP Request (Search Airtable for Contact)
   - Method: GET
   - URL: https://api.airtable.com/v0/{{ $env.AIRTABLE_BASE_ID }}/Contacts
   - Headers:
     Authorization: Bearer {{ $env.AIRTABLE_API_KEY }}
   - Query Parameters:
     filterByFormula: {Email}='{{ $json.email }}'

6. IF Node (Contact Exists in Airtable?)
   - Condition: {{ $json.records && $json.records.length > 0 }}
   - True → Update Airtable record
   - False → Create Airtable record

7a. Update Airtable:
    - HTTP Request (PATCH)
    - URL: https://api.airtable.com/v0/BASE/Contacts/{{ $json.records[0].id }}
    - Body:
      {
        "fields": {
          "First Name": "{{ $('Loop').item.json.firstName }}",
          "Last Name": "{{ $('Loop').item.json.lastName }}",
          "Email": "{{ $('Loop').item.json.email }}",
          "Phone": "{{ $('Loop').item.json.phone }}",
          "GHL ID": "{{ $('Loop').item.json.id }}",
          "Last Updated": "{{ $now.toISO() }}",
          "Tags": "{{ $('Loop').item.json.tags.join(', ') }}"
        }
      }

7b. Create Airtable Record:
    - HTTP Request (POST)
    - Similar to above but POST instead of PATCH

Part B: Airtable → GHL (When contact updated in Airtable)

8. Airtable Trigger (Webhook from Airtable automation)
   - Setup in Airtable: Automation → Webhook → Send to N8N

9. GoHighLevel Node (Search Contact by Email)
   - Resource: Contact
   - Operation: Get All
   - Filters: {"email": "{{ $json.email }}"}

10. IF Node (Contact Exists in GHL?)
    - True → Update GHL contact
    - False → Create GHL contact

11a/b. Create or Update accordingly
```

---

## Phase 7: Advanced Techniques (30 minutes)

### Technique 1: Batch Processing with Rate Limiting

**Problem:** GHL API has rate limits (typically 100-200 requests/minute)

**Solution:**
```
1. Split data into batches

Code Node (Create Batches):
```javascript
const items = $input.all();
const batchSize = 10; // Process 10 at a time
const batches = [];

for (let i = 0; i < items.length; i += batchSize) {
  batches.push({
    batchNumber: Math.floor(i / batchSize) + 1,
    items: items.slice(i, i + batchSize)
  });
}

return batches.map(batch => ({ json: batch }));
```

2. Loop Over Batches

3. For each batch:
   - Process items
   - Wait 6 seconds (ensures <10 batches/minute = <100 items/minute)

4. Loop Over Items in Batch
   - Make GHL API call
   - Wait 100ms between items

This ensures:
- Max 10 items per batch
- 6 seconds between batches
- = ~100 items per minute (under rate limit)
```

### Technique 2: Custom Field Mapping

**Problem:** Different systems use different field names

**Solution: Create mapping Code node**
```javascript
// Define field mappings
const fieldMap = {
  // External System → GHL
  'first_name': 'firstName',
  'last_name': 'lastName',
  'email_address': 'email',
  'phone_number': 'phone',
  'company_name': 'companyName',
  'lead_source': 'source',
  'status': 'tags', // Map status to tags
  'notes': 'notes'
};

const externalData = $json;
const ghlData = {
  customFields: {}
};

// Map standard fields
for (const [externalField, ghlField] of Object.entries(fieldMap)) {
  if (externalData[externalField]) {
    if (ghlField === 'tags') {
      ghlData[ghlField] = [externalData[externalField]];
    } else {
      ghlData[ghlField] = externalData[externalField];
    }
  }
}

// Map custom fields (anything not in standard mapping)
for (const [key, value] of Object.entries(externalData)) {
  if (!fieldMap[key]) {
    ghlData.customFields[key] = value;
  }
}

return [{ json: ghlData }];
```

### Technique 3: Error Handling with Retry Logic

**For GHL operations that might fail temporarily**

```javascript
// Code node wrapper for GHL operations
async function callGHLWithRetry(operation, maxRetries = 3) {
  let lastError;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Attempt operation
      const result = await operation();
      return result;

    } catch (error) {
      lastError = error;

      // Check if error is retryable
      const isRateLimitError = error.message?.includes('429') ||
                               error.message?.includes('rate limit');
      const isServerError = error.message?.includes('500') ||
                           error.message?.includes('502') ||
                           error.message?.includes('503');

      if (isRateLimitError || isServerError) {
        // Wait before retry (exponential backoff)
        const waitTime = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
        console.log(`Retry ${attempt}/${maxRetries} after ${waitTime}ms`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
        continue;
      } else {
        // Non-retryable error
        throw error;
      }
    }
  }

  // All retries failed
  throw new Error(`Operation failed after ${maxRetries} attempts: ${lastError.message}`);
}

// Usage in workflow:
try {
  const result = await callGHLWithRetry(async () => {
    // Your GHL operation here
    return await createContact(contactData);
  });

  return [{ json: result }];
} catch (error) {
  return [{
    json: {
      error: true,
      message: error.message,
      contactData: contactData
    }
  }];
}
```

### Technique 4: Webhook Signature Verification (Security)

**When receiving webhooks FROM GoHighLevel**

```javascript
// Code node to verify GHL webhook signature
const crypto = require('crypto');

const signature = $json.headers['x-ghl-signature'];
const timestamp = $json.headers['x-ghl-timestamp'];
const body = JSON.stringify($json.body);
const webhookSecret = $env.GHL_WEBHOOK_SECRET;

// GHL signature format: timestamp.signature
const [receivedTimestamp, receivedSignature] = signature.split('.');

// Verify timestamp (prevent replay attacks)
const currentTime = Math.floor(Date.now() / 1000);
const timeDiff = currentTime - parseInt(receivedTimestamp);

if (timeDiff > 300) { // 5 minutes
  throw new Error('Webhook timestamp too old - possible replay attack');
}

// Verify signature
const signaturePayload = `${receivedTimestamp}.${body}`;
const expectedSignature = crypto
  .createHmac('sha256', webhookSecret)
  .update(signaturePayload)
  .digest('hex');

if (receivedSignature !== expectedSignature) {
  throw new Error('Invalid webhook signature');
}

// Signature valid, continue processing
return [{ json: $json.body }];
```

---

## Common Mistakes to Avoid

### Mistake 1: App Not Published
```
Symptom: "Please log in the serum" error when connecting
Cause: App in GHL developer portal is still in test/draft mode

Solution:
1. Go to GHL Developer Portal
2. Your app → Publishing/Audience section
3. Click "Publish App"
4. Wait 1-2 minutes
5. Try connecting in N8N again
```

### Mistake 2: Wrong Redirect URL
```
Symptom: "Redirect URI mismatch" error
Cause: N8N OAuth redirect URL doesn't match GHL app settings

Solution:
1. Get exact URL from N8N credential screen
2. Verify in GHL app settings (Advanced → OAuth → Redirect URL)
3. Must be exact match including https:// and path
4. Click Save in GHL after any change
```

### Mistake 3: Missing or Incorrect Scopes
```
Symptom: "Insufficient permissions" or operations fail after connecting
Cause: Required scopes not added to GHL app

Solution:
1. GHL Developer Portal → Your app → OAuth → Scopes
2. Add required scopes for your operations:
   - contacts.readonly + contacts.write for contact operations
   - opportunities.readonly + opportunities.write for pipeline operations
3. Click Save
4. Reconnect in N8N (old connection won't have new scopes)
```

### Mistake 4: Forgetting to Save in GHL Developer Portal
```
Symptom: Changes not taking effect
Cause: Clicked "Add" but didn't click "Save" at bottom of page

Solution:
- After adding redirect URLs, scopes, or any settings
- Scroll to bottom of page
- Click "Save" button
- Look for success confirmation
```

### Mistake 5: Using Wrong Account Type
```
Symptom: Can't access client locations
Cause: Using agency account instead of location account, or vice versa

Solution:
1. Understand your GHL structure:
   - Agency Account: Top-level management
   - Location/Sub-Account: Individual client accounts

2. For most automations, connect to specific location:
   - When authorizing in OAuth, select correct location from dropdown

3. For agency-level operations:
   - Use agency OAuth (requires different setup)
   - Most common use case is location-specific
```

### Mistake 6: Not Storing IDs as Environment Variables
```
Symptom: Hardcoded IDs in workflow, breaks when copying to new location
Cause: Location IDs, Pipeline IDs hardcoded instead of using variables

Solution:
Store in environment variables:
```yaml
# Railway → N8N Service → Variables
GHL_LOCATION_ID=your-location-id-here
GHL_PIPELINE_ID=your-pipeline-id-here
GHL_NEW_LEAD_STAGE_ID=first-stage-id
GHL_QUALIFIED_STAGE_ID=qualified-stage-id
GHL_SALES_USER_ID=assigned-user-id
```

Then use in workflows:
```
{{ $env.GHL_LOCATION_ID }}
{{ $env.GHL_PIPELINE_ID }}
```

### Mistake 7: Not Handling Duplicates
```
Symptom: Creating duplicate contacts
Cause: Not checking if contact exists before creating

Solution:
Always search before create:
1. GHL Node: Get All Contacts
   - Filters: {"email": "{{ $json.email }}"}
   - Limit: 1
2. IF Node: Check if contacts array has items
3. True → Update existing
4. False → Create new
```

### Mistake 8: Ignoring Rate Limits
```
Symptom: Random failures, "429 Too Many Requests" errors
Cause: Making too many API calls too quickly

Solution:
1. Add Wait nodes (500-1000ms) between GHL operations
2. Use Loop Over Items for batch operations
3. Implement batch processing (see Technique 1 above)
4. Add retry logic with exponential backoff
```

---

## Troubleshooting

### Issue 1: OAuth Connection Fails Completely
**Symptoms:** Can't get past OAuth screen, various errors

**Diagnosis Steps:**
1. Check app is published (not in test mode)
2. Verify redirect URL exact match
3. Verify Client ID and Secret correct (no extra spaces)
4. Check scopes are space-separated in N8N
5. Ensure N8N instance is accessible publicly (Railway, not localhost)

**Solutions by Error:**

**"Invalid client"**
- Regenerate Client ID and Secret in GHL
- Copy fresh credentials to N8N

**"Redirect URI mismatch"**
- Copy redirect URL from N8N
- Paste exactly in GHL (including https://)
- Save in GHL
- Try again

**"Please log in the serum"**
- Publish app in GHL Developer Portal
- Wait 2 minutes
- Clear browser cache
- Try again

### Issue 2: Can't Find Location ID
**Symptoms:** Don't know which Location ID to use

**Solution:**
```
Method 1: From GHL URL
- Log into GoHighLevel
- Navigate to any page for that location
- URL shows: https://app.gohighlevel.com/location/LOCATION_ID/...
- Copy LOCATION_ID part

Method 2: Using N8N
1. Create workflow
2. Add GoHighLevel node
3. Credential: [Your connected credential]
4. Resource: Location
5. Operation: Get All
6. Execute node
7. Response shows all locations with IDs
8. Copy desired location's "id" field
```

### Issue 3: Contact/Opportunity Not Appearing in GHL
**Symptoms:** Operation succeeds in N8N but data not in GHL

**Diagnosis:**
1. Check response in N8N execution:
   - Success should return object with "id" field
   - If no "id", operation failed (check error message)

2. Verify Location ID is correct:
   - Must match location you're viewing in GHL
   - Check environment variable value

3. Check GHL filters:
   - In GHL, remove all filters on contacts/opportunities
   - Search by email/name to find newly created item

4. Check tags/status:
   - Item might be created but filtered out by view settings
   - Look in "All Contacts" or "All Opportunities"

**Common Causes:**
- Wrong Location ID (created in different location)
- Item created but filtered from current view
- Missing required fields (check GHL custom field requirements)

### Issue 4: Updates Not Applying
**Symptoms:** Update operation succeeds but changes don't show

**Solutions:**
1. **Verify Contact/Opportunity ID:**
   ```javascript
   // In Code node before update
   console.log('Updating contact ID:', $json.contactId);

   if (!$json.contactId) {
     throw new Error('Contact ID is missing');
   }
   ```

2. **Check Field Names Match GHL:**
   - firstName (not first_name)
   - lastName (not last_name)
   - customFields is object (not array)

3. **Verify Fields are Updateable:**
   - Some GHL fields are read-only
   - Check GHL API documentation
   - Try updating via GHL UI first to confirm field is editable

4. **Force Refresh in GHL:**
   - Sometimes UI doesn't refresh immediately
   - Close and reopen contact record
   - Or hard refresh (Ctrl+Shift+R)

### Issue 5: Random 500 Errors from GHL API
**Symptoms:** Intermittent failures, not consistent

**Solutions:**
1. **Add Retry Logic:**
   ```yaml
   HTTP Request Node (or GHL Node):
   Options → Add Option → Retry on Fail
   Max Tries: 3
   Wait Between Tries: 2000 (ms)
   ```

2. **Implement Exponential Backoff:**
   - See Technique 3 above
   - Handles temporary API issues gracefully

3. **Check GHL Status:**
   - Visit status.gohighlevel.com
   - See if there are known API issues

4. **Contact GHL Support:**
   - If persistent 500 errors
   - Provide: Location ID, approximate timestamp, operation attempted

---

## Success Metrics

### Immediate Success (Day 1)
- ✅ Developer account created and logged in
- ✅ OAuth application created and published
- ✅ N8N successfully connected to GHL account
- ✅ Can read contacts from GHL
- ✅ Can create test contact from N8N
- ✅ Understanding of Location IDs and scopes

### Short-Term Success (Week 1)
- ✅ 3+ workflows integrating GHL with other platforms
- ✅ Form submissions automatically creating GHL contacts
- ✅ Opportunity creation workflow operational
- ✅ No OAuth connection issues
- ✅ Error handling implemented on GHL operations
- ✅ Team trained on GHL automation capabilities

### Long-Term Success (Month 1+)
- ✅ 10+ production GHL workflows running
- ✅ 95%+ success rate on GHL operations
- ✅ Bi-directional sync with external systems working
- ✅ Client satisfaction with automated lead management
- ✅ Reduced manual data entry by 80%+
- ✅ Can troubleshoot GHL integration issues independently

---

## Related Skills
- **build_n8n_workflow.md** - Core workflow building concepts
- **setup_n8n_triggers_agents.md** - Webhook and trigger setup for GHL integrations
- **setup_n8n_error_handling.md** - Critical for production GHL workflows
- **setup_n8n_google_oauth.md** - Similar OAuth setup process

---

**Skill Version:** 1.0
**Last Updated:** 2024
**Estimated Execution Time:** 60-90 minutes first time, 15-20 minutes after mastery
**Difficulty:** Intermediate
**Prerequisites:** N8N workflow understanding, basic OAuth knowledge
