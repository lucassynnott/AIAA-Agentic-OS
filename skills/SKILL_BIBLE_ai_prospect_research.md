# SKILL BIBLE: AI-Powered Prospect Research & Enrichment Systems

## Executive Summary

This skill bible teaches you to build comprehensive AI-powered prospect research workflows that automatically find, enrich, and analyze target prospects at scale. You'll learn to integrate multiple data sources (SURF API, Explorium, Poppy.ai) with AI agents to create detailed prospect lists with contact information, professional backgrounds, and actionable insights for sales teams.

The system covers three distinct workflow types: automated prospect list building for cold outreach campaigns, inbound lead enrichment for meeting preparation, and high-touch Dream 100 research for top prospects. By mastering these workflows, you'll be able to transform raw prospect data into comprehensive intelligence that drives sales conversations and improves conversion rates.

This skill is essential for sales teams, marketing professionals, and business development representatives who need to research prospects efficiently while maintaining personalization at scale. The workflows can process hundreds of prospects automatically while providing the depth of research typically reserved for manual, high-touch approaches.

## Source
- **Type:** Internal SOP/Skill Document
- **Category:** ai-workflows
- **Original File:** ai_prospect_research.md

## Core Principles

### 1. Multi-Source Data Integration
Combine multiple enrichment sources (SURF API, Explorium, LinkedIn) to create comprehensive prospect profiles. No single data source provides complete information, so layering multiple sources ensures higher data quality and completeness. This approach reduces the risk of missing critical prospect information that could impact outreach effectiveness.

### 2. Quality Over Quantity Prioritization
Focus on highly-targeted prospects that match your Ideal Customer Profile (ICP) rather than generating large volumes of loosely-matched contacts. 50 highly-targeted prospects with complete data profiles will outperform 500 generic contacts with minimal information. This principle drives better conversion rates and reduces wasted outreach efforts.

### 3. Automated Workflow Orchestration
Design workflows that handle the complete prospect research lifecycle from initial discovery through CRM integration. Automation should include data validation, enrichment status monitoring, duplicate detection, and error handling to ensure reliable operation without manual intervention.

### 4. AI-Enhanced Analysis and Personalization
Leverage AI agents to transform raw prospect data into actionable insights, meeting preparation documents, and personalized outreach messages. AI analysis should identify conversation starters, potential pain points, recent activities, and strategic talking points that human researchers would discover manually.

### 5. Cost-Conscious Scaling
Implement rate limiting, batch processing, and usage tracking to manage enrichment costs while maintaining data quality. Monitor monthly API usage, implement delays between requests, and track cost-per-prospect to ensure sustainable scaling without budget overruns.

### 6. Real-Time Enrichment Triggers
Set up event-driven enrichment workflows that activate when prospects take specific actions (booking meetings, visiting websites, downloading content). This ensures sales teams have fresh research available exactly when they need it for maximum impact.

### 7. Structured Data Output
Standardize prospect data formats for consistent CRM integration and AI agent consumption. Use structured schemas that include required fields, optional enrichment data, and metadata for tracking data sources and freshness.

### 8. Continuous Quality Validation
Implement validation checks at each workflow stage to ensure data accuracy, completeness, and relevance. Include email validation, duplicate detection, ICP scoring, and data freshness tracking to maintain high-quality prospect databases.

## Step-by-Step Process

### Phase 1: Workflow Architecture Setup

**Step 1: Define Prospect Research Requirements**
- Identify your Ideal Customer Profile (ICP) criteria including industry, company size, job titles, and geographic location
- Determine required data fields for your sales process (contact info, company details, professional background)
- Establish data quality standards and validation rules
- Define success metrics for prospect research workflows

**Step 2: Configure Data Source APIs**
- Set up SURF API account and obtain API key from surfe.com settings
- Configure Explorium API access through their sales team
- Create Poppy.ai account for Dream 100 research
- Test API connections and understand rate limits and pricing structures

**Step 3: Prepare N8N Environment**
- Install required N8N nodes (HTTP Request, Code, Gmail, Google Docs, CRM connectors)
- Configure authentication credentials for each API service
- Set up error handling and logging mechanisms
- Create development and production workflow environments

### Phase 2: Automated Prospect List Builder Implementation

**Step 4: Build Prospect Criteria Input Form**
Create form with fields:
- Industry (text input with examples: "SaaS", "E-commerce", "Marketing Agencies")
- Max Employee Count (number input: 50, 200, 1000)
- Country Code (dropdown: US, UK, CA, AU)
- Your Name and Email for notifications

