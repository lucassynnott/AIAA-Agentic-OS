#!/usr/bin/env python3
"""
Lead Deduplication - Remove duplicate leads from lists.

Usage:
    python3 execution/dedupe_leads.py \
        --input leads.csv \
        --keys "email,linkedin_url" \
        --output deduped_leads.json
"""

import argparse, csv, json, sys
from datetime import datetime
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Deduplicate lead lists")
    parser.add_argument("--input", "-i", required=True, help="Input file (CSV or JSON)")
    parser.add_argument("--keys", "-k", default="email", help="Comma-separated dedup keys")
    parser.add_argument("--output", "-o", default=".tmp/deduped_leads.json")
    parser.add_argument("--keep", default="first", choices=["first", "last"], help="Which duplicate to keep")
    args = parser.parse_args()

    keys = [k.strip() for k in args.keys.split(",")]
    
    # Load data
    input_path = Path(args.input)
    leads = []
    
    if input_path.suffix == ".csv":
        with open(input_path) as f:
            leads = list(csv.DictReader(f))
    elif input_path.suffix == ".json":
        with open(input_path) as f:
            data = json.load(f)
            leads = data if isinstance(data, list) else data.get("leads", data.get("data", []))

    print(f"\n🔄 Lead Deduplication")
    print(f"   Input: {len(leads)} leads")
    print(f"   Keys: {keys}")
    print(f"   Keep: {args.keep}\n")

    # Deduplicate
    seen = {}
    duplicates = []
    unique = []
    
    if args.keep == "last":
        leads = leads[::-1]  # Reverse to keep last
    
    for lead in leads:
        # Create composite key
        key_values = []
        for k in keys:
            val = lead.get(k, "").strip().lower()
            if val:
                key_values.append(val)
        
        if not key_values:
            unique.append(lead)
            continue
        
        key = "|".join(key_values)
        
        if key in seen:
            duplicates.append({"lead": lead, "duplicate_of": seen[key]})
        else:
            seen[key] = key_values[0]  # Store first key value as reference
            unique.append(lead)
    
    if args.keep == "last":
        unique = unique[::-1]  # Restore order

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "deduped_at": datetime.now().isoformat(),
        "keys_used": keys,
        "summary": {
            "original": len(leads),
            "unique": len(unique),
            "duplicates_removed": len(duplicates)
        },
        "leads": unique,
        "duplicates": duplicates[:100]  # Store first 100 dupes for review
    }
    
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✅ Deduplication complete!")
    print(f"   Original: {len(leads)}")
    print(f"   Unique: {len(unique)}")
    print(f"   Removed: {len(duplicates)} duplicates")
    print(f"   📄 Output: {output_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
