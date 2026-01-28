#!/usr/bin/env python3
"""
YouTube Scriptwriter Workflow

Generates comprehensive YouTube scripts (3000-6000 words) based on:
- Creator's existing content style (YouTube transcripts, social media)
- Deep topic research via Perplexity
- Best practices from skill bibles

Follows directive: directives/youtube_scriptwriter_workflow.md
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
    import requests
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("❌ Error: Required packages not installed")
    print("   Install with: pip install openai requests python-dotenv")
    sys.exit(1)


# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
OUTPUT_DIR = PROJECT_ROOT / ".tmp" / "youtube_scripts"

WORD_COUNT_TARGETS = {
    "short": 3000,
    "medium": 4500,
    "long": 6000
}


# ============================================================================
# API CLIENTS
# ============================================================================

def get_llm_client():
    """Get OpenAI client configured for OpenRouter or OpenAI."""
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
    elif os.getenv("OPENAI_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        print("❌ No LLM API key found (OPENROUTER_API_KEY or OPENAI_API_KEY)")
        sys.exit(1)


def get_model():
    """Get the model to use."""
    if os.getenv("OPENROUTER_API_KEY"):
        return "anthropic/claude-sonnet-4"
    return "gpt-4o"


def call_llm(client, system_prompt: str, user_prompt: str, max_tokens: int = 8000, temperature: float = 0.7) -> str:
    """Call LLM with retry logic."""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=get_model(),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt == 2:
                raise e
            print(f"  Retry {attempt + 1}/3: {e}")
    return ""


def call_perplexity(query: str) -> str:
    """Call Perplexity API for research."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        print("⚠️  PERPLEXITY_API_KEY not configured, skipping research")
        return ""

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": query}],
        "temperature": 0.2,
        "max_tokens": 2000,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"⚠️  Perplexity API error: {response.status_code}")
            return ""
    except Exception as e:
        print(f"⚠️  Perplexity request failed: {e}")
        return ""


# ============================================================================
# CONTENT GATHERING
# ============================================================================

def download_youtube_transcripts(channel_url: str, max_videos: int = 5) -> list[str]:
    """Download transcripts from a YouTube channel using yt-dlp."""
    print(f"📺 Downloading transcripts from {channel_url}...")

    # Create temp directory
    temp_dir = OUTPUT_DIR / "temp_transcripts"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Download auto-generated subtitles
        cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--skip-download",
            "--max-downloads", str(max_videos),
            "-o", str(temp_dir / "%(title)s.%(ext)s"),
            f"{channel_url}/videos"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)

        if result.returncode != 0:
            print(f"⚠️  yt-dlp warning: {result.stderr[:200]}")

        # Parse VTT files
        transcripts = []
        for vtt_file in temp_dir.glob("*.vtt"):
            transcript = parse_vtt_file(vtt_file)
            if transcript:
                transcripts.append({
                    "title": vtt_file.stem.replace(".en", ""),
                    "content": transcript
                })

        print(f"   ✅ Downloaded {len(transcripts)} transcripts")
        return transcripts

    except subprocess.TimeoutExpired:
        print("⚠️  Transcript download timed out")
        return []
    except FileNotFoundError:
        print("⚠️  yt-dlp not found, skipping transcript download")
        return []
    except Exception as e:
        print(f"⚠️  Error downloading transcripts: {e}")
        return []


def parse_vtt_file(vtt_path: Path) -> str:
    """Parse VTT file to clean text."""
    try:
        content = vtt_path.read_text(encoding="utf-8")
        lines = content.split('\n')

        text_lines = []
        seen_text = set()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('WEBVTT'):
                continue
            if line.startswith('Kind:') or line.startswith('Language:'):
                continue
            if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}', line):
                continue
            if re.match(r'^\d+$', line):
                continue
            if '-->' in line:
                continue

            line = re.sub(r'<[^>]+>', '', line)
            line = re.sub(r'\[.*?\]', '', line)
            line = ' '.join(line.split())

            if line and line not in seen_text:
                seen_text.add(line)
                text_lines.append(line)

        return ' '.join(text_lines)
    except Exception as e:
        print(f"⚠️  Error parsing {vtt_path}: {e}")
        return ""


