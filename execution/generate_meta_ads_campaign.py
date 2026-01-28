#!/usr/bin/env python3
"""
Ultimate Meta Ads Campaign Generator

Generates complete Meta/Facebook/Instagram ad campaigns with
copy, creative briefs, targeting, and campaign structure.

Usage:
    python3 execution/generate_meta_ads_campaign.py \
        --client "Acme SaaS" \
        --product "Project Management Tool" \
        --offer "14-day free trial" \
        --target-audience "Small business owners"

Follows directive: directives/ultimate_meta_ads_campaign.md
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

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

try:
    from PIL import Image, ImageDraw, ImageFont
    import io
    import base64
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class MetaAdsCampaignGenerator:
    """Generate complete Meta ads campaigns with AI"""

    def __init__(self, **kwargs):
        self.client = kwargs.get("client", "")
        self.product = kwargs.get("product", "")
        self.offer = kwargs.get("offer", "")
        self.target_audience = kwargs.get("target_audience", "")
        self.monthly_budget = kwargs.get("monthly_budget", 5000)
        self.objective = kwargs.get("objective", "conversions")
        self.funnel_stage = kwargs.get("funnel_stage", "cold")
        self.competitors = kwargs.get("competitors", [])
        self.variations = kwargs.get("variations", 5)

        # Generate campaign slug
        client_slug = re.sub(r'[^a-zA-Z0-9]', '_', self.client.lower())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Setup output directory
        self.output_dir = Path(f".tmp/meta_ads_campaigns/{client_slug}_{timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for subdir in ["research", "audiences", "creatives", "campaign_structure", "optimization"]:
            (self.output_dir / subdir).mkdir(exist_ok=True)

        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.fal_key = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY")
        self.generate_images = kwargs.get("generate_images", False)

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
                    "temperature": 0.7,
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

    def generate_image_nano_banana(self, prompt: str, ad_number: int) -> Optional[str]:
        """Generate ad creative using Nano Banana Pro via fal.ai"""
        if not self.fal_key:
            self.log("FAL_KEY/FAL_API_KEY not set, skipping image generation", "WARNING")
            return None
        
        try:
            response = requests.post(
                "https://fal.run/fal-ai/nano-banana-pro",
                headers={
                    "Authorization": f"Key {self.fal_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "aspect_ratio": "1:1",
                    "resolution": "2K"
                },
                timeout=180
            )
            
            if response.status_code == 200:
                result = response.json()
                # fal.ai returns images array with url
                images = result.get("images", [])
                if images:
                    image_url = images[0].get("url")
                    if image_url:
                        # Download image
                        img_response = requests.get(image_url, timeout=60)
                        if img_response.status_code == 200:
                            img_path = self.output_dir / "creatives" / f"ad_{ad_number}_creative.png"
                            with open(img_path, 'wb') as f:
                                f.write(img_response.content)
                            return str(img_path)
            else:
                self.log(f"fal.ai error: {response.status_code} - {response.text[:200]}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Image generation error: {e}", "ERROR")
            return None

    def build_image_prompt(self, ad: Dict) -> str:
        """Build structured image generation prompt with text positioning"""
        angle = ad.get("ad_angle", "Hook-focused")
        headline = ad.get("headlines", [""])[0] if ad.get("headlines") else ""
        primary_text = ad.get("primary_text", "")[:80]  # Shorter for image
        cta = ad.get("cta_button", "Learn More")
        creative_direction = ad.get("creative_direction", "")
        
        # Structured prompt with text positioning based on ad angle
        prompt_templates = {
            "Hook-focused": f"""<ad_creative>
