# Website Contact Page Scraper

## What This Workflow Is
This workflow scrapes company websites to extract contact information including emails, phone numbers, and contact page URLs.

## What It Does
1. Takes list of company domains
2. Scrapes main and contact pages
3. Extracts emails, phones
4. Finds social profiles
5. Outputs structured contact data

## Prerequisites

### Required API Keys (add to .env)
```
# No API keys required for basic scraping
```

### Installation
```bash
pip install httpx beautifulsoup4
```

## How to Run
```bash
python3 execution/scrape_contacts.py --domains "domains.csv" --output .tmp/contacts.json
```

## Goal
Extract contact information from company websites including emails, phones, and contact forms.

## Inputs
- **Website List**: URLs to scrape
- **Data Points**: Email, phone, social links, contact form URL

## Process

### 1. Scrape Websites
```bash
python3 execution/scrape_website_contacts.py \
  --urls websites.csv \
  --output .tmp/contacts.json
```

### 2. Pages to Check
- Contact page (/contact, /contact-us)
- About page (/about, /about-us)
- Footer (all pages)
- Team page (/team, /our-team)
- Privacy policy (often has email)

### 3. Data Extracted
- General email (info@, hello@)
- Sales email (sales@)
- Support email (support@)
- Phone numbers
- Physical address
- Social media links
- Contact form URL

### 4. Email Pattern Detection
If no email found, detect pattern:
```
firstname@domain.com
first.last@domain.com
flast@domain.com
```

Then generate for decision makers.

### 5. Output
```json
{
  "website": "example.com",
  "emails": {
    "general": "info@example.com",
    "sales": "sales@example.com"
  },
  "phone": "+1-555-123-4567",
  "address": "123 Main St, City, ST",
  "social": {
    "linkedin": "linkedin.com/company/example",
    "twitter": "twitter.com/example"
  },
  "contact_form": "example.com/contact"
}
```

### 6. Validation
- Verify email format
- Check if email is deliverable
- Validate phone format
- Confirm links work

## Integrations
- Custom scraper or Apify
- Email validation API

## Cost
- Scraping: ~$0.01/website
- Validation: ~$0.003/email
