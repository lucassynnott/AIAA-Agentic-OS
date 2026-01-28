#!/usr/bin/env python3
"""
SEO Audit Automation - Analyze a website for SEO issues and opportunities.

Usage:
    python3 execution/generate_seo_audit.py \
        --url "https://example.com" \
        --output .tmp/seo_audit.md
"""

import argparse, os, re, sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    import requests
except ImportError:
    print("Error: Required packages not installed. Run: pip install openai requests")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

def fetch_page(url):
    """Fetch page content."""
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        return resp.text
    except Exception as e:
        return f"Error: {e}"

def extract_seo_elements(html):
    """Extract key SEO elements from HTML."""
    elements = {}
    
    # Title
    title = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    elements['title'] = title.group(1).strip() if title else "Missing"
    
    # Meta description
    meta = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.I)
    elements['meta_description'] = meta.group(1) if meta else "Missing"
    
    # H1
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    elements['h1_count'] = len(h1s)
    elements['h1_text'] = [re.sub(r'<[^>]+>', '', h).strip() for h in h1s[:3]]
    
    # H2s
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.I | re.S)
    elements['h2_count'] = len(h2s)
    
    # Images without alt
    imgs = re.findall(r'<img[^>]*>', html, re.I)
    imgs_no_alt = [i for i in imgs if 'alt=' not in i.lower() or 'alt=""' in i.lower()]
    elements['images_total'] = len(imgs)
    elements['images_missing_alt'] = len(imgs_no_alt)
    
    # Links
    links = re.findall(r'<a[^>]*href=["\'](.*?)["\']', html, re.I)
    elements['internal_links'] = len([l for l in links if l.startswith('/') or 'example.com' in l])
    elements['external_links'] = len([l for l in links if l.startswith('http') and 'example.com' not in l])
    
    return elements

def main():
    parser = argparse.ArgumentParser(description="Generate SEO audit")
    parser.add_argument("--url", "-u", required=True, help="URL to audit")
    parser.add_argument("--output", "-o", default=".tmp/seo_audit.md")
    args = parser.parse_args()

    print(f"\n🔍 SEO Audit\n   URL: {args.url}\n")
    
    # Fetch page
    print("   Fetching page...")
    html = fetch_page(args.url)
    if html.startswith("Error"):
        print(f"   ❌ {html}")
        return 1
    
    # Extract elements
    print("   Extracting SEO elements...")
    elements = extract_seo_elements(html)
    
    # AI Analysis
    print("   Analyzing...")
    client = get_client()
    
    analysis = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You are an SEO expert providing actionable audit recommendations."},
            {"role": "user", "content": f"""Analyze this page's SEO:

URL: {args.url}

EXTRACTED ELEMENTS:
- Title: {elements['title']} ({len(elements['title'])} chars)
- Meta Description: {elements['meta_description'][:200]}... ({len(elements['meta_description'])} chars)
- H1 Count: {elements['h1_count']}
- H1 Text: {elements['h1_text']}
- H2 Count: {elements['h2_count']}
- Images: {elements['images_total']} total, {elements['images_missing_alt']} missing alt
- Internal Links: {elements['internal_links']}
- External Links: {elements['external_links']}

PAGE CONTENT (first 3000 chars):
{re.sub(r'<[^>]+>', ' ', html)[:3000]}

PROVIDE AUDIT:

## SEO Score: X/100

## Critical Issues (Fix Immediately)
- Issue with impact and fix

## Warnings (Should Fix)
- Warning with recommendation

## Opportunities (Nice to Have)
- Opportunity for improvement

## Technical SEO
- Title tag analysis
- Meta description analysis
- Heading structure
- Image optimization
- Internal linking

## Content Analysis
- Keyword usage
- Content quality
- Readability

## Recommendations (Priority Order)
1. Highest impact fix
2. Second priority
3. Third priority

Be specific with recommendations."""}
        ],
        temperature=0.5,
        max_tokens=2500
    ).choices[0].message.content

    output = f"""# SEO Audit Report

**URL:** {args.url}
**Date:** {datetime.now().strftime("%Y-%m-%d")}

---

## Quick Stats

| Element | Value | Status |
|---------|-------|--------|
| Title | {len(elements['title'])} chars | {"✅" if 30 <= len(elements['title']) <= 60 else "⚠️"} |
| Meta Description | {len(elements['meta_description'])} chars | {"✅" if 120 <= len(elements['meta_description']) <= 160 else "⚠️"} |
| H1 Tags | {elements['h1_count']} | {"✅" if elements['h1_count'] == 1 else "⚠️"} |
| H2 Tags | {elements['h2_count']} | {"✅" if elements['h2_count'] >= 2 else "⚠️"} |
| Images Missing Alt | {elements['images_missing_alt']}/{elements['images_total']} | {"✅" if elements['images_missing_alt'] == 0 else "⚠️"} |

---

{analysis}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    
    print(f"\n✅ Audit saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
