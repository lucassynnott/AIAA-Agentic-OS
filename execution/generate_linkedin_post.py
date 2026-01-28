#!/usr/bin/env python3
"""
LinkedIn Post Generator - Generate optimized LinkedIn posts with hooks and CTAs.

Usage:
    python3 execution/generate_linkedin_post.py \
        --topic "How I landed my first client" \
        --type story \
        --tone casual \
        --cta comments \
        --output .tmp/linkedin_post.md
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
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise e
            print(f"  Retry {attempt + 1}/3: {e}")
    return ""


def generate_post(client: OpenAI, topic: str, post_type: str, tone: str, cta: str) -> dict:
    """Generate a LinkedIn post."""
    
    # Structure templates
    structures = {
        "story": """[Hook - 1 line that stops scroll]

[Setup - context in 2-3 lines]

[Conflict - the problem/challenge]

[Resolution - what happened]

[Lesson - the takeaway]

[CTA - engagement question]""",
        
        "tips": """[Hook - provocative statement]

Here's what I learned:

1. [Tip 1]
↳ [Explanation]

2. [Tip 2]
↳ [Explanation]

3. [Tip 3]
↳ [Explanation]

[CTA]""",
        
        "contrarian": """[Hot take that challenges conventional wisdom]

Here's why everyone's wrong:

[Argument 1]

[Argument 2]

[Argument 3]

[Nuanced conclusion]

[CTA - Agree or disagree?]""",
        
        "question": """[Thought-provoking question]

[Context - why you're asking]

[Your perspective - brief take]

[Open-ended question for engagement]""",
        
        "listicle": """[Hook with number]

1. [Point 1]
2. [Point 2]
3. [Point 3]
4. [Point 4]
5. [Point 5]

[Summary/takeaway]

[CTA]"""
    }
    
    cta_types = {
        "comments": "Ask a question that invites comments and discussion",
        "dms": "Invite people to DM for more details or a resource",
        "link": "Tease a link that will be in the comments",
        "share": "Ask people to share if they found it valuable"
    }
    
    structure = structures.get(post_type, structures["story"])
    cta_instruction = cta_types.get(cta, cta_types["comments"])
    
    system_prompt = """You are an expert LinkedIn content creator with 100K+ followers.
Your posts consistently get high engagement because you:
1. Write scroll-stopping hooks
2. Use short, punchy paragraphs
3. Format for easy reading
4. End with compelling CTAs"""
    
    user_prompt = f"""Create a LinkedIn post about:

TOPIC: {topic}
TYPE: {post_type}
TONE: {tone}
CTA GOAL: {cta_instruction}

STRUCTURE TO FOLLOW:
{structure}

LINKEDIN BEST PRACTICES:
- First line is EVERYTHING (must stop scroll)
- Short paragraphs (1-2 sentences max)
- Use line breaks liberally
- Emojis sparingly (0-3 total)
- No external links in post body
- 1,200-1,500 characters ideal
- End with question or clear CTA

HOOK FORMULAS TO CONSIDER:
- "I was wrong about [X]. Here's what I learned."
- "Stop [common advice]. Do this instead:"
- "[Number] years ago, I [failure]. Today, [success]."
- "Unpopular opinion: [contrarian take]"
- "The best [role] I know all do this:"

Write the complete post. Make it {tone} but valuable.
Format it exactly as it should appear on LinkedIn (line breaks included)."""

    post_content = call_llm(client, system_prompt, user_prompt, temperature=0.8)
    
    # Generate metadata
    meta_prompt = f"""For this LinkedIn post:

{post_content[:500]}

Provide:
1. Best posting time (based on general LinkedIn data)
2. 3-5 relevant hashtags
3. A suggested first comment (to boost engagement)

Format as:
BEST TIME: [time and day]
HASHTAGS: #tag1 #tag2 #tag3
FIRST COMMENT: [your comment to pin]"""

    metadata = call_llm(client, "You are a LinkedIn algorithm expert.", meta_prompt, temperature=0.5)
    
    return {
        "post": post_content,
        "metadata": metadata,
        "topic": topic,
        "type": post_type,
        "tone": tone
    }


def generate_hook_variations(client: OpenAI, topic: str) -> str:
    """Generate multiple hook options."""
    
    system_prompt = "You are a copywriter specializing in social media hooks."
    
    user_prompt = f"""Generate 5 different LinkedIn hooks for this topic:

TOPIC: {topic}

Create hooks using different frameworks:
1. Contrarian/Hot take
2. Personal failure story
3. Curiosity gap
4. Direct value promise
5. Question hook

For each, write just the hook (first 1-2 lines only).
Make them specific and scroll-stopping."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.9)


def main():
    parser = argparse.ArgumentParser(description="Generate LinkedIn posts")
    parser.add_argument("--topic", "-t", required=True, help="Post topic or idea")
    parser.add_argument("--type", "-y", default="story", 
        choices=["story", "tips", "contrarian", "question", "listicle"],
        help="Post type/structure")
    parser.add_argument("--tone", "-n", default="casual",
        choices=["professional", "casual", "inspirational", "educational"],
        help="Writing tone")
    parser.add_argument("--cta", "-c", default="comments",
        choices=["comments", "dms", "link", "share"],
        help="Call to action type")
    parser.add_argument("--output", "-o", default=".tmp/linkedin_post.md", help="Output file")
    parser.add_argument("--hooks_only", action="store_true", help="Only generate hook variations")
    parser.add_argument("--count", type=int, default=1, help="Number of posts to generate")
    
    args = parser.parse_args()
    
    print(f"\n📱 LinkedIn Post Generator")
    print(f"   Topic: {args.topic}")
    print(f"   Type: {args.type}")
    print(f"   Tone: {args.tone}\n")
    
    client = get_client()
    
    if args.hooks_only:
        hooks = generate_hook_variations(client, args.topic)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f"# LinkedIn Hook Variations\n\n**Topic:** {args.topic}\n\n{hooks}")
        print(f"✅ Hooks saved to: {output_path}")
        return 0
    
    results = []
    for i in range(args.count):
        if args.count > 1:
            print(f"Generating post {i+1}/{args.count}...")
        result = generate_post(client, args.topic, args.type, args.tone, args.cta)
        results.append(result)
    
    # Format output
    output_content = f"""# LinkedIn Posts: {args.topic}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Type:** {args.type}
**Tone:** {args.tone}

---

"""
    
    for i, result in enumerate(results, 1):
        if args.count > 1:
            output_content += f"## POST {i}\n\n"
        
        output_content += f"""### POST CONTENT

```
{result['post']}
```

### METADATA

{result['metadata']}

---

"""
    
    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_content, encoding="utf-8")
    
    print(f"✅ Generated {args.count} post(s)")
    print(f"   📄 Output: {output_path}")
    
    # Print the post for quick copy
    if args.count == 1:
        print(f"\n--- POST PREVIEW ---\n")
        print(results[0]['post'][:500] + "..." if len(results[0]['post']) > 500 else results[0]['post'])
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