**Step 5: Implement Company Search Logic**
```javascript
// SURF API company search configuration
{
  "filters": {
    "industry": "{{$json['industry']}}",
    "employee_count_max": {{$json["maxEmployees"]}},
    "country": "{{$json['country']}}"
  },
  "limit": 20
}
```

**Step 6: Extract and Process Company Data**
- Parse company search results to extract names, domains, employee counts
- Filter companies based on additional criteria if needed
- Prepare data structure for employee search phase

**Step 7: Search for Target Employees**
Configure employee search with job title targeting:
```javascript
{
  "company_domain": "{{$json['domain']}}",
  "job_titles": [
    "CEO", "Founder", "Owner",
    "VP Marketing", "CMO", "Marketing Director"
  ],
  "limit": 5
}
```

**Step 8: Implement Contact Enrichment**
- Submit person IDs for enrichment with required fields (email, phone, LinkedIn)
- Monitor enrichment status with polling loop and 3-second delays
- Handle enrichment timeouts and retry logic

**Step 9: Process Enriched Data**
```javascript
// Structure enriched prospect data
const people = enrichmentResults.map(person => ({
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
```

**Step 10: Validate and Clean Data**
- Implement email validation using regex patterns
- Check for duplicate contacts in existing CRM
- Verify required fields are populated
- Flag incomplete profiles for manual review

### Phase 3: CRM Integration and Notification

**Step 11: Integrate with Go High Level CRM**
Configure contact creation with fields:
- Basic contact information (name, email, phone)
- Company details and job title
- Source tracking and enrichment metadata
- Appropriate tags for segmentation

**Step 12: Set Up Automated Notifications**
- Email notifications with prospect counts and next steps
- Slack notifications for team awareness
- Dashboard updates for tracking workflow performance

### Phase 4: Inbound Lead Enrichment Workflow

**Step 13: Configure Calendly Webhook Integration**
- Set up webhook to trigger on meeting bookings
- Extract prospect information from Calendly payload
- Check for existing contacts in CRM before processing

**Step 14: Implement Explorium Enrichment**
```javascript
// Explorium match and enrich process
{
  "email": "{{$json['email']}}",
  "name": "{{$json['name']}}",
  "company": "{{$json['company']}}"
}
```

**Step 15: Structure Profile Data for AI Analysis**
```javascript
// Format enriched data for AI consumption
const bio = {
  name: profile.full_name,
  city: profile.location.city,
  currentPosition: profile.current_job.title,
  currentCompany: profile.current_job.company,
  companyDescription: profile.current_job.description,
  previousExperience: profile.work_history,
  linkedinUrl: profile.linkedin_url,
  education: profile.education
};
```

### Phase 5: AI-Powered Meeting Preparation

**Step 16: Configure AI Research Agent**
Set up OpenRouter with Claude 3.5 Sonnet:
- Temperature: 0.7 for balanced creativity and accuracy
- Max Tokens: 3000 for comprehensive analysis
- Include Perplexity tool for additional research

**Step 17: Implement Meeting Prep Document Generation**
Create comprehensive system prompt for AI agent:
```
You are an AI agent specializing in generating meeting preparation documents.

Research Focus:
- Recent company news and updates (last 3 months)
- Industry trends affecting their company
- Competitive landscape
- Recent professional activity
- Company growth trajectory

Output Format:
# Meeting Prep: [Name]
## Executive Summary
## Professional Background
## Company Context
## Meeting Strategy
## Quick Facts
```

**Step 18: Generate and Distribute Research Documents**
- Convert AI output to Google Docs using MD2Docs
- Send HTML email with formatted research
- Store documents in organized folder structure

### Phase 6: Dream 100 High-Touch Research

**Step 19: Set Up Poppy.ai Research Board**
Create three groups:
- Dream 100 Prospects (LinkedIn, YouTube, Twitter URLs)
- System Prompt (research and writing instructions)
- Information About You (your offer and context)

**Step 20: Configure Personalization Prompts**
```
System Instructions:
Find key information and write personalized first-line DM mentioning something specific about them in positive manner.

Structure: "I made you [DELIVERABLE] because I saw [SPECIFIC OBSERVATION] on your [PLATFORM]."

Guidelines:
- Reference something SPECIFIC (not generic)
- Show genuine research and understanding
- Create relevance to your offer
- Be conversational, not salesy
- 2-3 sentences maximum
```

