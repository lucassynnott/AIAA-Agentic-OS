# Invoice Generator

## What This Workflow Is
This workflow generates professional PDF invoices from your data and automatically sends them to clients with integrated payment links.

## What It Does
1. Takes invoice details (client, services, amounts)
2. Generates a branded PDF invoice
3. Creates Stripe/PayPal payment link
4. Emails invoice to client with pay button
5. Tracks invoice status in Google Sheets

## Prerequisites

### Required API Keys (add to .env)
```
STRIPE_API_KEY=your_stripe_key            # For payment links
SENDGRID_API_KEY=your_sendgrid_key        # For email delivery
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Stripe account
- Email platform (SendGrid or Gmail)

### Installation
```bash
pip install stripe reportlab google-api-python-client
```

## How to Run

### Step 1: Prepare Invoice Data
Create `invoice_data.json`:
```json
{
  "client": {"name": "Acme Corp", "email": "billing@acme.com"},
  "invoice_number": "INV-2024-001",
  "due_date": "2024-01-30",
  "items": [
    {"description": "Monthly Retainer", "amount": 3000}
  ],
  "total": 3000
}
```

### Step 2: Generate Invoice
```bash
python3 execution/generate_invoice.py \
  invoice_data.json \
  --output .tmp/invoice.pdf
```

### Step 3: Send to Client
```bash
python3 execution/send_invoice_email.py \
  --to "billing@acme.com" \
  --invoice .tmp/invoice.pdf \
  --payment_link "auto"
```

### Quick One-Liner
```bash
python3 execution/generate_invoice.py invoice_data.json && \
python3 execution/send_invoice_email.py --to "client@email.com" --invoice .tmp/invoice.pdf
```

### Recurring Monthly Invoices (Cron)
```bash
0 9 1 * * cd /path/to/project && python3 execution/run_monthly_invoices.py
```

## Goal
Automatically generate professional invoices and send to clients with payment links.

## Inputs
- **Client Name**: Business or individual name
- **Client Email**: Where to send invoice
- **Services**: Line items with descriptions and amounts
- **Due Date**: Payment deadline
- **Payment Methods**: Stripe, PayPal, Bank Transfer

## Tools/Scripts
- `execution/generate_invoice.py` - Create invoice PDF
- `execution/send_invoice_email.py` - Email delivery

## Process

### 1. Gather Invoice Details
```json
{
  "client": {
    "name": "Acme Corp",
    "email": "billing@acme.com",
    "address": "123 Main St, City, ST 12345"
  },
  "invoice_number": "INV-2024-001",
  "date": "2024-01-15",
  "due_date": "2024-01-30",
  "items": [
    {
      "description": "Monthly Retainer - Cold Email Services",
      "quantity": 1,
      "rate": 3000,
      "amount": 3000
    },
    {
      "description": "Lead List (500 contacts)",
      "quantity": 1,
      "rate": 500,
      "amount": 500
    }
  ],
  "subtotal": 3500,
  "tax": 0,
  "total": 3500,
  "payment_link": "https://stripe.com/pay/xxx"
}
```

### 2. Generate Invoice
```bash
python3 execution/generate_invoice.py invoice_data.json --output .tmp/invoice.pdf
```

### 3. Send to Client
```bash
python3 execution/send_invoice_email.py \
  --to "billing@acme.com" \
  --invoice .tmp/invoice.pdf \
  --payment_link "https://stripe.com/pay/xxx"
```

### 4. Email Template
```
Subject: Invoice #[NUMBER] from [YOUR_COMPANY] - Due [DATE]

Hi [CLIENT_NAME],

Please find attached invoice #[NUMBER] for [AMOUNT].

Payment is due by [DUE_DATE].

[PAY NOW BUTTON]

Invoice Summary:
- [SERVICE 1]: $[AMOUNT]
- [SERVICE 2]: $[AMOUNT]
Total: $[TOTAL]

Payment Methods:
- Credit Card: [STRIPE_LINK]
- Bank Transfer: [BANK_DETAILS]

Questions? Reply to this email.

Thanks,
[YOUR_NAME]
```

### 5. Track Payment Status
Log to Google Sheet:
- Invoice number
- Client
- Amount
- Sent date
- Due date
- Status (Sent/Paid/Overdue)

## Invoice Template Fields
- Your company logo
- Your company details
- Client details
- Invoice number
- Date and due date
- Line items
- Subtotal, tax, total
- Payment instructions
- Terms and conditions

## Automation Options

### Auto-Generate on Deal Close
Trigger invoice when CRM deal moves to "Closed Won"

### Recurring Invoices
Monthly retainer invoices on set schedule

### Payment Reminders
Auto-send reminder 3 days before due date

### Overdue Notices
Auto-send if unpaid after due date

## Integrations Required
- PDF generation library
- Email (Gmail/SendGrid)
- Stripe/PayPal (payment links)
- Google Sheets (tracking)

## Output
- PDF invoice
- Email sent confirmation
- Payment link
- Tracking entry

## Edge Cases
- International clients: Include currency conversion
- Tax requirements: Add tax fields as needed
- Partial payment: Track remaining balance