def analyze_creator_style(transcripts: list[dict], client) -> str:
    """Analyze creator's speaking style from transcripts."""
    if not transcripts:
        return ""

    print("🎨 Analyzing creator style...")

    # Combine transcripts (limit to avoid token limits)
    combined = "\n\n---\n\n".join([
        f"Video: {t['title']}\n{t['content'][:3000]}"
        for t in transcripts[:3]
    ])

    system_prompt = """You are an expert content analyst. Analyze the speaking style and patterns."""

    user_prompt = f"""Analyze these YouTube video transcripts and identify:

1. SPEAKING STYLE
- Tone (casual, professional, energetic, calm)
- Vocabulary level (simple, technical, mixed)
- Sentence structure (short punchy, long detailed, varied)

2. COMMON PATTERNS
- How they open videos
- Phrases they repeat
- How they transition between topics
- How they close/CTA

3. CONTENT STRUCTURE
- How they organize information
- Use of stories/examples
- Use of data/proof

4. PERSONALITY TRAITS
- Humor style (if any)
- Teaching approach
- Relationship with audience

TRANSCRIPTS:
{combined}

Provide a concise style guide (300-400 words) that could help someone write content matching this creator's voice."""

    return call_llm(client, system_prompt, user_prompt, max_tokens=1500)


# ============================================================================
# RESEARCH
# ============================================================================

def research_topic(topic: str) -> str:
    """Conduct deep research on the video topic."""
    print(f"🔍 Researching topic: {topic}...")

    queries = [
        f"What are the latest trends and best practices for {topic}? Include specific data and statistics.",
        f"What are the most common questions and misconceptions about {topic}?",
        f"What do experts recommend for {topic}? Include actionable advice.",
    ]

    results = []
    for i, query in enumerate(queries, 1):
        print(f"   Query {i}/3...")
        result = call_perplexity(query)
        if result:
            results.append(result)

    return "\n\n---\n\n".join(results)


def research_creator(creator_name: str) -> str:
    """Research the creator's background and expertise."""
    print(f"🔍 Researching creator: {creator_name}...")

    query = f"""Research {creator_name}. Provide:
- Professional background and expertise
- Business or content focus areas
- Notable achievements or credentials
- Target audience
- Content style and reputation"""

    return call_perplexity(query)


# ============================================================================
# SCRIPT GENERATION
# ============================================================================

def load_skill_bible() -> str:
    """Load the YouTube lead generation skill bible."""
    skill_path = SKILLS_DIR / "SKILL_BIBLE_youtube_lead_generation.md"
    if skill_path.exists():
        content = skill_path.read_text()
        # Extract key sections (limit size for token efficiency)
        return content[:15000]
    return ""


def generate_script(
    client,
    creator: str,
    topic: str,
    video_type: str,
    target_length: str,
    style_guide: str,
    topic_research: str,
    creator_research: str,
    target_audience: str = "",
    call_to_action: str = "",
    key_points: str = ""
) -> str:
    """Generate the full YouTube script."""
    print(f"✍️  Generating script...")

    word_target = WORD_COUNT_TARGETS.get(target_length, 4500)
    skill_bible = load_skill_bible()

    system_prompt = f"""You are an expert YouTube scriptwriter who creates high-converting educational content.
You write scripts that are engaging, well-researched, and follow proven frameworks.

Your scripts always:
- Hook viewers in the first 15 seconds with a clear subject and curiosity
- Start each section with WHY before HOW
- Include stories, examples, and specific data
- Maintain high value-per-minute
- Match the creator's voice and style

SKILL BIBLE REFERENCE:
{skill_bible[:8000]}"""

    user_prompt = f"""Write a comprehensive YouTube script for:

CREATOR: {creator}
VIDEO TOPIC: {topic}
VIDEO TYPE: {video_type}
TARGET LENGTH: {target_length} ({word_target} words)
TARGET AUDIENCE: {target_audience or "Business owners and entrepreneurs"}
CALL TO ACTION: {call_to_action or "Subscribe and comment"}
KEY POINTS TO COVER: {key_points or "Cover the main topic comprehensively"}

CREATOR STYLE GUIDE:
{style_guide or "Professional, educational, engaging"}

TOPIC RESEARCH:
{topic_research[:5000]}

CREATOR BACKGROUND:
{creator_research[:2000]}

SCRIPT REQUIREMENTS:
1. HOOK (150-200 words)
   - Pattern interrupt or bold claim
   - Single subject, single question principle
   - Include [VISUAL HOOK] suggestions

2. OPENING (400-600 words)
   - Establish credibility/proof
   - Promise what they'll learn
   - Preview the content structure

3. BODY SECTIONS (bulk of content)
   - 4-6 main sections
   - Each section starts with WHY
   - Include stories/examples in each section
   - Integrate research naturally
   - Include [B-ROLL] and [VISUAL] suggestions

4. CALL TO ACTION & CLOSE (200-300 words)
   - Recap key points
   - Clear CTA
   - Future pacing

FORMAT:
- Use markdown headers for sections
- Include [DELIVERY NOTES] for emphasis, pauses
- Include [VISUAL] suggestions throughout
- Write in spoken language, not written
- Include estimated timestamps

Write the complete script now. Target {word_target} words."""

    return call_llm(client, system_prompt, user_prompt, max_tokens=12000, temperature=0.7)


