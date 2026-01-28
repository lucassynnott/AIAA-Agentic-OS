#!/usr/bin/env python3
"""
Ultimate Content Calendar Generator

Generates 30-90 days of content across all platforms with
hooks, captions, hashtags, and repurposing strategies.

Usage:
    python3 execution/generate_content_calendar.py \
        --client "Acme Corp" \
        --industry "B2B SaaS" \
        --platforms "linkedin,twitter,instagram" \
        --days 30

Follows directive: directives/ultimate_content_calendar.md
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import requests
except ImportError:
    print("Error: requests required. pip install requests")
    sys.exit(1)


class ContentCalendarGenerator:
    """Generate complete content calendars with AI"""

    POSTING_TIMES = {
        "linkedin": ["07:00", "12:00", "17:00"],
        "twitter": ["08:00", "12:00", "16:00"],
        "instagram": ["11:00", "14:00", "19:00"],
        "youtube": ["14:00", "16:00"],
        "tiktok": ["07:00", "12:00", "19:00"]
    }

    BEST_DAYS = {
        "linkedin": ["Tuesday", "Wednesday", "Thursday"],
        "twitter": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "instagram": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "youtube": ["Thursday", "Friday", "Saturday"],
        "tiktok": ["Tuesday", "Thursday", "Saturday"]
    }

    def __init__(self, **kwargs):
        self.client = kwargs.get("client", "")
        self.industry = kwargs.get("industry", "")
        self.platforms = kwargs.get("platforms", ["linkedin", "twitter"])
        self.content_pillars = kwargs.get("content_pillars", [])
        self.posts_per_week = kwargs.get("posts_per_week", 5)
        self.days = kwargs.get("days", 30)
        self.brand_voice = kwargs.get("brand_voice", "professional yet approachable")

        # Generate calendar slug
        client_slug = re.sub(r'[^a-zA-Z0-9]', '_', self.client.lower())
        timestamp = datetime.now().strftime('%Y%m%d')

        # Setup output directory
        self.output_dir = Path(f".tmp/content_calendars/{client_slug}_{timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for subdir in ["research", "strategy", "calendar", "content"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)
        for platform in self.platforms:
            (self.output_dir / "content" / platform).mkdir(exist_ok=True)

        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

    def call_claude(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        if not self.openrouter_key:
            return None

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-sonnet-4",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "max_tokens": max_tokens
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            return None
        except Exception as e:
            self.log(f"Error: {e}", "ERROR")
            return None

    def generate_content_pillars(self) -> List[Dict]:
        """Generate content pillars if not provided"""
        if self.content_pillars:
            return [{"name": p, "percentage": 100 // len(self.content_pillars)} for p in self.content_pillars]

        self.log("Generating content pillars...", "INFO")

        prompt = f"""You are a content strategist. Create content pillars for a {self.industry} brand called {self.client}.

Return JSON format:
{{
    "pillars": [
        {{
            "name": "Pillar name",
            "description": "What this pillar covers",
            "percentage": 40,
            "content_types": ["Type 1", "Type 2"],
            "example_topics": ["Topic 1", "Topic 2", "Topic 3"]
        }}
    ]
}}

Create 4-5 pillars that cover:
1. Educational content (largest %)
2. Social proof/case studies
3. Behind the scenes/culture
4. Engagement/community
5. Promotional (smallest %)

Percentages must total 100. Return ONLY valid JSON."""

        result = self.call_claude(prompt)

        if result:
            try:
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    data = json.loads(json_match.group())
                    pillars = data.get("pillars", [])
                    self.log(f"Generated {len(pillars)} content pillars", "SUCCESS")
                    return pillars
            except json.JSONDecodeError:
                pass

        # Fallback pillars
        return [
            {"name": "Educational", "percentage": 40, "description": "Tips, tutorials, how-tos"},
            {"name": "Social Proof", "percentage": 25, "description": "Case studies, testimonials"},
            {"name": "Behind the Scenes", "percentage": 20, "description": "Team, culture, process"},
            {"name": "Engagement", "percentage": 15, "description": "Questions, polls, trends"}
        ]

    def generate_content_ideas(self, pillars: List[Dict], platform: str, count: int) -> List[Dict]:
        """Generate content ideas for a specific platform"""
        self.log(f"Generating {count} content ideas for {platform}...", "INFO")

        platform_guidelines = {
            "linkedin": "Long-form posts (1300+ chars), professional storytelling, industry insights, carousels",
            "twitter": "Short tweets, threads (5-10 tweets), witty observations, engagement prompts",
            "instagram": "Visual-first, carousel posts, Reels scripts, Stories, lifestyle content",
            "youtube": "Video scripts, educational content, tutorials, vlogs",
            "tiktok": "Trend-based, hooks in first 2 seconds, casual, entertaining"
        }

        prompt = f"""Generate {count} content ideas for {platform}.

