#!/usr/bin/env python3
"""
Client Feedback Collector - Analyze and categorize client feedback.

Usage:
    python3 execution/collect_feedback.py \
        --feedback "The onboarding was great but I wish the dashboard was faster" \
        --output .tmp/feedback_analysis.json
"""

import argparse, json, os, sys
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
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o-mini"

def analyze_feedback(client, feedback, source=""):
    """Analyze a piece of feedback."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You analyze customer feedback to extract actionable insights. Return JSON."},
            {"role": "user", "content": f"""Analyze this feedback:

FEEDBACK: {feedback}
SOURCE: {source or "Direct"}

RETURN JSON:
{{
  "sentiment": "positive|negative|mixed|neutral",
  "sentiment_score": -100 to 100,
  "categories": ["product", "support", "pricing", "onboarding", "performance", "feature", "other"],
  "key_themes": ["theme1", "theme2"],
  "praise_points": ["What they liked"],
  "improvement_areas": ["What needs work"],
  "feature_requests": ["Any features requested"],
  "urgency": "high|medium|low",
  "actionable": true|false,
  "suggested_actions": ["Action 1", "Action 2"],
  "nps_likely": 1-10,
  "follow_up_needed": true|false,
  "summary": "One sentence summary"
}}"""}
        ],
        temperature=0.4,
        max_tokens=600
    ).choices[0].message.content

    try:
        if "```" in response:
            response = response.split("```")[1]
            if response.startswith("json"):
                response = response[4:]
        return json.loads(response)
    except:
        return {"sentiment": "neutral", "error": "Parse failed"}

def main():
    parser = argparse.ArgumentParser(description="Analyze client feedback")
    parser.add_argument("--feedback", "-f", help="Feedback text")
    parser.add_argument("--file", help="File with feedback")
    parser.add_argument("--batch", "-b", help="JSON file with multiple feedback items")
    parser.add_argument("--source", "-s", default="", help="Feedback source")
    parser.add_argument("--output", "-o", default=".tmp/feedback_analysis.json")
    args = parser.parse_args()

    client = get_client()

    if args.batch:
        with open(args.batch) as f:
            items = json.load(f)
        
        results = []
        for i, item in enumerate(items, 1):
            text = item.get("feedback", item.get("text", item.get("comment", "")))
            print(f"[{i}/{len(items)}] Analyzing...", end=" ")
            result = analyze_feedback(client, text, item.get("source", ""))
            result["original"] = item
            results.append(result)
            print(f"→ {result.get('sentiment', 'unknown')}")
        
        # Aggregate stats
        sentiments = [r.get("sentiment") for r in results]
        output = {
            "analyzed_at": datetime.now().isoformat(),
            "summary": {
                "total": len(results),
                "positive": sentiments.count("positive"),
                "negative": sentiments.count("negative"),
                "mixed": sentiments.count("mixed"),
                "neutral": sentiments.count("neutral")
            },
            "results": results
        }
    else:
        if args.file:
            feedback = Path(args.file).read_text()
        else:
            feedback = args.feedback or ""
        
        print(f"\n📝 Feedback Analyzer\n")
        result = analyze_feedback(client, feedback, args.source)
        output = {"analyzed_at": datetime.now().isoformat(), **result}
        
        print(f"Sentiment: {result.get('sentiment', 'unknown').upper()} ({result.get('sentiment_score', 0)})")
        print(f"Categories: {', '.join(result.get('categories', []))}")
        print(f"Actionable: {'Yes' if result.get('actionable') else 'No'}")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Saved to: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
