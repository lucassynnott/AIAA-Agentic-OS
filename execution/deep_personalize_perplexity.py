#!/usr/bin/env python3
"""
Deep Personalization via Perplexity Research

Uses Perplexity AI to research each lead's LinkedIn posts, articles, podcast
appearances, and public content to generate truly personalized first lines.

Usage:
    python3 execution/deep_personalize_perplexity.py \
        --input leads.json \
        --output personalized_leads.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai not installed. Run: pip install openai")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()


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
    """Get model name."""
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def search_perplexity(query: str) -> str:
    """
    Search using Perplexity API for real-time web data.
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return ""

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-sonar-large-128k-online",
                "messages": [{"role": "user", "content": query}],
                "temperature": 0.1
            },
            timeout=45
        )
        if response.ok:
            return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"    Perplexity error: {e}")

    return ""


def research_person_deeply(name: str, company: str, title: str, linkedin_url: str) -> str:
    """
    Use Perplexity to deeply research a person's public content.
    """
    # Targeted research query for LinkedIn posts and public content
    query = f"""Find recent LinkedIn posts, articles, podcast appearances, or public content from {name}, {title} at {company}.

LinkedIn: {linkedin_url}

I need SPECIFIC things they've said, posted, or written about. Look for:
1. Their recent LinkedIn posts (quotes from actual posts)
2. Any articles they've written
3. Podcast or webinar appearances
4. Conference talks or presentations
5. Quotes in press/media
6. Their opinions on industry topics

Give me DIRECT QUOTES or specific content they've shared, not general information about them or their company. If you can't find specific content, say "No specific content found" rather than making assumptions."""

    return search_perplexity(query)


def generate_truly_personal_first_line(llm_client, lead: dict, research: str) -> dict:
    """
    Generate a truly personalized first line based on deep research.
    """
    name = lead.get("full_name") or f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
    company = lead.get("company_name", "")
    title = lead.get("job_title", "")
    headline = lead.get("headline", "")

    # Check if research found real content
    has_real_content = research and "no specific content found" not in research.lower() and len(research) > 100

    system_prompt = """You are a master at writing hyper-personalized cold email first lines that sound like they came from someone who actually knows the person.

Your job: Write ONE opening line (8-18 words) that references something SPECIFIC this person has said, posted, or believes.

CRITICAL RULES:
1. If research contains REAL quotes or specific content - USE IT. Reference their actual words/ideas.
2. If research is generic or empty - use their headline creatively, but be specific about what stands out.
3. NEVER use filler phrases like "I noticed" or "I came across" or "I saw that"
4. Sound like a peer who genuinely found their content interesting
5. Be conversational, not salesy
6. Reference IDEAS and OPINIONS, not just job facts

EXCELLENT examples (truly personal):
- "Your take on why intent data is overrated really challenged my thinking - especially the point about false positives."
- "That post about product-led growth being 'misunderstood as product-only growth' was perfectly put."
- "Loved your breakdown of why most ABM fails - the bit about spraying content vs actual relevance hit home."
- "Your comment about AI replacing the wrong parts of sales first really stuck with me."

BAD examples (generic):
- "As a Product Owner at Salesforce, you probably..."
- "I noticed you work in the SaaS space..."
- "Your experience at [Company] is impressive..."
- "I came across your profile and..."

If the research has good content, your line MUST reference it specifically.
Output ONLY the first line - no quotes, no explanation."""

    if has_real_content:
        user_prompt = f"""Write a hyper-personalized first line for:

NAME: {name}
TITLE: {title} at {company}
HEADLINE: {headline}

RESEARCH ON THEIR PUBLIC CONTENT:
{research[:2000]}

Your first line MUST reference something specific from the research above. What did they say or post that you can genuinely comment on?"""
    else:
        user_prompt = f"""Write a personalized first line for:

NAME: {name}
TITLE: {title} at {company}
HEADLINE: {headline}

No specific posts found, but their headline is: "{headline}"

Write a first line that picks up on something SPECIFIC and interesting from their headline - not generic role-based assumptions. What unique angle does their headline suggest?"""

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

        return {
            "personalized_first_line": first_line,
            "personalization_source": "linkedin_post" if has_real_content else "headline_creative",
            "research_found": has_real_content,
            "research_snippet": research[:300] if research else "",
            "confidence": "high" if has_real_content else "medium"
        }

    except Exception as e:
        return {
            "personalized_first_line": f"Error: {e}",
            "personalization_source": "error",
            "research_found": False,
            "research_snippet": "",
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
        description="Deep personalization via Perplexity research"
    )
    parser.add_argument("--input", "-i", required=True, help="Input leads JSON file")
    parser.add_argument("--output", "-o", default=".tmp/leads/deep_personalized.json",
                       help="Output file")
    parser.add_argument("--limit", "-l", type=int, default=0,
                       help="Limit number of leads (0 = all)")

    args = parser.parse_args()

    # Check for Perplexity API key
    if not os.getenv("PERPLEXITY_API_KEY"):
        print("Error: PERPLEXITY_API_KEY required in .env")
        sys.exit(1)

    print(f"\n{'='*60}")
    print("Deep Personalization via Perplexity Research")
    print(f"{'='*60}\n")

    # Load leads
    leads = load_leads(args.input)
    if args.limit > 0:
        leads = leads[:args.limit]
    print(f"Processing {len(leads)} leads\n")

    llm_client = get_llm_client()
    results = []

    for i, lead in enumerate(leads, 1):
        name = lead.get("full_name") or f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
        company = lead.get("company_name", "")
        title = lead.get("job_title", "")
        linkedin = lead.get("linkedin", "")

        print(f"[{i}/{len(leads)}] {name} @ {company}")
        print(f"    Researching public content...", end=" ")

        # Deep research via Perplexity
        research = research_person_deeply(name, company, title, linkedin)
        has_content = research and "no specific content found" not in research.lower() and len(research) > 100
        print(f"{'Found content!' if has_content else 'Using headline'}")

        # Generate personalized first line
        print(f"    Writing first line...", end=" ")
        personalization = generate_truly_personal_first_line(llm_client, lead, research)

        result = {**lead, **personalization}
        results.append(result)

        print(f"✓ ({personalization['confidence']})")
        print(f"    → \"{personalization['personalized_first_line'][:70]}...\"" if len(personalization['personalized_first_line']) > 70 else f"    → \"{personalization['personalized_first_line']}\"")
        print()

        # Rate limiting
        time.sleep(1.5)

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    high_confidence = sum(1 for r in results if r.get("confidence") == "high")

    output_data = {
        "generated_at": datetime.now().isoformat(),
        "total_leads": len(results),
        "high_confidence": high_confidence,
        "leads": results
    }

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    # Summary
    print(f"\n{'='*60}")
    print("Complete!")
    print(f"{'='*60}")
    print(f"Total processed: {len(results)}")
    print(f"High confidence (found real content): {high_confidence}")
    print(f"Medium confidence (headline-based): {len(results) - high_confidence}")
    print(f"Output: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
