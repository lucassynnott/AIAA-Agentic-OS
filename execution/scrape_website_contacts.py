#!/usr/bin/env python3
"""
Website Contact Scraper - Extract contact info from websites.

Usage:
    python3 execution/scrape_website_contacts.py \
        --url "https://example.com" \
        --output .tmp/contacts.json
"""

import argparse, json, re, sys
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_contacts(url):
    """Scrape contact information from a website."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        resp = requests.get(url, headers=headers, timeout=30)
        html = resp.text
        
        contacts = {
            "url": url,
            "emails": [],
            "phones": [],
            "social": {}
        }
        
        # Extract emails
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
        contacts["emails"] = list(set([e for e in emails if not e.endswith(('.png', '.jpg', '.gif'))]))
        
        # Extract phone numbers
        phones = re.findall(r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}', html)
        contacts["phones"] = list(set(phones))[:5]
        
        # Extract social links
        linkedin = re.findall(r'linkedin\.com/(?:company|in)/[a-zA-Z0-9_-]+', html)
        twitter = re.findall(r'twitter\.com/[a-zA-Z0-9_]+', html)
        facebook = re.findall(r'facebook\.com/[a-zA-Z0-9._-]+', html)
        
        if linkedin: contacts["social"]["linkedin"] = list(set(linkedin))[:3]
        if twitter: contacts["social"]["twitter"] = list(set(twitter))[:3]
        if facebook: contacts["social"]["facebook"] = list(set(facebook))[:3]
        
        # Try to find contact page
        contact_links = re.findall(r'href=["\']([^"\']*(?:contact|about)[^"\']*)["\']', html, re.I)
        contacts["contact_pages"] = list(set(contact_links))[:5]
        
        return contacts
        
    except Exception as e:
        return {"url": url, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Scrape website contacts")
    parser.add_argument("--url", "-u", required=True, help="Website URL")
    parser.add_argument("--output", "-o", default=".tmp/contacts.json")
    args = parser.parse_args()

    if not args.url.startswith("http"):
        args.url = "https://" + args.url

    print(f"\n🔍 Website Contact Scraper\n   URL: {args.url}\n")

    contacts = scrape_contacts(args.url)
    contacts["scraped_at"] = datetime.now().isoformat()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(contacts, f, indent=2)

    print(f"   Emails found: {len(contacts.get('emails', []))}")
    print(f"   Phones found: {len(contacts.get('phones', []))}")
    print(f"   Social profiles: {len(contacts.get('social', {}))}")
    print(f"\n✅ Saved to: {args.output}")
    
    if contacts.get("emails"):
        print(f"\n   Sample emails: {', '.join(contacts['emails'][:3])}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
