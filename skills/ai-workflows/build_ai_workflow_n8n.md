# Building AI Workflows in N8N with Agents

## Overview

This comprehensive guide teaches you how to build production-ready AI automation workflows using N8N, AI agents, and integrated tools. Master the complete workflow architecture used in high-performing agency automations.

## Table of Contents

1. [Workflow Architecture Fundamentals](#workflow-architecture-fundamentals)
2. [N8N Setup and Configuration](#n8n-setup-and-configuration)
3. [AI Agent Integration Patterns](#ai-agent-integration-patterns)
4. [Complete Workflow Templates](#complete-workflow-templates)
5. [Error Handling and Monitoring](#error-handling-and-monitoring)
6. [Advanced Techniques](#advanced-techniques)

---

## Workflow Architecture Fundamentals

### Core Building Blocks

Every N8N AI workflow consists of these essential components:

#### 1. Trigger Nodes
**Purpose**: Initiate workflow execution

**Common Triggers**:
- **Webhook**: For external API calls, form submissions, Zapier integrations
- **Schedule**: For recurring tasks (daily prospect research, content generation)
- **Manual**: For testing and on-demand execution
- **Chat Message Received**: For interactive AI assistants
- **Platform-Specific**: Calendly events, Go High Level updates, Google Drive changes

**Webhook Setup Example**:
```
Method: POST
Authentication: None (for internal use) or Header Auth (for security)
Response Mode: "When Last Node Finishes"
Production URL: Use for live workflows
Test URL: Use during development
```

#### 2. Data Processing Nodes
**Purpose**: Transform, validate, and prepare data

**Essential Nodes**:
- **Set**: Manually define values and variables
- **Edit Fields**: Rename, transform, or extract specific data
- **Code**: JavaScript for complex transformations
- **Split/Merge**: Handle batch operations
- **IF/Switch**: Conditional routing based on logic
- **Loop Over Items**: Process arrays and lists

**Data Processing Pattern**:
```javascript
// Example: Extract and format prospect data
items.map(item => ({
  json: {
    prospectName: item.json.firstName + ' ' + item.json.lastName,
    companyName: item.json.company,
    email: item.json.email.toLowerCase(),
    researchDate: new Date().toISOString()
  }
}))
```

#### 3. AI Agent Nodes
**Purpose**: Perform intelligent operations

**Agent Components**:
- **Chat Model**: OpenRouter, Claude, GPT-4, etc.
- **System Prompt**: Define agent role and behavior
- **Tools**: Perplexity search, Reddit API, custom functions
- **Memory**: Store conversation context
- **Output Parsers**: Structure AI responses

#### 4. Integration Nodes
**Purpose**: Connect to external services

**Essential Integrations**:
- **Google Sheets**: Data storage and logging
- **Google Docs**: Document generation
- **Google Drive**: File organization
- **Slack**: Notifications and approvals
- **Gmail**: Email sending
- **CRM Systems**: Go High Level, HubSpot
- **APIs**: Custom HTTP requests

#### 5. Output Nodes
**Purpose**: Deliver results and notifications

**Common Outputs**:
- **Google Docs Creation**: MD2Docs for formatted documents
- **Slack Messages**: Notifications with links
- **Email Sending**: Gmail with HTML formatting
- **CRM Updates**: Contact and task creation
- **Webhook Response**: API endpoint responses

---

## N8N Setup and Configuration

### Cloud vs Self-Hosted Setup

#### N8N Cloud Setup
**Advantages**:
- Instant deployment
- Automatic updates
- Built-in OAuth for Google services
- No server management

**Setup Steps**:
1. Sign up at n8n.cloud
2. Create new workflow
3. Authenticate services via OAuth
4. Deploy and activate

#### Self-Hosted Setup
**Advantages**:
- Complete control
- No execution limits
- Custom security policies
- Cost-effective for high volume

**Docker Compose Setup**:
```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=secure_password
      - N8N_HOST=your-domain.com
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://your-domain.com/
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
```

**Google OAuth Setup for Self-Hosted**:
1. Go to Google Cloud Console (console.cloud.google.com)
2. Create new project
3. Enable APIs: Google Drive, Google Docs, Google Sheets, Gmail
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `https://your-n8n-domain.com/rest/oauth2-credential/callback`
6. In N8N, use "OAuth2 API" authentication method
7. Enter Client ID and Client Secret
8. Authorize and connect

### Essential API Integrations

#### OpenRouter Setup (AI Models)
**Purpose**: Access multiple AI models through one API

**Setup**:
1. Sign up at openrouter.ai
2. Generate API key from dashboard
3. In N8N, create "HTTP Request" credentials
4. Use Header Authentication
5. Header: `Authorization`
6. Value: `Bearer YOUR_API_KEY`

**Model Selection**:
- **Claude 3.5 Sonnet** (`anthropic/claude-3.5-sonnet`): Best for complex writing
- **GPT-4 Turbo** (`openai/gpt-4-turbo`): Great for structured tasks
- **DeepSeek R1 Free** (`deepseek/deepseek-r1`): Free for simple operations
- **Gemini 2.0 Flash** (`google/gemini-2.0-flash-exp:free`): Fast and free

#### Perplexity Setup (Research)
**Purpose**: AI-powered web search and research

**Setup**:
1. Sign up at perplexity.ai
2. Get API key from settings
3. In N8N Perplexity node, add API key
4. Configure search parameters:
   - Model: `sonar-pro` for detailed research
   - Return sources: Yes
   - Max tokens: 4000+

#### Go High Level Setup (CRM)
**Purpose**: Client management and task tracking

**Complex Setup Process**:
1. Sign up for Go High Level agency account
2. Go to Settings > API & Webhooks
3. Create API key with full permissions
4. In N8N, use "Go High Level OAuth2 API"
5. Enter Location ID (sub-account identifier)
6. Enter API Key
7. Test connection with "Get Contact" operation

**Common Operations**:
- Create Contact
- Update Contact
- Create Task
- Create Opportunity
- Add Tag
- Send Webhook

#### Slack Setup (Notifications)
**Purpose**: Team notifications and workflow approvals

**Setup**:
1. Create Slack workspace
2. In N8N, add Slack node
3. Click "Connect my account"
4. Authorize workspace access
5. Select channel or user

**Message Formatting**:
```markdown
*New Lead Generated!*
Name: {{$json["prospectName"]}}
Company: {{$json["companyName"]}}
Link: {{$json["documentUrl"]}}
```

#### Google Services Setup

**Google Sheets**:
- Store data, logs, and content calendars
- Use "Append" for adding rows
- Use "Update" for modifying existing data
- Use "Lookup" for searching records

**Google Docs**:
- Create formatted documents
- Use MD2Docs node for markdown conversion
- OAuth2 required for authentication

**Google Drive**:
- Organize files into client folders
- Use "Search" to find existing folders
- Use "Create Folder" for new clients
- Use "Move" to organize files

---

## AI Agent Integration Patterns

### Agent Architecture

#### Basic Agent Structure
```
AI Agent Node Configuration:
├── Chat Model: OpenRouter
├── System Prompt: Define role and expertise
├── Tools:
│   ├── Perplexity (Research)
│   ├── Reddit Search (Community insights)
│   ├── Custom functions
├── Memory: Window Buffer Memory
├── Output: JSON or Text
└── Error Handling: Fallback model
```

#### System Prompt Engineering

**Effective Prompt Structure**:
```
You are a [ROLE] specializing in [EXPERTISE].

Your responsibilities:
1. [Primary Task]
2. [Secondary Task]
3. [Quality Standards]

Context:
- [Relevant Information]
- [Constraints]
- [Success Criteria]

Output Requirements:
- Format: [JSON/Markdown/Text]
- Length: [Specific range]
- Style: [Professional/Casual/Technical]
- Must include: [Required elements]
```

**Example: Prospect Research Agent**
```
You are an expert B2B prospect research analyst specializing in creating comprehensive meeting preparation documents for business professionals.

Your responsibilities:
1. Analyze LinkedIn profiles and professional backgrounds
2. Identify key business challenges and opportunities
3. Research company context and market position
4. Generate actionable insights for sales conversations

You receive:
- Name: {{$json["prospectName"]}}
- Company: {{$json["companyName"]}}
- Position: {{$json["position"]}}
- LinkedIn URL: {{$json["linkedinUrl"]}}
- Previous Experience: {{$json["experience"]}}
- Education: {{$json["education"]}}

Research Focus:
- Current company trajectory and recent news
- Industry challenges and trends
- Personal career journey and achievements
- Potential pain points related to our solution
- Conversation starters and rapport-building topics

Output Format:
Generate a comprehensive meeting prep document with:
1. Executive Summary (3-4 sentences)
2. Professional Background
3. Company Context
4. Potential Pain Points
5. Recommended Talking Points
6. Questions to Ask

Maintain professional tone and cite sources where relevant.
```

**Example: Cold Email Icebreaker Writer**
```
You are an expert cold email icebreaker writer for B2B outreach campaigns.

Your goal is to write a highly personalized first line that:
1. References specific, recent activity or achievement
2. Shows genuine research (not generic compliments)
3. Creates curiosity and relevance
4. Flows naturally into the email body
5. Is 1-2 sentences maximum

You receive:
- Prospect Name: {{$json["prospectName"]}}
- Company: {{$json["companyName"]}}
- Research Analysis: {{$json["researchReport"]}}
- Email Body Context: {{$json["emailBody"]}}

Research Analysis Format:
The research analysis contains specific information about:
- Recent company news or achievements
- Prospect's content (podcasts, posts, articles)
- Professional background and expertise
- Company initiatives and projects

Writing Guidelines:
- Be specific, not generic ("saw your company" is weak)
- Reference something recent (last 3 months)
- Show you understand their world
- Create natural transition to email body
- Avoid over-the-top flattery
- No asking questions in icebreaker

GOOD Examples:
"Loved your breakdown on scaling agencies to 10K MRR in 6 months on The Sauce podcast - the content flywheel strategy especially resonated."

"Noticed you just launched the new AI-powered analytics dashboard last week - the real-time cohort analysis feature looks game-changing."

BAD Examples:
"I love what you're doing at [Company]" (too generic)
"Your company is amazing!" (no specificity)
"Can I ask you about [topic]?" (don't ask in icebreaker)

Output:
Provide only the icebreaker text, no explanation or formatting.
```

### Multi-Agent Workflows

#### Sequential Agent Pattern
**Use Case**: Complex tasks requiring specialized expertise at each stage

**Structure**:
```
Input Data
    ↓
Research Agent (Gather information)
    ↓
Analysis Agent (Process findings)
    ↓
Writing Agent (Create output)
    ↓
Quality Check Agent (Review)
    ↓
Final Output
```

**Example: VSL Script Creation**
1. **Hook Agent**: Creates 3 opening hook variations
2. **Story Agent**: Builds narrative architecture
3. **Objection Handler**: Addresses common concerns
4. **CTA Agent**: Crafts compelling call-to-action
5. **Compiler**: Assembles complete script

#### Parallel Agent Pattern
**Use Case**: Generate multiple content pieces simultaneously

**Structure**:
```
Input Transcript
    ↓
    ├── YouTube Script Agent → Doc Creation
    ├── LinkedIn Post Agent → Doc Creation
    ├── Twitter Thread Agent → Doc Creation
    └── Newsletter Agent → Doc Creation
```

#### Agent with Tools Pattern
**Use Case**: Agents that need external information

**Configuration**:
```javascript
AI Agent Node Settings:
{
  "chatModel": "openrouter",
  "model": "anthropic/claude-3.5-sonnet",
  "systemPrompt": "{{$json['systemPrompt']}}",
  "tools": [
    {
      "type": "perplexity",
      "name": "web_search",
      "description": "Search the web for current information"
    },
    {
      "type": "reddit",
      "name": "community_insights",
      "description": "Search Reddit for community discussions"
    }
  ],
  "memory": {
    "type": "bufferWindowMemory",
    "sessionId": "{{$json['sessionId']}}",
    "contextWindowLength": 5
  }
}
```

### Memory and Context Management

#### Session Management
```javascript
// Generate unique session ID
const sessionId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

return [{
  json: {
    sessionId: sessionId,
    timestamp: new Date().toISOString()
  }
}];
```

#### Buffer Window Memory
**Purpose**: Keep recent conversation context

**Configuration**:
- Context Window: 5-10 messages
- Session ID: Unique per workflow execution
- Use Case: Multi-turn conversations, iterative refinement

#### Persistent Memory
**Purpose**: Remember information across workflow runs

**Implementation**:
- Store in Google Sheets or database
- Load context at workflow start
- Update at workflow end

---

## Complete Workflow Templates

### Template 1: Cold Email Mass Personalizer

**Workflow Purpose**: Generate personalized cold email campaigns at scale

**Architecture Overview**:
```
Form Submission (Sender info, email body, lead list CSV)
    ↓
Process CSV (Parse leads)
    ↓
Create Google Sheet (Campaign storage)
    ↓
Loop Over Leads:
    ├── Research Agent (Perplexity-powered prospect research)
    ├── Icebreaker Writer (Personalized first line)
    ├── Format Email (Combine icebreaker + body)
    └── Append to Sheet (Store results)
    ↓
Slack Notification (Campaign complete)
```

**Node-by-Node Breakdown**:

**1. Form Submission Node**
```
Fields:
- Sender Name: Text
- Sender Title: Text
- Email Script Body: Long Text
- Lead List: CSV Upload
```

**2. Read Binary File (Process CSV)**
```
Convert uploaded CSV to JSON array with fields:
- firstName
- lastName
- email
- company
- linkedinUrl (optional)
```

**3. Create Blank Sheet**
```
Google Sheets: Create Spreadsheet
Name: "Cold Email Campaign - {{$now.format('YYYY-MM-DD')}}"
```

**4. Loop Over Items**
```
For each prospect:
- Extract name, company, email
- Pass to research agent
```

**5. Prospect Research Agent**
```
System Prompt:
"You are a prospect research specialist. Research this prospect and provide relevant information for cold email personalization."

Input:
Name: {{$json["firstName"]}} {{$json["lastName"]}}
Company: {{$json["company"]}}
LinkedIn: {{$json["linkedinUrl"]}}

Tools:
- Perplexity search (enabled)

Output:
Detailed research report including:
- Recent activity
- Company news
- Professional background
- Potential pain points
```

**6. Icebreaker Writer Agent**
```
System Prompt:
[Use icebreaker prompt from earlier section]

Input:
- Prospect Name
- Company
- Research Analysis
- Email Body (for context)

Output:
1-2 sentence personalized icebreaker
```

**7. Format Final Email**
```javascript
// Code node to combine icebreaker + body
const icebreaker = $json["icebreaker"];
const emailBody = $input.first().json["emailBody"];
const prospectName = $json["prospectName"];

const finalEmail = `Hi ${prospectName.split(' ')[0]}, ${icebreaker}\n\n${emailBody}`;

return [{
  json: {
    prospectName: $json["prospectName"],
    prospectEmail: $json["email"],
    companyName: $json["company"],
    icebreaker: icebreaker,
    emailBody: emailBody,
    personalizedEmail: finalEmail
  }
}];
```

**8. Append to Google Sheet**
```
Columns:
- Prospect Name
- Prospect Email
- Company Name
- Icebreaker
- Email Body
- Personalized Email
```

**9. Slack Notification**
```markdown
*Cold Email Campaign Complete!*

Campaign: {{$node["Create Blank Sheet"].json["spreadsheetUrl"]}}
Leads Processed: {{$json["itemsProcessed"]}}

Next Steps:
1. Review personalized emails
2. Download as CSV
3. Upload to Smartlead/Instantly
4. Map custom fields
```

**Usage Instructions**:
1. Fill form with sender details and email body template
2. Upload CSV with columns: firstName, lastName, email, company
3. Workflow researches each prospect
4. Generates personalized first lines
5. Outputs to Google Sheet
6. Download CSV and upload to email sending tool
7. Map "icebreaker" column as custom variable in email template

---

### Template 2: Booked Meeting Research & Notification

**Workflow Purpose**: Automatically research prospects when they book meetings

**Architecture Overview**:
```
Calendly Webhook (New meeting booked)
    ↓
Search Go High Level CRM (Check existing contact)
    ↓
├── Existing Lead → Update Status
└── New Lead → Create Contact + Opportunity
    ↓
Enrichment Process:
    ├── Explorium Match (Find contact data)
    ├── Explorium Enrich (Get detailed profile)
    └── Format Bio (Structure information)
    ↓
AI Research Agent (Generate meeting prep document)
    ↓
Output:
    ├── Email with HTML Report
    ├── Google Doc with Research
    └── Slack Notification
```

**Node-by-Node Breakdown**:

**1. Calendly Trigger**
```
Setup:
1. Create Calendly Developer Account (developer.calendly.com)
2. Create OAuth App
3. Copy OAuth Redirect URL from N8N
4. Get Client ID and Client Secret
5. In N8N Calendly node, use OAuth2
6. Trigger: On "invitee.created" event
```

**2. Go High Level CRM Search**
```
Operation: Search Contacts
Field: Email
Value: {{$json["email"]}}

Returns: Existing contact or empty result
```

**3. Conditional Branch (IF Node)**
```
Condition: {{$json["contacts"].length}} > 0

True Branch:
  → Get Contact Details
  → Update Contact Status to "Meeting Booked"

False Branch:
  → Create New Contact
  → Create Opportunity in CRM
```

**4. Explorium Match Prospects**
```
API Call: POST to https://api.explorium.ai/v1/match
Headers:
- Authorization: Bearer {{$credentials.explorium}}

Body:
{
  "email": "{{$json['email']}}",
  "name": "{{$json['name']}}",
  "company": "{{$json['company']}}"
}

Returns: Prospect ID for enrichment
```

**5. Explorium Enrich Profile**
```
API Call: POST to https://api.explorium.ai/v1/enrich
Body:
{
  "prospect_ids": ["{{$json['prospectId']}}"]
}

Returns:
- LinkedIn URL
- Job title
- Company details
- Previous experience
- Education
- Contact information
```

**6. Format Bio (Code Node)**
```javascript
// Structure enriched data for AI agent
const profile = $json["enrichedData"];

const bio = {
  name: profile.fullName,
  city: profile.location.city,
  country: profile.location.country,
  currentPosition: profile.currentJob.title,
  currentCompany: profile.currentJob.company,
  companyDescription: profile.currentJob.description,
  previousExperience: profile.workHistory.map(job => ({
    title: job.title,
    company: job.company,
    duration: job.duration
  })),
  linkedinUrl: profile.linkedinUrl,
  education: profile.education.map(edu => ({
    degree: edu.degree,
    school: edu.school,
    year: edu.year
  }))
};

return [{ json: bio }];
```

**7. AI Meeting Prep Agent**
```
System Prompt:
"You are an AI agent specializing in generating meeting preparation documents for business professionals.

You will receive a JSON object containing LinkedIn profile information. Your task is to:
1. Analyze the prospect's professional background
2. Identify relevant talking points
3. Suggest questions to ask
4. Highlight potential pain points
5. Recommend conversation approaches

Generate a comprehensive meeting preparation document."

Input Data:
{{$json["bio"]}}

Tools:
- Perplexity (for additional company research)

Output Format: Markdown document with sections:
1. Executive Summary
2. Professional Background
3. Company Context
4. Recommended Talking Points
5. Questions to Ask
6. Potential Objections
```

**8. Create HTML Email Report**
```javascript
// Code node to convert markdown to HTML
const markdown = $json["meetingPrepDocument"];

// Simple markdown to HTML conversion
let html = markdown
  .replace(/^# (.*$)/gim, '<h1>$1</h1>')
  .replace(/^## (.*$)/gim, '<h2>$1</h2>')
  .replace(/^### (.*$)/gim, '<h3>$1</h3>')
  .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
  .replace(/\*(.*)\*/gim, '<em>$1</em>')
  .replace(/\n/gim, '<br>');

return [{
  json: {
    htmlContent: `
      <html>
        <body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
          <h1 style="color: #2c3e50;">Meeting Prep: ${$json["prospectName"]}</h1>
          <p><strong>Date:</strong> ${$json["meetingDate"]}</p>
          ${html}
        </body>
      </html>
    `
  }
}];
```

**9. Send Email**
```
Gmail: Send Email
To: {{$json["clientEmail"]}} (or your own email)
Subject: "New Meeting Booked: {{$json['prospectName']}}"
Body (HTML): {{$json["htmlContent"]}}
```

**10. Create Google Doc**
```
MD2Docs: Create Document
Document Name: "Meeting Prep - {{$json['prospectName']}} - {{$now.format('YYYY-MM-DD')}}"
Content: {{$json["meetingPrepDocument"]}}
```

**11. Move to Prospect Research Folder**
```
Google Drive: Move File
File ID: {{$json["documentId"]}}
Folder Name: "Prospect Research" (create this folder in advance)
```

**12. Slack Notification**
```markdown
*New Call Booked!*

📅 Date: {{$json["meetingDate"]}}
📝 Call Title: {{$json["eventType"]}}
👤 Prospect: {{$json["prospectName"]}}
🏢 Company: {{$json["companyName"]}}
📧 Email: {{$json["email"]}}

📄 Research Document: {{$json["documentUrl"]}}
```

**Setup Requirements**:
1. Calendly OAuth App configured
2. Explorium API account and key
3. Go High Level CRM connected
4. Google Workspace authenticated
5. Slack workspace connected
6. Create "Prospect Research" folder in Google Drive

---

### Template 3: AI Client Onboarding Automation

**Workflow Purpose**: Automate new client onboarding with task creation and team notifications

**Architecture Overview**:
```
Form Submission (Client details, scope)
    ↓
Check PDF Upload:
    ├── PDF Provided → Extract Text
    └── No PDF → Use Form Text
    ↓
Create Google Drive Folder (Client workspace)
    ↓
Create Go High Level Contact
    ↓
AI Task Generation Agent (Break down project)
    ↓
Loop: Create Tasks in CRM
    ↓
Team Setup:
    ├── Create Slack Channel
    ├── Post Welcome Message
    └── Send Welcome Email
    ↓
Log to Project Tracker
```

**Node-by-Node Breakdown**:

**1. Onboarding Form**
```
Fields:
- Client Name: Text
- Client Email: Email
- Company Name: Text
- Website: URL
- PDF Proposal Upload: File (optional)
- Client Information and Tasks: Long Text (alternative to PDF)

Example Text Input:
"Paid 50% of $10,000 starting fee. Creating new website and VSL.
Setting up funnel. Setting up Google Analytics. Need Google account
login details. Need to write copy based on their current products."
```

**2. Check for PDF (IF Node)**
```
Condition: {{$json["pdfFile"]}} !== undefined

True Branch: Extract PDF Text
False Branch: Use form text input
```

**3. Extract PDF Text (if uploaded)**
```
Node: Extract from File
Binary Property: pdfFile
Output: Text content
```

**4. Create Main Client Folder**
```
Google Drive: Create Folder
Folder Name: "{{$json['companyName']}}"
Parent Folder: "Clients" (create this folder first)
```

**5. Create Contact in Go High Level**
```
Operation: Create Contact
Fields:
- First Name: {{$json["clientName"].split(' ')[0]}}
- Last Name: {{$json["clientName"].split(' ').slice(1).join(' ')}}
- Email: {{$json["email"]}}
- Company Name: {{$json["companyName"]}}
- Website: {{$json["website"]}}
- Tags: ["Active Client", "Onboarding"]
- Source: "Direct Sign Up"
```

**6. AI Task Breakdown Agent**
```
System Prompt:
"You are a project management AI that breaks down client projects into actionable tasks.

You will receive information about a new client engagement including:
- Services provided
- Payment details
- Project scope
- Requirements

Your task:
1. Analyze the project scope
2. Break it down into specific, actionable tasks
3. Organize tasks by logical sequence
4. Include any prerequisites or dependencies

Output a JSON array of tasks with:
- title: Clear, actionable task name
- description: Detailed description
- priority: high, medium, or low
- estimatedHours: Rough time estimate
- dependencies: Array of prerequisite tasks (if any)

Focus on deliverables the client expects. Include tasks for:
- Gathering information/assets from client
- Technical setup and configuration
- Creative work (design, copy, content)
- Review and approval stages
- Handoff and training
"

Input:
{{$json["clientInformation"]}} or {{$json["pdfText"]}}

Output Format: JSON array
[
  {
    "title": "Create client payment schedule",
    "description": "Set up recurring payment tracking for remaining $5,000",
    "priority": "high",
    "estimatedHours": 1
  },
  {
    "title": "Request Google account access",
    "description": "Email client for Google Analytics and Google Ads login credentials",
    "priority": "high",
    "estimatedHours": 0.5
  },
  {
    "title": "Create website project brief",
    "description": "Document website goals, pages, desired functionality, and design preferences",
    "priority": "high",
    "estimatedHours": 2
  }
]
```

**7. Split Out to Array**
```
Node: Split Out
Field: tasks
Output: Individual task objects
```

**8. Loop Over Tasks: Create in Go High Level**
```
Loop node processing each task:

Go High Level: Create Task
Fields:
- Title: {{$json["title"]}}
- Description: {{$json["description"]}}
- Contact ID: {{$node["Create Contact"].json["contactId"]}}
- Due Date: {{$now.plus(7, 'days').format('YYYY-MM-DD')}}
- Status: "Open"
- Priority: {{$json["priority"]}}
```

**9. Aggregate (Wait for all tasks)**
```
Node: Aggregate
Wait for all loop items to complete before proceeding
```

**10. Create Slack Channel**
```
Slack: Create Channel
Channel Name: "{{$json['companyName'].toLowerCase().replace(/\s+/g, '-')}}"
Purpose: "Client workspace for {{$json['companyName']}}"
Is Private: false
```

**11. Post Welcome Message to Channel**
```
Slack: Post Message
Channel: {{$json["channelId"]}}
Message:
"👋 Welcome to {{$json['companyName']}}!

We're excited to kick off this project. This channel will be our central place for communication, updates, and collaboration throughout your journey with us.

✅ Next Steps:
- Kickoff call scheduled
- Project tasks created in CRM
- Google Drive workspace set up

Let's crush it! 🚀"
```

**12. Send Welcome Email**
```
Gmail: Send Email
To: {{$json["clientEmail"]}}
Subject: "Welcome to [Your Agency Name]!"
Body (HTML):
"Hi {{$json['clientName']}},

Welcome aboard! Your project workspace is now live and ready to go.

📌 Quick Links:
- Google Drive Folder: {{$json['driveFolderUrl']}}
- Slack Channel: {{$json['slackChannelUrl']}}
- Schedule Your Onboarding Call: [YOUR CALENDLY LINK]

📋 What's Next:
We've created a detailed project plan with all the tasks needed to bring your vision to life. You'll receive invites to:
1. Join our Slack workspace
2. Access your Google Drive folder
3. Schedule your onboarding call

During the onboarding call, we'll:
- Walk through the project timeline
- Gather any necessary assets or information
- Answer your questions
- Align on next steps

Looking forward to working together!

Best regards,
[Your Name]
[Your Agency]
[Your Website]"
```

**Setup Requirements**:
1. Create "Clients" folder in Google Drive
2. Go High Level CRM configured
3. Slack workspace set up
4. Gmail connected
5. OpenRouter API for task generation

**Workflow Activation**:
1. Set workflow to "Active"
2. Share form URL with sales team
3. When client signs up, fill out form
4. Workflow handles everything automatically

---

### Template 4: Automated Prospect List Builder with SURF

**Workflow Purpose**: Build enriched prospect lists using AI-powered search

**Architecture Overview**:
```
Form Submission (ICP criteria)
    ↓
Search ICP Companies (SURF API)
    ↓
Prepare Prospect Data
    ↓
Search Employees in Companies (SURF API)
    ↓
Prepare Enrichment Request
    ↓
Enrich Prospects (Get contact details)
    ↓
Check Enrichment Status (Loop until complete)
    ↓
Extract People List
    ↓
Add to Go High Level CRM
    ↓
Email Notification
```

**Node-by-Node Breakdown**:

**1. Prospect Criteria Form**
```
Fields:
- Industry: Text (e.g., "SaaS", "E-commerce", "Marketing Agencies")
- Max Employee Count: Number
- Country Code: Dropdown (US, UK, CA, AU, etc.)
- Your Name: Text
- Your Email: Email
```

**2. Set Prospect Data**
```
Code Node:
return [{
  json: {
    industry: $json["industry"],
    maxEmployees: $json["maxEmployeeCount"],
    country: $json["countryCode"],
    userName: $json["yourName"],
    userEmail: $json["yourEmail"]
  }
}];
```

**3. Search ICP Companies (SURF API)**
```
HTTP Request Node:
Method: POST
URL: https://api.surfe.com/v2/company/search
Authentication: Header Auth
  - Name: Authorization
  - Value: [YOUR SURF API KEY]

Body (JSON):
{
  "filters": {
    "industry": "{{$json['industry']}}",
    "employee_count_max": {{$json["maxEmployees"]}},
    "country": "{{$json['country']}}"
  },
  "limit": 20
}

Returns: Array of companies with domains
```

**4. Prepare JSON Payload**
```
Code Node:
// Extract company names and domains
const companies = $json["companies"].map(company => ({
  name: company.name,
  domain: company.domain
}));

return [{
  json: { companies: companies }
}];
```

**5. Search for Employees (SURF API)**
```
HTTP Request Node:
Method: POST
URL: https://api.surfe.com/v2/person/search
Authentication: Header Auth
  - Name: Authorization
  - Value: [YOUR SURF API KEY]

Body (JSON):
{
  "company_domain": "{{$json['domain']}}",
  "job_titles": ["CEO", "Founder", "Owner", "Marketing Director", "CMO"],
  "limit": 5
}

Returns: Array of employees with LinkedIn profiles
```

**6. Prepare Enrichment Request**
```
Code Node:
// Format person IDs for enrichment
const personIds = $json["persons"].map(person => person.id);

return [{
  json: {
    personIds: personIds,
    companyDomain: $json["companyDomain"]
  }
}];
```

**7. Enrich Prospects (SURF API)**
```
HTTP Request Node:
Method: POST
URL: https://api.surfe.com/v2/enrich
Authentication: Header Auth
  - Name: Authorization
  - Value: [YOUR SURF API KEY]

Body (JSON):
{
  "person_ids": {{$json["personIds"]}},
  "fields": ["email", "phone", "linkedin_url", "job_title", "location"]
}

Returns: Enrichment job ID
```

**8. Check Enrichment Status (Loop)**
```
Setup: Loop with Wait node

HTTP Request Node:
Method: GET
URL: https://api.surfe.com/v2/enrich/{{$json['enrichmentId']}}
Authentication: Header Auth

IF Node:
Condition: {{$json["status"]}} === "completed"
  True → Continue to next step
  False → Wait 3 seconds, check again
```

**9. Extract People List**
```
Code Node:
// Parse enriched data
const people = $json["enrichmentResults"].map(person => ({
  firstName: person.first_name,
  lastName: person.last_name,
  email: person.email,
  phone: person.phone,
  linkedinUrl: person.linkedin_url,
  jobTitle: person.job_title,
  company: person.company_name,
  location: person.location
}));

return people.map(person => ({ json: person }));
```

**10. Add to Go High Level CRM**
```
Loop over each person:

Go High Level: Create Contact
Fields:
- First Name: {{$json["firstName"]}}
- Last Name: {{$json["lastName"]}}
- Email: {{$json["email"]}}
- Phone: {{$json["phone"]}}
- Company Name: {{$json["company"]}}
- Source: "SURF Prospecting"
- Tags: ["Prospect", "{{$json['industry']}}"]
- Custom Fields:
  - LinkedIn: {{$json["linkedinUrl"]}}
  - Job Title: {{$json["jobTitle"]}}
```

**11. Email Notification**
```
Gmail: Send Email
To: {{$node["Set Prospect Data"].json["userEmail"]}}
Subject: "Prospect Enrichment Complete"
Body:
"Your prospect enrichment is complete!

Industry: {{$json['industry']}}
Prospects Added: {{$json['totalProspects']}}

Check your Go High Level CRM to view the new contacts.

Next steps:
1. Review prospect list
2. Filter by job title/company
3. Launch cold email campaign"
```

**SURF API Setup**:
1. Sign up at surfe.com
2. Go to Settings → API
3. Generate API key
4. In N8N HTTP Request nodes, use Header Auth
5. Header name: "Authorization"
6. Value: Paste your SURF API key

**Alternative: Schedule-Based Prospecting**
Replace Form Trigger with Schedule Trigger:
- Runs every 24 hours
- Hard-code ICP criteria in "Set Prospect Data" node
- Automatically enriches X prospects daily
- Keeps your CRM fresh with leads

---

### Template 5: Multi-Platform Content Factory

**Workflow Purpose**: Transform call transcripts into multi-platform content

**Architecture Overview**:
```
Trigger:
├── Webhook (Fathom via Zapier) [Automated]
└── Chat Message [Manual Paste]
    ↓
Content Generation (Parallel):
├── YouTube Script Agent → Create Doc → Move to Folder → Notify
├── LinkedIn Post Agent → Create Doc → Move → Approve → Schedule
├── Twitter Thread Agent → Create Doc → Move → Approve → Schedule
└── Newsletter Agent → Create Doc → Move → Approve → Add to ConvertKit
    ↓
Log to Content Calendar (Google Sheets)
```

**Node-by-Node Breakdown**:

**1A. Webhook Trigger (Automated)**
```
Setup Zapier Integration:
1. Create Zap: Fathom → Webhooks by Zapier
2. Trigger: New Transcript in Fathom
3. Action: POST Webhook
4. URL: [N8N Webhook URL]
5. Method: POST
6. Data:
   - transcript: {{transcript}}
   - title: {{title}}
   - duration: {{duration}}
   - date: {{date}}
```

**1B. Chat Message Trigger (Manual)**
```
Node: When Chat Message Received
Opens chat interface at bottom of N8N
User pastes call transcript directly
Workflow processes immediately
```

**2. YouTube Script Agent**
```
System Prompt:
"You are an expert YouTube script writer who transforms raw transcripts into engaging, structured video scripts.

Your task:
1. Analyze the call transcript
2. Identify key insights and teaching moments
3. Structure content with strong hook, body, and CTA
4. Add timestamps and visual cues
5. Optimize for watch time and engagement

Script Structure:
- Hook (0-15 seconds): Attention-grabbing opener
- Introduction (15-45 seconds): What viewers will learn
- Main Content (80% of video): Core teaching with examples
- Recap (Last 60 seconds): Summary of key points
- CTA: Like, subscribe, and next action

Writing Style:
- Conversational and energetic
- Direct address to viewer ("you")
- Short sentences and paragraphs
- Include [VISUAL CUE] notes for editor
- Add emphasis with CAPS for key words

Output: Full YouTube script in markdown format"

Input: {{$json["transcript"]}}

Model: Claude 3.5 Sonnet (best for long-form writing)
Max Tokens: 4000
```

**3. Create YouTube Script Title**
```
AI Agent (DeepSeek R1 Free model):

Prompt:
"Create a compelling YouTube video title based on this script.
Requirements:
- 50-70 characters
- Include curiosity gap
- Use power words
- Optimize for CTR

Script excerpt: {{$json['scriptExcerpt']}}"

Output: Video title only
```

**4. Create Google Doc (YouTube)**
```
MD2Docs: Create from Markdown
Document Name: "YouTube - {{$json['title']}} - {{$now.format('YYYY-MM-DD')}}"
Content: {{$json["scriptContent"]}}

Returns: Document ID and URL
```

**5. Move to YouTube Scripts Folder**
```
Google Drive: Move File
File: {{$json["documentId"]}}
Destination: "YouTube Scripts" (create folder first)
```

**6. Slack Notification**
```
Slack: Send Message to User
User: @your-username
Message:
"📺 *YouTube Script Ready!*

Title: {{$json['title']}}
Duration: ~{{$json['estimatedMinutes']}} minutes

📄 Script: {{$json['documentUrl']}}

Next: Record, edit, and schedule"
```

**7. Prepare YouTube Content for Calendar**
```
Code Node:
return [{
  json: {
    platform: "YouTube",
    contentType: "Video Script",
    title: $json["title"],
    documentUrl: $json["documentUrl"],
    date: new Date().toISOString()
  }
}];
```

**8. Log to Content Calendar**
```
Google Sheets: Append Row
Spreadsheet: "Content Calendar" (create with columns: Platform, Date, Link, Title)
Values:
- Platform: {{$json["platform"]}}
- Date: {{$json["date"]}}
- Link: {{$json["documentUrl"]}}
- Title: {{$json["title"]}}
```

**9-16. LinkedIn Post Agent** (Parallel Branch)
```
System Prompt:
"You are a LinkedIn content strategist who creates engaging professional posts.

Transform this transcript into a LinkedIn post that:
1. Hooks attention in first line
2. Delivers value and insights
3. Uses line breaks for readability
4. Includes relevant emoji (sparingly)
5. Ends with engaging question or CTA
6. Optimal length: 150-300 words

Format:
- Short paragraphs (1-2 sentences)
- Use bullet points for lists
- Bold key phrases
- Add 3-5 relevant hashtags

Tone: Professional but conversational"

Input: {{$json["transcript"]}}
Output: LinkedIn post in markdown

→ Create Title
→ Create Google Doc
→ Move to "LinkedIn Posts" folder
→ Send Slack message with preview
→ Wait for Approval
→ IF Approved: Schedule via Blotato
→ Log to Content Calendar
```

**Blotato Scheduling Setup**:
```
Install Community Node: n8n-nodes-blotato
1. Click + in workflow
2. Search "blotato"
3. Click "Install Community Node"

Blotato Node Configuration:
- Operation: Create Post
- Platform: LinkedIn
- Content: {{$json["postContent"]}}
- Schedule: Queue (posts at optimal time)

Authentication:
1. Sign up at blotato.com
2. Connect LinkedIn account
3. Get API key from settings
4. In N8N, use API key authentication
```

**17-24. Twitter Thread Agent** (Parallel Branch)
```
System Prompt:
"You are a Twitter/X content expert who creates viral thread hooks and engaging threads.

Transform this transcript into a Twitter thread (8-12 tweets) that:
1. Opens with pattern-interrupt hook
2. Breaks down insights into tweetable chunks
3. Uses curiosity gaps between tweets
4. Includes relevant hashtags (max 2 per tweet)
5. Ends with strong CTA

Format:
Tweet 1: Hook (make them NEED to read more)
Tweet 2-10: Core content (one idea per tweet)
Final Tweet: CTA + call for engagement

Each tweet:
- Max 280 characters
- Can include line breaks
- Number tweets (1/12, 2/12, etc.)

Output: Numbered thread in markdown"

Input: {{$json["transcript"]}}

→ Create Title
→ Create Google Doc
→ Move to "Twitter Posts" folder
→ Send Slack message with preview
→ Wait for Approval
→ IF Approved: Schedule via Blotato
→ Log to Content Calendar
```

**25-32. Newsletter Agent** (Parallel Branch)
```
System Prompt:
"You are an email newsletter writer who creates engaging, value-packed content.

Transform this transcript into an email newsletter that:
1. Compelling subject line
2. Personal opening (like talking to friend)
3. Main insights with examples
4. Actionable takeaways
5. Clear CTA
6. P.S. with additional value or humor

Structure:
- Subject Line
- Preheader Text (50 characters)
- Opening (build rapport)
- Main Content (3-5 key points)
- Recap/Action Steps
- CTA
- P.S.

Length: 400-800 words
Tone: Helpful expert and friend hybrid"

Input: {{$json["transcript"]}}

→ Create Title
→ Create Google Doc
→ Move to "Newsletters" folder
→ Send Slack message with preview
→ Wait for Approval
→ IF Approved: Create Draft in ConvertKit
→ Log to Content Calendar
```

**ConvertKit Setup**:
```
ConvertKit Node Configuration:
- Operation: Create Broadcast (draft)
- Subject: {{$json["subjectLine"]}}
- Preheader: {{$json["preheader"]}}
- Content: {{$json["newsletterContent"]}}
- Status: draft

Authentication:
1. Sign up at convertkit.com
2. Go to Settings → API
3. Copy API Secret
4. In N8N ConvertKit node, paste API key
```

**Approval Pattern** (Used for LinkedIn, Twitter, Newsletter):
```
Send Slack Message:
"[Platform] Post Ready for Review

Preview:
{{$json['contentPreview']}}

📄 Full Document: {{$json['documentUrl']}}

Reply 'approve' to schedule, or 'skip' to pass."

→ Wait for Message Reply
→ IF message contains "approve":
    → Schedule via Blotato (or ConvertKit)
→ ELSE:
    → End branch (skip scheduling)
```

**Content Calendar Sheet Setup**:
Create Google Sheet named "Content Calendar"
Columns:
- Platform (YouTube, LinkedIn, Twitter, Newsletter)
- Date (auto-generated timestamp)
- Link (Google Doc URL)
- Title
- Status (Created, Scheduled, Published)

**Full Setup Requirements**:
1. Google Drive folders: "YouTube Scripts", "LinkedIn Posts", "Twitter Posts", "Newsletters"
2. Google Sheet: "Content Calendar" with proper columns
3. Slack workspace connected
4. Blotato account + API key + platforms connected
5. ConvertKit account + API key
6. OpenRouter account for AI models
7. Optional: Fathom + Zapier for automation

**Usage**:
- **Automated**: Fathom records call → Zapier sends transcript → Workflow runs → 4 pieces of content created
- **Manual**: Paste transcript in chat interface → Workflow runs → Content generated

**Customization Options**:
- Change AI models per content type
- Adjust post lengths and styles
- Add more platforms (Instagram, TikTok, etc.)
- Skip approval for YouTube (no scheduling needed)
- Auto-approve certain content types

---

## Error Handling and Monitoring

### Error Handling Strategies

#### 1. Try-Catch Pattern
```
Main Workflow Path
    ↓
[Try]
    ↓
Critical Operation
    ↓
[Error Trigger]
    ↓
├── Log Error to Sheet
├── Send Slack Alert
└── Notify Admin
```

#### 2. Fallback AI Models
```
AI Agent Configuration:
- Primary Model: Claude 3.5 Sonnet
- Enable Fallback Model: Yes
- Fallback Model: Gemini 2.0 Flash Pro

Use Case:
If Claude hits token limit or rate limit,
automatically retry with Gemini
```

**Configuration**:
```
In AI Agent Node:
1. Select primary model
2. Scroll to "Advanced Options"
3. Toggle "Enable fallback model"
4. Select fallback model (larger context window)
```

#### 3. API Rate Limit Handling
```
HTTP Request Node Settings:
- Timeout: 30000 (30 seconds)
- Retry on Fail: Yes
- Max Retries: 3
- Retry Wait: 5000 (5 seconds between retries)
```

#### 4. Conditional Error Routes
```
IF Node:
Condition: {{$json["status"]}} === "error"

True Path:
  → Log error details
  → Send alert
  → Try alternative method

False Path:
  → Continue normal workflow
```

#### 5. Data Validation
```
Code Node (Validate Input):
// Check required fields before processing
const requiredFields = ['email', 'name', 'company'];
const missingFields = [];

for (const field of requiredFields) {
  if (!$json[field] || $json[field].trim() === '') {
    missingFields.push(field);
  }
}

if (missingFields.length > 0) {
  throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
}

return $input.all();
```

### Monitoring and Alerts

#### 1. Slack Error Notifications
```
Error Trigger Node:
Connected to main workflow

Slack: Send Message
Channel: #n8n-alerts
Message:
"🚨 *Workflow Error*

Workflow: {{$workflow.name}}
Execution: {{$execution.id}}
Error: {{$json['error']['message']}}
Node: {{$json['node']['name']}}
Time: {{$now.format('YYYY-MM-DD HH:mm:ss')}}

Check N8N dashboard for details."
```

#### 2. Google Sheets Error Log
```
Google Sheets: Append Row
Sheet: "N8N Error Log"
Columns:
- Timestamp: {{$now.format()}}
- Workflow: {{$workflow.name}}
- Node: {{$json['node']['name']}}
- Error Message: {{$json['error']['message']}}
- Input Data: {{JSON.stringify($json)}}
- Execution ID: {{$execution.id}}
```

#### 3. Success Tracking
```
At end of every workflow:

Google Sheets: Append Row
Sheet: "Workflow Executions"
Columns:
- Date: {{$now.format()}}
- Workflow: {{$workflow.name}}
- Status: "Success"
- Items Processed: {{$json['itemCount']}}
- Duration: {{$execution.duration}}
```

#### 4. Email Alerts for Critical Failures
```
Gmail: Send Email
To: admin@youragency.com
Subject: "[URGENT] N8N Workflow Failure"
Priority: High
Body:
"Critical workflow failure detected.

Workflow: {{$workflow.name}}
Error: {{$json['error']}}
Time: {{$now}}

Immediate action required."
```

---

## Advanced Techniques

### 1. Webhook Security

**Header Authentication**:
```
Webhook Node Settings:
- Authentication: Header Auth
- Header Name: "X-API-Key"
- Expected Value: "your-secret-key-here"

Only requests with matching header will execute workflow
```

**IP Whitelist (Self-Hosted)**:
```
Nginx Configuration:
location /webhook/ {
    allow 123.45.67.89;  # Zapier IP
    allow 98.76.54.32;   # Your server IP
    deny all;
    proxy_pass http://n8n:5678;
}
```

### 2. Dynamic Workflow Routing

**Use Case**: Route to different agents based on content type

```
Switch Node:
Mode: "Expression"

Rules:
- Case 1: {{$json["contentType"]}} === "blog"
    → Route to Blog Writer Agent
- Case 2: {{$json["contentType"]}} === "social"
    → Route to Social Media Agent
- Case 3: {{$json["contentType"]}} === "email"
    → Route to Email Writer Agent
- Default:
    → Error: Unknown content type
```

### 3. Batch Processing with Rate Limiting

**Problem**: API has rate limit of 10 requests/minute

**Solution**:
```
Loop Node: Process items
    ↓
HTTP Request to API
    ↓
Code Node: Check iteration count
    ↓
IF: {{$json["iterationCount"]}} % 10 === 0
    True → Wait 60 seconds
    False → Continue immediately
```

**Implementation**:
```javascript
// Code node to track iterations
const currentItem = $input.item;
const allItems = $input.all();
const currentIndex = allItems.findIndex(item => item.json === currentItem.json);

return [{
  json: {
    ...currentItem.json,
    iterationCount: currentIndex + 1,
    shouldWait: (currentIndex + 1) % 10 === 0
  }
}];
```

### 4. Multi-Language Content Generation

**Use Case**: Generate content in multiple languages

```
Set Languages:
languages: ["en", "es", "fr", "de"]
    ↓
Loop Over Languages:
    ↓
AI Agent:
System Prompt:
"Generate [content type] in {{$json['language']}} language.
Ensure native fluency and cultural appropriateness."
    ↓
Create Doc: "{{$json['title']}} - {{$json['language']}}"
```

### 5. A/B Testing Content Variations

**Generate Multiple Versions**:
```
AI Agent: Generate Content
System Prompt:
"Create 3 variations of [content type]:
1. Logical/Data-Driven approach
2. Emotional/Story-Driven approach
3. Humor/Entertainment approach"
    ↓
Split Out Variations
    ↓
Create Separate Docs for Each
    ↓
Send for Team Review
```

### 6. Scheduled Content Pipeline

**Use Case**: Generate week's worth of content every Monday

```
Schedule Trigger: Every Monday 9am
    ↓
Get Content Topics from Sheet
    ↓
Loop Over Topics:
    ├── Generate Blog Post
    ├── Generate Social Posts
    ├── Generate Newsletter
    └── Generate Video Script
    ↓
Schedule Throughout Week (Blotato)
```

### 7. Client-Specific Customization

**Store Client Preferences**:
```
Google Sheets: "Client Preferences"
Columns: ClientName, ToneStyle, BrandVoice, Keywords, Hashtags

Workflow:
Lookup Client Preferences
    ↓
Inject into AI Prompts:
"Write in {{$json['toneStyle']}} tone.
Brand voice: {{$json['brandVoice']}}
Include keywords: {{$json['keywords']}}"
```

### 8. Quality Assurance Agent

**Add QA Step Before Output**:
```
Content Generation Agent
    ↓
QA Agent:
System Prompt:
"Review this content and check:
1. Grammar and spelling
2. Brand voice consistency
3. Factual accuracy
4. CTA clarity
5. Length requirements

If issues found, provide specific corrections.
If approved, respond with 'APPROVED'"
    ↓
IF contains "APPROVED":
    → Proceed to publish
ELSE:
    → Send for human review
```

### 9. Performance Tracking

**Track AI Agent Performance**:
```javascript
// Code node before AI agent
const startTime = Date.now();

return [{
  json: {
    ....$json,
    aiStartTime: startTime
  }
}];

// Code node after AI agent
const endTime = Date.now();
const duration = endTime - $json["aiStartTime"];

// Log to sheet
Google Sheets: Append Row
Sheet: "AI Performance"
Values:
- Agent: {{$json["agentName"]}}
- Model: {{$json["model"]}}
- Duration: {{duration}}ms
- Tokens Used: {{$json["usage"]["totalTokens"]}}
- Cost: {{$json["usage"]["totalCost"]}}
```

### 10. Incremental Enrichment

**Use Case**: Enrich leads gradually to avoid hitting API limits

```
Schedule: Every 4 hours
    ↓
Google Sheets: Read Rows
  Where Status = "Unenriched"
  Limit: 50
    ↓
Enrich via SURF/Explorium
    ↓
Update Sheet: Status = "Enriched"
    ↓
Repeat until all leads enriched
```

---

## Best Practices and Tips

### Workflow Organization

1. **Naming Conventions**:
   - Workflows: "[CLIENT] - [PURPOSE] - [DATE]"
   - Nodes: Descriptive action names
   - Example: "Acme Inc - Lead Gen - 2024"

2. **Documentation**:
   - Add Sticky Notes to explain complex logic
   - Document API keys in password manager
   - Keep workflow documentation updated

3. **Version Control**:
   - Export workflows as JSON backups
   - Store in Git repository
   - Tag major versions

4. **Testing**:
   - Use manual triggers for testing
   - Test with small datasets first
   - Monitor first 10-20 executions closely

5. **Security**:
   - Never hard-code API keys in workflows
   - Use credential system
   - Rotate keys quarterly
   - Audit webhook endpoints

### Performance Optimization

1. **Minimize HTTP Requests**:
   - Batch API calls when possible
   - Cache frequently accessed data
   - Use parallel execution for independent tasks

2. **Efficient Loops**:
   - Process in batches of 10-50 items
   - Add wait nodes to prevent rate limiting
   - Use "Split In Batches" for large datasets

3. **AI Model Selection**:
   - Use cheaper models for simple tasks
   - Reserve premium models for complex reasoning
   - Implement fallback models

4. **Execution Limits**:
   - Cloud: 5000 executions/month (Growth plan)
   - Self-hosted: Unlimited
   - Consider self-hosting for high-volume

### Cost Management

1. **AI Usage**:
   - GPT-4: ~$0.01-0.03 per execution
   - Claude: ~$0.015-0.04 per execution
   - DeepSeek Free: $0.00 per execution
   - Use free models where appropriate

2. **API Costs**:
   - Perplexity: $5-20/month
   - SURF: $42-84/month
   - Explorium: Custom pricing
   - Go High Level: $97-297/month

3. **Monitoring Spend**:
   - Track execution costs in spreadsheet
   - Set budget alerts
   - Review monthly usage reports

---

## Troubleshooting Common Issues

### Issue 1: Webhook Not Triggering

**Symptoms**: Workflow doesn't execute when webhook is called

**Solutions**:
1. Check webhook URL is correct
2. Verify HTTP method (POST vs GET)
3. Test with Postman or curl
4. Check firewall rules (self-hosted)
5. Ensure workflow is activated

**Test Command**:
```bash
curl -X POST https://your-n8n.com/webhook/test \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Issue 2: Google OAuth Failing

**Symptoms**: "Invalid credentials" or "Authorization failed"

**Solutions**:
1. Check OAuth redirect URI matches exactly
2. Ensure all required APIs are enabled
3. Verify Client ID and Secret are correct
4. Try "Connect my account" again
5. Clear browser cache and retry

### Issue 3: AI Agent Timeout

**Symptoms**: Agent node fails with timeout error

**Solutions**:
1. Increase timeout setting (default: 30s, try 60s)
2. Reduce input text length
3. Use model with larger context window
4. Split into multiple smaller requests
5. Enable fallback model

### Issue 4: Rate Limit Errors

**Symptoms**: "429 Too Many Requests" error

**Solutions**:
1. Add Wait nodes between requests
2. Implement batch processing
3. Reduce loop iterations
4. Upgrade API plan
5. Spread executions over time

### Issue 5: Memory/Context Issues

**Symptoms**: Agent forgets previous context or gives inconsistent responses

**Solutions**:
1. Verify session ID is passed correctly
2. Check memory configuration
3. Increase context window length
4. Clear memory between workflows if needed
5. Use "Window Buffer Memory" not "Buffer Memory"

---

## Conclusion

You now have a complete understanding of building production-ready AI workflows in N8N. These patterns and templates are battle-tested in real agency environments processing thousands of executions monthly.

**Next Steps**:
1. Import provided workflow templates
2. Configure your API credentials
3. Test with small datasets
4. Monitor first 20-30 executions
5. Gradually increase automation scope
6. Document your modifications
7. Share learnings with your team

**Remember**: Start simple, test thoroughly, scale gradually. The most effective workflows are often the simplest ones that solve real problems reliably.

**Support Resources**:
- N8N Documentation: docs.n8n.io
- N8N Community Forum: community.n8n.io
- Workflow Templates: n8n.io/workflows
- This Course Community: [Your community link]

Happy automating!
