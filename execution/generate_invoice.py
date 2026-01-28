#!/usr/bin/env python3
"""
Invoice Generator - Generate professional invoices.

Usage:
    python3 execution/generate_invoice.py \
        --client "Acme Corp" \
        --items "Service A:1000,Service B:500" \
        --due_days 30 \
        --output .tmp/invoice.md
"""

import argparse, os, sys
from datetime import datetime, timedelta
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Generate invoices")
    parser.add_argument("--client", "-c", required=True)
    parser.add_argument("--client_email", default="")
    parser.add_argument("--items", "-i", required=True, help="Format: 'Item:Price,Item2:Price2'")
    parser.add_argument("--due_days", "-d", type=int, default=30)
    parser.add_argument("--invoice_num", default="")
    parser.add_argument("--notes", "-n", default="")
    parser.add_argument("--company", default="Your Company Name")
    parser.add_argument("--output", "-o", default=".tmp/invoice.md")
    args = parser.parse_args()

    # Parse items
    items = []
    total = 0
    for item in args.items.split(","):
        parts = item.strip().rsplit(":", 1)
        if len(parts) == 2:
            name, price = parts[0], float(parts[1])
            items.append({"name": name, "price": price})
            total += price

    invoice_num = args.invoice_num or f"INV-{datetime.now().strftime('%Y%m%d%H%M')}"
    due_date = datetime.now() + timedelta(days=args.due_days)

    items_table = "\n".join([f"| {i['name']} | ${i['price']:,.2f} |" for i in items])

    invoice = f"""# INVOICE

**Invoice Number:** {invoice_num}
**Date:** {datetime.now().strftime("%Y-%m-%d")}
**Due Date:** {due_date.strftime("%Y-%m-%d")}

---

## From
**{args.company}**

## Bill To
**{args.client}**
{args.client_email}

---

## Services

| Description | Amount |
|-------------|--------|
{items_table}

---

**Subtotal:** ${total:,.2f}
**Tax (0%):** $0.00
**Total Due:** ${total:,.2f}

---

## Payment Terms
- Due within {args.due_days} days
- Late payments subject to 1.5% monthly interest

{f'## Notes{chr(10)}{args.notes}' if args.notes else ''}

---

Thank you for your business!
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(invoice, encoding="utf-8")
    print(f"✅ Invoice {invoice_num} generated: {args.output}")
    print(f"   Total: ${total:,.2f}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
