# SKILL BIBLE: Monetizable Agentic Workflows ($5K+ Systems)

## Executive Summary

This skill bible documents three specific agentic workflows that can generate $5,000+ in revenue within a single month. These aren't theoretical—they're production systems built in under 15 minutes each using Claude Code in VS Code, demonstrating the practical application of the directive-orchestration-execution framework.

**Core Insight:** "The bottleneck isn't ideas anymore. It isn't even execution. The bottleneck is just deciding what to build next."

The three workflows covered are: (1) Upwork Job Scraper with AI Proposal Generation, (2) Instantly Campaign Writer for Cold Email at Scale, and (3) Google Maps Lead Scraper with Contact Enrichment. Each can be sold as a service or used to acquire clients directly.

---

## 1. The Upwork Job Scraper System

### What It Does
Scrapes Upwork jobs matching specific criteria, analyzes client profiles, generates customized proposals, and outputs everything to a Google Sheet with one-click apply links.

### Technical Architecture

```
User Prompt → Claude Code Agent
    ↓
Reads directives/ and execution/ folders
    ↓
Runs Apify Upwork Scraper (automation keyword filter)
    ↓
Analyzes: Budget, Client Spend, Client Hires, Job Requirements
    ↓
Generates: Cover Letter + Custom Proposal Doc per job
    ↓
Outputs: Google Sheet with Apply Links + Proposal Column
```

### Key Components

| Component | Purpose |
|-----------|---------|
| Apify Scraper | Finds automation-related jobs from last 24 hours |
| Client Analysis | Identifies "top picks" by client spend and hire history |
| Cover Letter Generator | Best practices-based cover letter per job |
| Proposal Doc Generator | One-page customized proposal Google Doc |
| Google Sheet Output | All jobs with one-click apply links |

### Proposal Document Structure
- Personalized intro (15 minutes put into this)
- Social proof (companies worked with)
- Deep research on their specific problem
- Scope and approach
- Timeline and deliverables

### Business Application
- Apply to 10+ Upwork jobs with high-quality proposals in minutes vs hours
- Identify serious clients via spending history
- Generate Google Docs that pitch customized solutions
- Options: Workflow diagrams (Google Nano Banana Pro), custom Looms, detailed proposals

---

## 2. The Instantly Campaign Writer System

### What It Does
Automatically creates split-test cold email campaigns in Instantly based on offer details, using a repository of high-performing copy examples.

### Technical Architecture

```
Offer Details (Company, Guarantees, Value Props)
    ↓
Claude Code Agent reads directives/
    ↓
Loads campaigns/ folder (high-performing examples)
    ↓
HTTP requests to Instantly API
    ↓
Creates 3+ campaign variants for A/B testing
    ↓
Status code verification + Campaign review
```

### Campaign Structure (Per Variant)

| Element | Description |
|---------|-------------|
| First Name | Personalization variable |
| Icebreaker | AI-generated personalized snippet |
| Value Prop | Specific to target industry |
| Social Proof | Relevant case studies |
| CTA | Soft ask (conversation starter) |
| Follow-ups | Multi-step sequence |

### Example Copy Structure
```
Subject: [Personalized based on company/industry]

Hey {first_name},

{icebreaker - AI generated based on company research}

I work specifically with [industry] on [outcome].
Have helped a lot of [businesses] with [result] over the past few years.

I looked into {company_name} a bit and think there's some interesting stuff we could do together.

Not trying to pitch you a cookie cutter package or anything like that. More just curious to be open to a conversation about what's working for you now and where you want to grow.

[Specific value prop based on offer]

Every [business type] is different. Love to learn more about your situation. See if there's a fit.
```

### Guarantee Copy Examples
- "10 new patients in 30 days or I send you $1,000"
- "Let me send you 3 [results] completely free"
- "10 new [outcome] in 30 days or I send you $1K. Not a typo. If we don't hit [target], I will literally Venmo you 1k"

### Business Application
- Spin up draft campaigns in minutes vs hours
- Built-in split testing (run at scale, filter losers, isolate winners)
- Uses proven copy repository as foundation
- Reduces campaign setup time for cold email services

---

## 3. The Google Maps Lead Scraper System

### What It Does
Scrapes businesses from Google Maps, deep crawls their websites for contact information, uses Claude to extract and structure the data, then outputs to Google Sheet.

### Technical Architecture

