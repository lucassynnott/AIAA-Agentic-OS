#!/usr/bin/env python3
"""
Landing Page CRO Analyzer - Analyze landing pages for conversion rate optimization
opportunities using AI, providing actionable recommendations.

Usage:
    python3 execution/analyze_landing_page.py \
        --url "https://example.com/landing-page" \
        --client "Client Name" \
        --funnel_type "VSL" \
        --industry "SaaS" \
        --output_dir ".tmp/cro_analysis"
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests package not installed. Run: pip install requests")
    sys.exit(1)

from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY or OPENAI_API_KEY required in .env")
    sys.exit(1)


def get_client() -> OpenAI:
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"


def load_landing_page_skill_bible() -> str:
    """Load landing page skill bible for enhanced CRO analysis context."""
    skill_path = Path(__file__).parent.parent / "skills" / "SKILL_BIBLE_landing_page_ai_mastery.md"
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        # Extract key sections for context
        sections = []
        for section in ["## Best Practices", "## Common Mistakes", "## Quick Reference Checklist"]:
            if section in content:
                start = content.find(section)
                next_section = content.find("\n## ", start + len(section))
                if next_section > start:
                    sections.append(content[start:next_section])
                else:
                    sections.append(content[start:start + 2000])
        return "\n".join(sections)[:4000]
    return ""


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


def fetch_page_content(url: str) -> str:
    """Fetch landing page and convert to readable text."""
    print(f"🌐 Fetching: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html = response.text
        
        # Basic HTML to text conversion
        # Remove scripts and styles
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Unknown"
        
        # Extract meta description
        meta_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
        meta_desc = meta_match.group(1) if meta_match else ""
        
        # Extract headings
        headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.IGNORECASE | re.DOTALL)
        headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]
        
        # Extract button text
        buttons = re.findall(r'<button[^>]*>(.*?)</button>', html, re.IGNORECASE | re.DOTALL)
        buttons += re.findall(r'<a[^>]*class=["\'][^"\']*(?:btn|button|cta)[^"\']*["\'][^>]*>(.*?)</a>', html, re.IGNORECASE | re.DOTALL)
        buttons = [re.sub(r'<[^>]+>', '', b).strip() for b in buttons if b.strip()]
        
        # Extract main text content
        # Remove all tags
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Build content summary
        content = f"""PAGE TITLE: {title}

META DESCRIPTION: {meta_desc}

HEADINGS:
{chr(10).join(['- ' + h for h in headings[:20] if h])}

BUTTON/CTA TEXT:
{chr(10).join(['- ' + b for b in buttons[:10] if b])}

PAGE CONTENT (first 5000 chars):
{text[:5000]}
"""
        return content
        
    except Exception as e:
        return f"Error fetching page: {e}"


def analyze_cro(client: OpenAI, page_content: str, config: dict) -> str:
    """Analyze landing page for CRO opportunities."""
    print("🔍 Analyzing for CRO opportunities...")

    # Load skill bible for enhanced context
    skill_context = load_landing_page_skill_bible()

    skill_section = ""
    if skill_context:
        skill_section = f"""

APPLY THESE EXPERT CRO PRINCIPLES IN YOUR ANALYSIS:
{skill_context[:3000]}
"""

    system_prompt = f"""You are a CRO expert who has optimized hundreds of landing pages. Provide specific, actionable recommendations backed by conversion data.
{skill_section}"""
    
    user_prompt = f"""Analyze this landing page for conversion rate optimization:

CLIENT: {config.get('client', 'Unknown')}
URL: {config['url']}
FUNNEL TYPE: {config.get('funnel_type', 'Unknown')}
INDUSTRY: {config.get('industry', 'Unknown')}
CURRENT METRICS: {config.get('metrics', 'Not provided')}

PAGE CONTENT:
{page_content}

PROVIDE COMPREHENSIVE CRO ANALYSIS:

## 1. OVERALL SCORE
- Give a score out of 100
- Top 3 strengths
- Top 3 weaknesses

## 2. ABOVE THE FOLD ANALYSIS
- Headline evaluation
- Subheadline effectiveness
- First impression assessment
- Visual hierarchy

## 3. COPY ANALYSIS
- Headline strength (1-10)
- Benefit clarity (1-10)
- Emotional triggers present
- Objection handling
- Social proof usage
- CTA strength

## 4. TRUST ELEMENTS
- Testimonials quality
- Social proof effectiveness
- Authority indicators
- Guarantee visibility

## 5. CONVERSION FRICTION POINTS
- Form complexity
- Unclear CTAs
- Missing information
- Confusing navigation

