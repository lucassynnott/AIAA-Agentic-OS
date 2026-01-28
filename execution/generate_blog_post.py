#!/usr/bin/env python3
"""
Blog Post Writer - Generate SEO-optimized blog posts.

Usage:
    python3 execution/generate_blog_post.py \
        --topic "How to Scale Cold Email Outreach" \
        --keyword "cold email outreach" \
        --length "1500" \
        --output .tmp/blog_post.md
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv()


def get_client() -> OpenAI:
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def call_llm(client: OpenAI, system: str, user: str, temp: float = 0.7) -> str:
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=get_model(),
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=temp, max_tokens=4000
            )
            return resp.choices[0].message.content
        except Exception as e:
            if attempt == 2: raise e
    return ""


def generate_blog(client: OpenAI, topic: str, keyword: str, length: int, tone: str) -> dict:
    """Generate complete blog post."""
    
    print("📋 Creating outline...")
    outline = call_llm(client,
        "You are an SEO content strategist.",
        f"""Create a blog post outline for:
TOPIC: {topic}
TARGET KEYWORD: {keyword}
LENGTH: {length} words

Include:
- H1 title (with keyword)
- Meta description (155 chars)
- 5-7 H2 sections
- Key points under each H2
- FAQs (3-5)
- Internal/external link opportunities""", 0.6)
    
    print("📝 Writing content...")
    content = call_llm(client,
        f"You are an expert blog writer. Write in a {tone} tone. Make content actionable and valuable.",
        f"""Write a complete {length}-word blog post:

TOPIC: {topic}
KEYWORD: {keyword}
TONE: {tone}

OUTLINE:
{outline}

REQUIREMENTS:
- Use keyword naturally (1-2% density)
- Short paragraphs (2-3 sentences)
- Use bullet points and numbered lists
- Include actionable takeaways
- Add relevant statistics/data where appropriate
- Write compelling intro that hooks reader
- Strong conclusion with CTA
- H2 and H3 subheadings throughout

Format in markdown with proper headings.""", 0.7)
    
    print("🔍 Generating SEO metadata...")
    seo = call_llm(client, "You are an SEO expert.",
        f"""For this blog post about "{topic}" with keyword "{keyword}":

CONTENT:
{content[:2000]}

Generate:
1. SEO Title (60 chars max, include keyword)
2. Meta Description (155 chars, include keyword, compelling)
3. URL Slug (lowercase, hyphens)
4. Focus Keyphrase
5. Secondary Keywords (5)
6. Internal Link Suggestions (3 topics to link)
7. Schema Markup Type (Article, HowTo, FAQ)""", 0.5)
    
    return {"outline": outline, "content": content, "seo": seo}


def main():
    parser = argparse.ArgumentParser(description="Generate SEO blog posts")
    parser.add_argument("--topic", "-t", required=True, help="Blog topic")
    parser.add_argument("--keyword", "-k", default="", help="Target SEO keyword")
    parser.add_argument("--length", "-l", type=int, default=1500, help="Word count target")
    parser.add_argument("--tone", "-n", default="professional", 
        choices=["professional", "casual", "authoritative", "conversational"])
    parser.add_argument("--output", "-o", default=".tmp/blog_post.md")
    
    args = parser.parse_args()
    keyword = args.keyword or args.topic.lower()
    
    print(f"\n📝 Blog Post Writer")
    print(f"   Topic: {args.topic}")
    print(f"   Keyword: {keyword}")
    print(f"   Length: {args.length} words\n")
    
    client = get_client()
    result = generate_blog(client, args.topic, keyword, args.length, args.tone)
    
    output = f"""# Blog Post: {args.topic}

**Generated:** {datetime.now().strftime("%Y-%m-%d")}
**Target Keyword:** {keyword}
**Target Length:** {args.length} words

---

## SEO METADATA

{result['seo']}

---

## OUTLINE

{result['outline']}

---

## FULL CONTENT

{result['content']}
"""
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    
    print(f"\n✅ Blog post complete!")
    print(f"   📄 Output: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