CLIENT: {self.client}
INDUSTRY: {self.industry}
BRAND VOICE: {self.brand_voice}
PLATFORM STYLE: {platform_guidelines.get(platform, 'General social media')}

CONTENT PILLARS:
{json.dumps(pillars, indent=2)}

Return JSON format:
{{
    "content_ideas": [
        {{
            "id": 1,
            "pillar": "Pillar name",
            "content_type": "Post type (carousel/thread/reel/etc)",
            "topic": "Content topic",
            "hook": "Opening hook/first line",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "cta": "Call to action",
            "hashtags": ["hashtag1", "hashtag2"],
            "estimated_engagement": "high/medium/low"
        }}
    ]
}}

Make content diverse across pillars and content types. Return ONLY valid JSON."""

        result = self.call_claude(prompt, max_tokens=6000)

        if result:
            try:
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    data = json.loads(json_match.group())
                    ideas = data.get("content_ideas", [])
                    self.log(f"Generated {len(ideas)} ideas for {platform}", "SUCCESS")
                    return ideas
            except json.JSONDecodeError:
                pass

        # Fallback ideas
        return [
            {
                "id": i + 1,
                "pillar": pillars[i % len(pillars)]["name"],
                "content_type": "Post",
                "topic": f"Topic {i + 1} for {self.industry}",
                "hook": f"Hook for topic {i + 1}",
                "key_points": ["Point 1", "Point 2"],
                "cta": "Follow for more",
                "hashtags": [self.industry.lower().replace(" ", "")],
                "estimated_engagement": "medium"
            }
            for i in range(count)
        ]

    def generate_full_content(self, idea: Dict, platform: str) -> str:
        """Generate full content for a single idea"""
        prompt = f"""Write the full content for this {platform} post.

IDEA: {json.dumps(idea, indent=2)}
CLIENT: {self.client}
BRAND VOICE: {self.brand_voice}

PLATFORM FORMATTING:
- LinkedIn: Use line breaks, bullet points (→), professional tone
- Twitter: Thread format if multiple points, use 1/, 2/, numbering
- Instagram: Caption format, use line breaks, emojis sparingly, hashtags at end

Write the complete, ready-to-post content. Include all hashtags at the end."""

        result = self.call_claude(prompt, max_tokens=1500)
        return result or idea.get("hook", "")

    def create_calendar_schedule(self, ideas_by_platform: Dict) -> List[Dict]:
        """Create the posting schedule"""
        self.log("Creating posting schedule...", "INFO")

        schedule = []
        start_date = datetime.now() + timedelta(days=1)  # Start tomorrow

        post_id = 1
        for day_offset in range(self.days):
            current_date = start_date + timedelta(days=day_offset)
            day_name = current_date.strftime("%A")

            for platform in self.platforms:
                best_days = self.BEST_DAYS.get(platform, ["Monday", "Wednesday", "Friday"])
                posting_times = self.POSTING_TIMES.get(platform, ["12:00"])

                if day_name in best_days and ideas_by_platform.get(platform):
                    # Get next idea for this platform
                    idea = ideas_by_platform[platform].pop(0)
                    ideas_by_platform[platform].append(idea)  # Cycle back

                    schedule.append({
                        "id": post_id,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "day": day_name,
                        "time": posting_times[0],
                        "platform": platform,
                        "pillar": idea.get("pillar", ""),
                        "content_type": idea.get("content_type", ""),
                        "topic": idea.get("topic", ""),
                        "hook": idea.get("hook", ""),
                        "status": "scheduled"
                    })
                    post_id += 1

        return schedule

    def save_calendar_csv(self, schedule: List[Dict]) -> Path:
        """Save calendar as CSV"""
        csv_path = self.output_dir / "calendar" / "master_calendar.csv"

        if schedule:
            with open(csv_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=schedule[0].keys())
                writer.writeheader()
                writer.writerows(schedule)

        return csv_path

    def save_content_files(self, ideas_by_platform: Dict):
        """Save individual content files"""
        for platform, ideas in ideas_by_platform.items():
            platform_dir = self.output_dir / "content" / platform

            for i, idea in enumerate(ideas[:20], 1):  # Limit to 20 per platform
                content = f"""# {idea.get('topic', 'Untitled')}

**Platform:** {platform.title()}
**Pillar:** {idea.get('pillar', '')}
**Content Type:** {idea.get('content_type', '')}

---

## Hook
{idea.get('hook', '')}

## Key Points
"""
                for point in idea.get('key_points', []):
                    content += f"- {point}\n"

                content += f"""
## CTA
{idea.get('cta', '')}

## Hashtags
{' '.join(['#' + h for h in idea.get('hashtags', [])])}

---

## Full Content (Draft)
[Generate using generate_full_content or write manually]

---