**Step 21: Generate and Track Personalized Outreach**
- Process prospects in batches of 10-20
- Generate personalized first lines for each
- Copy outputs to tracking spreadsheet
- Monitor response rates and iterate messaging

### Phase 7: Quality Assurance and Optimization

**Step 22: Implement Data Quality Checks**
```javascript
// Email validation function
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email) && email.length > 5;
}

// Duplicate detection
const existingEmails = new Set(crmContacts.map(c => c.email));
const newProspects = prospects.filter(p => !existingEmails.has(p.email));
```

**Step 23: Monitor and Optimize Performance**
- Track enrichment success rates by source
- Monitor API usage and costs
- Measure prospect-to-opportunity conversion rates
- Adjust ICP criteria based on results

**Step 24: Scale and Maintain Workflows**
- Implement batch processing for large prospect lists
- Set up monitoring alerts for workflow failures
- Regular API credential rotation and testing
- Documentation updates for team training

## Frameworks & Templates

### SURF API Integration Framework

**Authentication Setup:**
```
HTTP Request Node Configuration:
├── Method: POST
├── URL: https://api.surfe.com/v2/[endpoint]
├── Authentication: Header Auth
└── Credentials:
    ├── Name: Authorization
    └── Value: [SURF_API_KEY]
```

**Company Search Template:**
```json
{
  "filters": {
    "industry": "{{industry}}",
    "employee_count_max": {{maxEmployees}},
    "employee_count_min": {{minEmployees}},
    "country": "{{countryCode}}",
    "technologies": ["{{techStack}}"],
    "funding_stage": "{{fundingStage}}"
  },
  "limit": 50,
  "offset": 0
}
```

**Employee Search Template:**
```json
{
  "company_domain": "{{companyDomain}}",
  "job_titles": [
    "CEO", "Founder", "Co-Founder",
    "VP Marketing", "CMO", "Marketing Director",
    "VP Sales", "CRO", "Sales Director",
    "CTO", "VP Engineering", "Head of Product"
  ],
  "seniority_levels": ["senior", "executive"],
  "departments": ["marketing", "sales", "executive"],
  "limit": 10
}
```

### Explorium Enrichment Framework

**Profile Matching Template:**
```json
{
  "contacts": [
    {
      "email": "{{email}}",
      "first_name": "{{firstName}}",
      "last_name": "{{lastName}}",
      "company": "{{company}}",
      "job_title": "{{jobTitle}}"
    }
  ],
  "match_threshold": 0.8,
  "include_social_profiles": true
}
```

**Enrichment Request Template:**
```json
{
  "prospect_ids": ["{{prospectId}}"],
  "fields": [
    "professional_background",
    "work_history",
    "education",
    "social_profiles",
    "contact_information",
    "company_information",
    "location_data"
  ]
}
```

### AI Meeting Prep Document Template

```markdown
# Meeting Prep: {{prospectName}}

## Executive Summary
{{aiGeneratedSummary}}

## Professional Background
### Current Role
- **Position:** {{currentJobTitle}}
- **Company:** {{currentCompany}}
- **Tenure:** {{jobTenure}}
- **Responsibilities:** {{jobDescription}}

### Career Journey
{{formattedWorkHistory}}

### Education & Expertise
{{educationBackground}}
{{keyExpertiseAreas}}

## Company Context
### About {{companyName}}
- **Industry:** {{industry}}
- **Size:** {{employeeCount}} employees
- **Founded:** {{foundedYear}}
- **Mission:** {{companyMission}}

### Recent Developments
{{recentCompanyNews}}

### Industry Landscape
{{industryTrends}}
{{competitivePosition}}

## Meeting Strategy
### Recommended Talking Points
1. {{talkingPoint1}}
2. {{talkingPoint2}}
3. {{talkingPoint3}}

### Questions to Ask
1. {{strategicQuestion1}}
2. {{strategicQuestion2}}
3. {{strategicQuestion3}}

### Potential Objections
- {{objection1}} → {{response1}}
- {{objection2}} → {{response2}}

## Quick Facts
- **Meeting Date:** {{meetingDate}}
- **Duration:** {{meetingDuration}}
- **Decision Authority:** {{decisionMakingRole}}
- **Budget Authority:** {{budgetInfluence}}
```

### CRM Integration Schema