<style>Professional social media advertisement, 1:1 square format, bold modern design</style>
<background>Dark gradient background (#1a1a2e to #16213e), subtle geometric patterns</background>

<text_elements>
  <headline position="top-center" size="large" color="white" font="bold sans-serif">
    {headline}
  </headline>
  <subtext position="center" size="medium" color="#e0e0e0">
    {primary_text}
  </subtext>
  <cta position="bottom-center" size="medium" color="white" background="#ff6b35" shape="rounded-button">
    {cta}
  </cta>
</text_elements>

<visual_elements>
  <main_visual position="center-right">Confident professional person or abstract success imagery</main_visual>
  <accent>Orange/coral highlight accents, subtle glow effects</accent>
</visual_elements>

<requirements>
- Text must be crisp, readable, and spelled correctly
- High contrast between text and background
- Professional advertising quality
- {creative_direction}
</requirements>
</ad_creative>""",

            "Problem-focused": f"""<ad_creative>
<style>Split comparison advertisement, 1:1 square format, before/after layout</style>
<layout>Vertical split - left side dark/negative, right side bright/positive</layout>

<left_side background="#2d2d2d">
  <label position="top-left" color="#ff4444" size="small">THE PROBLEM</label>
  <visual>Stressed, frustrated person or chaotic imagery</visual>
</left_side>

<right_side background="#f8f9fa">
  <label position="top-right" color="#22c55e" size="small">THE SOLUTION</label>
  <visual>Happy, successful person or organized imagery</visual>
</right_side>

<text_elements>
  <headline position="top-center-spanning-both-sides" size="large" color="white" background="rgba(0,0,0,0.8)">
    {headline}
  </headline>
  <cta position="bottom-center" size="medium" color="white" background="#ff6b35" shape="pill-button">
    {cta}
  </cta>
</text_elements>

<requirements>
- Clear visual contrast between problem and solution sides
- Text must be spelled correctly and highly readable
- {creative_direction}
</requirements>
</ad_creative>""",

            "Solution-focused": f"""<ad_creative>
<style>Premium product showcase, 1:1 square format, clean minimalist design</style>
<background>Soft gradient (#667eea to #764ba2), clean and professional</background>

<text_elements>
  <headline position="top-center" size="extra-large" color="white" font="bold">
    {headline}
  </headline>
  <body_text position="upper-center" size="medium" color="rgba(255,255,255,0.9)">
    {primary_text}
  </body_text>
  <cta position="bottom-center" size="large" color="white" background="#22c55e" shape="rounded-rectangle">
    {cta}
  </cta>
</text_elements>

<visual_elements>
  <product_visual position="center">Abstract representation of growth, success, or transformation</product_visual>
  <decorative>Subtle floating elements, light particles, premium feel</decorative>
</visual_elements>

<requirements>
- Headline must be the dominant text element
- Clean, uncluttered layout
- Text perfectly legible
- {creative_direction}
</requirements>
</ad_creative>""",

            "Social Proof": f"""<ad_creative>
<style>Testimonial advertisement, 1:1 square format, trust-building design</style>
<background>Warm neutral gradient (#fef9f3 to #f5e6d3)</background>

<text_elements>
  <quote_marks position="top-left" size="large" color="#ff6b35">"</quote_marks>
  <testimonial_text position="center" size="medium" color="#1a1a1a" font="serif-italic">
    {primary_text}
  </testimonial_text>
  <headline position="upper-center" size="large" color="#1a1a1a" font="bold">
    {headline}
  </headline>
  <cta position="bottom-center" size="medium" color="white" background="#1a1a1a" shape="pill">
    {cta}
  </cta>
</text_elements>

<visual_elements>
  <testimonial_photo position="bottom-left" shape="circle">Professional headshot placeholder</testimonial_photo>
  <stars position="below-headline" color="#fbbf24">5 gold stars rating</stars>
</visual_elements>

<requirements>
- Warm, trustworthy aesthetic
- Text must be perfectly spelled and readable
- Authentic, not stock-photo feeling
- {creative_direction}
</requirements>
</ad_creative>""",

            "FOMO/Urgency": f"""<ad_creative>
<style>Urgency/scarcity advertisement, 1:1 square format, high-energy design</style>
<background>Bold red-to-orange gradient (#dc2626 to #ea580c), energetic</background>

<text_elements>
  <urgency_badge position="top-center" size="small" color="#1a1a1a" background="#fbbf24" shape="banner">
    LIMITED TIME OFFER
  </urgency_badge>
  <headline position="center-top" size="extra-large" color="white" font="extra-bold">
    {headline}
  </headline>
  <subtext position="center" size="medium" color="rgba(255,255,255,0.95)">
    {primary_text}
  </subtext>
  <cta position="bottom-center" size="large" color="#dc2626" background="white" shape="rounded-rectangle">
    {cta}
  </cta>
</text_elements>

<visual_elements>
  <timer_visual position="above-cta">Countdown timer graphic or "ENDING SOON" badge</timer_visual>
  <energy_elements>Dynamic lines, sparkles, or motion blur effects</energy_elements>
</visual_elements>

<requirements>
- High energy, creates urgency
- Text must be bold and impossible to miss
- Perfectly spelled, highly readable
- {creative_direction}
</requirements>
</ad_creative>"""
        }
        
        return prompt_templates.get(angle, prompt_templates["Hook-focused"])

    def generate_ad_creatives(self, ad_data: Dict) -> Dict:
        """Generate actual ad creative images for each ad variation"""
        if not self.generate_images:
            return {}
        
        self.log("Generating ad creative images...", "INFO")
        
        generated_images = {}
        ads = ad_data.get("ads", [])
        
        for ad in ads:
            ad_num = ad.get("ad_number", 1)
            self.log(f"  Generating creative for Ad {ad_num}: {ad.get('ad_angle', 'Unknown')}...", "INFO")
            
            # Build optimized prompt
            prompt = self.build_image_prompt(ad)
            
            # Generate with Google's Nano Banana via fal.ai
            img_path = self.generate_image_nano_banana(prompt, ad_num)
            
            if img_path:
                generated_images[ad_num] = {
                    "path": img_path,
                    "prompt": prompt,
                    "model": "nano-banana-pro",
                    "angle": ad.get("ad_angle", "")
                }
                self.log(f"  ✓ Ad {ad_num} creative saved", "SUCCESS")
            else:
                self.log(f"  ✗ Ad {ad_num} creative failed", "WARNING")
        
        # Save image generation manifest
        if generated_images:
            manifest_path = self.output_dir / "creatives" / "image_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(generated_images, f, indent=2)
            self.log(f"Generated {len(generated_images)}/{len(ads)} ad creatives", "SUCCESS")
        
        return generated_images

    def generate_ad_copy(self) -> Dict:
        """Generate ad copy variations"""
        self.log("Generating ad copy variations...", "INFO")

        prompt = f"""You are an expert Meta ads copywriter. Generate ad copy for a {self.funnel_stage} traffic campaign.

CLIENT: {self.client}
PRODUCT: {self.product}
OFFER: {self.offer}
TARGET AUDIENCE: {self.target_audience}
OBJECTIVE: {self.objective}
BUDGET: ${self.monthly_budget}/month

Generate {self.variations} complete ad variations in JSON format:
{{
    "ads": [
        {{
            "ad_number": 1,
            "ad_angle": "Hook-focused",
            "primary_text": "125 characters max - main body copy",
            "primary_text_extended": "Optional longer version (500 chars)",
            "headlines": ["Headline 1 (40 chars)", "Headline 2", "Headline 3"],
            "descriptions": ["Description 1 (30 chars)", "Description 2"],
            "cta_button": "Learn More",
            "creative_direction": "What image/video should show"
        }}
    ],
    "targeting_recommendations": {{
        "interests": ["interest 1", "interest 2"],
        "behaviors": ["behavior 1"],
        "demographics": "description",
        "lookalike_sources": ["source 1", "source 2"],
        "exclusions": ["what to exclude"]
    }},
    "campaign_structure": {{
        "campaign_name": "Campaign name",
        "ad_sets": [
            {{
                "name": "Ad Set Name",
                "audience_type": "cold/warm/hot",
                "budget_percentage": 40,
                "ads_to_include": [1, 2]
            }}
        ]
    }}
}}

AD ANGLES TO COVER:
1. Hook/Pattern Interrupt - Grab attention
2. Problem-focused - Agitate pain point
3. Solution-focused - Show the outcome
4. Social Proof - Testimonial/results
5. FOMO/Urgency - Scarcity or time-limit

RULES:
- Primary text under 125 chars for mobile
- Headlines under 40 characters
- Strong hooks in first line
- Clear value proposition
- Emotional triggers
- Specific numbers when possible

Return ONLY valid JSON."""

        result = self.call_claude(prompt)

        if result:
            try:
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    ad_data = json.loads(json_match.group())
                    self.log(f"Generated {len(ad_data.get('ads', []))} ad variations", "SUCCESS")
                    return ad_data
            except json.JSONDecodeError:
                pass

        return self._get_fallback_ads()

    def _get_fallback_ads(self) -> Dict:
        """Return fallback ad structure"""
        return {
            "ads": [
                {
                    "ad_number": 1,
                    "ad_angle": "Hook-focused",
                    "primary_text": f"🚀 {self.product} is changing the game for {self.target_audience}.",
                    "primary_text_extended": f"Tired of struggling with [problem]? {self.product} helps you [benefit]. {self.offer} - Try it risk-free.",
                    "headlines": [
                        f"Try {self.product} Free",
                        "Transform Your Results",
                        "See Why Everyone's Switching"
                    ],
                    "descriptions": [
                        "Start Your Free Trial",
                        "No Credit Card Required"
                    ],
                    "cta_button": "Learn More",
                    "creative_direction": "Show product in action, clean interface, happy user"
                },
                {
                    "ad_number": 2,
                    "ad_angle": "Problem-focused",
                    "primary_text": f"Still struggling with [common problem]? There's a better way.",
                    "headlines": [
                        "Tired of [Problem]?",
                        "There's a Better Way",
                        "Stop Wasting Time"
                    ],
                    "descriptions": [
                        "Free Solution Inside",
                        "Works in Minutes"
                    ],
                    "cta_button": "Get Started",
                    "creative_direction": "Before/after comparison, problem visualization"
                }
            ],
            "targeting_recommendations": {
                "interests": ["Business", "Entrepreneurship", "Marketing"],
                "behaviors": ["Small business owners", "Engaged shoppers"],
                "demographics": f"{self.target_audience}",
                "lookalike_sources": ["Website visitors", "Email list", "Purchasers"],
                "exclusions": ["Existing customers", "Employees"]
            },
            "campaign_structure": {
                "campaign_name": f"{self.client} - {self.objective.title()} - {self.funnel_stage.title()}",
                "ad_sets": [
                    {
                        "name": f"{self.funnel_stage.title()} - Interests",
                        "audience_type": self.funnel_stage,
                        "budget_percentage": 50,
                        "ads_to_include": [1, 2]
                    },
                    {
                        "name": f"{self.funnel_stage.title()} - Lookalike 1%",
                        "audience_type": self.funnel_stage,
                        "budget_percentage": 50,
                        "ads_to_include": [1, 2]
                    }
                ]
            }
        }

    def generate_creative_briefs(self, ad_data: Dict) -> str:
        """Generate creative briefs for designers"""
        self.log("Generating creative briefs...", "INFO")

        briefs = f"""# Creative Briefs for {self.client} Meta Ads Campaign

**Product:** {self.product}
**Offer:** {self.offer}
**Target Audience:** {self.target_audience}
**Generated:** {datetime.now().strftime('%Y-%m-%d')}

---

## Image Ad Specifications

**Dimensions:**
- Feed: 1080x1080 (1:1)
- Stories/Reels: 1080x1920 (9:16)
- Right Column: 1200x628 (1.91:1)

**General Guidelines:**
- Minimal text overlay (<20%)
- High contrast, bright colors
- Clear focal point
- Brand colors: [Add client colors]
- Font: [Add client font]

---

## Creative Concepts

"""
        for ad in ad_data.get("ads", []):
            briefs += f"""### Ad {ad.get('ad_number', '?')}: {ad.get('ad_angle', 'Unknown')}

**Creative Direction:** {ad.get('creative_direction', 'N/A')}

**Copy to Include:**
- Headline: {ad.get('headlines', [''])[0]}
- CTA: {ad.get('cta_button', 'Learn More')}

**Image Concept:**
- Main visual: [Description]
- Text overlay: [If any]
- Logo placement: Bottom right

**Video Concept (15-30 sec):**
- Hook (0-3s): [Attention grabber]
- Problem (3-8s): [Pain point visualization]
- Solution (8-20s): [Product demo]
- CTA (20-30s): [Clear action]

---

"""

        briefs += """## UGC Style Content

**Talking Head Video:**
- Person speaking directly to camera
- Authentic, not overly produced
- Good lighting, clear audio
- 15-60 seconds

**Testimonial Format:**
- Real customer (or actor)
- Specific results mentioned
- Before/after story
- Call to action at end

**Product Demo:**
- Screen recording or product in use
- Highlight key features
- Show ease of use
- End with offer/CTA

---

## Carousel Concepts

**Feature Walkthrough (5 slides):**
1. Hook/Problem statement
2. Feature 1 + benefit
3. Feature 2 + benefit
4. Feature 3 + benefit
5. CTA with offer

**Customer Journey (5 slides):**
1. "Before" state/problem
2. Discovery of solution
3. Implementation
4. Results achieved
5. CTA to start their journey
"""

        brief_path = self.output_dir / "creatives" / "creative_briefs.md"
        brief_path.write_text(briefs, encoding="utf-8")
        self.log("Creative briefs saved", "SUCCESS")
        return briefs

    def generate_optimization_playbook(self) -> str:
        """Generate optimization playbook"""
        playbook = f"""# Meta Ads Optimization Playbook

**Client:** {self.client}
**Campaign:** {self.product} - {self.objective.title()}
**Monthly Budget:** ${self.monthly_budget}

---

## Phase 1: Learning (Days 1-3)

**DO:**
- Let ads run without changes
- Monitor for policy violations
- Track all metrics for baseline

**DON'T:**
- Make any optimizations
- Panic about high CPMs
- Add/remove ads

**Key Metrics to Track:**
- Impressions
- CPM
- CTR
- CPC
- Conversions (if any)

---

## Phase 2: Initial Optimization (Days 4-7)

**Kill Criteria:**
- CTR < 1% after 1000 impressions
- CPM 3x higher than others
- 0 conversions after $50 spend

**Scale Criteria:**
- CTR > 2%
- CPA below target
- Consistent performance

**Actions:**
- Turn off underperformers
- Increase budget on winners by 20%
- Launch backup creatives if needed

---

## Phase 3: Scaling (Week 2+)

**Horizontal Scaling:**
- Duplicate winning ad sets
- Test new audiences with proven creatives
- Expand lookalike percentages (1% → 2% → 5%)

**Vertical Scaling:**
- Increase budgets 20% every 3 days
- Never more than 30% at once
- Monitor for efficiency drops

**Creative Refresh:**
- New creatives every 2-3 weeks
- Rotate hooks while keeping winning body
- Test new formats (static → video → carousel)

---

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| High CPM | Audience too small or competitive | Broaden targeting |
| Low CTR | Creative not resonating | Test new hooks |
| High CPC | CTR okay, competition high | Improve relevance score |
| Low Conversions | Traffic quality issue | Refine targeting or landing page |
| Frequency > 3 | Audience fatigued | Expand audience or pause |

---

## Weekly Checklist

- [ ] Review all ad performance
- [ ] Kill underperformers
- [ ] Scale winners
- [ ] Check frequency levels
- [ ] Review audience overlap
- [ ] Plan creative refresh
- [ ] Update client on progress

---

## Monthly Review

- Total spend vs. budget
- CPA trend
- ROAS calculation
- Top performing creatives
- Audience insights
- Next month strategy
"""

        playbook_path = self.output_dir / "optimization" / "playbook.md"
        playbook_path.write_text(playbook, encoding="utf-8")
        return playbook

    def execute(self) -> Dict:
        """Execute complete campaign generation"""
        self.log(f"🚀 Starting Meta Ads Campaign Generation", "INFO")
        self.log(f"   Client: {self.client}", "INFO")
        self.log(f"   Product: {self.product}", "INFO")
        self.log(f"   Budget: ${self.monthly_budget}/mo", "INFO")

        start_time = time.time()

        # Generate ad copy and structure
        ad_data = self.generate_ad_copy()

        # Save ad data
        ad_path = self.output_dir / "creatives" / "ad_copy.json"
        with open(ad_path, 'w') as f:
            json.dump(ad_data, f, indent=2)

        # Generate creative briefs
        self.generate_creative_briefs(ad_data)

        # Generate actual ad creative images if enabled
        generated_images = {}
        if self.generate_images:
            generated_images = self.generate_ad_creatives(ad_data)

        # Generate optimization playbook
        self.generate_optimization_playbook()

        # Generate campaign structure markdown
        structure_md = f"""# Campaign Structure: {self.client}

**Objective:** {self.objective.title()}
**Funnel Stage:** {self.funnel_stage.title()}
**Monthly Budget:** ${self.monthly_budget}

---

## Campaign Architecture

"""
        campaign = ad_data.get("campaign_structure", {})
        structure_md += f"### {campaign.get('campaign_name', 'Campaign')}\n\n"

        for ad_set in campaign.get("ad_sets", []):
            budget = int(self.monthly_budget * ad_set.get("budget_percentage", 50) / 100)
            structure_md += f"""#### Ad Set: {ad_set.get('name', 'Ad Set')}
- **Audience Type:** {ad_set.get('audience_type', 'unknown')}
- **Budget:** ${budget}/mo ({ad_set.get('budget_percentage', 50)}%)
- **Ads:** {', '.join([f"Ad {n}" for n in ad_set.get('ads_to_include', [])])}

"""

        structure_md += """---

## Targeting Recommendations

"""
        targeting = ad_data.get("targeting_recommendations", {})
        structure_md += f"""**Interests:** {', '.join(targeting.get('interests', []))}

**Behaviors:** {', '.join(targeting.get('behaviors', []))}

**Demographics:** {targeting.get('demographics', '')}

**Lookalike Sources:** {', '.join(targeting.get('lookalike_sources', []))}

**Exclusions:** {', '.join(targeting.get('exclusions', []))}
"""

        structure_path = self.output_dir / "campaign_structure" / "architecture.md"
        structure_path.write_text(structure_md, encoding="utf-8")

        execution_time = time.time() - start_time

        result = {
            "success": True,
            "client": self.client,
            "product": self.product,
            "ads_generated": len(ad_data.get("ads", [])),
            "images_generated": len(generated_images),
            "execution_time": f"{int(execution_time)}s",
            "output_dir": str(self.output_dir),
            "files": {
                "ad_copy": str(ad_path),
                "creative_briefs": str(self.output_dir / "creatives" / "creative_briefs.md"),
                "campaign_structure": str(structure_path),
                "optimization_playbook": str(self.output_dir / "optimization" / "playbook.md")
            },
            "generated_images": generated_images
        }

        result_path = self.output_dir / "result.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, indent=2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ META ADS CAMPAIGN GENERATED", "SUCCESS")
        self.log(f"   Ads: {len(ad_data.get('ads', []))}", "INFO")
        if generated_images:
            self.log(f"   Images: {len(generated_images)} creatives generated", "INFO")
        self.log(f"   Output: {self.output_dir}", "INFO")
        self.log("=" * 50, "INFO")

        return result


def main():
    parser = argparse.ArgumentParser(description="Generate Meta ads campaigns")

    parser.add_argument("--client", required=True, help="Client/brand name")
    parser.add_argument("--product", required=True, help="Product/service name")
    parser.add_argument("--offer", required=True, help="What you're promoting")
    parser.add_argument("--target-audience", required=True, help="Target audience")
    parser.add_argument("--monthly-budget", type=int, default=5000)
    parser.add_argument("--objective", default="conversions",
                       choices=["awareness", "traffic", "conversions", "leads"])
    parser.add_argument("--funnel-stage", default="cold", choices=["cold", "warm", "hot"])
    parser.add_argument("--variations", type=int, default=5)
    parser.add_argument("--generate-images", action="store_true",
                       help="Generate ad creative images using Google Nano Banana (fal.ai)")

    args = parser.parse_args()

    generator = MetaAdsCampaignGenerator(
        client=args.client,
        product=args.product,
        offer=args.offer,
        target_audience=args.target_audience,
        monthly_budget=args.monthly_budget,
        objective=args.objective,
        funnel_stage=args.funnel_stage,
        variations=args.variations,
        generate_images=args.generate_images
    )

    result = generator.execute()
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
