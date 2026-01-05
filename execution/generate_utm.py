#!/usr/bin/env python3
"""
UTM Generator - Generate UTM-tagged URLs for campaign tracking.

Usage:
    python3 execution/generate_utm.py \
        --url "https://example.com" \
        --source "linkedin" \
        --medium "social" \
        --campaign "q1_launch" \
        --output .tmp/utm_urls.md
"""

import argparse, sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, urlparse, urlunparse

def main():
    parser = argparse.ArgumentParser(description="Generate UTM URLs")
    parser.add_argument("--url", "-u", required=True, help="Base URL")
    parser.add_argument("--source", "-s", required=True, help="Traffic source (google, linkedin, etc)")
    parser.add_argument("--medium", "-m", required=True, help="Medium (cpc, social, email, etc)")
    parser.add_argument("--campaign", "-c", required=True, help="Campaign name")
    parser.add_argument("--term", "-t", default="", help="UTM term (keywords)")
    parser.add_argument("--content", default="", help="UTM content (ad variant)")
    parser.add_argument("--variants", "-v", default="", help="Comma-separated content variants")
    parser.add_argument("--output", "-o", default=".tmp/utm_urls.md")
    args = parser.parse_args()

    print(f"\n🔗 UTM Generator\n   URL: {args.url}\n")

    # Parse base URL
    parsed = urlparse(args.url)
    base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

    urls = []
    
    # Generate main URL
    params = {
        "utm_source": args.source,
        "utm_medium": args.medium,
        "utm_campaign": args.campaign
    }
    if args.term:
        params["utm_term"] = args.term
    if args.content:
        params["utm_content"] = args.content
    
    main_url = f"{base_url}?{urlencode(params)}"
    urls.append({"name": "Main", "url": main_url, "params": params.copy()})

    # Generate variants
    if args.variants:
        for variant in args.variants.split(","):
            variant = variant.strip()
            params["utm_content"] = variant
            variant_url = f"{base_url}?{urlencode(params)}"
            urls.append({"name": variant, "url": variant_url, "params": params.copy()})

    # Generate output
    output = f"""# UTM URLs

**Base URL:** {args.url}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Campaign Parameters

| Parameter | Value |
|-----------|-------|
| Source | {args.source} |
| Medium | {args.medium} |
| Campaign | {args.campaign} |
| Term | {args.term or "Not set"} |
| Content | {args.content or "Not set"} |

---

## Generated URLs

"""
    
    for item in urls:
        output += f"""### {item['name']}

```
{item['url']}
```

---

"""

    # Add tracking table
    output += """## Tracking Reference

Copy this to your campaign tracker:

| Variant | URL | Source | Medium | Campaign | Content |
|---------|-----|--------|--------|----------|---------|
"""
    for item in urls:
        p = item['params']
        output += f"| {item['name']} | [Link]({item['url']}) | {p['utm_source']} | {p['utm_medium']} | {p['utm_campaign']} | {p.get('utm_content', '')} |\n"

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    
    print(f"✅ Generated {len(urls)} UTM URLs")
    print(f"   📄 Output: {args.output}")
    print(f"\n   Main URL:\n   {main_url}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