## 6. PRIORITY RECOMMENDATIONS

### HIGH IMPACT (Do First):
1. [Specific recommendation with expected impact]
2. [Specific recommendation]
3. [Specific recommendation]

### MEDIUM IMPACT:
1. [Recommendation]
2. [Recommendation]

### LOW-HANGING FRUIT (Quick Wins):
1. [Easy fix]
2. [Easy fix]

## 7. HEADLINE REWRITES
Provide 3 improved headline options

## 8. CTA REWRITES  
Provide 3 improved CTA options

## 9. A/B TEST RECOMMENDATIONS
- Test 1: [What to test and hypothesis]
- Test 2: [What to test and hypothesis]
- Test 3: [What to test and hypothesis]

Be specific with copy examples and expected improvements."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.6)


def analyze_copy_deep(client: OpenAI, page_content: str, config: dict) -> str:
    """Deep copy analysis."""
    print("📝 Deep copy analysis...")
    
    system_prompt = """You are a direct response copywriter. Analyze copy for persuasion effectiveness."""
    
    user_prompt = f"""Perform deep copy analysis on this landing page:

PAGE CONTENT:
{page_content[:4000]}

FUNNEL TYPE: {config.get('funnel_type', 'Unknown')}

ANALYZE:

## 1. PERSUASION FRAMEWORK CHECK
- [ ] Attention (headline hooks)
- [ ] Interest (curiosity builders)
- [ ] Desire (benefit stacking)
- [ ] Action (clear CTAs)

## 2. EMOTIONAL TRIGGERS
List which are present and which are missing:
- Fear/Loss aversion
- Greed/Desire
- Social proof
- Authority
- Scarcity
- Urgency
- Curiosity

## 3. SPECIFICITY ANALYSIS
- Are claims specific or vague?
- Numbers and statistics used?
- Concrete examples?

## 4. OBJECTION HANDLING
- What objections are addressed?
- What objections are missing?
- How can objections be better handled?

## 5. VOICE OF CUSTOMER
- Does copy use customer language?
- Pain points addressed authentically?
- Transformation clearly painted?

## 6. REWRITTEN SECTIONS
Rewrite the weakest sections with improved copy."""

    return call_llm(client, system_prompt, user_prompt, temperature=0.7)


def save_output(output_dir: Path, filename: str, content: str) -> str:
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Analyze landing page for CRO")
    parser.add_argument("--url", required=True, help="Landing page URL to analyze")
    parser.add_argument("--client", default="", help="Client name")
    parser.add_argument("--funnel_type", default="", help="Type of funnel (VSL, Webinar, etc.)")
    parser.add_argument("--industry", default="", help="Industry/niche")
    parser.add_argument("--metrics", default="", help="Current funnel metrics")
    parser.add_argument("--output_dir", default=".tmp/cro_analysis", help="Output directory")
    parser.add_argument("--deep", action="store_true", help="Include deep copy analysis")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    config = {
        "url": args.url,
        "client": args.client or "Unknown",
        "funnel_type": args.funnel_type or "Unknown",
        "industry": args.industry or "Unknown",
        "metrics": args.metrics
    }
    
    print(f"\n🎯 Landing Page CRO Analyzer")
    print(f"   URL: {config['url']}")
    print(f"   Client: {config['client']}")
    print(f"   Output: {output_dir}\n")
    
    # Fetch page
    page_content = fetch_page_content(config['url'])
    if page_content.startswith("Error"):
        print(f"   ❌ {page_content}")
        return 1
    print(f"   ✅ Page fetched successfully")
    
    client = get_client()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save raw content
    raw_file = save_output(output_dir, f"00_page_content_{timestamp}.txt", page_content)
    print(f"   ✅ Saved: {raw_file}")
    
    # CRO Analysis
    cro_analysis = analyze_cro(client, page_content, config)
    cro_file = save_output(output_dir, f"01_cro_analysis_{timestamp}.md",
        f"# CRO Analysis: {config['client']}\n\n**URL:** {config['url']}\n**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n{cro_analysis}")
    print(f"   ✅ Saved: {cro_file}")
    
    # Deep copy analysis (optional)
    if args.deep:
        copy_analysis = analyze_copy_deep(client, page_content, config)
        copy_file = save_output(output_dir, f"02_copy_analysis_{timestamp}.md",
            f"# Deep Copy Analysis: {config['client']}\n\n{copy_analysis}")
        print(f"   ✅ Saved: {copy_file}")
    
    print(f"\n✅ CRO analysis complete!")
    print(f"   📁 Output: {output_dir}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