```
Search Query (e.g., "100 HVAC companies in Texas")
    ↓
Google Maps API Scrape
    ↓
For each business:
    ├── Main website scrape
    ├── About page scrape
    ├── Team/Founders page scrape
    └── Contact page scrape
    ↓
Compile into text block
    ↓
Claude extraction (JSON schema)
    ↓
Google Sheet (incremental batches)
```

### Data Fields Captured

| Field | Capture Rate |
|-------|--------------|
| Business Name | ~100% |
| Category | ~100% |
| Address | ~95% |
| Phone Number | ~90% |
| Email Address | ~40-50% |
| Owner Name | ~60% |
| Team Contacts | Variable |
| Social Profiles | Variable |
| Map Location Pin | ~100% |

### Cost Analysis
- Claude: NOT the bottleneck (minimal cost)
- Apify: ~$0.01 per lead
- Total: Approximately 1 cent per enriched lead
- Alternative scrapers available for even cheaper lead scraping

### Geographic Density Feature
Specify tighter regions for local systems:
- "HVAC companies in Fort Worth" (high density)
- "Restaurants in downtown Dallas" (hyper-local)
- Perfect for door-knocking teams or geo-targeted outreach

### Business Application
- Local lead generation service
- Outbound sales teams
- Door-to-door sales support
- B2B data enrichment
- Lead lists for cold email/calling

---

## 4. Setting Up The Development Environment

### Required Components

1. **IDE**: Visual Studio Code or Anti-gravity
2. **Extension**: Claude Code for VS Code (or OpenAI Codex, Gemini 3)
3. **Plan**: Some sort of API access plan

### Folder Structure

```
project/
├── agents.md          # High-level instructions for all agents
├── claude.md          # Same content (Claude-specific)
├── gemini.md          # Same content (Gemini-specific)
├── directives/        # What to do (natural language SOPs)
├── execution/         # How to do it (Python scripts)
├── .env               # API keys (plain text)
├── credentials.json   # Google OAuth
└── token.json         # Auth tokens
```

### The agents.md File
Contains instructions that get injected into every prompt:
- How to structure directives
- How to create execution scripts
- Self-annealing instructions (if error, fix and update)
- Authentication flow guidance

### Bypass Permissions Mode
At bottom of Claude Code instance: Change mode to "bypass permissions"
- Allows autonomous operation
- No double-checking for every action
- Assumes model knows better about code implementation

---

## 5. Parallelization Strategy

### Running Multiple Agents
Can run multiple Claude Code instances simultaneously within the same folder:
- Each works on different directives/executions
- No context pollution between instances
- Dramatically speeds up build time

### Separating Build vs Execute
- **Build instances**: Have context about how system was built
- **Execute instances**: Fresh context, tests system as end user would experience
- Use `/clear` or `/new` to start fresh conversation
- Prevents context pollution

### When to Separate
- After building, create new instance for testing
- For daily operations, use fresh instance without build context
- Keeps execution clean and predictable

---

## 6. Authentication Flow

### The Model Handles Auth
Don't need to know how to get credentials ahead of time:
1. Ask agent to build the workflow
2. Agent identifies required authentications
3. Agent walks you through OAuth flows
4. One-click Google sign-ins where applicable

### Common Auth Requirements
- Google Sheets/Docs (OAuth)
- Instantly API key
- Apify API key
- Any third-party service API keys

### Storage Locations
- `.env` file: API keys as plain text
- `credentials.json`: Google OAuth credentials
- `token.json`: Auth tokens from OAuth flows

---

## 7. Self-Annealing Process

### Error Handling Philosophy
Instructions in agents.md include:
- "If you screw up, that's okay. Just keep going."
- "Keep going until you make it work."
- "Once it works, update the instruction set to prevent same error."

### The Loop

```
1. Agent attempts task
2. Error occurs (bash request fails, API error, etc.)
3. Agent reads error
4. Agent fixes approach
5. Agent retries
6. On success: Updates directives with learnings
7. System is now stronger
```

### Cost Consideration
If price sensitive about tokens (Apify, Instantly credits):
- Check in more often during build
- For most: Cost of time waiting > cost of erroneous credits

### Management Philosophy
"Treat this the same way I treat managing staff members—give it creative freedom. Define the WHAT, have it figure out the HOW."

---

## 8. Output Validation

