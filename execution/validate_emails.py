#!/usr/bin/env python3
"""
Bulk Email Validator - Validate email addresses for deliverability.

Usage:
    python3 execution/validate_emails.py \
        --input emails.csv \
        --output validated_emails.json
"""

import argparse, csv, json, os, re, sys
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

def validate_syntax(email):
    """Basic email syntax validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def check_disposable(domain):
    """Check if domain is disposable email provider."""
    disposable = ['tempmail', 'throwaway', 'guerrilla', 'mailinator', '10minute', 'temp-mail']
    return any(d in domain.lower() for d in disposable)

def validate_with_hunter(email):
    """Validate with Hunter.io API."""
    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        return None
    try:
        resp = requests.get(
            f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}",
            timeout=10
        )
        if resp.ok:
            data = resp.json().get("data", {})
            return {
                "status": data.get("status"),
                "score": data.get("score"),
                "deliverable": data.get("status") == "valid"
            }
    except:
        pass
    return None

def validate_with_zerobounce(email):
    """Validate with ZeroBounce API."""
    api_key = os.getenv("ZEROBOUNCE_API_KEY")
    if not api_key:
        return None
    try:
        resp = requests.get(
            f"https://api.zerobounce.net/v2/validate?api_key={api_key}&email={email}",
            timeout=10
        )
        if resp.ok:
            data = resp.json()
            return {
                "status": data.get("status"),
                "sub_status": data.get("sub_status"),
                "deliverable": data.get("status") == "valid"
            }
    except:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Validate email addresses")
    parser.add_argument("--input", "-i", required=True, help="Input file (CSV or JSON)")
    parser.add_argument("--email_column", "-e", default="email", help="Email column name")
    parser.add_argument("--output", "-o", default=".tmp/validated_emails.json")
    parser.add_argument("--api", "-a", default="basic", choices=["basic", "hunter", "zerobounce"])
    args = parser.parse_args()

    # Load emails
    input_path = Path(args.input)
    emails = []
    
    if input_path.suffix == ".csv":
        with open(input_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get(args.email_column, "").strip()
                if email:
                    emails.append({"email": email, "data": row})
    elif input_path.suffix == ".json":
        with open(input_path) as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    email = item.get(args.email_column, item.get("email", ""))
                    if email:
                        emails.append({"email": email, "data": item})

    print(f"\n📧 Email Validator\n   Emails: {len(emails)}\n   Method: {args.api}\n")

    results = {"valid": [], "invalid": [], "unknown": []}
    
    for i, item in enumerate(emails, 1):
        email = item["email"]
        print(f"[{i}/{len(emails)}] {email}...", end=" ")
        
        # Basic validation
        if not validate_syntax(email):
            item["validation"] = {"status": "invalid", "reason": "Invalid syntax"}
            results["invalid"].append(item)
            print("❌ Invalid syntax")
            continue
        
        domain = email.split("@")[1]
        if check_disposable(domain):
            item["validation"] = {"status": "invalid", "reason": "Disposable domain"}
            results["invalid"].append(item)
            print("❌ Disposable")
            continue
        
        # API validation
        if args.api == "hunter":
            result = validate_with_hunter(email)
        elif args.api == "zerobounce":
            result = validate_with_zerobounce(email)
        else:
            result = None
        
        if result:
            item["validation"] = result
            if result.get("deliverable"):
                results["valid"].append(item)
                print("✅ Valid")
            else:
                results["invalid"].append(item)
                print(f"❌ {result.get('status', 'Invalid')}")
        else:
            item["validation"] = {"status": "unknown", "reason": "Basic validation only"}
            results["valid"].append(item)  # Assume valid if no API
            print("✓ Syntax OK")

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "validated_at": datetime.now().isoformat(),
        "method": args.api,
        "summary": {
            "total": len(emails),
            "valid": len(results["valid"]),
            "invalid": len(results["invalid"]),
            "unknown": len(results["unknown"])
        },
        "results": results
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n✅ Validation complete!")
    print(f"   Valid: {len(results['valid'])} | Invalid: {len(results['invalid'])}")
    print(f"   📄 Output: {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
