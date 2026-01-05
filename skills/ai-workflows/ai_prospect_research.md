# Automated Prospect Research with AI

## Overview

Build comprehensive AI-powered prospect research workflows that automatically find, enrich, and analyze target prospects. Learn to integrate SURF API, Explorium, and AI agents to create detailed prospect lists with contact information, professional backgrounds, and actionable insights for sales teams.

## Table of Contents

1. [Research Workflow Types](#research-workflow-types)
2. [Prospecting with SURF API](#prospecting-with-surf-api)
3. [Contact Enrichment with Explorium](#contact-enrichment-with-explorium)
4. [AI-Powered Analysis](#ai-powered-analysis)
5. [Dream 100 Research (Poppy.ai)](#dream-100-research-poppyai)
6. [CRM Integration](#crm-integration)

---

## Research Workflow Types

### 1. Automated Prospect List Builder

**Purpose**: Find and enrich ICP prospects at scale

**Flow**:
```
Form Input (ICP criteria)
    ↓
Search ICP Companies (SURF API)
    ↓
Search Employees in Companies (SURF API)
    ↓
Enrich Prospect Contact Details
    ↓
Check Enrichment Status (Loop until complete)
    ↓
Extract Contact Information
    ↓
Add to Go High Level CRM
    ↓
Email Notification
```

**Use Case**: Build targeted prospect lists for cold outreach campaigns

### 2. Inbound Lead Enrichment

**Purpose**: Automatically research leads when they book meetings

**Flow**:
```
Calendly Webhook (Meeting booked)
    ↓
Search CRM (Check if existing contact)
    ↓
IF New → Create Contact | IF Existing → Update Status
    ↓
Explorium Match (Find profile data)
    ↓
Explorium Enrich (Get detailed info)
    ↓
AI Meeting Prep Agent (Generate research doc)
    ↓
Create Google Doc + Send Email + Slack Notification
```

**Use Case**: Prepare sales reps for meetings with comprehensive prospect research

### 3. Dream 100 Deep Research

**Purpose**: Manual, high-touch research for top prospects

**Tool**: Poppy.ai

**Flow**:
```
Input: Prospect LinkedIn URL
    ↓
Load Profile + Your Info
    ↓
AI Research & First Line Writer
    ↓
Generate Personalized Outreach
```

**Use Case**: Highly personalized outreach to dream clients

---

## Prospecting with SURF API

### What is SURF?

**SURF (surfe.com)** is a prospecting tool that provides:
- Company search by ICP criteria
- Employee discovery within companies
- Contact enrichment (emails, phone numbers)
- LinkedIn profile data

**Pricing**:
```
Free Trial: Available
Essential: $42/month (150 email finders)
Pro: $84/month (1,000 email finders)
Unlimited email validation on all tiers
```

### SURF API Setup in N8N

**Step 1: Get API Key**
```
1. Sign up at surfe.com
2. Install Chrome extension (required)
3. Go to Settings → Use SURF API
4. Copy API key
```

**Step 2: Configure N8N HTTP Request Node**
```
Method: POST
URL: https://api.surfe.com/v2/[endpoint]
Authentication: Generic Credential Type → Header Auth

Credentials:
├── Name: Authorization (capital A)
└── Value: [Paste your SURF API key]
```

### Complete SURF Prospecting Workflow

#### Node 1: Prospect Criteria Form

**Form Fields**:
```
├── Industry (Text)
│   Example: "SaaS", "E-commerce", "Marketing Agencies"
├── Max Employee Count (Number)
│   Example: 50, 200, 1000
├── Country Code (Dropdown)
│   Options: US, UK, CA, AU, etc.
├── Your Name (Text)
└── Your Email (Email)
```

#### Node 2: Set Prospect Data

**Code Node**:
```javascript
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

#### Node 3: Search ICP Companies

**HTTP Request Configuration**:
```
Method: POST
URL: https://api.surfe.com/v2/company/search
Authentication: Header Auth (configured above)

Body (JSON):
{
  "filters": {
    "industry": "{{$json['industry']}}",
    "employee_count_max": {{$json["maxEmployees"]}},
    "country": "{{$json['country']}}"
  },
  "limit": 20
}
```

**Response Example**:
```json
{
  "companies": [
    {
      "name": "Acme SaaS Inc",
      "domain": "acmesaas.com",
      "employee_count": 45,
      "industry": "SaaS",
      "location": "San Francisco, CA"
    }
  ]
}
```

#### Node 4: Prepare JSON Payload

**Code Node**:
```javascript
// Extract company names and domains
const companies = $json["companies"].map(company => ({
  name: company.name,
  domain: company.domain,
  employeeCount: company.employee_count,
  industry: company.industry
}));

return [{
  json: {
    companies: companies,
    totalCompanies: companies.length
  }
}];
```

#### Node 5: Search for Employees

**HTTP Request Configuration**:
```
Method: POST
URL: https://api.surfe.com/v2/person/search
Authentication: Header Auth

Body (JSON):
{
  "company_domain": "{{$json['domain']}}",
  "job_titles": [
    "CEO",
    "Founder",
    "Owner",
    "VP Marketing",
    "CMO",
    "Marketing Director"
  ],
  "limit": 5
}
```

**Response Example**:
```json
{
  "persons": [
    {
      "id": "person_123abc",
      "first_name": "John",
      "last_name": "Doe",
      "job_title": "CEO",
      "linkedin_url": "https://linkedin.com/in/johndoe",
      "company_domain": "acmesaas.com"
    }
  ]
}
```

#### Node 6: Prepare Enrichment Request

**Code Node**:
```javascript
// Format person IDs for enrichment
const personIds = $json["persons"].map(person => person.id);

return [{
  json: {
    personIds: personIds,
    companyDomain: $json["companyDomain"],
    companyName: $json["companyName"]
  }
}];
```

#### Node 7: Enrich Prospects

**HTTP Request Configuration**:
```
Method: POST
URL: https://api.surfe.com/v2/enrich
Authentication: Header Auth

Body (JSON):
{
  "person_ids": {{$json["personIds"]}},
  "fields": [
    "email",
    "phone",
    "linkedin_url",
    "job_title",
    "location",
    "company_name"
  ]
}
```

**Response**:
```json
{
  "enrichment_id": "enrich_xyz789",
  "status": "processing"
}
```

#### Node 8: Check Enrichment Status

**Loop with Wait Node**:

```
HTTP Request Node:
Method: GET
URL: https://api.surfe.com/v2/enrich/{{$json['enrichmentId']}}
Authentication: Header Auth

↓

IF Node:
Condition: {{$json["status"]}} === "completed"
  True → Continue to Extract People
  False → Wait 3 seconds → Check again
```

#### Node 9: Extract People List

**Code Node**:
```javascript
// Parse enriched data
const people = $json["enrichmentResults"].map(person => ({
  firstName: person.first_name,
  lastName: person.last_name,
  email: person.email,
  phone: person.phone,
  linkedinUrl: person.linkedin_url,
  jobTitle: person.job_title,
  company: person.company_name,
  location: person.location,
  source: "SURF",
  enrichedDate: new Date().toISOString()
}));

return people.map(person => ({ json: person }));
```

#### Node 10: Add to Go High Level CRM

**Loop Over Each Person**:

```
Go High Level: Create Contact
Fields:
├── First Name: {{$json["firstName"]}}
├── Last Name: {{$json["lastName"]}}
├── Email: {{$json["email"]}}
├── Phone: {{$json["phone"]}}
├── Company Name: {{$json["company"]}}
├── Source: "SURF Prospecting"
├── Tags: ["Prospect", "{{$json['industry']}}"]
└── Custom Fields:
    ├── LinkedIn: {{$json["linkedinUrl"]}}
    ├── Job Title: {{$json["jobTitle"]}}
    └── Enriched Date: {{$json["enrichedDate"]}}
```

#### Node 11: Email Notification

**Gmail Configuration**:
```
To: {{$node["Set Prospect Data"].json["userEmail"]}}
Subject: "Prospect Enrichment Complete - {{$json['totalProspects']}} Added"

Body:
Your prospect enrichment is complete!

Industry: {{$json['industry']}}
Companies Found: {{$json['totalCompanies']}}
Prospects Added: {{$json['totalProspects']}}

Check your Go High Level CRM to view the new contacts.

Next steps:
1. Review prospect list in CRM
2. Filter by job title/company
3. Export for cold email campaign
4. Launch outreach sequence
```

### Schedule-Based Prospecting

**Alternative: Automatic Daily Prospecting**

Replace Form Trigger with Schedule Trigger:

```
Schedule Trigger: Every 24 hours at 9:00 AM

Set Prospect Data (Hard-coded):
{
  industry: "SaaS",
  maxEmployees: 100,
  country: "US"
}

→ Rest of workflow runs automatically
→ Adds 20-50 new prospects daily
→ Keeps CRM fresh with leads
```

---

## Contact Enrichment with Explorium

### What is Explorium?

**Explorium** is a contact enrichment service that provides:
- LinkedIn profile matching
- Professional background details
- Work history and education
- Additional contact information

**Pricing**: Custom pricing (contact sales)

### Explorium API Setup

**Step 1: Get API Key**
```
1. Sign up at explorium.ai
2. Contact sales for API access
3. Get API key from dashboard
```

**Step 2: Configure N8N**
```
HTTP Request Node:
Authentication: Header Auth

Credentials:
├── Name: Authorization (capital A)
└── Value: Bearer YOUR_EXPLORIUM_API_KEY
```

### Explorium Enrichment Workflow

#### Match Prospects

**HTTP Request**:
```
Method: POST
URL: https://api.explorium.ai/v1/match

Body (JSON):
{
  "email": "{{$json['email']}}",
  "name": "{{$json['name']}}",
  "company": "{{$json['company']}}"
}

Response:
{
  "prospect_id": "expl_abc123",
  "confidence": 0.95,
  "match_status": "found"
}
```

#### Enrich Profiles

**HTTP Request**:
```
Method: POST
URL: https://api.explorium.ai/v1/enrich

Body (JSON):
{
  "prospect_ids": ["{{$json['prospectId']}}"]
}

Response:
{
  "enriched_data": {
    "full_name": "John Doe",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "current_job": {
      "title": "VP Marketing",
      "company": "Acme Corp",
      "start_date": "2022-01",
      "description": "Leading marketing team..."
    },
    "work_history": [...],
    "education": [...],
    "location": {
      "city": "San Francisco",
      "state": "CA",
      "country": "US"
    }
  }
}
```

#### Format Bio for AI Agent

**Code Node**:
```javascript
// Structure enriched data for AI consumption
const profile = $json["enrichedData"];

const bio = {
  name: profile.full_name,
  city: profile.location.city,
  country: profile.location.country,
  currentPosition: profile.current_job.title,
  currentCompany: profile.current_job.company,
  companyDescription: profile.current_job.description,
  previousExperience: profile.work_history.map(job => ({
    title: job.title,
    company: job.company,
    duration: `${job.start_date} - ${job.end_date || 'Present'}`
  })),
  linkedinUrl: profile.linkedin_url,
  education: profile.education.map(edu => ({
    degree: edu.degree,
    school: edu.school,
    year: edu.graduation_year
  }))
};

return [{ json: bio }];
```

---

## AI-Powered Analysis

### Meeting Preparation Agent

**Purpose**: Generate comprehensive meeting prep documents

**AI Agent Configuration**:
```
Chat Model: OpenRouter (Claude 3.5 Sonnet)
Temperature: 0.7
Max Tokens: 3000

Tools:
└── Perplexity (for additional company research)
```

**System Prompt**:
```
You are an AI agent specializing in generating meeting preparation documents for business professionals.

You receive a JSON object containing LinkedIn profile information and company data.

Your task:
1. Analyze the prospect's professional background
2. Research current company context and recent news
3. Identify relevant talking points for the meeting
4. Suggest strategic questions to ask
5. Highlight potential pain points or opportunities
6. Recommend conversation approaches

Input Data:
- Name: {{$json["name"]}}
- Current Position: {{$json["currentPosition"]}}
- Company: {{$json["currentCompany"]}}
- Location: {{$json["city"]}}, {{$json["country"]}}
- LinkedIn: {{$json["linkedinUrl"]}}
- Work History: {{$json["previousExperience"]}}
- Education: {{$json["education"]}}

Research Focus:
Use web search to find:
- Recent company news and updates (last 3 months)
- Industry trends affecting their company
- Competitive landscape
- Recent professional activity (posts, articles, interviews)
- Company growth trajectory

Output Format (Markdown):

# Meeting Prep: [Name]

## Executive Summary
[3-4 sentence overview of who they are and why this meeting matters]

## Professional Background
### Current Role
[Details about current position, responsibilities, tenure]

### Career Journey
[Notable previous roles and progression]

### Education & Expertise
[Educational background and key areas of expertise]

## Company Context
### About [Company]
[Company overview, mission, market position]

### Recent Developments
[Recent news, funding, product launches, challenges]

### Industry Landscape
[Industry trends, competitive position]

## Meeting Strategy
### Recommended Talking Points
1. [Specific topic based on their role/interests]
2. [Relevant pain point you can address]
3. [Connection to their recent activity]

### Questions to Ask
1. [Strategic question about their priorities]
2. [Question about specific company initiative]
3. [Question about challenges they're facing]

### Potential Objections
- [Likely concern 1] → [How to address]
- [Likely concern 2] → [How to address]

## Quick Facts
- **Meeting Date**: [Date]
- **Duration**: [Length]
- **Location**: [Virtual/In-person]
- **Decision Authority**: [Assessment of their role in decision-making]

---
*Document generated by AI Research Agent*
*Sources: [List sources used]*
```

### Create Google Doc Output

**MD2Docs Node**:
```
Document Name: "Meeting Prep - {{$json['name']}} - {{$now.format('YYYY-MM-DD')}}"
Content: {{$json["meetingPrepDocument"]}}
Folder: "Prospect Research"
```

### Send via Email (HTML)

**Code Node - Convert to HTML**:
```javascript
const markdown = $json["meetingPrepDocument"];

// Simple markdown to HTML conversion
let html = markdown
  .replace(/^# (.*$)/gim, '<h1>$1</h1>')
  .replace(/^## (.*$)/gim, '<h2>$1</h2>')
  .replace(/^### (.*$)/gim, '<h3>$1</h3>')
  .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
  .replace(/\*(.*?)\*/gim, '<em>$1</em>')
  .replace(/^- (.*$)/gim, '<li>$1</li>')
  .replace(/\n/gim, '<br>');

return [{
  json: {
    htmlContent: `
      <html>
      <head>
        <style>
          body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
          }
          h1 { color: #2c3e50; border-bottom: 2px solid #3498db; }
          h2 { color: #34495e; margin-top: 30px; }
          h3 { color: #7f8c8d; }
          .quick-facts {
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
          }
        </style>
      </head>
      <body>
        <h1>Meeting Prep: ${$json["prospectName"]}</h1>
        <p><strong>Date:</strong> ${$json["meetingDate"]}</p>
        ${html}
      </body>
      </html>
    `
  }
}];
```

**Gmail Node**:
```
To: {{$json["clientEmail"]}} (or your email)
Subject: "New Meeting Booked: {{$json['prospectName']}} - Research Doc Attached"
Body (HTML): {{$json["htmlContent"]}}
```

---

## Dream 100 Research (Poppy.ai)

### What is Poppy.ai?

**Poppy.ai** is a multi-source AI research platform that:
- Loads LinkedIn profiles
- Analyzes YouTube transcripts
- Reviews website content
- Generates personalized outreach

**Use Case**: High-touch research for your top 100 dream prospects

### Dream 100 Research Setup

**Poppy Board Structure**:
```
Three Groups:
├── Dream 100 Prospects (Social media profiles)
├── System Prompt (Agent instructions)
└── Information About You (Your offer context)
```

#### Group 1: Dream 100 Prospects

**Content**:
```
Add URLs:
- LinkedIn profile: linkedin.com/in/prospect-name
- YouTube videos: youtube.com/watch?v=video-id
- Twitter/X profile: twitter.com/prospect-name
- Blog posts: prospect-blog.com/article
- Podcast episodes: podcast-platform/episode
```

#### Group 2: System Prompt

**Prompt Template**:
```
You are a detailed ICP researcher and first line writer for Dream 100 outreach.

Your task: Find key information, details, and updates about prospects and write a personalized first-line DM mentioning something specific about them in a positive manner before pitching services.

Follow-up structure:
"I made you [DELIVERABLE] because I saw [SPECIFIC OBSERVATION] on your [PLATFORM]."

Research Focus:
- Recent activity (last 3 months)
- Content they've created
- Achievements or milestones
- Professional expertise areas
- Unique positioning

Writing Guidelines:
- Reference something SPECIFIC (not generic)
- Show genuine research and understanding
- Create relevance to your offer
- Be conversational, not salesy
- 2-3 sentences maximum

Output: Personalized first-line DM only, no explanation.
```

#### Group 3: Information About You

**Content to Add**:
```
Add:
- Your website homepage
- YouTube video about your service
- Case study or portfolio
- LinkedIn profile
- Service offering page
```

### Generate Personalized Outreach

**Prompt**:
```
Follow your system instructions and write a personalized first line for a DM to the person in the Dream 100 Prospects group.

Write the message from me, [YOUR NAME], offering [YOUR DELIVERABLE/SERVICE], tailored to their work.

Write it more direct and casual, emulating my speaking style from the content in the Information About You group.
```

**Example Output**:
```
Hey [Name], just saw your breakdown on [specific topic] from your [podcast/post/video] -
the [specific insight] especially resonated since that's exactly what we help [their role]
solve. I actually put together a [deliverable] specifically for your [specific situation] -
want me to send it over?
```

### Dream 100 at Scale

**Process**:
```
1. Add 10-20 prospects to Poppy board
2. Generate personalized first lines for each
3. Copy outputs to spreadsheet
4. Manually review and refine
5. Send outreach one by one
6. Track responses and iterate
```

---

## CRM Integration

### Go High Level Setup

**Create Contact**:
```
Operation: Create Contact
Fields:
├── First Name: {{$json["firstName"]}}
├── Last Name: {{$json["lastName"]}}
├── Email: {{$json["email"]}}
├── Phone: {{$json["phone"]}}
├── Company Name: {{$json["company"]}}
├── Website: {{$json["website"]}}
├── Source: "Automated Prospecting"
├── Tags: ["Prospect", "Enriched", "{{$json['industry']}}"]
└── Custom Fields:
    ├── LinkedIn URL: {{$json["linkedinUrl"]}}
    ├── Job Title: {{$json["jobTitle"]}}
    ├── Location: {{$json["location"]}}
    ├── Enrichment Date: {{$now.format('YYYY-MM-DD')}}
    └── Enrichment Source: {{$json["source"]}}
```

### Update Existing Contacts

**Search First**:
```
Go High Level: Search Contacts
Field: Email
Value: {{$json["email"]}}

↓

IF Node: Contact exists?
  True → Update Contact (add enriched data)
  False → Create Contact (new prospect)
```

### Create Opportunity

```
Go High Level: Create Opportunity
Fields:
├── Contact ID: {{$json["contactId"]}}
├── Name: "{{$json['company']}} - {{$json['firstName']}} {{$json['lastName']}}"
├── Pipeline: "Outbound Sales"
├── Stage: "Prospect"
├── Value: $5000 (estimated deal size)
├── Status: "Open"
└── Custom Fields:
    └── Research Completed: Yes
```

---

## Best Practices

### 1. Data Quality

**Validate Emails**:
```javascript
// Code node for email validation
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

const validProspects = $input.all().filter(item =>
  isValidEmail(item.json.email) &&
  item.json.email.length > 5
);

return validProspects;
```

**Check for Duplicates**:
```javascript
// Before adding to CRM
const existingEmails = new Set($json["crmContacts"].map(c => c.email));
const newProspects = $input.all().filter(item =>
  !existingEmails.has(item.json.email)
);
```

### 2. Rate Limiting

**SURF API Limits**:
```
Essential Plan: 150 enrichments/month
Pro Plan: 1000 enrichments/month

Strategy:
- Process in batches of 20-50
- Add 3-second delays between enrichment requests
- Track monthly usage
```

**Implementation**:
```
Loop Over Items
    ↓
Enrich Contact
    ↓
Wait Node (3 seconds)
    ↓
Continue to next
```

### 3. Cost Management

**Track Enrichment Costs**:
```javascript
// Code node to log costs
const enrichmentCost = {
  date: new Date().toISOString(),
  source: $json["enrichmentSource"],
  prospectsEnriched: $json["count"],
  estimatedCost: $json["count"] * 0.50, // $0.50 per prospect
  monthlyTotal: $json["monthlyTotal"] + ($json["count"] * 0.50)
};

// Log to Google Sheets for tracking
```

### 4. Quality Over Quantity

**Focus on ICP Match**:
```
Better: 50 highly-targeted prospects
Worse: 500 loosely-matched prospects

Prioritize:
- Exact job title match
- Company size in range
- Industry alignment
- Geographic targeting
```

---

## Troubleshooting

### Issue: Low Match Rate

**Solutions**:
1. Improve search criteria specificity
2. Use multiple data sources (SURF + Explorium)
3. Broaden job title variations
4. Check company domain accuracy

### Issue: Enrichment Timeouts

**Solutions**:
1. Increase timeout settings (60s → 120s)
2. Process smaller batches
3. Add retry logic with delays
4. Use fallback enrichment sources

### Issue: Incomplete Data

**Solutions**:
1. Use multiple enrichment providers
2. Implement data merging from multiple sources
3. Flag incomplete profiles for manual review
4. Set minimum data requirements

---

## Next Steps

1. **Choose your workflow type**:
   - Automated prospecting (SURF)
   - Inbound enrichment (Explorium)
   - Dream 100 research (Poppy.ai)

2. **Set up prerequisites**:
   - API keys and credentials
   - CRM connection
   - Testing environment

3. **Build and test**:
   - Start with 5-10 test prospects
   - Verify data quality
   - Adjust criteria and prompts

4. **Scale gradually**:
   - Increase batch sizes
   - Monitor costs and quality
   - Iterate based on results

**Related Skills**:
- `mass_personalize_with_ai.md` - Use research for personalization
- `ai_meeting_summarization.md` - Meeting intelligence
- `setup_ai_agent.md` - Agent configuration

---

## Resources

**Tools**:
- SURF: surfe.com
- Explorium: explorium.ai
- Poppy.ai: poppy.ai
- Go High Level: gohighlevel.com

**N8N Documentation**:
- HTTP Request node
- Conditional routing
- Loop patterns
- Error handling

---

Build comprehensive prospect intelligence systems that fuel your sales pipeline with qualified, researched leads.
