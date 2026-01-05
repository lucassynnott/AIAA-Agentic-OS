# Mass Personalization with AI for Cold Email Campaigns

## Overview

Learn how to build a complete N8N workflow that automatically researches prospects and generates highly personalized email icebreakers at scale. Transform generic cold email campaigns into targeted, research-backed outreach that dramatically improves response rates.

## Table of Contents

1. [Workflow Architecture](#workflow-architecture)
2. [Prerequisites and Setup](#prerequisites-and-setup)
3. [Complete Workflow Breakdown](#complete-workflow-breakdown)
4. [Prompt Engineering for Personalization](#prompt-engineering-for-personalization)
5. [Integration with Email Tools](#integration-with-email-tools)
6. [Scaling and Optimization](#scaling-and-optimization)

---

## Workflow Architecture

### What This Workflow Does

**Purpose**: Generate personalized cold email campaigns at scale

**Input**:
- Sender information (name, title)
- Email body template
- Lead list CSV (firstName, lastName, email, company, linkedinUrl)

**Process**:
1. Parse lead list
2. Research each prospect using AI + Perplexity
3. Generate personalized icebreaker for each
4. Combine icebreaker with email body
5. Store results in Google Sheet
6. Send completion notification

**Output**:
- Google Sheet with personalized emails
- Ready to upload to Smartlead/Instantly
- Custom field mapping for email tools

### High-Level Flow

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

---

## Prerequisites and Setup

### Required Services

**1. Google Sheets**
- **Purpose**: Store personalized campaign data
- **Setup**: OAuth2 connection
- **Permissions**: Create and edit spreadsheets

**2. OpenRouter**
- **Purpose**: AI model access (Claude 3.5 Sonnet recommended)
- **Setup**: API key from openrouter.ai
- **Cost**: ~$0.02-0.05 per prospect researched
- **Configuration**:
  ```
  Header Authentication:
  - Header: Authorization
  - Value: Bearer YOUR_API_KEY
  ```

**3. Perplexity**
- **Purpose**: Web research for prospect information
- **Setup**: API key from perplexity.ai/settings
- **Cost**: ~$5-20/month depending on volume
- **Model**: sonar-pro recommended for detailed research

**4. Slack**
- **Purpose**: Campaign completion notifications
- **Setup**: OAuth connection to workspace
- **Configuration**: Select notification channel

### Lead List CSV Format

**Required Columns**:
```csv
firstName,lastName,email,company,linkedinUrl
John,Doe,john@company.com,Acme Corp,https://linkedin.com/in/johndoe
Jane,Smith,jane@startup.io,Startup Inc,https://linkedin.com/in/janesmith
```

**Optional Columns**:
- `position` - Job title
- `website` - Company website
- `industry` - Industry sector
- `customField1` - Additional context

---

## Complete Workflow Breakdown

### Node 1: Campaign Request Form

**Purpose**: Collect campaign parameters from user

**Configuration**:
```
Form Fields:
├── Sender Name (Text)
│   Example: "Lucas Nolan"
├── Sender Title (Text)
│   Example: "Founder at Innovative"
├── Email Script Body (Long Text)
│   Example: "I help agencies automate their operations..."
└── Lead List (CSV Upload)
    Accepts: .csv files only
```

**Form Output**:
```json
{
  "senderName": "Lucas Nolan",
  "senderTitle": "Founder at Innovative",
  "emailBody": "I help agencies automate their operations with AI workflows...",
  "leadListFile": "binary_data"
}
```

### Node 2: Process CSV

**Purpose**: Convert uploaded CSV to JSON array

**Configuration**:
```
Node Type: Read Binary File
Binary Property: leadListFile
Options:
  - Include Binary Data: No
  - Output Format: JSON
```

**Output Example**:
```json
[
  {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@company.com",
    "company": "Acme Corp",
    "linkedinUrl": "https://linkedin.com/in/johndoe"
  },
  {
    "firstName": "Jane",
    "lastName": "Smith",
    "email": "jane@startup.io",
    "company": "Startup Inc",
    "linkedinUrl": "https://linkedin.com/in/janesmith"
  }
]
```

### Node 3: Normalize Data

**Purpose**: Standardize prospect data format

**Code Node**:
```javascript
// Normalize and validate prospect data
const items = $input.all();

const normalizedData = items.map(item => {
  const firstName = item.json.firstName || item.json['First Name'] || '';
  const lastName = item.json.lastName || item.json['Last Name'] || '';
  const email = item.json.email || item.json.Email || '';
  const company = item.json.company || item.json.Company || '';
  const linkedin = item.json.linkedinUrl || item.json['LinkedIn URL'] || '';

  return {
    json: {
      firstName: firstName.trim(),
      lastName: lastName.trim(),
      fullName: `${firstName.trim()} ${lastName.trim()}`,
      email: email.toLowerCase().trim(),
      company: company.trim(),
      linkedinUrl: linkedin.trim(),
      prospectId: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    }
  };
});

return normalizedData;
```

### Node 4: Create Campaign Sheet

**Purpose**: Create Google Sheet to store results

**Configuration**:
```
Google Sheets: Create Spreadsheet
Name: "Cold Email Campaign - {{$now.format('YYYY-MM-DD HH:mm')}}"

Headers:
- Prospect Name
- Prospect Email
- Company Name
- Icebreaker
- Email Body
- Personalized Email
```

**Store Sheet URL**:
```javascript
// Code node after sheet creation
return [{
  json: {
    spreadsheetId: $json["spreadsheetId"],
    spreadsheetUrl: $json["spreadsheetUrl"],
    campaignName: `Campaign ${new Date().toISOString()}`
  }
}];
```

### Node 5: Loop Over Items

**Purpose**: Process each prospect individually

**Configuration**:
```
Loop Over Items Node:
- Mode: "Run Once for Each Item"
- Batch Size: 1
```

### Node 6: Prospect Research Agent

**Purpose**: Research prospect using AI and web search

**AI Agent Configuration**:
```
Chat Model: OpenRouter (Claude 3.5 Sonnet)
Temperature: 0.7
Max Tokens: 2000

Tools Enabled:
└── Perplexity
    ├── Model: sonar-pro
    ├── Max Tokens: 4000
    └── Return Sources: Yes
```

**System Prompt**:
```
You are a prospect research specialist for B2B cold email campaigns.

Your task: Research this prospect and find specific, recent information that can be used for email personalization.

Prospect Details:
- Name: {{$json["fullName"]}}
- Company: {{$json["company"]}}
- LinkedIn: {{$json["linkedinUrl"]}}

Research Focus:
1. Recent professional activity (last 3 months)
   - LinkedIn posts or articles
   - Podcast appearances
   - Conference talks or webinars
   - Company announcements

2. Company context
   - Recent funding or growth
   - New product launches
   - Market position and competitors
   - Notable achievements

3. Personal professional brand
   - Areas of expertise
   - Content themes
   - Industry involvement
   - Unique positioning

Research Guidelines:
- Prioritize RECENT information (last 3 months preferred)
- Find SPECIFIC events, not generic information
- Look for PUBLIC content they created or participated in
- Identify potential pain points in their role/industry

Output Requirements:
Provide a structured research report with:

**Recent Activity**:
[Specific recent events, posts, announcements]

**Company Context**:
[Current company situation, recent news, market position]

**Professional Focus**:
[Their expertise areas, content themes, industry involvement]

**Potential Pain Points**:
[Challenges they likely face based on role/industry]

**Personalization Hooks**:
[3-5 specific things that could be referenced in email]

Be specific and factual. Cite dates when possible.
```

**Output Example**:
```
Recent Activity:
- Posted on LinkedIn about scaling agency operations on March 15, 2025
- Appeared on "The Sauce" podcast discussing 10K MRR strategies on March 10, 2025
- Launched new AI automation service offering on February 28, 2025

Company Context:
- Agency specializing in content marketing for B2B SaaS
- Recently expanded team from 5 to 12 people
- Targeting mid-market companies ($5M-50M revenue)

Professional Focus:
- Systems and automation for agencies
- Content marketing strategies
- AI implementation for service businesses

Potential Pain Points:
- Managing larger team while maintaining quality
- Scaling operations without proportional cost increase
- Content production bottlenecks
- Client onboarding and delivery systems

Personalization Hooks:
1. Reference "The Sauce" podcast episode on scaling to 10K MRR
2. Mention recent team expansion and scaling challenges
3. Connect to AI automation service launch
4. Reference content flywheel strategy mentioned in LinkedIn post
5. Address systems needed for 5-figure MRR operations
```

### Node 7: Icebreaker Writer Agent

**Purpose**: Generate personalized first line for email

**AI Agent Configuration**:
```
Chat Model: OpenRouter (Claude 3.5 Sonnet)
Temperature: 0.8 (slightly higher for creativity)
Max Tokens: 200
```

**System Prompt**:
```
You are an expert cold email icebreaker writer for B2B outreach campaigns.

Your goal is to write a highly personalized first line that:
1. References specific, recent activity or achievement
2. Shows genuine research (not generic compliments)
3. Creates curiosity and relevance
4. Flows naturally into the email body
5. Is 1-2 sentences maximum

You receive:
- Prospect Name: {{$json["fullName"]}}
- Company: {{$json["company"]}}
- Research Analysis: {{$json["researchReport"]}}
- Email Body Context: {{$json["emailBody"]}}

Context About the Email:
The email body discusses: {{$json["emailBody"]}}
This icebreaker needs to transition naturally into that topic.

Writing Guidelines:
✅ DO:
- Reference something SPECIFIC (not "I saw your company")
- Mention something from the last 3 months
- Show you understand their world
- Be conversational and genuine
- Create relevance to the email topic

❌ DON'T:
- Use generic compliments ("Your company is great!")
- Ask questions in the icebreaker
- Use over-the-top flattery
- Be vague ("I love what you're doing")
- Make it about you

GOOD Examples:
"Just caught your breakdown on scaling agencies to 10K MRR in 6 months on The Sauce podcast - the content flywheel strategy you outlined really resonated."

"Noticed you launched the new AI-powered analytics dashboard last week - the real-time cohort analysis feature looks like it could be a game-changer for your space."

"Saw your LinkedIn post about finally cracking the content production bottleneck at scale - that's exactly what we've been helping agencies like yours solve."

BAD Examples:
"I love what you're doing at [Company]" (too generic, no specifics)
"Your company is amazing!" (empty flattery, no value)
"Can I ask you about [topic]?" (don't ask questions in opener)
"I wanted to reach out because..." (makes it about sender, not recipient)

Output Format:
Provide ONLY the icebreaker text. No explanation, no formatting, no quotation marks.
Just the 1-2 sentence icebreaker that will be used as the email opener.
```

**Output Example**:
```
Just caught your latest episode on The Sauce podcast about scaling agencies to 10K MRR in 6 months - the content flywheel strategy you broke down especially resonated with challenges we're seeing across agencies in your space.
```

### Node 8: Format Final Email

**Purpose**: Combine icebreaker with email body

**Code Node**:
```javascript
// Combine icebreaker with email body template
const icebreaker = $json["icebreaker"].trim();
const emailBody = $input.first().json["emailBody"];
const firstName = $json["firstName"];

// Format final personalized email
const personalizedEmail = `Hi ${firstName},

${icebreaker}

${emailBody}`;

return [{
  json: {
    prospectName: $json["fullName"],
    prospectEmail: $json["email"],
    companyName: $json["company"],
    icebreaker: icebreaker,
    emailBody: emailBody,
    personalizedEmail: personalizedEmail,
    researchSummary: $json["researchReport"],
    timestamp: new Date().toISOString()
  }
}];
```

**Output Example**:
```
Hi John,

Just caught your latest episode on The Sauce podcast about scaling agencies to 10K MRR in 6 months - the content flywheel strategy you broke down especially resonated with challenges we're seeing across agencies in your space.

I help agencies automate their operations with AI workflows that eliminate bottlenecks in content production and client delivery. We've helped similar agencies scale from 5 to 15+ clients without adding proportional overhead.

Would love to show you how we could help systemize your operations as you continue scaling. Are you open to a quick 15-minute call this week?

Best,
Lucas Nolan
Founder, Innovative
```

### Node 9: Append to Google Sheet

**Purpose**: Store personalized email in campaign sheet

**Configuration**:
```
Google Sheets: Append Row
Spreadsheet: {{$node["Create Campaign Sheet"].json["spreadsheetId"]}}
Sheet: Sheet1

Columns:
├── A: {{$json["prospectName"]}}
├── B: {{$json["prospectEmail"]}}
├── C: {{$json["companyName"]}}
├── D: {{$json["icebreaker"]}}
├── E: {{$json["emailBody"]}}
└── F: {{$json["personalizedEmail"]}}
```

### Node 10: Slack Notification

**Purpose**: Notify when campaign is complete

**Configuration**:
```
Slack: Send Message
Channel: #campaigns (or your preferred channel)

Message:
*Cold Email Campaign Complete!* ✅

Campaign Sheet: {{$node["Create Campaign Sheet"].json["spreadsheetUrl"]}}
Leads Processed: {{$json["totalLeads"]}}
Completion Time: {{$now.format('HH:mm')}}

*Next Steps:*
1. Review personalized emails in sheet
2. Download as CSV
3. Upload to Smartlead/Instantly
4. Map 'icebreaker' column as custom variable
5. Launch campaign

The icebreaker column should be mapped as a custom field in your email template:
`Hi {{firstName}}, {{custom.icebreaker}}`
```

---

## Prompt Engineering for Personalization

### Research Quality Principles

**1. Specificity Over Generality**
```
❌ Bad: "They work in marketing"
✅ Good: "Posted about scaling content production 80% faster using AI on LinkedIn March 15, 2025"
```

**2. Recency Matters**
```
❌ Bad: "The company was founded in 2018"
✅ Good: "Just launched new AI automation service 2 weeks ago"
```

**3. Public Actions > Assumptions**
```
❌ Bad: "Probably struggles with team management"
✅ Good: "Mentioned team scaling challenges in podcast interview"
```

### Icebreaker Writing Principles

**1. Reference Formula**:
```
[Action you took] + [Specific thing you found] + [Why it's relevant/resonated]

Example:
"Just caught your breakdown on scaling agencies to 10K MRR on The Sauce podcast -
the content flywheel strategy especially resonated."
```

**2. Transition Bridge**:
```
Icebreaker should naturally lead into email body topic

If email is about automation:
✅ "Saw your post about content production bottlenecks - that's exactly what we solve"
❌ "Congrats on the award!" (doesn't connect to automation topic)
```

**3. Tone Calibration**:
```
Match prospect's communication style:

Corporate Executive:
"Noticed the Q4 earnings call mentioned operational efficiency as a 2025 priority"

Startup Founder:
"Just saw you're finally tackling the content bottleneck - been there!"
```

---

## Integration with Email Tools

### Smartlead Integration

**Step 1: Export from Google Sheet**
```
1. Open campaign sheet
2. File → Download → CSV (.csv)
3. Save as: campaign-YYYY-MM-DD.csv
```

**Step 2: Upload to Smartlead**
```
1. Go to Smartlead dashboard
2. Campaigns → Create New Campaign
3. Upload CSV file
4. Map columns:
   - Email → prospectEmail
   - First Name → firstName (from prospectName)
   - Company → companyName
   - Custom Field 1 → icebreaker
```

**Step 3: Create Email Template**
```
Subject: Quick question about {{company}}

Body:
Hi {{firstName}},

{{custom_field_1}}

I help agencies automate their operations with AI workflows that eliminate
bottlenecks in content production and client delivery. We've helped similar
agencies scale from 5 to 15+ clients without adding proportional overhead.

Would love to show you how we could help systemize your operations as you
continue scaling. Are you open to a quick 15-minute call this week?

Best,
{{sender_name}}
{{sender_title}}
```

### Instantly Integration

**CSV Mapping**:
```
Instantly Required Columns:
├── email → prospectEmail
├── firstName → (extract from prospectName)
├── lastName → (extract from prospectName)
├── companyName → companyName
└── icebreaker → icebreaker (custom variable)
```

**Email Template**:
```
Subject: {{firstName}}, saw your recent work on [topic]

Body:
Hi {{firstName}},

{{icebreaker}}

[Rest of email body]

Best,
[Your name]
```

### Custom Variable Best Practices

**1. Always Use Custom Variables for Icebreakers**
```
❌ Bad: Hard-code icebreaker into template
✅ Good: Use {{custom.icebreaker}} variable
```

**2. Fallback Values**
```
Template with fallback:
{{custom.icebreaker | default: "I came across your profile and thought you might be interested in..."}}
```

**3. Testing**
```
Before launching:
1. Send test email to yourself
2. Verify icebreaker renders correctly
3. Check spacing and formatting
4. Confirm links work
```

---

## Scaling and Optimization

### Batch Processing

**Handle Large Lead Lists**:

```javascript
// Split large lists into batches of 50
const allItems = $input.all();
const batchSize = 50;
const batches = [];

for (let i = 0; i < allItems.length; i += batchSize) {
  batches.push(allItems.slice(i, i + batchSize));
}

// Process each batch with delay
return batches.map((batch, index) => ({
  json: {
    batchNumber: index + 1,
    batchSize: batch.length,
    leads: batch,
    delaySeconds: index * 60 // 60 second delay between batches
  }
}));
```

### Rate Limiting

**Perplexity API Limits**:
```
Free Tier: 5 requests/minute
Pro Tier: 50 requests/minute

Solution: Add wait node between research calls
Wait Time:
- Free tier: 15 seconds between requests
- Pro tier: 2 seconds between requests
```

**Implementation**:
```
Loop Over Items
    ↓
Research Agent
    ↓
Wait Node (15 seconds)
    ↓
Icebreaker Writer
    ↓
Continue...
```

### Cost Optimization

**Model Selection by Task**:

```
Research Agent:
├── Primary: Claude 3.5 Sonnet (~$0.015/prospect)
│   - Best quality research
└── Budget: Gemini 2.0 Flash Free (~$0.00/prospect)
    - Good for high volume, lower quality acceptable

Icebreaker Writer:
├── Primary: Claude 3.5 Sonnet (~$0.005/prospect)
│   - Best personalization quality
└── Budget: GPT-4 Turbo (~$0.003/prospect)
    - Good balance of quality and cost
```

**Cost Per Prospect**:
```
Full Quality:
- Research: $0.015
- Icebreaker: $0.005
- Total: $0.02 per prospect

Budget Mode:
- Research: $0.00 (Gemini Free)
- Icebreaker: $0.003 (GPT-4 Turbo)
- Total: $0.003 per prospect

100 prospects:
- Full Quality: $2.00
- Budget Mode: $0.30
```

### Quality Control

**Icebreaker Validation**:

```javascript
// Code node after Icebreaker Writer
const icebreaker = $json["icebreaker"];

// Quality checks
const issues = [];

// Check length
if (icebreaker.length < 50) {
  issues.push("Too short - needs more substance");
}
if (icebreaker.length > 300) {
  issues.push("Too long - should be 1-2 sentences");
}

// Check for generic phrases
const genericPhrases = [
  "I love what you're doing",
  "your company is amazing",
  "I wanted to reach out",
  "hope you're doing well"
];

genericPhrases.forEach(phrase => {
  if (icebreaker.toLowerCase().includes(phrase)) {
    issues.push(`Contains generic phrase: "${phrase}"`);
  }
});

// Check for question marks (shouldn't ask questions)
if (icebreaker.includes('?')) {
  issues.push("Contains question - icebreakers shouldn't ask questions");
}

return [{
  json: {
    icebreaker: icebreaker,
    qualityScore: issues.length === 0 ? "PASS" : "REVIEW",
    issues: issues,
    prospectName: $json["prospectName"]
  }
}];
```

**Manual Review Workflow**:
```
IF Quality Score = "REVIEW":
    → Send to Slack for human review
    → Pause workflow
    → Wait for approval/edit
ELSE:
    → Proceed automatically
```

### Performance Monitoring

**Track Campaign Metrics**:

```javascript
// After campaign completion
const metrics = {
  campaignId: $json["spreadsheetId"],
  timestamp: new Date().toISOString(),
  totalLeads: $json["totalLeads"],
  successfulResearch: $json["researchSuccess"],
  failedResearch: $json["researchFailed"],
  averageResearchTime: $json["avgResearchTime"],
  averageIcebreakerLength: $json["avgIcebreakerLength"],
  totalCost: $json["totalApiCost"],
  costPerLead: $json["totalApiCost"] / $json["totalLeads"]
};

// Log to tracking sheet
Google Sheets: Append Row
Sheet: "Campaign Metrics"
Values: metrics
```

---

## Troubleshooting

### Issue: Research Agent Returns Generic Info

**Solutions**:
1. **Improve research prompt specificity**:
   ```
   Add: "Focus on the last 3 months of activity ONLY"
   Add: "Prioritize content they created over company info"
   ```

2. **Enable Perplexity sources**:
   ```
   Return Sources: Yes
   Recent: Last 3 months
   ```

3. **Add validation step**:
   ```javascript
   // Check if research includes dates
   if (!$json["researchReport"].match(/\d{4}|\b(january|february|march|...|december)\b/i)) {
     // Flag for manual review
   }
   ```

### Issue: Icebreakers Too Generic

**Solutions**:
1. **Add negative examples to prompt**:
   ```
   "DO NOT write things like:
   - I love what you're doing
   - Your company is great
   - I wanted to reach out"
   ```

2. **Increase temperature slightly**:
   ```
   Temperature: 0.8 (from 0.7)
   - More creative/specific icebreakers
   ```

3. **Require specific elements**:
   ```
   "Your icebreaker MUST include:
   - A specific date OR
   - A specific piece of content OR
   - A specific achievement"
   ```

### Issue: High API Costs

**Solutions**:
1. **Use free models for testing**:
   ```
   Research: Gemini 2.0 Flash (free)
   Icebreaker: DeepSeek R1 (free)
   ```

2. **Reduce research depth**:
   ```
   Max Tokens: 2000 → 1000
   Perplexity searches: 3 → 1
   ```

3. **Batch process during off-peak**:
   ```
   Schedule workflow for night/weekend
   Process 100-200 leads at once
   ```

### Issue: Workflow Timeout

**Solutions**:
1. **Increase timeout**:
   ```
   AI Agent timeout: 60s → 90s
   Workflow timeout: 5min → 10min
   ```

2. **Add error recovery**:
   ```
   On Error: Continue with next item
   Log failed items to separate sheet
   Retry failed items later
   ```

3. **Process in smaller batches**:
   ```
   Batch size: 100 → 25 prospects per run
   Multiple workflow executions
   ```

---

## Advanced Techniques

### Multi-Language Support

```javascript
// Detect prospect language from LinkedIn URL
const linkedinUrl = $json["linkedinUrl"];
const language = linkedinUrl.includes('/in/') ? 'en' :
                linkedinUrl.includes('/fr/') ? 'fr' : 'en';

// Add to research prompt
const researchPrompt = `Research this prospect and generate insights in ${language}.`;
```

### Industry-Specific Research

```javascript
// Customize research based on industry
const industryResearchFocus = {
  'saas': 'product launches, feature updates, user growth',
  'agency': 'client work, case studies, team scaling',
  'ecommerce': 'revenue milestones, product lines, market expansion',
  'consulting': 'thought leadership, speaking engagements, publications'
};

const focus = industryResearchFocus[$json["industry"]] || 'recent professional activity';
```

### A/B Testing Icebreakers

```
Generate 3 variations per prospect:
1. Reference-based: Mention specific content
2. Achievement-based: Highlight accomplishment
3. Problem-based: Address pain point

Store all 3 in sheet
Manually select best one before sending
Track which type performs best
```

---

## Next Steps

1. **Set up workflow** following node-by-node guide
2. **Test with 5-10 prospects** before scaling
3. **Review quality** of research and icebreakers
4. **Adjust prompts** based on output quality
5. **Scale to full campaigns** once validated
6. **Track response rates** and iterate

**Related Skills**:
- `ai_prospect_research.md` - Deep research workflows
- `setup_ai_agent.md` - Agent configuration details
- `build_ai_workflow_n8n.md` - General N8N workflows

---

## Resources

**N8N Nodes Used**:
- Form Trigger
- Read Binary File (CSV)
- Code (JavaScript)
- AI Agent with Perplexity
- Google Sheets
- Slack

**External Tools**:
- Smartlead: smartlead.ai
- Instantly: instantly.ai
- Perplexity: perplexity.ai
- OpenRouter: openrouter.ai

---

Transform generic cold email into research-backed, personalized outreach at scale.
