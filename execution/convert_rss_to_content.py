#!/usr/bin/env python3
"""
RSS to Content Pipeline - Convert RSS feed items into social content.

Usage:
    python3 execution/convert_rss_to_content.py \
        --feed "https://example.com/rss" \
        --platforms "linkedin,twitter" \
        --output .tmp/rss_content.md
"""

import argparse, os, sys
from datetime import datetime
from pathlib import Path
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

def fetch_rss(url):
    """Fetch and parse RSS feed."""
    try:
        resp = requests.get(url, timeout=30)
        # Simple XML parsing for common fields
        import re
        items = []
        for match in re.finditer(r'<item>(.*?)</item>', resp.text, re.DOTALL):
            item = match.group(1)
            title = re.search(r'<title>(.*?)</title>', item, re.DOTALL)
            link = re.search(r'<link>(.*?)</link>', item, re.DOTALL)
            desc = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            items.append({
                "title": title.group(1).strip() if title else "",
                "link": link.group(1).strip() if link else "",
                "description": desc.group(1).strip()[:500] if desc else ""
            })
        return items[:5]  # Get latest 5
    except Exception as e:
        return []

def main():
    parser = argparse.ArgumentParser(description="Convert RSS to social content")
    parser.add_argument("--feed", "-f", required=True, help="RSS feed URL")
    parser.add_argument("--platforms", "-p", default="linkedin,twitter")
    parser.add_argument("--items", "-i", type=int, default=3, help="Items to convert")
    parser.add_argument("--output", "-o", default=".tmp/rss_content.md")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")]
    print(f"\n📰 RSS to Content\n   Feed: {args.feed}\n   Platforms: {platforms}\n")

    items = fetch_rss(args.feed)
    if not items:
        print("   ❌ Could not fetch RSS feed")
        return 1

    items = items[:args.items]
    print(f"   Found {len(items)} items\n")

    client = get_client()
    all_content = []

    for i, item in enumerate(items, 1):
        print(f"   [{i}/{len(items)}] {item['title'][:40]}...")
        
        content = client.chat.completions.create(
            model=get_model(),
            messages=[
                {"role": "system", "content": "You repurpose articles into engaging social media content."},
                {"role": "user", "content": f"""Convert this article to social content:

TITLE: {item['title']}
LINK: {item['link']}
EXCERPT: {item['description']}

CREATE FOR: {', '.join(platforms)}

{'## LinkedIn Post' if 'linkedin' in platforms else ''}
{'- Hook' if 'linkedin' in platforms else ''}
{'- Key insight from article' if 'linkedin' in platforms else ''}
{'- Your take/opinion' if 'linkedin' in platforms else ''}
{'- CTA (link in comments)' if 'linkedin' in platforms else ''}

{'## Twitter/X' if 'twitter' in platforms else ''}
{'- Tweet with link' if 'twitter' in platforms else ''}
{'- OR Thread option (3-5 tweets)' if 'twitter' in platforms else ''}

Add your unique perspective, don't just summarize."""}
            ],
            temperature=0.8,
            max_tokens=1000
        ).choices[0].message.content

        all_content.append(f"# Article {i}: {item['title']}\n\n**Source:** {item['link']}\n\n{content}")

    output = f"""# RSS Content: {args.feed}

**Items Converted:** {len(items)}
**Platforms:** {', '.join(platforms)}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{"---".join(all_content)}
"""

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"\n✅ Content saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