**Go High Level Contact Creation:**
```json
{
  "firstName": "{{firstName}}",
  "lastName": "{{lastName}}",
  "email": "{{email}}",
  "phone": "{{phone}}",
  "companyName": "{{company}}",
  "website": "{{companyWebsite}}",
  "source": "Automated Prospecting",
  "tags": ["Prospect", "Enriched", "{{industry}}"],
  "customFields": {
    "LinkedIn_URL": "{{linkedinUrl}}",
    "Job_Title": "{{jobTitle}}",
    "Location": "{{location}}",
    "Enrichment_Date": "{{enrichmentDate}}",
    "Enrichment_Source": "{{enrichmentSource}}",
    "Company_Size": "{{employeeCount}}",
    "Industry": "{{industry}}",
    "ICP_Score": "{{icpScore}}"
  }
}
```

### Prospect Scoring Framework

**ICP Scoring Matrix:**
```javascript
function calculateICPScore(prospect) {
  let score = 0;
  
  // Company size (0-30 points)
  if (prospect.employeeCount >= 50 && prospect.employeeCount <= 500) score += 30;
  else if (prospect.employeeCount >= 20 && prospect.employeeCount <= 1000) score += 20;
  else score += 10;
  
  // Industry match (0-25 points)
  const targetIndustries = ['SaaS', 'Technology', 'Marketing', 'E-commerce'];
  if (targetIndustries.includes(prospect.industry)) score += 25;
  
  // Job title relevance (0-25 points)
  const decisionMakers = ['CEO', 'Founder', 'VP', 'Director', 'CMO', 'CTO'];
  if (decisionMakers.some(title => prospect.jobTitle.includes(title))) score += 25;
  
  // Geographic preference (0-10 points)
  const preferredRegions = ['US', 'CA', 'UK', 'AU'];
  if (preferredRegions.includes(prospect.country)) score += 10;
  
  // Data completeness (0-10 points)
  const requiredFields = ['email', 'phone', 'linkedinUrl'];
  const completedFields = requiredFields.filter(field => prospect[field]);
  score += (completedFields.length / requiredFields.length) * 10;
  
  return Math.round(score);
}
```

## Best Practices

### Data Quality Management

**Email Validation Standards:**
- Use regex pattern: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- Minimum length: 5 characters
- Exclude role-based emails (info@, admin@, support@)
- Verify domain exists and accepts mail
- Check against suppression lists

**Duplicate Prevention:**
- Search CRM before creating new contacts
- Use email as primary deduplication key
- Check LinkedIn URLs for profile matches
- Implement fuzzy matching for name variations
- Maintain master prospect database with unique identifiers

**Data Freshness Tracking:**
- Timestamp all enrichment activities
- Set data expiration periods (90 days for contact info, 30 days for job titles)
- Flag stale data for re-enrichment
- Track data source reliability scores
- Implement automatic data refresh workflows

### API Rate Limiting and Cost Control

**SURF API Optimization:**
- Process prospects in batches of 20-50
- Implement 3-second delays between enrichment requests
- Monitor monthly usage against plan limits (150 for Essential, 1000 for Pro)
- Use company search filters to reduce irrelevant results
- Cache company data to avoid duplicate searches

**Explorium Cost Management:**
- Batch enrichment requests to minimize API calls
- Use match confidence thresholds to avoid low-quality enrichments
- Implement prospect scoring to prioritize high-value targets
- Track cost-per-prospect and ROI metrics
- Set monthly budget alerts and automatic shutoffs

