# Multi-Platform Lead Deduplication

## What This Workflow Is
This workflow removes duplicate leads across multiple lists using email, domain, and fuzzy company name matching.

## What It Does
1. Combines multiple lead lists
2. Matches on email, phone, domain
3. Fuzzy matches company names
4. Applies merge rules for duplicates
5. Outputs clean deduplicated list

## Prerequisites

### Required API Keys (add to .env)
```
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # If using Sheets
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install pandas fuzzywuzzy python-Levenshtein
```

## How to Run

### Step 1: Deduplicate Leads
```bash
python3 execution/dedupe_leads.py \
  --sources "list1.csv,list2.csv,sheet_url" \
  --match_keys "email,domain" \
  --output .tmp/deduped.csv
```

### Quick One-Liner
```bash
python3 execution/dedupe_leads.py --sources "[FILES]" --match_keys email,domain
```

## Goal
Remove duplicate leads across multiple lists and platforms to maintain clean data.

## Inputs
- **Lead Lists**: Multiple CSVs or Sheet URLs
- **Match Keys**: Email, domain, phone, company name
- **Merge Rules**: Which record to keep

## Process

### 1. Combine Lists
```bash
python3 execution/dedupe_leads.py \
  --sources "list1.csv,list2.csv,sheet_url" \
  --match_keys "email,domain" \
  --output .tmp/deduped.csv
```

### 2. Matching Logic

**Exact Match:**
- Email (primary key)
- Phone number
- LinkedIn URL

**Fuzzy Match:**
- Company name (Acme Inc = Acme, Inc.)
- Person name (variations)
- Domain (with/without www)

### 3. Merge Rules
When duplicate found:
- Keep most recent record
- Keep most complete record
- Merge fields from both
- Flag for manual review

### 4. Field Priority
```json
{
  "email": "keep_verified",
  "phone": "keep_most_recent",
  "company": "keep_longest",
  "notes": "combine_all",
  "source": "keep_original"
}
```

### 5. Output
- Deduplicated master list
- Duplicate report (what was merged)
- Conflict log (manual review needed)
- Statistics (original vs final count)

### 6. Dedup Stats
```markdown
# Deduplication Report

## Summary
- Records processed: 5,000
- Unique leads: 3,847
- Duplicates removed: 1,153
- Dedup rate: 23%

## By Source
| Source | Original | After Dedup | Dupes |
|--------|----------|-------------|-------|
| List 1 | 2,000 | 1,847 | 153 |
| List 2 | 3,000 | 2,000 | 1,000 |

## Conflicts (Review)
- 12 records with mismatched emails
- 5 records with different company names
```

### 7. Ongoing Deduplication
- Run before campaigns
- Run after imports
- Schedule weekly cleanup

## Integrations
- Google Sheets
- CRM import
- Email platforms

## Cost
- Processing: Free (local)
- ~1-2 seconds per 1,000 records
