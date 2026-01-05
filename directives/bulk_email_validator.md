# Bulk Email Validation

## What This Workflow Is
This workflow validates your email lists before campaigns to remove invalid addresses, detect spam traps, and improve deliverability.

## What It Does
1. Checks email syntax validity
2. Verifies domain has MX records
3. Confirms mailbox exists via SMTP
4. Detects disposable and role-based emails
5. Identifies spam traps and catch-all domains
6. Outputs clean list with validity scores

## Prerequisites

### Required API Keys (add to .env)
```
ZEROBOUNCE_API_KEY=your_zerobounce_key    # Or NEVERBOUNCE, KICKBOX
```

### Required Tools
- Python 3.10+
- Email validation API account

### Installation
```bash
pip install requests
```

## How to Run

### Step 1: Validate Email List
```bash
python3 execution/validate_emails.py \
  --input leads.csv \
  --level deep \
  --output .tmp/validated.csv
```

### Step 2: Review Results
Output CSV will have columns:
- email
- status (valid/invalid/risky/unknown)
- reason (if invalid)
- deliverability_score

### Quick One-Liner
```bash
python3 execution/validate_emails.py --input leads.csv --level deep --output validated.csv
```

### From Google Sheet
```bash
python3 execution/validate_emails.py --sheet "[SHEET_URL]" --level deep --update_sheet
```

## Goal
Validate email lists to remove invalid, risky, and spam-trap emails before sending campaigns.

## Inputs
- **Email List**: CSV or Google Sheet with emails
- **Validation Level**: Basic (syntax), Standard (MX check), Deep (full verification)

## Process

### 1. Upload List
```bash
python3 execution/validate_emails.py \
  --input leads.csv \
  --level deep \
  --output .tmp/validated.csv
```

### 2. Validation Checks
- Syntax validation
- Domain exists (MX records)
- Mailbox exists (SMTP check)
- Disposable email detection
- Role-based detection (info@, support@)
- Spam trap detection
- Catch-all domain detection

### 3. Output Categories
| Status | Action |
|--------|--------|
| Valid | Safe to send |
| Risky | Send with caution |
| Invalid | Remove from list |
| Unknown | Manual review |

### 4. Results
- Valid emails: X%
- Invalid removed: X
- Risky flagged: X
- Estimated deliverability: X%

## Integrations
- ZeroBounce, NeverBounce, or Kickbox API

## Cost
- ~$0.003-0.01 per email
- 1000 emails: ~$5-10
