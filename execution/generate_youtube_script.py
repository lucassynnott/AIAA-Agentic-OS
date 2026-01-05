#!/usr/bin/env python3
"""
YouTube Script Creator - Generate optimized video scripts with hooks, structure, and CTAs.

Usage:
    python3 execution/generate_youtube_script.py \
        --topic "How to Build a 6-Figure Business" \
        --length "10min" \
        --style "educational" \
        --output .tmp/youtube_script.md
"""

import argparse
import json
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
    elif os.getenv("OPENAI_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY required")
        sys.exit(1)


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def call_llm(client: OpenAI, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=get_model(),
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
                temperature=temperature,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise e
            print(f"  Retry {attempt + 1}/3: {e}")
    return ""


def generate_hooks(client: OpenAI, topic: str, style: str, audience: str) -> str:
    """Generate compelling hook options."""
    print("🎣 Generating hooks...")
    
    system_prompt = """You are a YouTube scriptwriter specializing in viral hooks. 
Your hooks stop viewers from scrolling within 5 seconds and confirm they clicked the right video."""
    
    user_prompt = f"""Create 5 powerful hooks for this YouTube video:

TOPIC: {topic}
STYLE: {style}
AUDIENCE: {audience}

Generate 5 different hooks using these frameworks:

1. CURIOSITY GAP: Open a loop that MUST be closed
   - "There's a reason [X] that nobody talks about..."

2. BOLD CLAIM: Make a specific, intriguing promise
   - "This one change added $X to my business..."

3. CONTRARIAN: Challenge what viewers believe
   - "Everything you know about [X] is wrong..."

4. STORY HOOK: Start mid-action
   - "I was about to give up when..."

5. QUESTION HOOK: Make them reflect
   - "What if I told you [X]?"

For each hook:
- The exact opening line (first 5 seconds)
- The next 10-15 seconds (setup)
- Why it works psychologically

Make them specific to the topic, not generic."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.8)


def generate_outline(client: OpenAI, topic: str, length: str, style: str) -> str:
    """Generate video structure/outline."""
    print("📋 Creating outline...")
    
    # Calculate approximate word count
    length_map = {"5min": 750, "10min": 1500, "15min": 2250, "20min": 3000}
    words = length_map.get(length, 1500)
    
    system_prompt = """You are a YouTube content strategist specializing in retention optimization.
Create video structures that maintain 50%+ retention throughout."""
    
    user_prompt = f"""Create a detailed outline for this video:

TOPIC: {topic}
LENGTH: {length} (~{words} words)
STYLE: {style}

CREATE OUTLINE WITH:

## HOOK (0:00-0:30)
- Opening line
- Setup/context
- Promise of value

## SECTION 1: [Title] (0:30-X:XX)
- Main point
- Supporting details
- Example/story
- Re-hook to next section

## SECTION 2: [Title]
(repeat structure)

## SECTION 3: [Title]
(repeat structure)

## SECTION 4: [Title] (if needed)
(repeat structure)

## CONCLUSION (Last 60-90 seconds)
- Recap key points
- Big takeaway
- CTA setup

## CTA
- Subscribe prompt
- Next video tease
- Comment question

For each section:
- Exact timestamp range
- Main point in one sentence
- 2-3 supporting points
- Re-hook to maintain retention

Include "open loops" (curiosity hooks) to tease upcoming content."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.6)


def generate_full_script(client: OpenAI, topic: str, hooks: str, outline: str, style: str, length: str) -> str:
    """Generate the complete script."""
    print("📝 Writing full script...")
    
    length_map = {"5min": 750, "10min": 1500, "15min": 2250, "20min": 3000}
    words = length_map.get(length, 1500)
    
    system_prompt = """You are an elite YouTube scriptwriter. Your scripts achieve:
- 50%+ retention throughout
- High engagement (likes, comments, shares)
- Strong CTR from end screens

Write in a conversational, engaging style. Every line must either advance the content or create curiosity."""
    
    user_prompt = f"""Write the complete YouTube script:

TOPIC: {topic}
LENGTH: {length} (~{words} words)
STYLE: {style}

SELECTED HOOK (use this):
{hooks[:500]}

OUTLINE TO FOLLOW:
{outline}

WRITE THE FULL SCRIPT:

Format:
[TIMESTAMP: 0:00-0:30]
HOOK
[Exact words to say]

[TIMESTAMP: 0:30-X:XX]
SECTION 1: [Title]
[Exact words to say]
[B-ROLL: description] - for visual cues
[ON-SCREEN TEXT: text] - for key points

(continue for all sections)

SCRIPT RULES:
1. Write at 6th grade reading level
2. Short sentences (under 20 words)
3. Use "you" language (make it about the viewer)
4. Include verbal re-hooks ("but here's where it gets interesting...")
5. Add [PAUSE] markers for emphasis
6. Include [B-ROLL] and [ON-SCREEN TEXT] cues
7. Make every 30 seconds deliver value
8. End each section with an open loop

Write ~{words} words total. Make it conversational - this is meant to be spoken, not read."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def generate_seo(client: OpenAI, topic: str, script: str) -> str:
    """Generate SEO package (title, description, tags)."""
    print("🔍 Creating SEO package...")
    
    system_prompt = "You are a YouTube SEO specialist. Optimize for discoverability and CTR."
    
    user_prompt = f"""Create an SEO package for this video:

TOPIC: {topic}

SCRIPT SUMMARY:
{script[:1500]}

GENERATE:

## TITLE OPTIONS (3)
- Under 60 characters
- Include keyword naturally
- Create curiosity or promise value

## DESCRIPTION
- First 100 chars are crucial (shown in search)
- Include keywords naturally
- Timestamps for all sections
- Related videos/playlists
- Social links section
- 2000+ characters total

## TAGS (20-30)
- Primary keyword variations
- Long-tail keywords
- Related topics
- Common misspellings

## THUMBNAIL TEXT
- 3-4 words max
- High contrast recommendation
- Emotion to convey

## HASHTAGS (3-5)
- Relevant to topic
- Mix of broad and specific

## SUGGESTED COMMENT
- Pin as first comment
- Include extra value or question"""

    return call_llm(client, system_prompt, user_prompt, temperature=0.5)


def save_output(output_path: Path, content: str):
    """Save content to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate YouTube video scripts")
    parser.add_argument("--topic", "-t", required=True, help="Video topic")
    parser.add_argument("--length", "-l", default="10min", choices=["5min", "10min", "15min", "20min"], 
        help="Video length")
    parser.add_argument("--style", "-s", default="educational", 
        choices=["educational", "entertaining", "storytelling", "tutorial", "review"],
        help="Video style")
    parser.add_argument("--audience", "-a", default="General audience", help="Target audience")
    parser.add_argument("--output", "-o", default=".tmp/youtube_script.md", help="Output file")
    parser.add_argument("--hooks_only", action="store_true", help="Only generate hooks")
    
    args = parser.parse_args()
    
    print(f"\n🎬 YouTube Script Creator")
    print(f"   Topic: {args.topic}")
    print(f"   Length: {args.length}")
    print(f"   Style: {args.style}\n")
    
    client = get_client()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate hooks
    hooks = generate_hooks(client, args.topic, args.style, args.audience)
    
    if args.hooks_only:
        output_path = Path(args.output)
        save_output(output_path, f"# YouTube Hooks: {args.topic}\n\n{hooks}")
        print(f"\n✅ Hooks saved to: {output_path}")
        return 0
    
    # Generate outline
    outline = generate_outline(client, args.topic, args.length, args.style)
    
    # Generate full script
    script = generate_full_script(client, args.topic, hooks, outline, args.style, args.length)
    
    # Generate SEO
    seo = generate_seo(client, args.topic, script)
    
    # Compile final output
    final_output = f"""# YouTube Script: {args.topic}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Length:** {args.length}
**Style:** {args.style}

---

# HOOK OPTIONS

{hooks}

---

# VIDEO OUTLINE

{outline}

---

# FULL SCRIPT

{script}

---

# SEO PACKAGE

{seo}
"""
    
    output_path = Path(args.output)
    save_output(output_path, final_output)
    
    print(f"\n✅ Script complete!")
    print(f"   📄 Output: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
