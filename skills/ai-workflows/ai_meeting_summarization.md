# AI Meeting Summarization and Intelligence

## Overview

Transform meeting recordings into comprehensive research documents, actionable summaries, and multi-platform content. Learn to build automated workflows that process call transcripts, generate meeting preparation docs, and create follow-up materials that improve sales effectiveness and team coordination.

## Table of Contents

1. [Meeting Intelligence Workflows](#meeting-intelligence-workflows)
2. [Booked Meeting Research Automation](#booked-meeting-research-automation)
3. [Call Transcript Analysis](#call-transcript-analysis)
4. [Multi-Content Generation from Meetings](#multi-content-generation-from-meetings)
5. [Meeting Follow-Up Automation](#meeting-follow-up-automation)

---

## Meeting Intelligence Workflows

### Use Cases

**1. Pre-Meeting Preparation**
- Automated prospect research when meeting is booked
- Generate briefing documents for sales reps
- Identify talking points and potential objections

**2. Post-Meeting Analysis**
- Summarize key discussion points
- Extract action items and commitments
- Analyze sentiment and engagement

**3. Content Repurposing**
- Transform call recordings into blog posts
- Generate social media content from meetings
- Create training materials from sales calls

---

## Booked Meeting Research Automation

### Workflow Purpose

**Automatically research prospects when they book meetings via Calendly**

**Trigger**: Calendly webhook (meeting booked)
**Output**: Comprehensive meeting prep document + CRM update + notifications

### Complete Workflow Architecture

```
Calendly Webhook (New meeting booked)
    ↓
Search Go High Level CRM (Check existing contact)
    ↓
├── Existing Lead → Update Status to "Meeting Booked"
└── New Lead → Create Contact + Create Opportunity
    ↓
Enrichment Process:
    ├── Explorium Match (Find contact data)
    ├── Explorium Enrich (Get detailed profile)
    └── Format Bio (Structure information)
    ↓
AI Research Agent (Generate meeting prep document)
    ↓
Output Delivery:
    ├── Create HTML Email Report
    ├── Create Google Doc
    ├── Move to "Prospect Research" folder
    └── Send Slack Notification
```

### Prerequisites and Setup

**Required Services**:

**1. Calendly Developer Account**
- Sign up at developer.calendly.com
- Create OAuth app
- Get Client ID and Client Secret

**2. Explorium API**
- Contact enrichment service
- API key for authentication
- Profile matching and enrichment

**3. Go High Level CRM**
- Contact management
- Opportunity tracking
- Status updates

**4. Google Services**
- Google Docs (document creation)
- Google Drive (file organization)
- Gmail (email notifications)

**5. Slack**
- Team notifications
- Meeting alerts

**6. OpenRouter + Perplexity**
- AI research and analysis
- Additional company research

### Node-by-Node Breakdown

#### Node 1: Calendly Trigger Setup

**Purpose**: Listen for new meeting bookings

**Configuration Steps**:

1. **Create Calendly Developer App**:
```
Go to: developer.calendly.com
1. Sign in with Google
2. Account → My Apps
3. New App
4. Name: "N8N Meeting Research"
5. Environment: Production
```

2. **Get OAuth Details**:
```
Copy from N8N Calendly node:
- OAuth Redirect URL: https://your-n8n.com/rest/oauth2-credential/callback

Paste into Calendly app:
- Redirect URI: [N8N URL]

Copy from Calendly app:
- Client ID: [Copy to N8N]
- Client Secret: [Copy to N8N]
```

3. **N8N Calendly Configuration**:
```
Calendly Trigger Node:
├── Authentication: OAuth2
├── Client ID: [From Calendly]
├── Client Secret: [From Calendly]
├── Event: invitee.created
└── Connect My Account
```

**Output Data**:
```json
{
  "event": "invitee.created",
  "payload": {
    "email": "prospect@company.com",
    "name": "John Doe",
    "event_type": "Discovery Call",
    "start_time": "2025-12-20T14:00:00Z",
    "timezone": "America/New_York",
    "reschedule_url": "https://...",
    "cancel_url": "https://...",
    "questions_and_answers": [
      {
        "question": "Company Name",
        "answer": "Acme Corp"
      }
    ]
  }
}
```

#### Node 2: Search Go High Level CRM

**Purpose**: Check if prospect is existing contact

**Configuration**:
```
Go High Level: Search Contacts
Operation: Search Contacts
Search By: Email
Value: {{$json["payload"]["email"]}}
```

**Output**:
```json
{
  "contacts": [
    {
      "id": "contact_123",
      "email": "prospect@company.com",
      "firstName": "John",
      "lastName": "Doe",
      "tags": ["Lead", "Interested"]
    }
  ]
}
```

#### Node 3: Conditional Branch

**Purpose**: Route based on contact existence

**IF Node Configuration**:
```
Condition: {{$json["contacts"].length}} > 0

True Branch (Existing Contact):
    → Get Contact Details
    → Update Contact Status to "Meeting Booked"

False Branch (New Contact):
    → Create New Contact
    → Create Opportunity
```

#### Node 4A: Update Existing Contact

**Go High Level: Update Contact**:
```
Contact ID: {{$json["contacts"][0]["id"]}}
Fields to Update:
├── Status: "Meeting Booked"
├── Last Activity: {{$now.toISO()}}
└── Tags: Add "Meeting Scheduled"
```

#### Node 4B: Create New Contact + Opportunity

**Create Contact**:
```
Go High Level: Create Contact
Fields:
├── First Name: {{$json["payload"]["name"].split(' ')[0]}}
├── Last Name: {{$json["payload"]["name"].split(' ').slice(1).join(' ')}}
├── Email: {{$json["payload"]["email"]}}
├── Source: "Calendly"
├── Tags: ["New Lead", "Meeting Scheduled"]
└── Custom Fields:
    ├── Meeting Type: {{$json["payload"]["event_type"]}}
    ├── Scheduled Date: {{$json["payload"]["start_time"]}}
    └── Timezone: {{$json["payload"]["timezone"]}}
```

**Create Opportunity**:
```
Go High Level: Create Opportunity
Fields:
├── Contact ID: {{$json["contactId"]}}
├── Name: "{{$json['payload']['event_type']}} - {{$json['payload']['name']}}"
├── Pipeline: "Sales"
├── Stage: "Meeting Scheduled"
├── Value: $5000 (estimated)
└── Status: "Open"
```

#### Node 5: Explorium Match Prospects

**Purpose**: Find prospect profile in Explorium database

**HTTP Request Configuration**:
```
Method: POST
URL: https://api.explorium.ai/v1/match
Authentication: Header Auth
  - Name: Authorization
  - Value: Bearer YOUR_EXPLORIUM_API_KEY

Body (JSON):
{
  "email": "{{$json['payload']['email']}}",
  "name": "{{$json['payload']['name']}}",
  "company": "{{$json['companyName']}}"
}
```

**Response**:
```json
{
  "prospect_id": "expl_abc123",
  "confidence": 0.95,
  "match_status": "found"
}
```

#### Node 6: Explorium Enrich Profile

**Purpose**: Get detailed prospect information

**HTTP Request Configuration**:
```
Method: POST
URL: https://api.explorium.ai/v1/enrich
Authentication: Header Auth

Body (JSON):
{
  "prospect_ids": ["{{$json['prospectId']}}"]
}
```

**Response**:
```json
{
  "enriched_data": {
    "full_name": "John Doe",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "current_job": {
      "title": "VP Marketing",
      "company": "Acme Corp",
      "start_date": "2022-01",
      "description": "Leading marketing strategy..."
    },
    "work_history": [
      {
        "title": "Marketing Director",
        "company": "Previous Company",
        "start_date": "2019-03",
        "end_date": "2021-12"
      }
    ],
    "education": [
      {
        "degree": "MBA",
        "school": "Harvard Business School",
        "graduation_year": "2018"
      }
    ],
    "location": {
      "city": "San Francisco",
      "state": "CA",
      "country": "US"
    }
  }
}
```

#### Node 7: Format Bio

**Purpose**: Structure enriched data for AI agent

**Code Node**:
```javascript
// Structure enriched data into clean format for AI
const profile = $json["enrichedData"];

const bio = {
  name: profile.full_name,
  city: profile.location?.city || 'Unknown',
  country: profile.location?.country || 'Unknown',
  currentPosition: profile.current_job?.title || 'Unknown',
  currentCompany: profile.current_job?.company || 'Unknown',
  companyDescription: profile.current_job?.description || '',
  startDate: profile.current_job?.start_date || '',

  previousExperience: (profile.work_history || []).map(job => ({
    title: job.title,
    company: job.company,
    duration: `${job.start_date} - ${job.end_date || 'Present'}`,
    description: job.description || ''
  })),

  linkedinUrl: profile.linkedin_url || '',

  education: (profile.education || []).map(edu => ({
    degree: edu.degree,
    school: edu.school,
    year: edu.graduation_year,
    field: edu.field_of_study || ''
  })),

  meetingDate: $node["Calendly Trigger"].json["payload"]["start_time"],
  meetingType: $node["Calendly Trigger"].json["payload"]["event_type"],
  prospectEmail: $node["Calendly Trigger"].json["payload"]["email"]
};

return [{ json: bio }];
```

#### Node 8: AI Meeting Prep Agent

**Purpose**: Generate comprehensive meeting preparation document

**AI Agent Configuration**:
```
Chat Model: OpenRouter (Claude 3.5 Sonnet)
Temperature: 0.7
Max Tokens: 3000

Tools Enabled:
└── Perplexity
    ├── Model: sonar-pro
    ├── Max Tokens: 4000
    └── Return Sources: Yes
```

**System Prompt**:
```
You are an AI agent specializing in generating meeting preparation documents for business professionals.

You will receive a JSON object containing LinkedIn profile information about a prospect who has booked a meeting. Your task is to:

1. Analyze the prospect's professional background
2. Research their current company using web search
3. Identify key talking points and areas of interest
4. Suggest strategic questions to ask
5. Highlight potential pain points or challenges
6. Recommend conversation approaches

Input Data:
- Name: {{$json["name"]}}
- Current Position: {{$json["currentPosition"]}}
- Current Company: {{$json["currentCompany"]}}
- Location: {{$json["city"]}}, {{$json["country"]}}
- LinkedIn: {{$json["linkedinUrl"]}}
- Time in Current Role: {{$json["startDate"]}}
- Previous Experience: {{$json["previousExperience"]}}
- Education: {{$json["education"]}}
- Meeting Type: {{$json["meetingType"]}}
- Meeting Date: {{$json["meetingDate"]}}

Research Instructions:
Use web search to find:
- Recent company news (last 3 months)
- Industry trends affecting their company
- Company growth trajectory and funding
- Competitive landscape
- Recent professional activity (LinkedIn posts, articles, interviews)
- Company challenges or initiatives

Output Format (Markdown):

# Meeting Prep: [Name]

**Meeting Details**
- Date: [Meeting Date]
- Type: [Meeting Type]
- Company: [Company Name]
- Role: [Position]

## Executive Summary
[3-4 sentence overview of who they are, their company context, and why this meeting matters]

## Professional Background

### Current Role at [Company]
- **Position**: [Title]
- **Tenure**: [Time in role]
- **Responsibilities**: [Key responsibilities based on role]
- **Company Stage**: [Startup/Growth/Enterprise - based on research]

### Career Journey
[Brief overview of career progression, highlighting 2-3 most relevant previous roles]

### Education & Expertise
[Educational background and key areas of professional expertise]

## Company Context

### About [Company Name]
- **Industry**: [Industry]
- **Size**: [Employee count/revenue if available]
- **Mission**: [Company mission or focus]
- **Market Position**: [Competitive positioning]

### Recent Developments
[List 3-5 recent company news items, funding, product launches, or challenges from the last 3 months]

### Industry Landscape
[Brief overview of industry trends, challenges, and opportunities relevant to their company]

## Meeting Strategy

### Recommended Talking Points
1. **[Topic 1]**: [Why this matters to them and how it connects to your offering]
2. **[Topic 2]**: [Specific pain point or opportunity you can address]
3. **[Topic 3]**: [Connection to their recent activity or company initiative]

### Strategic Questions to Ask
1. **Discovery**: "[Question about their current priorities or challenges]"
   - *Why ask*: [What this reveals]

2. **Qualification**: "[Question about their decision-making process or timeline]"
   - *Why ask*: [What this reveals]

3. **Engagement**: "[Question about specific company initiative or challenge]"
   - *Why ask*: [What this reveals]

### Potential Pain Points
Based on their role and company context:
- **[Pain Point 1]**: [Why this likely affects them]
- **Pain Point 2]**: [Evidence from research]
- **[Pain Point 3]**: [How your solution addresses this]

### Potential Objections & Responses
- **"[Likely objection 1]"**
  → Response: [How to address]

- **"[Likely objection 2]"**
  → Response: [How to address]

## Rapport Building

### Personal Connection Points
- [Something from their background that creates rapport]
- [Shared interest or experience]
- [Recent achievement to congratulate]

### Opening Lines
- "[Specific opener based on recent activity]"
- "[Alternative opener based on company news]"

## Quick Reference

**Decision Authority**: [Assessment: High/Medium/Low based on role]
**Budget Indicator**: [Company size/funding suggests budget tier]
**Urgency Level**: [Hot/Warm/Cold based on meeting type and research]
**Best Positioning**: [How to position your offering given their context]

## Action Items
- [ ] Review recent LinkedIn activity
- [ ] Check company website for updates
- [ ] Prepare case study from similar industry
- [ ] Send pre-meeting confirmation with agenda
- [ ] Add to CRM with appropriate tags

---
*Research Sources*: [List key sources used]
*Document Generated*: [Timestamp]
*Confidence Level*: [High/Medium/Low based on data availability]
```

**Output**: Comprehensive markdown document with all meeting prep information

#### Node 9: Create HTML Email Report

**Purpose**: Format meeting prep as HTML email

**Code Node**:
```javascript
// Convert markdown to HTML
const markdown = $json["meetingPrepDocument"];
const prospectName = $json["name"];
const meetingDate = new Date($json["meetingDate"]).toLocaleString();

// Simple markdown to HTML conversion
let html = markdown
  .replace(/^# (.*$)/gim, '<h1 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">$1</h1>')
  .replace(/^## (.*$)/gim, '<h2 style="color: #34495e; margin-top: 30px;">$1</h2>')
  .replace(/^### (.*$)/gim, '<h3 style="color: #7f8c8d; margin-top: 20px;">$1</h3>')
  .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
  .replace(/\*(.*?)\*/gim, '<em>$1</em>')
  .replace(/^- (.*$)/gim, '<li style="margin: 5px 0;">$1</li>')
  .replace(/^(\d+)\. (.*$)/gim, '<li style="margin: 5px 0;">$2</li>')
  .replace(/\n\n/gim, '</p><p>')
  .replace(/\n/gim, '<br>');

const htmlContent = `
  <!DOCTYPE html>
  <html>
  <head>
    <style>
      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        line-height: 1.6;
        color: #333;
      }
      .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px 10px 0 0;
        margin: -20px -20px 30px -20px;
      }
      .meeting-details {
        background: #f8f9fa;
        padding: 20px;
        border-left: 4px solid #3498db;
        margin: 20px 0;
        border-radius: 5px;
      }
      .pain-points {
        background: #fff3cd;
        padding: 15px;
        border-left: 4px solid #ffc107;
        margin: 20px 0;
        border-radius: 5px;
      }
      .talking-points {
        background: #d1ecf1;
        padding: 15px;
        border-left: 4px solid #17a2b8;
        margin: 20px 0;
        border-radius: 5px;
      }
      .action-items {
        background: #d4edda;
        padding: 15px;
        border-left: 4px solid #28a745;
        margin: 20px 0;
        border-radius: 5px;
      }
      h1 { font-size: 28px; margin: 0; }
      h2 { font-size: 22px; color: #34495e; margin-top: 30px; }
      h3 { font-size: 18px; color: #7f8c8d; margin-top: 20px; }
      ul, ol { padding-left: 20px; }
      li { margin: 8px 0; }
      .footer {
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #dee2e6;
        font-size: 14px;
        color: #6c757d;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>🎯 Meeting Preparation</h1>
      <p style="margin: 10px 0 0 0; font-size: 18px;">${prospectName}</p>
    </div>

    <div class="meeting-details">
      <strong>📅 Meeting Date:</strong> ${meetingDate}<br>
      <strong>📧 Email:</strong> ${$json["prospectEmail"]}<br>
      <strong>🎤 Meeting Type:</strong> ${$json["meetingType"]}
    </div>

    ${html}

    <div class="footer">
      <p>🤖 Generated by AI Research Agent</p>
      <p>Document created: ${new Date().toLocaleString()}</p>
    </div>
  </body>
  </html>
`;

return [{
  json: {
    htmlContent: htmlContent,
    prospectName: prospectName,
    meetingDate: meetingDate,
    prospectEmail: $json["prospectEmail"]
  }
}];
```

#### Node 10: Send Email Report

**Gmail Configuration**:
```
To: {{$json["clientEmail"]}} (or your email)
Subject: "New Meeting Booked: {{$json['prospectName']}} - {{$json['meetingDate']}}"
Body Type: HTML
Body: {{$json["htmlContent"]}}

Optional CC: Sales team email
Priority: High (for immediate meetings)
```

#### Node 11: Create Google Doc

**Purpose**: Store meeting prep as shareable document

**MD2Docs Node**:
```
Document Name: "Meeting Prep - {{$json['name']}} - {{$now.format('YYYY-MM-DD HH:mm')}}"
Content (Markdown): {{$json["meetingPrepDocument"]}}
```

**Returns**: Document ID and URL

#### Node 12: Move to Prospect Research Folder

**Google Drive: Move File**:
```
File ID: {{$json["documentId"]}}
Destination Folder: "Prospect Research"

Note: Create "Prospect Research" folder in Google Drive beforehand
To get Folder ID:
1. Open folder in Google Drive
2. Copy ID from URL: drive.google.com/drive/folders/[FOLDER_ID]
3. Paste FOLDER_ID in node configuration
```

#### Node 13: Send Slack Notification

**Slack: Send Message**:
```
Channel: #new-meetings (or your preferred channel)

Message:
*🎉 New Call Booked!*

*Meeting Details*
📅 Date: {{$json["meetingDate"]}}
🎤 Type: {{$json["meetingType"]}}
⏰ Timezone: {{$json["timezone"]}}

*Prospect Information*
👤 Name: {{$json["prospectName"]}}
🏢 Company: {{$json["companyName"]}}
📧 Email: {{$json["prospectEmail"]}}
💼 Position: {{$json["currentPosition"]}}

*Resources*
📄 Research Doc: {{$json["documentUrl"]}}
🔗 LinkedIn: {{$json["linkedinUrl"]}}
🗓 Reschedule: {{$json["rescheduleUrl"]}}
❌ Cancel: {{$json["cancelUrl"]}}

*Quick Intel*
• Current Role: {{$json["currentPosition"]}} at {{$json["companyName"]}}
• Location: {{$json["city"]}}, {{$json["country"]}}
• Background: {{$json["careerSummary"]}}

*Action Items*
✅ Meeting prep document created
✅ CRM updated
✅ Email sent to team

_Research Agent completed at {{$now.format('HH:mm')}}_ 🤖
```

---

## Call Transcript Analysis

### Use Case: Analyze Existing Sales Calls

**Input**: Call transcript (from Fathom, Fireflies, Gong, etc.)
**Output**: Summary, action items, sentiment analysis

### Workflow Architecture

```
Manual Input (Paste transcript)
    ↓
AI Analysis Agent
    ↓
Generate:
├── Executive Summary
├── Key Discussion Points
├── Action Items
├── Objections Raised
├── Sentiment Analysis
└── Follow-up Recommendations
    ↓
Create Google Doc + Send to Team
```

### Analysis Agent Prompt

```
You are an expert sales call analyzer.

Analyze this sales call transcript and provide:

**Call Transcript**:
{{$json["transcript"]}}

**Meeting Context**:
- Participants: {{$json["participants"]}}
- Date: {{$json["date"]}}
- Duration: {{$json["duration"]}}

Generate a comprehensive analysis:

## Executive Summary
[2-3 sentence overview of the call outcome and next steps]

## Key Discussion Points
1. [Main topic 1 with details]
2. [Main topic 2 with details]
3. [Main topic 3 with details]

## Prospect Needs & Pain Points
- [Need/pain point 1]
- [Need/pain point 2]
- [Need/pain point 3]

## Questions Asked by Prospect
1. [Question 1] → [How it was addressed]
2. [Question 2] → [How it was addressed]

## Objections Raised
- **[Objection 1]**: [How it was handled and whether resolved]
- **[Objection 2]**: [How it was handled and whether resolved]

## Commitments Made
**By Us**:
- [Commitment 1]
- [Commitment 2]

**By Prospect**:
- [Commitment 1]
- [Commitment 2]

## Action Items
### Our Team
- [ ] [Action item 1] - Owner: [Name] - Due: [Date]
- [ ] [Action item 2] - Owner: [Name] - Due: [Date]

### Prospect
- [ ] [Action item 1] - Due: [Date]
- [ ] [Action item 2] - Due: [Date]

## Sentiment Analysis
**Overall Tone**: [Positive/Neutral/Negative]
**Engagement Level**: [High/Medium/Low]
**Buying Intent**: [Strong/Moderate/Weak]

**Key Indicators**:
- [Positive indicator 1]
- [Concern indicator 1]

## Deal Assessment
**Stage**: [Discovery/Demo/Proposal/Negotiation]
**Probability**: [High/Medium/Low]
**Timeline**: [Expected close timeframe]
**Decision Makers**: [Identified decision makers]
**Budget**: [Budget indication if discussed]

## Follow-Up Strategy
**Immediate Actions** (Next 24 hours):
1. [Action]
2. [Action]

**Short Term** (Next week):
1. [Action]
2. [Action]

**Email Draft**:
Subject: [Suggested subject line]
Body: [Draft follow-up email based on call]

## Coaching Notes
**What Went Well**:
- [Positive aspect 1]
- [Positive aspect 2]

**Areas for Improvement**:
- [Improvement opportunity 1]
- [Improvement opportunity 2]

---
*Analyzed by AI Call Intelligence Agent*
```

---

## Multi-Content Generation from Meetings

### Use Case: Repurpose Meeting Content

Transform call transcripts into multiple content formats:
- YouTube video scripts
- LinkedIn posts
- Twitter threads
- Blog articles
- Email newsletters

### Workflow Architecture

```
Input: Call Transcript
    ↓
Parallel Content Generation:
├── YouTube Script Agent → Create Doc
├── LinkedIn Post Agent → Create Doc
├── Twitter Thread Agent → Create Doc
├── Blog Post Agent → Create Doc
└── Newsletter Agent → Create Doc
    ↓
Organize in Google Drive + Notify Team
```

### Content Agent Configurations

**YouTube Script Agent**:
```
Transform this call transcript into an engaging YouTube video script.

Structure:
- Hook (0-15 seconds)
- Introduction (15-45 seconds)
- Main Content (80% of video)
- Recap (Last 60 seconds)
- CTA

Output: Full video script with [VISUAL CUE] notes
```

**LinkedIn Post Agent**:
```
Create a LinkedIn post based on insights from this call.

Requirements:
- Hook in first line
- 150-300 words
- Professional but conversational tone
- 3-5 relevant hashtags
- Engaging question or CTA at end
```

**Twitter Thread Agent**:
```
Create a Twitter thread (8-12 tweets) from this transcript.

Requirements:
- Pattern-interrupt hook (tweet 1)
- One idea per tweet
- Max 280 characters each
- Number tweets (1/12, 2/12, etc.)
- Strong CTA at end
```

---

## Meeting Follow-Up Automation

### Automatic Follow-Up Email

**Workflow**:
```
Call Transcript Analysis
    ↓
Generate Follow-Up Email
    ↓
Send Draft to Sales Rep for Approval
    ↓
IF Approved → Send via Gmail
    ↓
Log in CRM + Update Deal Stage
```

### Follow-Up Email Agent

```
Based on this call analysis, generate a personalized follow-up email.

Call Summary:
{{$json["callSummary"]}}

Action Items:
{{$json["actionItems"]}}

Next Steps:
{{$json["nextSteps"]}}

Generate an email that:
1. Thanks them for their time
2. Recaps key discussion points
3. Confirms action items and next steps
4. Includes calendar link for next meeting
5. Professional but warm tone

Include subject line and full email body.
```

---

## Best Practices

### 1. Data Privacy

**Handle Sensitive Information**:
```
- Do NOT store credit card info in plain text
- Redact sensitive data from transcripts
- Use secure CRM fields for confidential info
- Set document permissions appropriately
```

### 2. Quality Control

**Validate AI Outputs**:
```javascript
// Check meeting prep quality
const qualityChecks = {
  hasExecutiveSummary: $json["output"].includes("Executive Summary"),
  hasTalkingPoints: $json["output"].includes("Talking Points"),
  hasActionItems: $json["output"].includes("Action Items"),
  minLength: $json["output"].length > 1000,
  hasSources: $json["output"].includes("Sources")
};

const passedChecks = Object.values(qualityChecks).filter(v => v).length;
const qualityScore = passedChecks / Object.keys(qualityChecks).length;

if (qualityScore < 0.8) {
  // Flag for human review
}
```

### 3. Team Coordination

**Notification Strategy**:
```
High Priority Meetings:
→ Slack notification + Email + SMS

Normal Meetings:
→ Slack notification + Email

Low Priority:
→ Email only
```

---

## Troubleshooting

### Issue: Explorium Enrichment Fails

**Solutions**:
1. Fallback to public data sources (LinkedIn scraping)
2. Flag for manual research
3. Use SURF API as alternative
4. Continue with available data

### Issue: AI Generates Generic Prep Docs

**Solutions**:
1. Improve system prompt specificity
2. Ensure Perplexity tool is enabled
3. Verify enrichment data quality
4. Add more context to prompts

### Issue: Webhook Not Triggering

**Solutions**:
1. Verify Calendly OAuth setup
2. Check webhook event type (invitee.created)
3. Test with manual Calendly booking
4. Review N8N execution logs

---

## Next Steps

1. **Set up Calendly integration** following OAuth steps
2. **Configure enrichment service** (Explorium or alternative)
3. **Test workflow** with test meeting booking
4. **Review output quality** and adjust prompts
5. **Scale to production** once validated

**Related Skills**:
- `ai_prospect_research.md` - Research techniques
- `setup_ai_agent.md` - Agent configuration
- `mass_personalize_with_ai.md` - Personalization workflows

---

## Resources

**Tools**:
- Calendly: calendly.com
- Explorium: explorium.ai
- Fathom: fathom.video
- Fireflies: fireflies.ai
- Go High Level: gohighlevel.com

**N8N Nodes**:
- Calendly Trigger
- AI Agent
- MD2Docs (Google Docs)
- Gmail
- Slack

---

Transform meetings from time spent into intelligence assets that drive better outcomes and team coordination.