**Error Handling and Retry Logic:**
```javascript
// Exponential backoff retry pattern
async function enrichWithRetry(prospectId, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await enrichProspect(prospectId);
      return result;
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### Workflow Performance Optimization

**Parallel Processing:**
- Process multiple prospects simultaneously where API limits allow
- Use N8N's split/merge patterns for batch operations
- Implement queue management for large prospect lists
- Monitor system resources and adjust concurrency

**Caching Strategies:**
- Cache company information to avoid duplicate lookups
- Store enriched profiles with expiration dates
- Implement local prospect database for quick searches
- Use Redis or similar for high-performance caching

**Monitoring and Alerting:**
- Set up workflow failure notifications
- Monitor API response times and error rates
- Track prospect processing volumes and success rates
- Implement health checks for critical workflow components

### AI Agent Optimization

**Prompt Engineering:**
- Use specific, detailed system prompts with clear output formats
- Include relevant context about your business and ideal prospects
- Implement few-shot examples for consistent output quality
- Test prompts with diverse prospect types and iterate

**Token Management:**
- Optimize prompt length to balance detail and cost
- Use structured output formats to reduce token usage
- Implement content summarization for long prospect profiles
- Monitor token usage and costs across all AI operations

**Quality Assurance:**
- Implement human review for high-value prospects
- Use AI confidence scores to flag uncertain analyses
- A/B test different prompt variations for effectiveness
- Maintain feedback loops to improve AI performance

## Common Mistakes to Avoid

### Data Quality Pitfalls

**Over-Reliance on Single Data Source:**
Never depend solely on one enrichment provider. SURF may have excellent company data but limited contact information, while Explorium might have detailed professional backgrounds but outdated job titles. Always implement multi-source validation and use the best data from each provider.

**Ignoring Data Validation:**
Failing to validate email addresses, phone numbers, and LinkedIn URLs leads to wasted outreach efforts and poor deliverability. Implement comprehensive validation at every step, including syntax checking, domain verification, and format standardization.

**Batch Processing Without Rate Limiting:**
Attempting to process large prospect lists without proper rate limiting will trigger API blocks and potentially get your account suspended. Always implement delays, monitor usage, and respect provider limits.

### Workflow Design Errors

**Insufficient Error Handling:**
Not implementing proper error handling and retry logic leads to workflow failures and data loss. Every API call should have timeout handling, retry mechanisms, and fallback options.

**Missing Duplicate Detection:**
Creating duplicate contacts in your CRM wastes resources and confuses sales teams. Always search for existing contacts before creating new ones, and implement deduplication logic based on email addresses and LinkedIn profiles.

**Poor Data Structure:**
Inconsistent data formatting makes it difficult to use prospect information effectively. Standardize all data fields, use consistent naming conventions, and implement validation schemas.

### AI Implementation Mistakes

**Generic Prompts:**
Using vague or generic prompts produces low-quality research and personalization. Be specific about the type of insights you want, the format of the output, and the context of your business.

**Insufficient Context:**
Not providing enough context about your business, ideal customers, and value proposition leads to irrelevant AI analysis. Include comprehensive background information in your prompts.

**No Quality Control:**
Accepting AI output without review can lead to embarrassing mistakes in prospect outreach. Always implement review processes for high-value prospects and maintain human oversight.

### Scaling Challenges

**Premature Scaling:**
Attempting to scale workflows before validating data quality and process effectiveness leads to expensive mistakes at scale. Start with small batches, validate results, and gradually increase volume.

**Cost Blindness:**
Not monitoring enrichment costs can lead to budget overruns. Track cost-per-prospect, set budget alerts, and optimize workflows for cost efficiency.

**Technical Debt:**
Building quick, hacky solutions without proper architecture creates maintenance nightmares. Invest time in proper workflow design, documentation, and testing.

### CRM Integration Issues

**Inadequate Field Mapping:**
Poor field mapping between enrichment sources and CRM systems leads to data loss and inconsistency. Create comprehensive field mapping documentation and test thoroughly.

**Missing Metadata:**
Not tracking enrichment sources, dates, and confidence scores makes it difficult to assess data quality and plan re-enrichment activities.

**Workflow Dependencies:**
Creating workflows that depend on specific CRM configurations makes them fragile and difficult to maintain. Design flexible integrations that can adapt to CRM changes.

## Tools & Resources

### Primary Enrichment Platforms

**SURF (surfe.com)**
- **Purpose:** Company discovery and employee prospecting
- **Pricing:** Free trial available, Essential $42/month (150 enrichments), Pro $84/month (1,000 enrichments)
- **Strengths:** Excellent company search filters, LinkedIn integration, unlimited email validation
- **API Documentation:** Available in dashboard after signup
- **Rate Limits:** Varies by plan, typically 1 request per second
- **Best For:** Automated prospect list building, cold outreach campaigns

**Explorium (explorium.ai)**
- **Purpose:** Professional background enrichment and detailed profile analysis
- **Pricing:** Custom pricing through sales team
- **Strengths:** Deep LinkedIn data, work history, education details, high match accuracy
- **API Access:** Contact sales for enterprise API access
- **Best For:** Meeting preparation, inbound lead enrichment, detailed prospect analysis

**Poppy.ai**
- **Purpose:** Multi-source research and personalized outreach generation
- **Pricing:** Subscription-based, multiple tiers available
- **Strengths:** Analyzes multiple content sources, generates personalized messaging
- **Best For:** Dream 100 research, high-touch prospect analysis, content-based personalization