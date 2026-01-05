#!/usr/bin/env python3
"""
Case Study Generator - Generate client case studies from results data.

Usage:
    python3 execution/generate_case_study.py \
        --client "Acme Corp" \
        --industry "SaaS" \
        --challenge "Low conversion rates" \
        --solution "Implemented AI-powered funnels" \
        --results "300% increase in conversions" \
        --output .tmp/case_study.md
"""

import argparse, os, sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

def call_llm(client, system, user, temp=0.7):
    for attempt in range(3):
        try:
            resp = client.chat.completions.create(model=get_model(), messages=[
                {"role": "system", "content": system}, {"role": "user", "content": user}
            ], temperature=temp, max_tokens=3000)
            return resp.choices[0].message.content
        except Exception as e:
            if attempt == 2: raise e
    return ""

def main():
    parser = argparse.ArgumentParser(description="Generate case studies")
    parser.add_argument("--client", "-c", required=True, help="Client name")
    parser.add_argument("--industry", "-i", default="", help="Client industry")
    parser.add_argument("--challenge", "-h", required=True, help="Main challenge/problem")
    parser.add_argument("--solution", "-s", required=True, help="Solution implemented")
    parser.add_argument("--results", "-r", required=True, help="Results achieved")
    parser.add_argument("--timeline", "-t", default="", help="Project timeline")
    parser.add_argument("--testimonial", default="", help="Client testimonial quote")
    parser.add_argument("--output", "-o", default=".tmp/case_study.md")
    args = parser.parse_args()

    print(f"\n📋 Case Study Generator\n   Client: {args.client}\n")
    client = get_client()

    case_study = call_llm(client,
        "You are an expert at writing compelling B2B case studies that drive sales.",
        f"""Write a complete case study:

CLIENT: {args.client}
INDUSTRY: {args.industry or "Not specified"}
CHALLENGE: {args.challenge}
SOLUTION: {args.solution}
RESULTS: {args.results}
TIMELINE: {args.timeline or "Not specified"}
TESTIMONIAL: {args.testimonial or "Not provided"}

STRUCTURE:
1. **Executive Summary** (2-3 sentences)
2. **About {args.client}** (company background)
3. **The Challenge** (pain points, impact on business)
4. **The Solution** (what was implemented, approach)
5. **The Results** (specific metrics, before/after)
6. **Key Takeaways** (3 bullet points)
7. **Client Quote** (testimonial or create placeholder)

Make it compelling, specific, and results-focused. Use numbers where possible.""", 0.7)

    output = f"""# Case Study: {args.client}

**Generated:** {datetime.now().strftime("%Y-%m-%d")}
**Industry:** {args.industry}

---

{case_study}
"""
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")
    print(f"✅ Case study saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