## Status
- [ ] Content written
- [ ] Visuals created
- [ ] Scheduled
- [ ] Posted
"""

                file_path = platform_dir / f"{i:02d}_{idea.get('topic', 'post')[:30].replace(' ', '_')}.md"
                file_path.write_text(content, encoding="utf-8")

    def execute(self) -> Dict:
        """Execute complete calendar generation"""
        self.log(f"🚀 Starting Content Calendar Generation", "INFO")
        self.log(f"   Client: {self.client}", "INFO")
        self.log(f"   Platforms: {', '.join(self.platforms)}", "INFO")
        self.log(f"   Duration: {self.days} days", "INFO")

        start_time = time.time()

        # Generate content pillars
        pillars = self.generate_content_pillars()

        # Save pillars
        pillars_path = self.output_dir / "strategy" / "content_pillars.json"
        with open(pillars_path, 'w') as f:
            json.dump(pillars, f, indent=2)

        # Calculate content needed per platform
        posts_needed = (self.days // 7) * self.posts_per_week

        # Generate ideas for each platform
        ideas_by_platform = {}
        total_ideas = 0

        for platform in self.platforms:
            ideas = self.generate_content_ideas(pillars, platform, posts_needed)
            ideas_by_platform[platform] = ideas
            total_ideas += len(ideas)

            # Save platform-specific ideas
            ideas_path = self.output_dir / "content" / platform / "ideas.json"
            with open(ideas_path, 'w') as f:
                json.dump(ideas, f, indent=2)

        # Create posting schedule
        schedule = self.create_calendar_schedule(ideas_by_platform.copy())

        # Save calendar
        csv_path = self.save_calendar_csv(schedule)

        # Save individual content files
        self.save_content_files(ideas_by_platform)

        # Generate strategy summary
        strategy_md = f"""# Content Strategy: {self.client}

**Industry:** {self.industry}
**Platforms:** {', '.join([p.title() for p in self.platforms])}
**Duration:** {self.days} days
**Posts per Week:** {self.posts_per_week}
**Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Content Pillars

"""
        for pillar in pillars:
            strategy_md += f"""### {pillar.get('name', 'Pillar')} ({pillar.get('percentage', 0)}%)
{pillar.get('description', '')}

"""

        strategy_md += f"""---

## Posting Schedule

| Platform | Best Days | Best Times |
|----------|-----------|------------|
"""
        for platform in self.platforms:
            days = ', '.join(self.BEST_DAYS.get(platform, [])[:3])
            times = ', '.join(self.POSTING_TIMES.get(platform, []))
            strategy_md += f"| {platform.title()} | {days} | {times} |\n"

        strategy_md += f"""
---

## Content Summary

- **Total Posts Planned:** {len(schedule)}
- **Content Ideas Generated:** {total_ideas}
- **Platforms Covered:** {len(self.platforms)}

---

## Next Steps

1. Review content ideas and select best ones
2. Create visual assets for each post
3. Write full captions/scripts
4. Schedule in social media tool
5. Monitor engagement and adjust
"""

        strategy_path = self.output_dir / "strategy" / "content_strategy.md"
        strategy_path.write_text(strategy_md, encoding="utf-8")

        execution_time = time.time() - start_time

        result = {
            "success": True,
            "client": self.client,
            "platforms": self.platforms,
            "days": self.days,
            "posts_scheduled": len(schedule),
            "ideas_generated": total_ideas,
            "execution_time": f"{int(execution_time)}s",
            "output_dir": str(self.output_dir),
            "files": {
                "strategy": str(strategy_path),
                "calendar": str(csv_path),
                "pillars": str(pillars_path),
                "content": str(self.output_dir / "content")
            }
        }

        result_path = self.output_dir / "result.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, indent=2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ CONTENT CALENDAR GENERATED", "SUCCESS")
        self.log(f"   Posts: {len(schedule)}", "INFO")
        self.log(f"   Ideas: {total_ideas}", "INFO")
        self.log(f"   Output: {self.output_dir}", "INFO")
        self.log("=" * 50, "INFO")

        return result


def main():
    parser = argparse.ArgumentParser(description="Generate content calendars")

    parser.add_argument("--client", required=True, help="Client/brand name")
    parser.add_argument("--industry", required=True, help="Industry/niche")
    parser.add_argument("--platforms", default="linkedin,twitter",
                       help="Comma-separated platforms")
    parser.add_argument("--content-pillars", help="Comma-separated content pillars")
    parser.add_argument("--posts-per-week", type=int, default=5)
    parser.add_argument("--days", type=int, default=30, choices=[30, 60, 90])
    parser.add_argument("--brand-voice", default="professional yet approachable")

    args = parser.parse_args()

    platforms = [p.strip().lower() for p in args.platforms.split(",")]
    pillars = [p.strip() for p in args.content_pillars.split(",")] if args.content_pillars else []

    generator = ContentCalendarGenerator(
        client=args.client,
        industry=args.industry,
        platforms=platforms,
        content_pillars=pillars,
        posts_per_week=args.posts_per_week,
        days=args.days,
        brand_voice=args.brand_voice
    )

    result = generator.execute()
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