# ============================================================================
# DELIVERY
# ============================================================================

def create_google_doc(title: str, content: str) -> dict:
    """Create Google Doc with proper formatting."""
    try:
        # Use centralized formatted doc creator for proper headings/bold/etc
        sys.path.insert(0, str(Path(__file__).parent))
        from create_formatted_google_doc import create_formatted_doc
        return create_formatted_doc(title, content)
    except ImportError:
        # Fallback to basic creator
        try:
            from create_google_doc import create_google_doc as gd_create
            return gd_create(title, content)
        except Exception as e:
            print(f"⚠️  Google Doc creation failed: {e}")
            return {"documentId": None, "documentUrl": None, "status": "failed"}
    except Exception as e:
        print(f"⚠️  Google Doc creation failed: {e}")
        return {"documentId": None, "documentUrl": None, "status": "failed"}


def send_slack_notification(
    creator: str,
    video_title: str,
    video_type: str,
    word_count: int,
    doc_url: str,
    topics: list
) -> bool:
    """Send Slack notification about completed script."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("⚠️  SLACK_WEBHOOK_URL not configured")
        return False

    estimated_minutes = round(word_count / 150)

    message = {
        "text": f"✅ YouTube Script Complete: {video_title}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"✅ YouTube Script Complete"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Creator:* {creator}"},
                    {"type": "mrkdwn", "text": f"*Video Type:* {video_type}"},
                    {"type": "mrkdwn", "text": f"*Word Count:* {word_count:,}"},
                    {"type": "mrkdwn", "text": f"*Est. Length:* ~{estimated_minutes} min"}
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Title:* {video_title}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Key Topics:* {', '.join(topics[:5])}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "📄 View Script"},
                        "url": doc_url or "#",
                        "action_id": "view_script"
                    }
                ]
            } if doc_url else {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "_Script saved locally (Google Doc not available)_"}
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=message, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"⚠️  Slack notification failed: {e}")
        return False


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate YouTube scripts")
    parser.add_argument("--creator", "-c", help="Creator name")
    parser.add_argument("--youtube-channel", "-y", help="YouTube channel URL")
    parser.add_argument("--twitter", help="Twitter/X profile URL")
    parser.add_argument("--linkedin", help="LinkedIn profile URL")
    parser.add_argument("--topic", "-t", help="Video topic/title")
    parser.add_argument("--video-type", choices=["educational", "story", "case-study", "interview"], default="educational")
    parser.add_argument("--target-length", choices=["short", "medium", "long"], default="medium")
    parser.add_argument("--target-audience", help="Target audience description")
    parser.add_argument("--cta", help="Call to action")
    parser.add_argument("--key-points", help="Key points to cover")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Output directory")

    args = parser.parse_args()

    # Interactive mode if missing required args
    if not args.creator:
        args.creator = input("👤 Who is this script for? (Creator name): ").strip()
    if not args.topic:
        args.topic = input("📝 What is the video topic? ").strip()

    if not args.creator or not args.topic:
        print("❌ Creator name and topic are required")
        sys.exit(1)

    # Ask for YouTube channel if not provided
    if not args.youtube_channel:
        yt = input("📺 YouTube channel URL (or press Enter to skip): ").strip()
        if yt:
            args.youtube_channel = yt

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r'[^a-z0-9]+', '_', args.creator.lower())[:20]

    print(f"\n🎬 YouTube Scriptwriter Workflow")
    print(f"   Creator: {args.creator}")
    print(f"   Topic: {args.topic}")
    print(f"   Type: {args.video_type}")
    print(f"   Target: {args.target_length}\n")

    client = get_llm_client()

    # Step 1: Gather content references
    transcripts = []
    style_guide = ""

    if args.youtube_channel:
        transcripts = download_youtube_transcripts(args.youtube_channel, max_videos=5)
        if transcripts:
            style_guide = analyze_creator_style(transcripts, client)

            # Save transcripts for reference
            transcript_file = output_dir / f"{slug}_transcripts_{timestamp}.md"
            with open(transcript_file, "w") as f:
                f.write(f"# Reference Transcripts for {args.creator}\n\n")
                for t in transcripts:
                    f.write(f"## {t['title']}\n\n{t['content'][:2000]}...\n\n---\n\n")
            print(f"   ✅ Saved transcripts: {transcript_file.name}")

    # Step 2: Research topic
    topic_research = research_topic(args.topic)

    # Step 3: Research creator
    creator_research = research_creator(args.creator) if args.creator else ""

    # Save research
    research_file = output_dir / f"{slug}_research_{timestamp}.md"
    with open(research_file, "w") as f:
        f.write(f"# Research: {args.topic}\n\n")
        f.write(f"## Creator: {args.creator}\n\n{creator_research}\n\n")
        f.write(f"## Topic Research\n\n{topic_research}\n\n")
        if style_guide:
            f.write(f"## Style Guide\n\n{style_guide}\n")
    print(f"   ✅ Saved research: {research_file.name}")

    # Step 4: Generate script
    script = generate_script(
        client=client,
        creator=args.creator,
        topic=args.topic,
        video_type=args.video_type,
        target_length=args.target_length,
        style_guide=style_guide,
        topic_research=topic_research,
        creator_research=creator_research,
        target_audience=args.target_audience or "",
        call_to_action=args.cta or "",
        key_points=args.key_points or ""
    )

    # Calculate stats
    word_count = len(script.split())
    estimated_minutes = round(word_count / 150)

    # Save script locally
    script_file = output_dir / f"{slug}_script_{timestamp}.md"
    script_content = f"""# {args.topic}

