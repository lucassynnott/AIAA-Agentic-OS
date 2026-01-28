#!/usr/bin/env python3
"""
AI Landing Page Generator - Generate and Deploy Beautiful Landing Pages

Generates high-converting landing pages using AI (Claude) and optionally
deploys them to Cloudflare Pages automatically.

Usage:
    python3 execution/generate_landing_page.py \
        --product "AI Course" \
        --headline "Master AI in 30 Days" \
        --price "$497" \
        --style "modern-gradient" \
        --deploy

Follows directive: directives/ai_landing_page_generator.md
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


# Anthropic Frontend Design Skill - Anti-AI-Slop Design System
# Source: SKILL_BIBLE_frontend_design_mastery.md
# Creates distinctive, production-grade interfaces avoiding generic AI aesthetics

DESIGN_STYLES = {
    "neo-noir": {
        "name": "Neo-Noir Dark",
        "description": "Dark dramatic with sharp accent, cinematic feel",
        "font_display": "'Clash Display', sans-serif",
        "font_body": "'Satoshi', sans-serif",
        "font_url": "https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=satoshi@400,500,700&display=swap",
        "colors": {
            "primary": "#ff3366",
            "secondary": "#ff6b6b",
            "accent": "#ff3366",
            "bg_gradient_start": "#0a0a0a",
            "bg_gradient_end": "#141414",
            "text_primary": "#fafafa",
            "text_secondary": "#737373",
            "bg_main": "#0a0a0a",
            "bg_card": "rgba(20, 20, 20, 0.8)"
        },
        "effects": {
            "glow": "0 0 60px rgba(255, 51, 102, 0.3)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "noise": True
        }
    },
    "editorial-luxury": {
        "name": "Editorial Luxury",
        "description": "Elegant serif typography, refined minimalism",
        "font_display": "'Playfair Display', serif",
        "font_body": "'Source Sans 3', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800&family=Source+Sans+3:wght@400;500;600&display=swap",
        "colors": {
            "primary": "#b8860b",
            "secondary": "#d4a574",
            "accent": "#b8860b",
            "bg_gradient_start": "#faf9f7",
            "bg_gradient_end": "#f5f3f0",
            "text_primary": "#1a1a1a",
            "text_secondary": "#666666",
            "bg_main": "#faf9f7",
            "bg_card": "#ffffff"
        },
        "effects": {
            "glow": "none",
            "border": "1px solid rgba(0, 0, 0, 0.08)",
            "noise": False
        }
    },
    "electric-tech": {
        "name": "Electric Tech",
        "description": "Futuristic blue glow, glass morphism, bold sans-serif",
        "font_display": "'Cabinet Grotesk', sans-serif",
        "font_body": "'General Sans', sans-serif",
        "font_url": "https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@400,500,700,800&f[]=general-sans@400,500,600&display=swap",
        "colors": {
            "primary": "#3b82f6",
            "secondary": "#06b6d4",
            "accent": "#3b82f6",
            "bg_gradient_start": "#020617",
            "bg_gradient_end": "#0f172a",
            "text_primary": "#f8fafc",
            "text_secondary": "#94a3b8",
            "bg_main": "#020617",
            "bg_card": "rgba(30, 41, 59, 0.5)"
        },
        "effects": {
            "glow": "0 0 80px rgba(59, 130, 246, 0.4)",
            "border": "1px solid rgba(59, 130, 246, 0.3)",
            "noise": True
        }
    },
    "warm-organic": {
        "name": "Warm Organic",
        "description": "Natural earth tones, flowing shapes, approachable",
        "font_display": "'Fraunces', serif",
        "font_body": "'Nunito Sans', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Fraunces:wght@400;500;600;700&family=Nunito+Sans:wght@400;500;600&display=swap",
        "colors": {
            "primary": "#e07a5f",
            "secondary": "#81b29a",
            "accent": "#e07a5f",
            "bg_gradient_start": "#fef7f0",
            "bg_gradient_end": "#fff5eb",
            "text_primary": "#3d3229",
            "text_secondary": "#7d7067",
            "bg_main": "#fef7f0",
            "bg_card": "#ffffff"
        },
        "effects": {
            "glow": "none",
            "border": "1px solid rgba(224, 122, 95, 0.2)",
            "noise": False
        }
    },
    "neubrutalism": {
        "name": "Neubrutalism",
        "description": "Bold borders, harsh shadows, raw and authentic",
        "font_display": "'Space Grotesk', sans-serif",
        "font_body": "'Work Sans', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Work+Sans:wght@400;500;600&display=swap",
        "colors": {
            "primary": "#ff5757",
            "secondary": "#5271ff",
            "accent": "#ff5757",
            "bg_gradient_start": "#fffef0",
            "bg_gradient_end": "#fff9db",
            "text_primary": "#000000",
            "text_secondary": "#333333",
            "bg_main": "#fffef0",
            "bg_card": "#ffffff"
        },
        "effects": {
            "glow": "none",
            "border": "3px solid #000000",
            "shadow": "8px 8px 0 #000000",
            "noise": False
        }
    },
    "modern-gradient": {
        "name": "Modern Gradient",
        "description": "Gradient backgrounds, glassmorphism, bold typography",
        "font_display": "'Syne', sans-serif",
        "font_body": "'Outfit', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Outfit:wght@400;500;600&display=swap",
        "colors": {
            "primary": "#8b5cf6",
            "secondary": "#a78bfa",
            "accent": "#f59e0b",
            "bg_gradient_start": "#7c3aed",
            "bg_gradient_end": "#4f46e5",
            "text_primary": "#1f2937",
            "text_secondary": "#6b7280",
            "bg_main": "#ffffff",
            "bg_card": "rgba(255, 255, 255, 0.8)"
        },
        "effects": {
            "glow": "0 0 100px rgba(139, 92, 246, 0.3)",
            "border": "1px solid rgba(255, 255, 255, 0.2)",
            "noise": True
        }
    },
    "minimal-clean": {
        "name": "Minimal Clean",
        "description": "White space, clean lines, subtle shadows",
        "font_display": "'Plus Jakarta Sans', sans-serif",
        "font_body": "'Plus Jakarta Sans', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
        "colors": {
            "primary": "#0f172a",
            "secondary": "#3b82f6",
            "accent": "#10b981",
            "bg_gradient_start": "#ffffff",
            "bg_gradient_end": "#f8fafc",
            "text_primary": "#0f172a",
            "text_secondary": "#64748b",
            "bg_main": "#ffffff",
            "bg_card": "#ffffff"
        },
        "effects": {
            "glow": "none",
            "border": "1px solid rgba(0, 0, 0, 0.06)",
            "noise": False
        }
    },
    "dark-mode": {
        "name": "Dark Mode",
        "description": "Dark backgrounds, neon accents, tech feel",
        "font_display": "'Clash Display', sans-serif",
        "font_body": "'Satoshi', sans-serif",
        "font_url": "https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=satoshi@400,500,700&display=swap",
        "colors": {
            "primary": "#a855f7",
            "secondary": "#06b6d4",
            "accent": "#f43f5e",
            "bg_gradient_start": "#0f172a",
            "bg_gradient_end": "#1e1b4b",
            "text_primary": "#f8fafc",
            "text_secondary": "#94a3b8",
            "bg_main": "#0f172a",
            "bg_card": "rgba(30, 41, 59, 0.6)"
        },
        "effects": {
            "glow": "0 0 60px rgba(168, 85, 247, 0.3)",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "noise": True
        }
    },
    "bold-colors": {
        "name": "Bold Colors",
        "description": "Vibrant colors, strong CTAs, high contrast",
        "font_display": "'DM Sans', sans-serif",
        "font_body": "'DM Sans', sans-serif",
        "font_url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap",
        "colors": {
            "primary": "#dc2626",
            "secondary": "#2563eb",
            "accent": "#16a34a",
            "bg_gradient_start": "#fef2f2",
            "bg_gradient_end": "#fee2e2",
            "text_primary": "#1f2937",
            "text_secondary": "#4b5563",
            "bg_main": "#ffffff",
            "bg_card": "#ffffff"
        }
    },
    "professional": {
        "name": "Professional",
        "description": "Corporate, trustworthy, traditional layout",
        "colors": {
            "primary": "#1e40af",
            "secondary": "#3b82f6",
            "accent": "#059669",
            "bg_gradient_start": "#f8fafc",
            "bg_gradient_end": "#e2e8f0",
            "text_primary": "#1e293b",
            "text_secondary": "#475569",
            "bg_main": "#ffffff",
            "bg_card": "#ffffff"
        }
    }
}


class LandingPageGenerator:
    """Generates beautiful landing pages using AI and deploys to Cloudflare"""

    def __init__(self, **kwargs):
        self.product = kwargs.get("product", "")
        self.headline = kwargs.get("headline", "")
        self.subheadline = kwargs.get("subheadline", "")
        self.price = kwargs.get("price", "")
        self.target_audience = kwargs.get("target_audience", "")
        self.website = kwargs.get("website", "")
        self.style = kwargs.get("style", "modern-gradient")
        self.do_research = kwargs.get("research", False)
        self.do_deploy = kwargs.get("deploy", False)
        self.project_name = kwargs.get("project_name", "")
        self.output_dir = kwargs.get("output_dir", "")
        self.cta_text = kwargs.get("cta_text", "")
        self.cta_url = kwargs.get("cta_url", "#")

        # Generate project slug
        self.project_slug = self._generate_slug(self.product)

        # Setup output directory
        if not self.output_dir:
            self.output_dir = f".tmp/landing_pages/{self.project_slug}"
        self.output_path = Path(self.output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)

        # Initialize data storage
        self.research_data = {}
        self.copy_data = {}
        self.design_config = DESIGN_STYLES.get(self.style, DESIGN_STYLES["modern-gradient"])

        # API keys
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.cloudflare_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")

    def _generate_slug(self, text: str) -> str:
        """Generate URL-safe slug from text"""
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = slug.strip('-')
        return slug[:50] if slug else f"landing-{int(time.time())}"

    def log(self, message: str, level: str = "INFO"):
        """Log progress"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

    def call_claude(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        """Call Claude via OpenRouter"""
        if not self.openrouter_key:
            self.log("OPENROUTER_API_KEY not set", "ERROR")
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
            else:
                self.log(f"Claude API error: {response.status_code}", "ERROR")
                return None

        except Exception as e:
            self.log(f"Error calling Claude: {e}", "ERROR")
            return None

    def research_market(self) -> dict:
        """Research market using Perplexity"""
        self.log("Researching market and competition...", "INFO")

        if not self.perplexity_key:
            self.log("Perplexity API not configured, skipping research", "WARNING")
            return {}

        try:
            query = f"""Research for landing page creation:
            Product: {self.product}
            Target Audience: {self.target_audience or 'General business audience'}
            
            Provide:
            1. Top 3 pain points this audience faces
            2. Common objections to purchasing
            3. Key benefits they're looking for
            4. Competitive landscape summary
            5. Recommended messaging angles"""

            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-small-128k-online",
                    "messages": [{"role": "user", "content": query}]
                },
                timeout=60
            )

            if response.status_code == 200:
                research = response.json()["choices"][0]["message"]["content"]
                self.log("Market research complete", "SUCCESS")
                return {"raw_research": research}

        except Exception as e:
            self.log(f"Research error: {e}", "WARNING")

        return {}

    def generate_copy(self) -> dict:
        """Generate landing page copy using Claude with funnel bible principles"""
        self.log("Generating conversion-optimized copy...", "INFO")

        research_context = ""
        if self.research_data:
            research_context = f"\n\nMarket Research:\n{self.research_data.get('raw_research', '')}"

        # Funnel Bible integrated prompt - incorporates VSL, sales funnel, and copywriting mastery
        prompt = f"""You are an expert direct-response copywriter using proven funnel frameworks.

PRODUCT/SERVICE: {self.product}
TARGET AUDIENCE: {self.target_audience or 'Business professionals'}
PRICE POINT: {self.price or 'Not specified'}
STYLE: {self.design_config['name']}
{research_context}

=== THE PROPS FORMULA (327% Conversion Increase - Apply This) ===

**P** - PROBLEM AMPLIFICATION: Use 3-layer deep process:
   Layer 1: Surface problem ("can't get clients")
   Layer 2: Tried everything ("courses, ads, cold outreach - nothing works")  
   Layer 3: Starting to believe ("maybe I'm not cut out for this")
   + Future pace: Where this leads if not fixed

**R** - RESULT DEMONSTRATION (Triple R Formula):
   - REAL: Specific numbers ("close 3 new clients in 30 days")
   - RELATABLE: Paint life change ("imagine finally taking that vacation")
   - REACHABLE: Break into chunks ("just one client every 10 days")

**O** - OBJECTION REMOVAL: Systematic grid covering:
   - Time: "Only 27 minutes a day"
   - Money: ROI testimonials
   - Past failure: "Those methods were designed to fail"
   - Skepticism: Skeptic testimonials

**P** - PROOF STACKING (Pyramid Structure):
   Base: Hard data, statistics, studies
   Middle: Journey testimonials (skeptic, imperfect user, home run)
   Top: Home run case study

**S** - SIMPLE NEXT STEP: Single CTA focus, no competing links

=== ABOVE-THE-FOLD REQUIREMENTS ===

1. "ATTENTION [TARGET AUDIENCE]" callout
2. Big promise headline
3. Subheadline backing promise
4. Hero image/video
5. Primary CTA button
6. Social proof near action points

=== HEADLINE FORMULAS (2026 Tested) ===

- "Why is this [authority] giving away his [big number] [benefit]"
- "Finally a way to [benefit] without [common struggle]"
- "Feeling frustrated that [problem] even though you [effort]"
- "Are you ready to [desired outcome]?"

Generate landing page copy following this JSON format:
{{
    "social_proof_header": "Short social proof line for header (e.g., 'Join 10,000+ professionals')",
    "headline": "4-8 word desire-based headline with action word (Unlock, Transform, Discover, Master)",
    "headline_variations": ["variation targeting fear", "variation targeting desire"],
    "subheadline": "Specific outcome + timeframe (e.g., 'Generate 50+ qualified leads in 30 days')",
    "hero_description": "2-3 sentences addressing THEIR situation - show you understand their world",
    "trust_badges": ["Trust element 1", "Trust element 2", "Trust element 3"],
    "problem_headline": "Agitation headline that makes them feel the pain",
    "problem_points": [
        "Specific pain point using their language",
        "Cost/consequence of not solving this",
        "Failed solutions they've tried before"
    ],
    "solution_headline": "Introduce your unique mechanism (not just product name)",
    "solution_description": "How your MECHANISM solves the root cause (not feature list)",
    "unique_mechanism": "The specific system/method/framework name that makes you different",
    "features": [
        {{"title": "Outcome-focused title", "description": "Benefit they get, not feature you have", "icon": "🚀"}},
        {{"title": "Transformation title", "description": "Before/after implied", "icon": "💡"}},
        {{"title": "Speed/ease title", "description": "How fast/easy they get results", "icon": "⚡"}},
        {{"title": "Proof title", "description": "Why this works (backed by data)", "icon": "🎯"}},
        {{"title": "Support title", "description": "They're not alone in this", "icon": "✨"}},
        {{"title": "Bonus value title", "description": "Extra value they didn't expect", "icon": "🔥"}}
    ],
    "social_proof_headline": "Specific number + outcome (e.g., '2,847 businesses transformed')",
    "testimonials": [
        {{"quote": "Specific result with numbers + transformation story", "author": "Full Name", "role": "Title, Company", "result": "Key metric achieved"}},
        {{"quote": "Different use case/persona testimonial", "author": "Full Name", "role": "Title, Company", "result": "Key metric achieved"}},
        {{"quote": "Addresses common objection through story", "author": "Full Name", "role": "Title, Company", "result": "Key metric achieved"}}
    ],
    "offer_stack": [
        {{"item": "Core product/service", "value": "$X,XXX value"}},
        {{"item": "Bonus 1", "value": "$XXX value"}},
        {{"item": "Bonus 2", "value": "$XXX value"}}
    ],
    "total_value": "Total value statement (e.g., '$4,997 Total Value')",
    "faq": [
        {{"question": "Objection disguised as question", "answer": "Overcome with proof/logic"}},
        {{"question": "Common concern about results", "answer": "Reassure with specifics"}},
        {{"question": "Question about who this is for", "answer": "Qualify ideal customer"}},
        {{"question": "Risk/guarantee question", "answer": "Explain risk reversal"}},
        {{"question": "Logistics/how it works", "answer": "Simple clear process"}}
    ],
    "cta_primary": "Action verb + outcome (e.g., 'Get Instant Access')",
    "cta_secondary": "Lower commitment option (e.g., 'See How It Works')",
    "guarantee": "Specific guarantee with timeframe and what they get if unsatisfied",
    "urgency_text": "Legitimate scarcity or urgency reason",
    "final_cta_headline": "Last chance headline that summarizes the transformation"
}}

CRITICAL: Write copy that sounds like a HUMAN wrote it, not AI. Use conversational language, specific numbers, and avoid generic marketing speak. Channel existing desires - don't try to create new ones.

Return ONLY the JSON, no explanation."""

        result = self.call_claude(prompt)

        if result:
            try:
                # Extract JSON from response
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    copy_data = json.loads(json_match.group())
                    self.log("Copy generation complete", "SUCCESS")
                    return copy_data
            except json.JSONDecodeError as e:
                self.log(f"JSON parse error: {e}", "WARNING")

        # Return fallback copy
        return self._get_fallback_copy()

    def _get_fallback_copy(self) -> dict:
        """Return fallback copy if AI generation fails"""
        return {
            "headline": self.headline or f"Transform Your Business with {self.product}",
            "headline_variations": [],
            "subheadline": self.subheadline or "The proven solution trusted by thousands of professionals",
            "hero_description": f"Discover how {self.product} can help you achieve your goals faster than ever before.",
            "problem_headline": "The Challenge You're Facing",
            "problem_points": [
                "Struggling to get consistent results",
                "Wasting time on ineffective solutions",
                "Missing out on opportunities"
            ],
            "solution_headline": "The Solution You've Been Looking For",
            "solution_description": f"{self.product} provides everything you need to succeed.",
            "features": [
                {"title": "Easy to Use", "description": "Get started in minutes", "icon": "🚀"},
                {"title": "Proven Results", "description": "Trusted by professionals", "icon": "💡"},
                {"title": "Fast Implementation", "description": "See results quickly", "icon": "⚡"},
                {"title": "Expert Support", "description": "We're here to help", "icon": "🎯"},
                {"title": "Continuous Updates", "description": "Always improving", "icon": "✨"},
                {"title": "Great Value", "description": "Worth every penny", "icon": "🔥"}
            ],
            "social_proof_headline": "What Our Customers Say",
            "testimonials": [
                {"quote": "This transformed our business completely.", "author": "Sarah M.", "role": "Business Owner"},
                {"quote": "Best decision we ever made.", "author": "John D.", "role": "Marketing Director"},
                {"quote": "Results exceeded our expectations.", "author": "Mike R.", "role": "CEO"}
            ],
            "faq": [
                {"question": "How does it work?", "answer": "Simply sign up and follow our proven process."},
                {"question": "Is there a guarantee?", "answer": "Yes, we offer a 30-day money-back guarantee."},
                {"question": "How long until I see results?", "answer": "Most users see results within the first week."},
                {"question": "Do I need technical skills?", "answer": "No, it's designed for everyone."},
                {"question": "Can I cancel anytime?", "answer": "Yes, no long-term commitments required."}
            ],
            "cta_primary": "Get Started Now",
            "cta_secondary": "Learn More",
            "guarantee": "30-Day Money-Back Guarantee",
            "urgency_text": ""
        }

    def generate_html(self) -> str:
        """Generate complete HTML landing page"""
        self.log("Generating HTML/CSS design...", "INFO")

        colors = self.design_config["colors"]
        copy = self.copy_data
        is_dark = self.style == "dark-mode"

        # Build features HTML
        features_html = ""
        for feature in copy.get("features", [])[:6]:
            features_html += f'''
            <div class="feature-card">
                <div class="feature-icon">{feature.get("icon", "✨")}</div>
                <h3>{feature.get("title", "Feature")}</h3>
                <p>{feature.get("description", "Description")}</p>
            </div>'''

        # Build testimonials HTML
        testimonials_html = ""
        for testimonial in copy.get("testimonials", [])[:3]:
            testimonials_html += f'''
            <div class="testimonial-card">
                <p class="testimonial-quote">"{testimonial.get("quote", "")}"</p>
                <p class="testimonial-author">— {testimonial.get("author", "Customer")}</p>
                <p class="testimonial-role">{testimonial.get("role", "")}</p>
            </div>'''

        # Build FAQ HTML
        faq_html = ""
        for i, faq in enumerate(copy.get("faq", [])[:5]):
            faq_html += f'''
            <div class="faq-item">
                <button class="faq-question" onclick="toggleFaq(this)">
                    <span>{faq.get("question", "Question?")}</span>
                    <span class="faq-icon">+</span>
                </button>
                <div class="faq-answer">
                    <p>{faq.get("answer", "Answer.")}</p>
                </div>
            </div>'''

        # Build problem points HTML
        problems_html = ""
        for point in copy.get("problem_points", []):
            problems_html += f'<li>{point}</li>'

        # Price display
        price_html = ""
        if self.price:
            price_html = f'<div class="price-display"><span class="price">{self.price}</span></div>'

        # CTA URL and text
        cta_url = self.cta_url or "#signup"
        cta_text = self.cta_text or copy.get("cta_primary", "Get Started Now")

        # Get font configuration from design style
        font_display = self.design_config.get("font_display", "'Inter', sans-serif")
        font_body = self.design_config.get("font_body", "'Inter', sans-serif")
        font_url = self.design_config.get("font_url", "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap")
        effects = self.design_config.get("effects", {})
        
        # Determine if dark theme based on background color
        is_dark = self.style in ["dark-mode", "neo-noir", "electric-tech"]
        
        # Build noise overlay CSS if enabled
        noise_css = ""
        if effects.get("noise", False):
            noise_css = """
        .noise-overlay::after {
            content: '';
            position: absolute;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
            opacity: 0.03;
            pointer-events: none;
            z-index: 0;
        }
            """
        
        # Build glow effect
        glow_effect = effects.get("glow", "none")
        border_effect = effects.get("border", "1px solid rgba(255,255,255,0.1)")
        shadow_effect = effects.get("shadow", "")
        
        # Neubrutalism special styling
        is_brutal = self.style == "neubrutalism"
        brutal_border = "3px solid #000000" if is_brutal else border_effect
        brutal_shadow = "8px 8px 0 #000000" if is_brutal else ""
        brutal_radius = "0" if is_brutal else "12px"

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{copy.get('subheadline', '')}">
    <title>{copy.get('headline', self.product)} | {self.product}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://api.fontshare.com">
    <link href="{font_url}" rel="stylesheet">
    <style>
        :root {{
            --font-display: {font_display};
            --font-body: {font_body};
            --primary: {colors["primary"]};
            --secondary: {colors["secondary"]};
            --accent: {colors["accent"]};
            --bg-gradient-start: {colors["bg_gradient_start"]};
            --bg-gradient-end: {colors["bg_gradient_end"]};
            --text-primary: {colors["text_primary"]};
            --text-secondary: {colors["text_secondary"]};
            --bg-main: {colors["bg_main"]};
            --bg-card: {colors["bg_card"]};
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: var(--font-body);
            line-height: 1.6;
            color: var(--text-primary);
            background: var(--bg-main);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-display);
        }}
        
        {noise_css}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        /* Header */
        .header {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: {"rgba(15, 23, 42, 0.95)" if is_dark else "rgba(255, 255, 255, 0.95)"};
            backdrop-filter: blur(10px);
            z-index: 1000;
            padding: 15px 0;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }}

        .header-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--primary);
        }}

        .header-cta {{
            background: var(--primary);
            color: white;
            padding: 10px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .header-cta:hover {{
            background: var(--secondary);
            transform: translateY(-2px);
        }}

        /* Hero Section */
        .hero {{
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
            padding: 160px 0 100px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.5;
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
        }}

        .hero h1 {{
            font-size: clamp(2.5rem, 6vw, 4.5rem);
            font-weight: 800;
            margin-bottom: 24px;
            letter-spacing: -0.03em;
            line-height: 1.05;
            {"color: white;" if is_dark or self.style == "modern-gradient" else ""}
        }}

        .hero .subheadline {{
            font-size: 1.25rem;
            color: {"rgba(255,255,255,0.9)" if is_dark or self.style == "modern-gradient" else "var(--text-secondary)"};
            max-width: 600px;
            margin: 0 auto 30px;
        }}

        .hero-description {{
            font-size: 1.1rem;
            color: {"rgba(255,255,255,0.8)" if is_dark or self.style == "modern-gradient" else "var(--text-secondary)"};
            max-width: 700px;
            margin: 0 auto 40px;
        }}

        .cta-group {{
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }}

        .cta-primary {{
            background: var(--accent);
            color: white;
            padding: 16px 40px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 700;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}

        .cta-primary:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}

        .cta-secondary {{
            background: transparent;
            color: {"white" if is_dark or self.style == "modern-gradient" else "var(--primary)"};
            padding: 16px 40px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1rem;
            border: 2px solid {"white" if is_dark or self.style == "modern-gradient" else "var(--primary)"};
            transition: all 0.3s ease;
        }}

        .cta-secondary:hover {{
            background: {"rgba(255,255,255,0.1)" if is_dark or self.style == "modern-gradient" else "var(--primary)"};
            color: white;
        }}

        /* Problem Section */
        .problem-section {{
            padding: 100px 0;
            background: var(--bg-main);
        }}

        .section-title {{
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 50px;
        }}

        .problem-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }}

        .problem-list {{
            list-style: none;
            padding: 0;
        }}

        .problem-list li {{
            padding: 20px 20px 20px 60px;
            margin-bottom: 15px;
            background: var(--bg-card);
            border-radius: 12px;
            position: relative;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        }}

        .problem-list li::before {{
            content: '✗';
            position: absolute;
            left: 20px;
            color: #ef4444;
            font-size: 1.5rem;
        }}

        /* Features Section */
        .features-section {{
            padding: 100px 0;
            background: {"var(--bg-card)" if is_dark else "#f8fafc"};
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
        }}

        .feature-card {{
            background: var(--bg-main);
            padding: 40px;
            border-radius: {brutal_radius};
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: {"8px 8px 0 #000000" if is_brutal else "0 4px 20px rgba(0,0,0,0.05)"};
            border: {brutal_border};
            position: relative;
            overflow: hidden;
        }}
        
        .feature-card::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, transparent 0%, {"rgba(255,255,255,0.03)" if is_dark else "rgba(0,0,0,0.02)"} 100%);
            opacity: 0;
            transition: opacity 0.4s ease;
        }}

        .feature-card:hover {{
            transform: translateY(-8px) {"" if is_brutal else "scale(1.02)"};
            box-shadow: {"12px 12px 0 #000000" if is_brutal else f"0 20px 50px rgba(0,0,0,0.15), {glow_effect}" if glow_effect != "none" else "0 20px 50px rgba(0,0,0,0.15)"};
        }}
        
        .feature-card:hover::before {{
            opacity: 1;
        }}

        .feature-icon {{
            font-size: 3rem;
            margin-bottom: 20px;
        }}

        .feature-card h3 {{
            font-size: 1.25rem;
            margin-bottom: 10px;
            color: var(--text-primary);
        }}

        .feature-card p {{
            color: var(--text-secondary);
        }}

        /* Testimonials Section */
        .testimonials-section {{
            padding: 100px 0;
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        }}

        .testimonials-section .section-title {{
            color: {"white" if is_dark or self.style == "modern-gradient" else "var(--text-primary)"};
        }}

        .testimonials-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 30px;
        }}

        .testimonial-card {{
            background: {"rgba(255,255,255,0.1)" if is_dark or self.style == "modern-gradient" else "white"};
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .testimonial-quote {{
            font-size: 1.1rem;
            font-style: italic;
            margin-bottom: 20px;
            color: {"white" if is_dark or self.style == "modern-gradient" else "var(--text-primary)"};
        }}

        .testimonial-author {{
            font-weight: 700;
            color: {"white" if is_dark or self.style == "modern-gradient" else "var(--text-primary)"};
        }}

        .testimonial-role {{
            font-size: 0.9rem;
            color: {"rgba(255,255,255,0.7)" if is_dark or self.style == "modern-gradient" else "var(--text-secondary)"};
        }}

        /* FAQ Section */
        .faq-section {{
            padding: 100px 0;
            background: var(--bg-main);
        }}

        .faq-container {{
            max-width: 800px;
            margin: 0 auto;
        }}

        .faq-item {{
            margin-bottom: 15px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}

        .faq-question {{
            width: 100%;
            padding: 20px 25px;
            background: var(--bg-card);
            border: none;
            text-align: left;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-primary);
            transition: background 0.3s ease;
        }}

        .faq-question:hover {{
            background: {"#2d3748" if is_dark else "#f1f5f9"};
        }}

        .faq-icon {{
            font-size: 1.5rem;
            transition: transform 0.3s ease;
        }}

        .faq-item.active .faq-icon {{
            transform: rotate(45deg);
        }}

        .faq-answer {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            background: {"#1e293b" if is_dark else "#f8fafc"};
        }}

        .faq-item.active .faq-answer {{
            max-height: 500px;
        }}

        .faq-answer p {{
            padding: 20px 25px;
            color: var(--text-secondary);
        }}

        /* CTA Section */
        .cta-section {{
            padding: 100px 0;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            text-align: center;
        }}

        .cta-section h2 {{
            color: white;
            font-size: 2.5rem;
            margin-bottom: 20px;
        }}

        .cta-section p {{
            color: rgba(255,255,255,0.9);
            font-size: 1.2rem;
            margin-bottom: 40px;
        }}

        .price-display {{
            margin-bottom: 30px;
        }}

        .price {{
            font-size: 3rem;
            font-weight: 800;
            color: white;
        }}

        .guarantee {{
            margin-top: 30px;
            color: rgba(255,255,255,0.9);
            font-size: 1rem;
        }}

        .guarantee::before {{
            content: '🛡️ ';
        }}

        /* Footer */
        .footer {{
            background: {"#0f172a" if is_dark else "#1e293b"};
            color: white;
            padding: 60px 0 30px;
        }}

        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
            margin-bottom: 40px;
        }}

        .footer-section h4 {{
            margin-bottom: 20px;
            font-size: 1.1rem;
        }}

        .footer-section a {{
            display: block;
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            margin-bottom: 10px;
            transition: color 0.3s ease;
        }}

        .footer-section a:hover {{
            color: white;
        }}

        .footer-bottom {{
            text-align: center;
            padding-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.5);
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .hero {{
                padding: 140px 0 80px;
            }}

            .hero h1 {{
                font-size: 2rem;
            }}

            .section-title {{
                font-size: 1.8rem;
            }}

            .cta-group {{
                flex-direction: column;
                align-items: center;
            }}

            .cta-primary, .cta-secondary {{
                width: 100%;
                max-width: 300px;
                text-align: center;
            }}
        }}
        
        /* Staggered Animation Reveals - Anthropic Frontend Design Skill */
        @keyframes fadeSlideUp {{
            from {{
                opacity: 0;
                transform: translateY(40px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes glowPulse {{
            0%, 100% {{
                box-shadow: 0 0 20px var(--primary);
            }}
            50% {{
                box-shadow: 0 0 40px var(--primary), 0 0 60px var(--secondary);
            }}
        }}
        
        .hero h1 {{
            animation: fadeSlideUp 0.8s ease-out forwards;
            animation-delay: 0.1s;
            opacity: 0;
        }}
        
        .hero .subheadline {{
            animation: fadeSlideUp 0.8s ease-out forwards;
            animation-delay: 0.2s;
            opacity: 0;
        }}
        
        .hero .hero-description {{
            animation: fadeSlideUp 0.8s ease-out forwards;
            animation-delay: 0.3s;
            opacity: 0;
        }}
        
        .hero .cta-group {{
            animation: fadeSlideUp 0.8s ease-out forwards;
            animation-delay: 0.4s;
            opacity: 0;
        }}
        
        .cta-primary {{
            position: relative;
            overflow: hidden;
        }}
        
        .cta-primary::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
        }}
        
        .cta-primary:hover::before {{
            transform: translateX(100%);
        }}
    </style>
</head>
<body>
    <!-- Header with Social Proof -->
    <header class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">{self.product}</div>
                <span class="social-proof-header" style="font-size: 0.85rem; color: var(--text-secondary); display: none;">{copy.get('social_proof_header', '')}</span>
                <a href="{cta_url}" class="header-cta">{cta_text}</a>
            </div>
        </div>
    </header>

    <!-- ============================================ -->
    <!-- PROPS FUNNEL STRUCTURE (from Video Research) -->
    <!-- P-Problem, R-Result, O-Objection, P-Proof, S-Simple -->
    <!-- ============================================ -->

    <!-- HERO: Audience Callout + Big Promise + Social Proof -->
    <section class="hero{"  noise-overlay" if effects.get("noise", False) else ""}">
        <div class="container">
            <div class="hero-content" style="position: relative; z-index: 1;">
                <!-- Audience Callout (Above Headline) -->
                <p class="audience-callout" style="font-size: 0.9rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: var(--primary); margin-bottom: 15px;">
                    ATTENTION: {self.target_audience.upper() if self.target_audience else 'BUSINESS OWNERS'}
                </p>
                <!-- Social Proof Badge -->
                <p class="social-proof-badge" style="display: inline-block; background: {"rgba(255,255,255,0.1)" if is_dark else "rgba(0,0,0,0.05)"}; padding: 8px 20px; border-radius: 50px; font-size: 0.9rem; margin-bottom: 20px; color: {"rgba(255,255,255,0.9)" if is_dark else "var(--text-secondary)"};">
                    ⭐ {copy.get('social_proof_header', 'Trusted by thousands')}
                </p>
                <!-- Main Headline -->
                <h1>{copy.get('headline', self.headline or f'Transform with {self.product}')}</h1>
                <!-- Subheadline with Specific Outcome -->
                <p class="subheadline">{copy.get('subheadline', self.subheadline or '')}</p>
                <!-- Hero Description -->
                <p class="hero-description">{copy.get('hero_description', '')}</p>
                <!-- Trust Badges Row -->
                <div class="trust-badges" style="display: flex; gap: 24px; justify-content: center; margin-bottom: 30px; flex-wrap: wrap;">
                    {"".join([f'<span style="font-size: 0.85rem; color: {"rgba(255,255,255,0.8)" if is_dark else "var(--text-secondary)"}; display: flex; align-items: center; gap: 6px;"><span style=\"color: var(--primary);\">✓</span> {badge}</span>' for badge in copy.get('trust_badges', ['Secure Checkout', 'Instant Access', 'Money-Back Guarantee'])[:4]])}
                </div>
                <!-- Primary CTA -->
                <div class="cta-group">
                    <a href="{cta_url}" class="cta-primary">{cta_text}</a>
                    <a href="#problem" class="cta-secondary">{copy.get('cta_secondary', 'Learn More')}</a>
                </div>
            </div>
        </div>
    </section>

    <!-- P: PROBLEM AMPLIFICATION (3-Layer Deep) -->
    <section class="problem-section" id="problem">
        <div class="container" style="max-width: 900px;">
            <h2 class="section-title">{copy.get('problem_headline', "Sound Familiar?")}</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 40px; font-size: 1.1rem;">
                If you're experiencing any of these, you're not alone...
            </p>
            <!-- 3-Layer Problem Display -->
            <div class="problem-layers" style="display: flex; flex-direction: column; gap: 20px;">
                {"".join([f'''
                <div class="problem-layer" style="background: {"rgba(255,255,255,0.03)" if is_dark else "rgba(0,0,0,0.02)"}; padding: 25px 30px; border-radius: {brutal_radius}; border-left: 4px solid {"#ef4444" if i == 0 else "#f97316" if i == 1 else "#eab308"}; border: {brutal_border if is_brutal else "none"}; box-shadow: {"8px 8px 0 #000" if is_brutal else "none"};">
                    <div style="display: flex; align-items: flex-start; gap: 15px;">
                        <span style="font-size: 1.5rem; color: {"#ef4444" if i == 0 else "#f97316" if i == 1 else "#eab308"};">{"😤" if i == 0 else "😩" if i == 1 else "😔"}</span>
                        <p style="font-size: 1.1rem; color: var(--text-primary); margin: 0; line-height: 1.6;">{point}</p>
                    </div>
                </div>
                ''' for i, point in enumerate(copy.get('problem_points', ['Problem 1', 'Problem 2', 'Problem 3'])[:3])])}
            </div>
            <!-- Future Pace -->
            <div style="text-align: center; margin-top: 40px; padding: 30px; background: {"rgba(239,68,68,0.1)" if is_dark else "rgba(239,68,68,0.05)"}; border-radius: {brutal_radius};">
                <p style="color: {"#fca5a5" if is_dark else "#dc2626"}; font-weight: 600; font-size: 1.1rem; margin: 0;">
                    ⚠️ If left unchecked, this problem only gets worse over time...
                </p>
            </div>
        </div>
    </section>

    <!-- R: RESULT DEMONSTRATION (Triple R Formula) -->
    <section class="results-section" id="features" style="padding: 100px 0; background: {"var(--bg-card)" if is_dark else "#f8fafc"};">
        <div class="container">
            <!-- Unique Mechanism Introduction -->
            <div style="text-align: center; margin-bottom: 60px;">
                <p style="color: var(--primary); font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;">INTRODUCING</p>
                <h2 class="section-title" style="margin-bottom: 20px;">{copy.get('unique_mechanism', 'The System')}</h2>
                <p style="max-width: 700px; margin: 0 auto; color: var(--text-secondary); font-size: 1.1rem;">
                    {copy.get('solution_description', 'A proven framework that addresses the root cause of your challenges.')}
                </p>
            </div>
            <!-- Features as Results (Outcome-Focused) -->
            <div class="features-grid">
                {features_html}
            </div>
            <!-- Mid-Page CTA -->
            <div style="text-align: center; margin-top: 50px;">
                <a href="{cta_url}" class="cta-primary">{cta_text}</a>
            </div>
        </div>
    </section>

    <!-- P: PROOF PYRAMID (Testimonials with Structure) -->
    <section class="testimonials-section">
        <div class="container">
            <h2 class="section-title">{copy.get('social_proof_headline', 'Real Results From Real People')}</h2>
            <p style="text-align: center; color: {"rgba(255,255,255,0.7)" if is_dark else "var(--text-secondary)"}; margin-bottom: 50px;">
                Don't just take our word for it - see what others have achieved
            </p>
            <!-- Testimonials Grid with Result Badges -->
            <div class="testimonials-grid">
                {testimonials_html}
            </div>
        </div>
    </section>

    <!-- O: OBJECTION HANDLING (FAQ as Objection Removal) -->
    <section class="faq-section">
        <div class="container">
            <h2 class="section-title">Still Have Questions?</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 40px;">
                We've answered the most common concerns below
            </p>
            <div class="faq-container">
                {faq_html}
            </div>
        </div>
    </section>

    <!-- S: SIMPLE NEXT STEP (Offer Stack + Single CTA) -->
    <section class="offer-stack-section" style="padding: 100px 0; background: {"#141414" if is_dark else "#f8fafc"};">
        <div class="container" style="max-width: 800px;">
            <h2 class="section-title" style="margin-bottom: 20px;">Everything You Get Today</h2>
            <p style="text-align: center; color: var(--text-secondary); margin-bottom: 40px;">
                One investment. Complete transformation.
            </p>
            <!-- Offer Stack Card -->
            <div class="offer-stack" style="background: var(--bg-card); border-radius: {brutal_radius}; padding: 40px; border: {brutal_border}; box-shadow: {"8px 8px 0 #000" if is_brutal else "0 10px 40px rgba(0,0,0,0.1)"};">
                {"".join([f'''
                <div class="offer-item" style="display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid {"rgba(255,255,255,0.1)" if is_dark else "rgba(0,0,0,0.1)"};">
                    <span style="font-weight: 500; display: flex; align-items: center; gap: 10px;"><span style="color: var(--primary);">✓</span> {item.get("item", "Bonus")}</span>
                    <span style="color: var(--text-secondary); text-decoration: line-through;">{item.get("value", "$XXX")}</span>
                </div>
                ''' for item in copy.get("offer_stack", [{"item": "Core Program", "value": "$997"}, {"item": "Bonus Training", "value": "$297"}, {"item": "Templates & Resources", "value": "$197"}])])}
                <!-- Total Value vs Price -->
                <div class="offer-total" style="padding-top: 30px; text-align: center; border-top: 2px solid var(--primary);">
                    <p style="font-size: 1rem; color: var(--text-secondary); margin-bottom: 5px; text-decoration: line-through;">{copy.get("total_value", "Total Value: $1,491")}</p>
                    <p style="font-size: 3rem; font-weight: 800; color: var(--primary); font-family: var(--font-display); margin: 10px 0;">Today Only: {self.price or "$497"}</p>
                </div>
            </div>
            <!-- Final CTA Button -->
            <div style="text-align: center; margin-top: 40px;">
                <a href="{cta_url}" class="cta-primary" style="font-size: 1.3rem; padding: 22px 60px; display: inline-block;">{cta_text}</a>
            </div>
            <!-- Guarantee Badge -->
            <div style="text-align: center; margin-top: 30px; padding: 25px; background: {"rgba(16,185,129,0.1)" if is_dark else "rgba(16,185,129,0.05)"}; border-radius: {brutal_radius}; border: {"3px solid #000" if is_brutal else "1px solid rgba(16,185,129,0.3)"};">
                <p style="font-weight: 600; color: {"#34d399" if is_dark else "#059669"}; margin: 0; font-size: 1.1rem;">
                    🛡️ {copy.get('guarantee', '30-Day Money-Back Guarantee - No Questions Asked')}
                </p>
            </div>
        </div>
    </section>

    <!-- URGENCY CLOSE (Final CTA Section) -->
    <section class="cta-section" id="signup">
        <div class="container">
            <h2>{copy.get('final_cta_headline', 'Your Transformation Starts Now')}</h2>
            <p style="max-width: 600px; margin: 0 auto 30px; color: rgba(255,255,255,0.9);">{copy.get('urgency_text', 'Limited spots available')}</p>
            {price_html}
            <a href="{cta_url}" class="cta-primary" style="font-size: 1.2rem; padding: 20px 50px;">{cta_text}</a>
            <p style="margin-top: 20px; color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                Join {copy.get('social_proof_header', 'thousands of others').replace('Join ', '').replace('join ', '')} who already made the decision
            </p>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>{self.product}</h4>
                    <p style="color: rgba(255,255,255,0.7);">{copy.get('subheadline', '')[:100]}</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <a href="#features">Features</a>
                    <a href="#signup">Get Started</a>
                    <a href="#">Contact</a>
                </div>
                <div class="footer-section">
                    <h4>Legal</h4>
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                    <a href="#">Refund Policy</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} {self.product}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        function toggleFaq(button) {{
            const item = button.parentElement;
            item.classList.toggle('active');
        }}
    </script>
</body>
</html>'''

        self.log("HTML generation complete", "SUCCESS")
        return html

    def save_locally(self, html: str) -> Path:
        """Save landing page files locally"""
        self.log(f"Saving to {self.output_path}...", "INFO")

        # Save HTML
        index_file = self.output_path / "index.html"
        index_file.write_text(html, encoding="utf-8")

        # Save metadata
        metadata = {
            "product": self.product,
            "headline": self.copy_data.get("headline", ""),
            "style": self.style,
            "generated_at": datetime.now().isoformat(),
            "files": ["index.html"]
        }

        metadata_file = self.output_path / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        # Save copy data for reference
        copy_file = self.output_path / "copy_data.json"
        with open(copy_file, "w") as f:
            json.dump(self.copy_data, f, indent=2)

        self.log(f"Files saved to {self.output_path}", "SUCCESS")
        return self.output_path

    def deploy_to_cloudflare(self) -> Optional[dict]:
        """Deploy landing page to Cloudflare Pages"""
        self.log("Deploying to Cloudflare Pages...", "INFO")

        if not self.cloudflare_token or not self.cloudflare_account_id:
            self.log("Cloudflare credentials not configured", "WARNING")
            self.log("Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in .env", "WARNING")
            return None

        project_name = self.project_name or f"landing-{self.project_slug}"

        # Try using wrangler CLI first (more reliable for file uploads)
        try:
            result = subprocess.run(
                [
                    "npx", "wrangler", "pages", "deploy",
                    str(self.output_path),
                    "--project-name", project_name
                ],
                capture_output=True,
                text=True,
                timeout=120,
                env={
                    **os.environ,
                    "CLOUDFLARE_API_TOKEN": self.cloudflare_token,
                    "CLOUDFLARE_ACCOUNT_ID": self.cloudflare_account_id
                }
            )

            if result.returncode == 0:
                # Parse URL from output
                output = result.stdout + result.stderr
                url_match = re.search(r'(https://[^\s]+\.pages\.dev)', output)
                live_url = url_match.group(1) if url_match else f"https://{project_name}.pages.dev"

                self.log(f"Deployed successfully: {live_url}", "SUCCESS")
                return {
                    "success": True,
                    "liveUrl": live_url,
                    "projectName": project_name
                }
            else:
                self.log(f"Wrangler deployment failed: {result.stderr}", "WARNING")

        except FileNotFoundError:
            self.log("Wrangler not found, trying API deployment...", "WARNING")
        except subprocess.TimeoutExpired:
            self.log("Wrangler deployment timed out", "WARNING")
        except Exception as e:
            self.log(f"Wrangler error: {e}", "WARNING")

        # Fallback: Try API deployment
        return self._deploy_via_api(project_name)

    def _deploy_via_api(self, project_name: str) -> Optional[dict]:
        """Deploy using Cloudflare API directly"""
        try:
            base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account_id}/pages/projects"
            headers = {
                "Authorization": f"Bearer {self.cloudflare_token}",
                "Content-Type": "application/json"
            }

            # Check if project exists, create if not
            check_response = requests.get(f"{base_url}/{project_name}", headers=headers)

            if check_response.status_code == 404:
                # Create project
                create_response = requests.post(
                    base_url,
                    headers=headers,
                    json={"name": project_name, "production_branch": "main"}
                )
                if create_response.status_code not in [200, 201]:
                    self.log(f"Failed to create project: {create_response.text}", "ERROR")
                    return None

            # For API deployment, we need to use the deployment endpoint
            # Note: Direct file upload via API is complex, wrangler is preferred
            live_url = f"https://{project_name}.pages.dev"

            self.log(f"Project ready at: {live_url}", "SUCCESS")
            self.log("Note: For full deployment, use 'npx wrangler pages deploy'", "INFO")

            return {
                "success": True,
                "liveUrl": live_url,
                "projectName": project_name,
                "note": "Project created. Run wrangler command to complete deployment."
            }

        except Exception as e:
            self.log(f"API deployment error: {e}", "ERROR")
            return None

    def execute(self) -> dict:
        """Execute the complete landing page generation pipeline"""
        self.log(f"🚀 Starting Landing Page Generation for: {self.product}", "INFO")
        self.log(f"   Style: {self.design_config['name']}", "INFO")

        start_time = time.time()

        # Step 1: Market Research (optional)
        if self.do_research:
            self.research_data = self.research_market()

        # Step 2: Generate Copy
        self.copy_data = self.generate_copy()

        # Override with user-provided values
        if self.headline:
            self.copy_data["headline"] = self.headline
        if self.subheadline:
            self.copy_data["subheadline"] = self.subheadline

        # Step 3: Generate HTML
        html = self.generate_html()

        # Step 4: Save Locally
        output_path = self.save_locally(html)

        # Step 5: Deploy (optional)
        deployment_result = None
        if self.do_deploy:
            deployment_result = self.deploy_to_cloudflare()

        # Calculate execution time
        execution_time = time.time() - start_time
        minutes = int(execution_time // 60)
        seconds = int(execution_time % 60)

        # Build result
        result = {
            "success": True,
            "product": self.product,
            "headline": self.copy_data.get("headline", ""),
            "style": self.style,
            "executionTime": f"{minutes}m {seconds}s",
            "localFiles": str(output_path),
            "files": {
                "html": str(output_path / "index.html"),
                "metadata": str(output_path / "metadata.json"),
                "copyData": str(output_path / "copy_data.json")
            }
        }

        if deployment_result:
            result["deployment"] = deployment_result
            result["liveUrl"] = deployment_result.get("liveUrl")

        # Save result
        result_file = output_path / "result.json"
        with open(result_file, "w") as f:
            json.dump(result, f, indent=2)

        self.log("=" * 50, "INFO")
        self.log(f"✅ LANDING PAGE COMPLETE: {self.product}", "SUCCESS")
        self.log(f"   Execution time: {minutes}m {seconds}s", "INFO")
        self.log(f"   Local files: {output_path}", "INFO")
        if deployment_result:
            self.log(f"   Live URL: {deployment_result.get('liveUrl', 'N/A')}", "INFO")
        self.log("=" * 50, "INFO")

        return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate beautiful landing pages with AI and deploy to Cloudflare"
    )

    parser.add_argument("--product", "-p", required=True, help="Product or service name")
    parser.add_argument("--headline", "-H", help="Main headline (AI generates if not provided)")
    parser.add_argument("--subheadline", help="Supporting subheadline")
    parser.add_argument("--price", help="Price point (e.g., $497)")
    parser.add_argument("--target-audience", "-t", help="Target audience description")
    parser.add_argument("--website", "-w", help="Company website for research")
    parser.add_argument("--style", "-s", default="modern-gradient",
                       choices=list(DESIGN_STYLES.keys()),
                       help="Design style")
    parser.add_argument("--research", "-r", action="store_true",
                       help="Run market research first")
    parser.add_argument("--deploy", "-d", action="store_true",
                       help="Deploy to Cloudflare Pages")
    parser.add_argument("--project-name", help="Cloudflare Pages project name")
    parser.add_argument("--output-dir", "-o", help="Output directory")
    parser.add_argument("--cta-text", help="CTA button text")
    parser.add_argument("--cta-url", help="CTA button URL")

    args = parser.parse_args()

    generator = LandingPageGenerator(
        product=args.product,
        headline=args.headline,
        subheadline=args.subheadline,
        price=args.price,
        target_audience=args.target_audience,
        website=args.website,
        style=args.style,
        research=args.research,
        deploy=args.deploy,
        project_name=args.project_name,
        output_dir=args.output_dir,
        cta_text=args.cta_text,
        cta_url=args.cta_url
    )

    result = generator.execute()

    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
