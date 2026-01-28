#!/usr/bin/env python3
"""
LinkedIn Posts Scraper + Personalized First Line Generator

Scrapes actual LinkedIn posts from profiles using supreme_coder/linkedin-post
actor and generates truly personalized first lines based on real content.

IMPORTANT: This uses the Apify actor 'supreme_coder/linkedin-post' which
scrapes actual post content from LinkedIn profiles for truly personalized
outreach.

Usage:
    # Basic usage - scrape and personalize
    python3 execution/scrape_linkedin_posts_personalize.py \
        --input leads.json \
        --output personalized_leads.json

    # With Instantly upload
    python3 execution/scrape_linkedin_posts_personalize.py \
        --input leads.json \
        --output personalized_leads.json \
        --instantly_campaign "campaign-id-here"
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from apify_client import ApifyClient
except ImportError:
    print("Error: apify-client not installed. Run: pip install apify-client")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai not installed. Run: pip install openai")
    sys.exit(1)

# Load env manually to avoid dotenv issues
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, val = line.strip().split('=', 1)
                val = val.strip('"').strip("'")
                os.environ.setdefault(key, val)

# Apify actor for LinkedIn posts - supreme_coder/linkedin-post
LINKEDIN_POST_ACTOR = "supreme_coder/linkedin-post"


def get_apify_client():
    """Get Apify client."""
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        print("Error: APIFY_API_TOKEN required in .env")
        sys.exit(1)
    return ApifyClient(token)


def get_llm_client():
    """Get LLM client (OpenRouter or OpenAI)."""
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
    elif os.getenv("OPENAI_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY required")
        sys.exit(1)


def get_model():
    """Get model name based on available API."""
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def scrape_linkedin_posts(linkedin_urls: list, posts_per_profile: int = 5) -> dict:
    """
    Scrape LinkedIn posts from profiles using supreme_coder/linkedin-post actor.

    Args:
        linkedin_urls: List of LinkedIn profile URLs
        posts_per_profile: Number of posts to fetch per profile

    Returns:
        Dict mapping LinkedIn URL to list of posts
    """
    client = get_apify_client()
    results = {}

    # This actor can handle multiple URLs in one call
    print(f"  Scraping posts from {len(linkedin_urls)} profiles...")

    try:
        run_input = {
            "urls": linkedin_urls,
            "deepScrape": True,
            "limitPerSource": posts_per_profile,
            "rawData": False
        }

        run = client.actor(LINKEDIN_POST_ACTOR).call(
            run_input=run_input,
            timeout_secs=600
        )

        print(f"  Run completed: {run.get('status')}")

        # Group posts by input URL (profile)
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            input_url = item.get("inputUrl", "").lower().rstrip("/")
            author_url = item.get("authorProfileUrl", "").lower().rstrip("/")

            # Match by input URL or author profile URL
            url_key = input_url or author_url

            if url_key:
                if url_key not in results:
                    results[url_key] = {
                        "author_name": item.get("authorName", ""),
                        "posts": []
                    }

                results[url_key]["posts"].append({
                    "text": item.get("text", ""),
                    "reactions": item.get("numLikes", 0),
                    "comments": item.get("numComments", 0),
                    "posted_at": item.get("postedAtISO", ""),
                    "time_since": item.get("timeSincePosted", ""),
                    "url": item.get("url", "")
                })

        print(f"  Found posts for {len(results)} profiles")

    except Exception as e:
        print(f"  Error scraping posts: {e}")

    return results


def generate_personalized_first_line(llm_client, lead: dict, posts_data: dict) -> dict:
    """
    Generate a truly personalized first line based on actual LinkedIn posts.

    Args:
        llm_client: OpenAI client
        lead: Lead data from our list
        posts_data: Scraped posts data from LinkedIn

    Returns:
        Dict with personalized first line and metadata
    """
    name = lead.get("full_name") or f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
    company = lead.get("company_name", "")
    title = lead.get("job_title", "")
    headline = lead.get("headline", "")

    # Extract posts content
    posts = posts_data.get("posts", []) if posts_data else []
    posts_text = ""
    if posts:
        for i, post in enumerate(posts[:5]):
            content = post.get("text", "")
            reactions = post.get("reactions", 0)
            time_since = post.get("time_since", "")
            if content:
                posts_text += f"\n--- Post {i+1} ({time_since}, {reactions} reactions) ---\n{content[:600]}\n"

    has_posts = bool(posts_text.strip())

    system_prompt = """You are a master at writing hyper-personalized cold email first lines that feel like they came from someone who actually read this person's LinkedIn.

Write ONE opening line (8-18 words) that references something SPECIFIC from their posts.

CRITICAL RULES:
1. If you have their posts - REFERENCE THEIR ACTUAL CONTENT. Quote or paraphrase their ideas.
2. NEVER use generic phrases like "I noticed" or "I came across" or "As a [title]"
3. Sound like a peer who genuinely found their content interesting
4. Reference their IDEAS and OPINIONS, not just job facts
5. Be conversational, not salesy
6. Don't start with "I" - start with something about THEM

EXCELLENT examples (post-based):
- "Your take on why intent data is overrated really challenged my thinking."
- "That post about product-led growth being 'misunderstood as product-only growth' was perfectly put."
- "Loved your breakdown of why most ABM fails - the bit about relevance over volume hit home."
- "Your point about AI automating the wrong sales tasks first really stuck with me."
- "The way you framed technical debt as 'borrowed time from your future self' was brilliant."

