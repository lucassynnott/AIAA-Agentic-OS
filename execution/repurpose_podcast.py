#!/usr/bin/env python3
"""
Podcast Repurposer - Convert podcast/video content into multiple formats.

Usage:
    python3 execution/repurpose_podcast.py \
        --transcript transcript.txt \
        --formats "linkedin,twitter,blog" \
        --output .tmp/repurposed/
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

def repurpose_to_format(client, transcript, format_type, title=""):
    """Repurpose transcript to a specific format."""
    prompts = {
        "linkedin": "Create 3 LinkedIn posts from key insights. Each post should have a hook, value, and CTA.",
        "twitter": "Create a 10-tweet thread with the best insights. Make it engaging and shareable.",
        "blog": "Create a 1000-word blog post with SEO optimization. Include headline, subheadings, and meta description.",
        "newsletter": "Create a newsletter edition with key takeaways and insights.",
        "shorts": "Identify 5 moments that would make great short-form video clips (30-60 seconds). Provide timestamp ranges and hooks.",
        "quotes": "Extract 10 quotable moments that could be used as social media graphics.",
        "summary": "Create an executive summary with key points, insights, and action items."
    }

    prompt = prompts.get(format_type, prompts["summary"])

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You repurpose long-form content into {format_type} format. Be creative and maintain the original voice."},
            {"role": "user", "content": f"""Repurpose this transcript into {format_type} content:

TITLE: {title or "Untitled"}

TRANSCRIPT:
{transcript[:6000]}

TASK: {prompt}

Create high-quality, engaging content that captures the best insights."""}
        ],
        temperature=0.7,
        max_tokens=3000
    ).choices[0].message.content

    return response

def main():
    parser = argparse.ArgumentParser(description="Repurpose podcast/video content")
    parser.add_argument("--transcript", "-t", required=True, help="Transcript file")
    parser.add_argument("--title", default="", help="Content title")
    parser.add_argument("--formats", "-f", default="linkedin,twitter,summary", 
        help="Comma-separated formats: linkedin,twitter,blog,newsletter,shorts,quotes,summary")
    parser.add_argument("--output", "-o", default=".tmp/repurposed/")
    args = parser.parse_args()

    transcript = Path(args.transcript).read_text()
    formats = [f.strip() for f in args.formats.split(",")]
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🔄 Podcast Repurposer\n   Formats: {formats}\n")
    client = get_client()

    results = {}
    for fmt in formats:
        print(f"   Creating {fmt}...", end=" ")
        content = repurpose_to_format(client, transcript, fmt, args.title)
        results[fmt] = content
        
        # Save individual file
        file_path = output_dir / f"{fmt}.md"
        file_path.write_text(f"# {fmt.title()} Content\n\n{content}", encoding="utf-8")
        print("✅")

    # Create master file
    master = f"""# Repurposed Content

**Source:** {args.title or Path(args.transcript).name}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}
**Formats:** {', '.join(formats)}

---

"""
    for fmt, content in results.items():
        master += f"\n## {fmt.upper()}\n\n{content}\n\n---\n"

    (output_dir / "all_content.md").write_text(master, encoding="utf-8")

    print(f"\n✅ Created {len(formats)} content pieces")
    print(f"   📁 Output: {output_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
