#!/usr/bin/env python3
"""
Social Media Scheduler - Generate optimal posting schedule.

Usage:
    python3 execution/schedule_social_media.py \
        --platforms "linkedin,twitter,instagram" \
        --posts_per_week 10 \
        --timezone "America/New_York" \
        --output .tmp/posting_schedule.md
"""

import argparse, sys
from datetime import datetime, timedelta
from pathlib import Path

OPTIMAL_TIMES = {
    "linkedin": {
        "best_days": ["Tuesday", "Wednesday", "Thursday"],
        "best_hours": [7, 8, 12, 17, 18],
        "avoid": ["Saturday", "Sunday"]
    },
    "twitter": {
        "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
        "best_hours": [8, 9, 12, 15, 17],
        "avoid": []
    },
    "instagram": {
        "best_days": ["Tuesday", "Wednesday", "Friday"],
        "best_hours": [7, 12, 17, 19, 21],
        "avoid": []
    },
    "facebook": {
        "best_days": ["Wednesday", "Thursday", "Friday"],
        "best_hours": [9, 13, 16],
        "avoid": []
    },
    "tiktok": {
        "best_days": ["Tuesday", "Thursday", "Friday"],
        "best_hours": [7, 12, 15, 19, 21],
        "avoid": []
    }
}

def generate_schedule(platforms, posts_per_week, weeks=4):
    """Generate posting schedule."""
    schedule = []
    start = datetime.now()
    
    for week in range(weeks):
        week_start = start + timedelta(weeks=week)
        week_posts = []
        
        for platform in platforms:
            times = OPTIMAL_TIMES.get(platform, OPTIMAL_TIMES["twitter"])
            posts_for_platform = max(1, posts_per_week // len(platforms))
            
            for i in range(posts_for_platform):
                day_idx = i % len(times["best_days"])
                hour_idx = i % len(times["best_hours"])
                
                day_name = times["best_days"][day_idx]
                hour = times["best_hours"][hour_idx]
                
                # Find the actual date
                days_ahead = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day_name)
                current_weekday = week_start.weekday()
                days_to_add = (days_ahead - current_weekday) % 7
                post_date = week_start + timedelta(days=days_to_add)
                
                week_posts.append({
                    "platform": platform,
                    "date": post_date.strftime("%Y-%m-%d"),
                    "day": day_name,
                    "time": f"{hour:02d}:00",
                    "week": week + 1
                })
        
        schedule.extend(sorted(week_posts, key=lambda x: (x["date"], x["time"])))
    
    return schedule

def main():
    parser = argparse.ArgumentParser(description="Generate social media schedule")
    parser.add_argument("--platforms", "-p", required=True, help="Comma-separated platforms")
    parser.add_argument("--posts_per_week", "-n", type=int, default=10)
    parser.add_argument("--weeks", "-w", type=int, default=4)
    parser.add_argument("--timezone", "-t", default="America/New_York")
    parser.add_argument("--output", "-o", default=".tmp/posting_schedule.md")
    args = parser.parse_args()

    platforms = [p.strip().lower() for p in args.platforms.split(",")]
    print(f"\n📅 Social Media Scheduler\n   Platforms: {platforms}\n   Posts/week: {args.posts_per_week}\n")

    schedule = generate_schedule(platforms, args.posts_per_week, args.weeks)

    # Format output
    output = f"""# Social Media Posting Schedule

**Platforms:** {', '.join(platforms)}
**Posts/Week:** {args.posts_per_week}
**Timezone:** {args.timezone}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

## Optimal Posting Times by Platform

"""
    for p in platforms:
        times = OPTIMAL_TIMES.get(p, {})
        output += f"### {p.title()}\n"
        output += f"- Best days: {', '.join(times.get('best_days', []))}\n"
        output += f"- Best hours: {', '.join([f'{h}:00' for h in times.get('best_hours', [])])}\n\n"

    output += "---\n\n## Weekly Schedule\n\n"
    
    current_week = 0
    for post in schedule:
        if post["week"] != current_week:
            current_week = post["week"]
            output += f"\n### Week {current_week}\n\n| Date | Day | Time | Platform |\n|------|-----|------|----------|\n"
        output += f"| {post['date']} | {post['day']} | {post['time']} | {post['platform'].title()} |\n"

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(output, encoding="utf-8")

    print(f"✅ Schedule created: {len(schedule)} posts over {args.weeks} weeks")
    print(f"   📄 Output: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