**Creator:** {args.creator}
**Video Type:** {args.video_type}
**Word Count:** {word_count:,}
**Estimated Length:** ~{estimated_minutes} minutes
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

{script}
"""
    script_file.write_text(script_content)
    print(f"   ✅ Saved script: {script_file.name}")
    print(f"   📊 Word count: {word_count:,} (~{estimated_minutes} min)")

    # Step 5: Create Google Doc
    doc_title = f"{args.creator} - {args.topic[:50]} - Script v1"
    doc_result = create_google_doc(doc_title, script_content)
    doc_url = doc_result.get("documentUrl")

    if doc_url:
        print(f"   ✅ Google Doc: {doc_url}")
    else:
        print(f"   ⚠️  Google Doc creation skipped (saved locally)")

    # Step 6: Send Slack notification
    # Extract key topics from script
    topics = re.findall(r'^##\s+(.+)$', script, re.MULTILINE)[:5]
    if not topics:
        topics = [args.topic]

    slack_sent = send_slack_notification(
        creator=args.creator,
        video_title=args.topic,
        video_type=args.video_type,
        word_count=word_count,
        doc_url=doc_url,
        topics=topics
    )

    if slack_sent:
        print(f"   ✅ Slack notification sent")
    else:
        print(f"   ⚠️  Slack notification skipped")

    # Summary
    print(f"\n✅ Script generation complete!")
    print(f"   📁 Output: {output_dir}")
    print(f"   📄 Script: {script_file.name}")
    if doc_url:
        print(f"   🔗 Google Doc: {doc_url}")

    return {
        "creator": args.creator,
        "topic": args.topic,
        "video_type": args.video_type,
        "word_count": word_count,
        "estimated_length": f"{estimated_minutes} minutes",
        "script_file": str(script_file),
        "research_file": str(research_file),
        "google_doc_url": doc_url,
        "topics": topics
    }


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
