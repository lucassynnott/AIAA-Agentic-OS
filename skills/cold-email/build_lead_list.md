# Build Lead List

## Skill Overview
This skill guides you through building targeted lead lists using B2B data providers to create high-quality prospect lists for cold email campaigns.

## Table of Contents
1. [Understanding Lead List Building](#understanding-lead-list-building)
2. [Lead List Components](#lead-list-components)
3. [Using B2B Data Tools](#using-b2b-data-tools)
4. [Filtering Strategy](#filtering-strategy)
5. [Export and Validation](#export-and-validation)
6. [Alternative Methods](#alternative-methods)
7. [Best Practices](#best-practices)

## Understanding Lead List Building

Lead list building is the process of creating a targeted database of prospects who match your ideal customer profile (ICP). This is a critical skill that directly impacts campaign performance.

### Why List Quality Matters

**Good list = good results:**
- Right decision makers
- Relevant companies
- Accurate contact information
- Better response rates

**Bad list = failed campaign:**
- Wrong contacts
- Irrelevant industries
- Invalid emails
- Wasted resources

### The Four Key Filters

Every company can be categorized by:
1. **Industry** - What sector/vertical (marketing, hospitality, construction, etc.)
2. **Company Size** - Number of employees (small, medium, large)
3. **Location** - Geographic targeting (US, UK, Florida, NYC, etc.)
4. **Job Title** - Decision maker role (CEO, CMO, VP Marketing, etc.)

## Lead List Components

### Required Data Fields

Your exported lead list should include:

**Essential Fields:**
- First Name
- Last Name
- Email Address
- Job Title
- Company Name

**Recommended Fields:**
- LinkedIn Profile URL
- Company Website
- Company Industry
- Company Size
- Location
- Phone Number (optional)

### Data Format

Lists are typically exported as CSV files that can be imported directly into:
- Smartlead
- Instantly
- Lemlist
- Other cold email platforms

## Using B2B Data Tools

### Recommended Tools

**List Kit** (used in training):
- Industry filtering
- Company size targeting
- Job title filtering
- Geographic selection
- 10 people per company option
- CSV export

**Alternative Tools:**
- Apollo.io
- ZoomInfo
- Lusha
- Hunter.io
- RocketReach
- Seamless.ai
- LeadIQ

### List Kit Setup Process

**Step 1: Define Industry**

1. Go to List Kit dashboard
2. Select **Industry** filter
3. Choose broad category (e.g., "Hospitality")
4. Add specific keywords (e.g., "hotel")

**Example:**
- Industry: Hospitality
- Keyword: hotel
- Result: 800,000 people at 14,000 companies

**Step 2: Filter by Company Size**

1. Select **Employee Count** filter
2. Define range based on ICP

**Common Ranges:**
- Small: 1-50 employees
- Medium: 51-200 employees
- Large: 201-1000 employees
- Enterprise: 1000+ employees

**Example:**
- Filter: 1-200 employees
- Result narrows from 800k to manageable number

**Step 3: Select Location**

1. Choose **Location** filter
2. Select country, state, or city

**Options:**
- Country level (United States, United Kingdom)
- State level (Florida, California, Texas)
- City level (New York, Los Angeles, Miami)

**Example:**
- Location: United States
- Combined with previous filters

**Step 4: Target Job Titles**

1. Select **Job Title** filter
2. Add all relevant decision maker titles

**Common Titles:**
- CEO
- Owner
- Founder
- Co-founder
- President
- CMO
- Chief Marketing Officer
- VP Marketing
- Head of Marketing
- Marketing Manager
- Director of Marketing

**Example Selection:**
```
- CEO
- Owner
- Founder
- CMO
- Chief Marketing Officer
- Head of Marketing
- Marketing Manager
- VP of Marketing
```

### Filter Refinement Process

Think of list building like assembling a puzzle:
1. Start broad
2. Add filters one by one
3. Review results after each filter
4. Refine until you get the right audience
5. Expect some outliers (nature of data)

### Export Settings

**People Per Company:**
- Recommended: 10 people per company
- Allows multi-threading (reaching multiple contacts)
- Increases chance of response

**Number of Leads:**
- Typical campaign: 3,000-5,000 leads
- Test campaign: 50-100 leads
- Large campaign: 10,000+ leads

**Export Process:**
1. Click "Export"
2. Set people per company (10)
3. Enter total lead count (e.g., 3,000)
4. Click "Redeem Credits"
5. Receive CSV file via email

## Filtering Strategy

### Industry-Specific Examples

**Example 1: Hotel Marketing**
```
Industry: Hospitality
Keyword: hotel
Location: United States
Employees: 1-200
Job Titles: CEO, Owner, Founder, CMO, Marketing Manager
```

**Example 2: Construction Services**
```
Industry: Construction
Keywords: contractor, home builder
Location: United States
Employees: 1-100
Job Titles: CEO, Owner, Founder
```

**Example 3: SaaS Companies**
```
Industry: Software
Keywords: SaaS, B2B software
Location: United States
Employees: 10-500
Job Titles: CEO, Founder, Head of Growth, VP Product
```

### Common Filtering Mistakes

**Too Broad:**
- No industry filter = random companies
- No job title filter = wrong contacts
- No size filter = unqualified prospects

**Too Narrow:**
- Too many filters = tiny list
- Overly specific keywords = missed opportunities
- Single job title = limited reach

**Optimal Approach:**
- 3-4 key filters
- Multiple job title variations
- Reasonable size ranges
- Specific but not restrictive keywords

## Export and Validation

### CSV File Structure

Your exported file will contain rows like:

| Email | First Name | Last Name | LinkedIn | Job Title | Company Name | Website |
|-------|------------|-----------|----------|-----------|--------------|---------|
| john@company.com | John | Smith | linkedin.com/in/john | CEO | Company Inc | company.com |

### Variable Mapping for Smartlead

These CSV columns map to Smartlead variables:

- `First Name` → `{{first_name}}`
- `Last Name` → `{{last_name}}`
- `Company Name` → `{{company_name}}`
- `Job Title` → `{{job_title}}`
- `LinkedIn` → `{{linkedin_profile}}`
- `Website` → `{{website}}`

**Email Copy Example:**
```
Hi {{first_name}},

I noticed {{company_name}} is [observation].

[Value proposition]

Would you be open to a quick call?

Best,
[Your name]
```

### Importing to Smartlead

1. Go to Smartlead campaign
2. Click **Import Leads**
3. Drag and drop CSV file
4. Map fields to Smartlead variables
5. Review import preview
6. Confirm import

### External Validation

**Do NOT validate inside Smartlead** - validate externally first.

**Recommended Validation Tools:**
- ZeroBounce
- NeverBounce
- BriteVerify
- Kickbox
- EmailListVerify

**Validation Process:**
1. Export list from data provider
2. Upload to validation service
3. Remove invalid/risky emails
4. Import clean list to Smartlead

**Target Bounce Rate:** Under 3%

## Alternative Methods

### Manual LinkedIn Scraping

**Process:**
1. Search LinkedIn for target profiles
2. Copy email addresses individually
3. Build list manually in spreadsheet

**Pros:**
- Free
- Complete control

**Cons:**
- Extremely time-consuming
- Not scalable
- Difficult to reach volume

**When to Use:** Very small lists (under 50 contacts)

### LinkedIn Sales Navigator Scraping

See separate skill: [Scrape LinkedIn Sales Navigator](./scrape_linkedin_sales_navigator.md)

**Benefits:**
- Highly targeted
- Fresh data
- Intent signals

**Drawbacks:**
- Requires Sales Navigator subscription
- Requires scraping tools
- More technical setup

### Company Website Scraping

**Process:**
1. Identify target companies
2. Visit their websites
3. Find contact pages
4. Extract emails manually or with tools

**Pros:**
- Direct source
- Accurate information

**Cons:**
- Time-intensive
- Low volume
- Many sites hide emails

## Best Practices

### Do's

**List Building:**
- Start with clear ICP definition
- Test filters before large exports
- Export 50-100 leads for testing first
- Validate emails externally
- Review sample records before export
- Include multiple job titles
- Set people per company to 10

**Cost Management:**
- Bake tool cost into client pricing
- Example: $297/month List Kit → included in $1,000 client setup fee
- Client pays for the tool, you manage it

**Quality Control:**
- Manually review first 10-20 records
- Check for industry relevance
- Verify job titles match ICP
- Confirm company size is correct

### Don'ts

**Avoid These Mistakes:**
- Don't skip validation
- Don't export without testing filters
- Don't ignore outliers completely
- Don't over-filter (too restrictive)
- Don't under-filter (too broad)
- Don't validate inside Smartlead
- Don't reuse same list repeatedly

### Pricing Strategy

**Tool Subscription:**
- List Kit: ~$297/month
- Apollo: $49-$149/month
- ZoomInfo: Custom pricing (expensive)

**Client Billing:**
- Include tool cost in setup fee
- Example: "Setup Fee: $1,000" (includes all tools)
- Or monthly retainer includes data costs
- Don't eat the cost yourself

### List Maintenance

**Fresh Lists:**
- Rebuild lists every 3-6 months
- Contacts change jobs
- Companies go out of business
- Data becomes stale

**List Hygiene:**
- Remove bounces immediately
- Track unsubscribes
- Maintain do-not-contact list
- Honor opt-outs

## Skill Mastery Checklist

To master list building, you must be able to:

- [ ] Understand client's ICP clearly
- [ ] Navigate B2B data tool efficiently
- [ ] Apply 4 key filters correctly
- [ ] Identify relevant job titles
- [ ] Choose appropriate company size ranges
- [ ] Use keywords effectively
- [ ] Export clean CSV files
- [ ] Validate emails externally
- [ ] Import to cold email platform
- [ ] Map variables correctly
- [ ] Review list quality before campaign
- [ ] Maintain list hygiene standards

## Common Use Cases

### Case 1: E-commerce Marketing Agency

**Client needs leads for e-commerce brands:**
```
Industry: E-commerce / Retail
Keywords: online store, e-commerce, DTC brand
Location: United States
Employees: 5-50
Job Titles: CEO, Founder, Owner, CMO, Marketing Director
```

### Case 2: B2B SaaS Sales Tool

**Client needs leads for SaaS companies:**
```
Industry: Software / Technology
Keywords: SaaS, B2B software, enterprise software
Location: United States + Canada
Employees: 20-500
Job Titles: CEO, Founder, CRO, VP Sales, Head of Sales
```

### Case 3: Local Service Provider

**Client needs leads for restaurants in Florida:**
```
Industry: Food & Beverage / Hospitality
Keywords: restaurant, dining, food service
Location: Florida
Employees: 10-100
Job Titles: Owner, General Manager, Operations Manager
```

### Case 4: Cybersecurity Service

**Client needs leads for enterprises:**
```
Industry: Technology, Finance, Healthcare (multi-select)
Location: United States
Employees: 500-10,000
Job Titles: CISO, CTO, VP IT, Director of Security
```

## Troubleshooting

**Issue: List is too small (under 500 contacts)**
- Remove one filter (usually location or size)
- Broaden keyword search
- Add more job title variations
- Expand company size range

**Issue: List is too large (over 50,000 contacts)**
- Add location filter
- Narrow company size range
- Be more specific with keywords
- Reduce job title options

**Issue: Wrong types of companies appearing**
- Refine keywords (more specific)
- Check industry filter accuracy
- Review sample records
- Add negative keywords if tool supports

**Issue: Wrong job titles in results**
- Remove broad titles (e.g., "Manager")
- Be more specific (e.g., "Marketing Manager" not "Manager")
- Review tool's job title taxonomy
- Manually clean if small list

## Related Skills
- [Setup Smartlead](./setup_smartlead.md)
- [Scrape LinkedIn Sales Navigator](./scrape_linkedin_sales_navigator.md)
- [Write Cold Email Script](./write_cold_email_script.md)
- [Personalize Cold Emails with AI](./personalize_cold_emails_with_ai.md)

## Resources

**B2B Data Providers:**
- List Kit: listkit.io
- Apollo: apollo.io
- ZoomInfo: zoominfo.com
- Lusha: lusha.com
- Hunter: hunter.io

**Email Validators:**
- ZeroBounce: zerobounce.net
- NeverBounce: neverbounce.com
- Kickbox: kickbox.com

**Search "Best B2B data providers"** for comprehensive tool lists and comparisons.