BAD examples (generic):
- "As a Product Owner at Salesforce, you probably..."
- "I noticed you work in the SaaS space..."
- "I came across your profile and..."
- "Your experience at [Company] is impressive..."

Output ONLY the first line. No quotes. No explanation."""

    if has_posts:
        user_prompt = f"""Write a hyper-personalized first line for:

NAME: {name}
TITLE: {title} at {company}

THEIR ACTUAL LINKEDIN POSTS:
{posts_text}

Pick ONE specific idea/opinion from their posts and write a first line that references it naturally. What did they say that you could genuinely comment on as a peer?"""
    else:
        user_prompt = f"""Write a personalized first line for:

NAME: {name}
TITLE: {title} at {company}
HEADLINE: {headline}

No posts available. Use their headline creatively - what unique angle does it suggest? Don't be generic about their role."""

    try:
        response = llm_client.chat.completions.create(
            model=get_model(),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.85,
            max_tokens=100
        )
        first_line = response.choices[0].message.content.strip().strip('"').strip("'")

        # Get a sample post for reference
        sample_post = posts[0].get("text", "")[:150] if posts else ""

        return {
            "personalized_first_line": first_line,
            "personalization_source": "linkedin_posts" if has_posts else "headline",
            "posts_found": len(posts),
            "sample_post": sample_post,
            "confidence": "high" if has_posts else "medium"
        }

    except Exception as e:
        return {
            "personalized_first_line": f"Error: {e}",
            "personalization_source": "error",
            "posts_found": 0,
            "sample_post": "",
            "confidence": "none"
        }


def load_leads(path: str) -> list:
    """Load leads from JSON file."""
    with open(path) as f:
        data = json.load(f)
        if isinstance(data, list):
            return data
        return data.get("leads", data.get("data", []))


def main():
    parser = argparse.ArgumentParser(
        description="Scrape LinkedIn posts and generate truly personalized first lines"
    )
    parser.add_argument("--input", "-i", required=True, help="Input leads JSON file")
    parser.add_argument("--output", "-o", default=".tmp/leads/truly_personalized.json",
                       help="Output file")
    parser.add_argument("--posts_per_profile", "-p", type=int, default=5,
                       help="Number of posts to fetch per profile")
    parser.add_argument("--limit", "-l", type=int, default=0,
                       help="Limit number of leads to process (0 = all)")

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("LinkedIn Posts Scraper + Personalized First Lines")
    print(f"Using: supreme_coder/linkedin-post actor")
    print(f"{'='*60}\n")

    # Load leads
    leads = load_leads(args.input)
    if args.limit > 0:
        leads = leads[:args.limit]
    print(f"Loaded {len(leads)} leads\n")

    # Extract LinkedIn URLs
    linkedin_urls = []
    url_to_lead_idx = {}
    for idx, lead in enumerate(leads):
        url = lead.get("linkedin", "")
        if url:
            linkedin_urls.append(url)
            url_key = url.lower().rstrip("/")
            url_to_lead_idx[url_key] = idx

    print(f"Found {len(linkedin_urls)} LinkedIn URLs\n")

    # Step 1: Scrape LinkedIn posts
    print("Step 1: Scraping LinkedIn posts...")
    print("-" * 40)
    posts_data = scrape_linkedin_posts(linkedin_urls, args.posts_per_profile)
    profiles_with_posts = sum(1 for p in posts_data.values() if p.get("posts"))
    print(f"  Profiles with posts: {profiles_with_posts}/{len(linkedin_urls)}\n")

    # Step 2: Generate personalized first lines
    print("Step 2: Generating personalized first lines...")
    print("-" * 40)

    llm_client = get_llm_client()
    results = []

    for i, lead in enumerate(leads, 1):
        name = lead.get("full_name") or f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
        company = lead.get("company_name", "")

        # Find matching posts data
        url = lead.get("linkedin", "").lower().rstrip("/")
        profile_posts = posts_data.get(url, {})

        posts_count = len(profile_posts.get("posts", []))
        print(f"[{i}/{len(leads)}] {name} @ {company} ({posts_count} posts)...", end=" ")

        # Generate personalized first line
        personalization = generate_personalized_first_line(llm_client, lead, profile_posts)

        # Merge with original lead data
        result = {**lead, **personalization}
        results.append(result)

        confidence = personalization.get('confidence', 'none')
        print(f"✓ ({confidence})")

        # Show first line for high confidence
        if confidence == "high":
            print(f"    → \"{personalization['personalized_first_line'][:60]}...\"")

        # Small delay to avoid rate limits
        time.sleep(0.3)

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    high_confidence = sum(1 for r in results if r.get("confidence") == "high")

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "total_leads": len(results),
        "profiles_with_posts": profiles_with_posts,
        "high_confidence": high_confidence,
        "leads": results
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    # Summary
    print(f"\n{'='*60}")
    print("COMPLETE!")
    print(f"{'='*60}")
    print(f"Total leads: {len(results)}")
    print(f"With posts (high confidence): {high_confidence}")
    print(f"Headline-based (medium): {len(results) - high_confidence}")
    print(f"Output: {output_path}")

    # Show sample high-confidence lines
    print(f"\nSample TRULY PERSONALIZED first lines (from posts):")
    print("-" * 50)
    shown = 0
    for r in results:
        if r.get("confidence") == "high" and shown < 5:
            name = r.get("full_name", "")
            line = r.get("personalized_first_line", "")
            sample = r.get("sample_post", "")[:80]
            print(f"\n{name}:")
            print(f"  First line: \"{line}\"")
            if sample:
                print(f"  Based on: \"{sample}...\"")
            shown += 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