### Real-Time Testing
After build completes:
1. Open output (Google Sheet, etc.)
2. Verify data structure matches expectations
3. Test actual functionality (click apply links, etc.)
4. Check formatting (markdown issues, etc.)

### Common Issues to Check
- Markdown not rendering (asterisks appearing)
- Missing data fields
- Incorrect API step timing (e.g., Instantly 0-day vs 1-day)
- Auth token expiration

### Feedback Loop
When issues found:
1. Tell agent what's wrong
2. Agent fixes
3. Agent updates directives
4. Run test again with new instance

---

## 9. Pricing These Services

### Upwork Scraper System
- Time saved: 1-2 hours per 10 applications
- Value: Higher quality proposals = higher win rate
- Price point: $500-2,000 one-time build
- Recurring: $200-500/month management

### Instantly Campaign Writer
- Time saved: Hours per campaign setup
- Value: Split-testing infrastructure built-in
- Price point: $1,000-3,000 one-time
- Recurring: $500-1,500/month for campaign management

### Google Maps Lead Scraper
- Cost per lead: ~$0.01
- Value: Email addresses worth $0.10-0.50 each
- Price point: $500-2,000 one-time build
- Recurring: $0.05-0.10 per lead delivered

### Combined Service Offering
Full lead generation system:
- Scrape → Enrich → Campaign → Apply/Outreach
- Price point: $5,000-15,000 implementation
- Recurring: $2,000-5,000/month management

---

## 10. Customization Options

### Upwork Scraper Variations
- Different platforms (Fiverr, Toptal, etc.)
- Different job categories
- Custom proposal templates per industry
- Integration with CRM for tracking

### Campaign Writer Variations
- Different cold email platforms (Lemlist, Woodpecker)
- SMS campaigns
- LinkedIn outreach sequences
- Multi-channel orchestration

### Lead Scraper Variations
- Different data sources (Yelp, industry directories)
- Additional enrichment (AnyMailFinder, Veyn)
- CRM integration
- Automated outreach triggers

---

## AI PARSING GUIDE

### Primary Objective
When user requests "build me a workflow that makes money" or "I need a lead generation system," use these three patterns as templates and customize to their specific needs.

### Critical Decision Points

**If User Says**: "I need more clients"
**Action Sequence**:
1. Ask: B2B or B2C? What industry?
2. Recommend: Upwork (service), Lead Scraper (local), or Campaign Writer (scale)
3. Build: Using directive-execution structure
4. Test: Verify with real data
5. Iterate: Based on user feedback

**If User Says**: "This isn't working"
**Action Sequence**:
1. Check output data structure
2. Verify authentication is current
3. Test API endpoints individually
4. Review and update directives
5. Rebuild affected execution scripts

### Integration Points
**Connects to**:
- `SKILL_BIBLE_do_framework_fundamentals.md` - Architecture principles
- `SKILL_BIBLE_cloud_deployment_methods.md` - Hosting these systems
- `SKILL_BIBLE_cold_dm_email_conversion.md` - Copy principles for campaigns

### Output Quality Standards
When building these workflows, verify:
1. ✅ Data extraction matches expected schema
2. ✅ Google Sheet formatting is clean
3. ✅ Links are clickable and functional
4. ✅ Copy is personalized (not obviously templated)
5. ✅ Error handling is in place

### Red Flags (Anti-Patterns)
❌ Building without testing with real data
❌ Not separating build context from execute context
❌ Ignoring auth errors (they compound)
❌ Over-engineering when simple works

---

## SOURCE ATTRIBUTION

**Primary Source:** Nick Saraev - "3 'Boring' Agentic Workflows That Will Make You $5,000+"
- **Video ID:** c7DKk9xHaaU
- **Duration:** 23 minutes
- **Context:** Live build demonstration of three production-ready systems
- **Key Contribution:** Practical, monetizable workflow templates with exact implementation
- **Authority Basis:** $160K/month combined revenue, 2,500+ member community
- **Technical Detail Level:** Complete build walkthrough with debugging
- **Unique Value:** Shows parallelization strategy and self-annealing in practice
- **Capture Date:** January 2026 (via yt-dlp VTT extraction)

**Synthesis Approach:** Extracted technical architecture, business applications, and implementation patterns from live demonstration, structured for AI agent parsing and human reference.

---

**END SKILL BIBLE: Monetizable Agentic Workflows**
