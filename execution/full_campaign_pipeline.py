#!/usr/bin/env python3
"""
Full Campaign Builder Pipeline

Complete end-to-end campaign generation:
1. Client Research (company, audience, competitors)
2. Meta Ads Manager Setup (via API)
3. Ad Copy Generation
4. Ad Image Generation
5. Landing Page Generation
6. Landing Page Image Generation
7. CRM Lead Flow Setup
8. Follow-up Email Sequences

Usage:
    python3 execution/full_campaign_pipeline.py \
        --client "Acme Corp" \
        --website "https://acmecorp.com" \
        --offer "AI Lead Generation" \
        --budget 5000 \
        --output-dir .tmp/campaigns/acme

Follows directive: directives/full_campaign_pipeline.md
"""

import os
import sys
import json
import argparse
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class CampaignPipeline:
    """Full campaign generation pipeline."""

    def __init__(self, client_name: str, website: str, offer: str, output_dir: Path):
        self.client_name = client_name
        self.website = website
        self.offer = offer
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.research = {}
        self.ad_copy = {}
        self.landing_page = {}
        self.email_sequence = {}
        self.images = {}
        self.meta_ads_context = self._load_meta_ads_skill_bible()

    def _load_meta_ads_skill_bible(self) -> str:
        """Load Meta Ads Manager skill bible for enhanced context."""
        skill_path = Path(__file__).parent.parent / "skills" / "SKILL_BIBLE_meta_ads_manager_technical.md"
        if skill_path.exists():
            content = skill_path.read_text(encoding="utf-8")
            # Extract key sections for context
            sections = []
            for section in ["## Core Principles", "## Best Practices", "## Common Mistakes"]:
                if section in content:
                    start = content.find(section)
                    # Find next section
                    next_section = content.find("\n## ", start + len(section))
                    if next_section > start:
                        sections.append(content[start:next_section])
                    else:
                        sections.append(content[start:start + 2000])
            return "\n".join(sections)[:4000]  # Limit context size
        return ""
        
    def log(self, message: str):
        print(f"  {message}")
        
    def call_llm(self, prompt: str, max_tokens: int = 4000) -> str:
        """Call Claude via OpenRouter."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY required")
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-sonnet-4",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": max_tokens
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"LLM API error: {response.status_code} - {response.text}")
    
    def call_perplexity(self, query: str) -> str:
        """Call Perplexity for research with retry and fallback."""
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            self.log("Warning: No Perplexity API key, using LLM for research")
            return self.call_llm(f"Research the following:\n\n{query}")
        
        for attempt in range(2):
            try:
                response = requests.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "sonar",
                        "messages": [{"role": "user", "content": query}],
                        "temperature": 0.2,
                        "max_tokens": 2000
                    },
                    timeout=90
                )
                
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    self.log(f"Perplexity error {response.status_code}, retrying...")
            except requests.exceptions.Timeout:
                self.log(f"Perplexity timeout (attempt {attempt+1}/2)")
            except Exception as e:
                self.log(f"Perplexity error: {e}")
        
        self.log("Falling back to LLM for research")
        return self.call_llm(f"Research the following:\n\n{query}")
    
    # =========================================================================
    # PHASE 1: CLIENT RESEARCH
    # =========================================================================
    
    def phase_1_research(self) -> dict:
        """Phase 1: Deep client and market research."""
        print("\n[PHASE 1/8] Client Research")
        print("-" * 40)
        
        # Company research
        self.log("Researching company...")
        company_research = self.call_perplexity(f"""
Research {self.client_name} ({self.website}):
- Company overview and mission
- Core products/services
- Target market
- Company size and stage
- Recent news
- Social media presence
""")
        
        # Audience research
        self.log("Researching target audience...")
        audience_research = self.call_perplexity(f"""
Research the target audience for {self.offer} by {self.client_name}:
- Demographics (job titles, company size, industry)
- Primary pain points (list 5+)
- Current solutions they use
- Buying triggers and motivations
- Common objections
- Language and terminology they use
""")
        
        # Competitor research
        self.log("Researching competitors...")
        competitor_research = self.call_perplexity(f"""
Research competitors of {self.client_name} offering {self.offer}:
- Top 5 direct competitors
- How they position their offers
- Pricing comparison
- Strengths and weaknesses
- Market gaps and opportunities
""")
        
        # Synthesize research
        self.log("Synthesizing research dossier...")
        synthesis_prompt = f"""
Based on this research, create a comprehensive client dossier:

COMPANY RESEARCH:
{company_research}

AUDIENCE RESEARCH:
{audience_research}

COMPETITOR RESEARCH:
{competitor_research}

Create a structured JSON dossier with:
{{
    "company": {{
        "name": "",
        "website": "",
        "overview": "",
        "core_offer": "",
        "unique_value_proposition": ""
    }},
    "target_audience": {{
        "demographics": "",
        "pain_points": [],
        "desires": [],
        "objections": [],
        "buying_triggers": []
    }},
    "transformation": {{
        "before_state": "",
        "after_state": "",
        "mechanism": ""
    }},
    "competitors": [],
    "messaging_angles": [],
    "hooks": []
}}

Output ONLY valid JSON.
"""
        
        dossier_text = self.call_llm(synthesis_prompt)
        
        # Extract JSON
        try:
            # Find JSON in response
            import re
            json_match = re.search(r'\{[\s\S]*\}', dossier_text)
            if json_match:
                self.research = json.loads(json_match.group())
            else:
                self.research = {"raw": dossier_text}
        except json.JSONDecodeError:
            self.research = {"raw": dossier_text}
        
        # Save research
        research_file = self.output_dir / "01_research.json"
        with open(research_file, "w") as f:
            json.dump(self.research, f, indent=2)
        
        self.log(f"Saved: {research_file}")
        return self.research
    
    # =========================================================================
    # PHASE 2: META ADS SETUP
    # =========================================================================
    
    def phase_2_meta_ads_setup(self, budget: float = 5000) -> dict:
        """Phase 2: Generate Meta Ads campaign structure."""
        print("\n[PHASE 2/8] Meta Ads Campaign Setup")
        print("-" * 40)

        self.log("Generating campaign structure...")

        # Add skill bible context for enhanced Meta Ads expertise
        meta_expertise = """
META ADS EXPERTISE (Apply these principles):
- Create PERSONA-LED creative strategy - persona changes drive 10x more impact than copy changes
- Ensure TRUE creative diversity - vary location, narrative, AND person across variations
- Focus on INCREMENTAL REACH - optimize for reaching new audiences, not increased frequency
- Technical setup first - proper pixel implementation, Conversions API, audience infrastructure
- Budget allocation: 70% proven performers, 30% testing
- Maintain 50+ conversions per week per ad set for optimization
- Apply Andromeda update strategies for 2025/2026
"""
        if self.meta_ads_context:
            meta_expertise += f"\n\nDETAILED CONTEXT:\n{self.meta_ads_context[:2000]}"

        prompt = f"""
Create a complete Meta Ads campaign structure for:

CLIENT: {self.client_name}
OFFER: {self.offer}
MONTHLY BUDGET: ${budget}
TARGET AUDIENCE: {json.dumps(self.research.get('target_audience', {}), indent=2)[:2000]}

{meta_expertise}

Generate a campaign structure with:

1. **Campaign Settings**
   - Campaign name
   - Objective (conversions, leads, etc.)
   - Budget allocation strategy

2. **Ad Sets** (create 3-5 ad sets)
   For each ad set:
   - Name
   - Targeting (interests, behaviors, demographics)
   - Placements
   - Budget allocation
   - Bid strategy

3. **Audience Segments**
   - Cold audience definitions
   - Warm audience (retargeting) definitions
   - Lookalike audience strategy

4. **Testing Strategy**
   - What to test first
   - How to scale winners
   - Kill criteria for losers

Format as detailed JSON structure ready for API integration.
"""
        
        campaign_structure = self.call_llm(prompt, max_tokens=4000)
        
        # Parse and save
        self.meta_ads = {
            "client": self.client_name,
            "budget": budget,
            "structure": campaign_structure,
            "generated_at": datetime.now().isoformat()
        }
        
        ads_file = self.output_dir / "02_meta_ads_setup.json"
        with open(ads_file, "w") as f:
            json.dump(self.meta_ads, f, indent=2)
        
        # Also save readable version
        ads_md = self.output_dir / "02_meta_ads_setup.md"
        ads_md.write_text(f"""# Meta Ads Campaign Setup: {self.client_name}

**Budget:** ${budget}/month
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{campaign_structure}
""", encoding="utf-8")
        
        self.log(f"Saved: {ads_file}")
        return self.meta_ads
    
    # =========================================================================
    # PHASE 3: AD COPY GENERATION
    # =========================================================================
    
    def phase_3_ad_copy(self) -> dict:
        """Phase 3: Generate ad copy variations."""
        print("\n[PHASE 3/8] Ad Copy Generation")
        print("-" * 40)

        self.log("Generating ad copy variations...")

        # Enhanced prompt with Meta Ads skill bible context
        creative_expertise = """
META ADS CREATIVE PRINCIPLES (Apply these):
- PERSONA-LED variations - create truly different personas, not just copy changes
- EMOTIONAL narratives - connect personally, avoid rational feature lists
- MOBILE-FIRST - 90%+ of Meta traffic is mobile, design for thumb-stopping
- STRONG HOOKS - must stop scroll within first 3 seconds
- TRUE DIVERSITY - vary location, narrative, AND person across variations
- INCREMENTAL REACH focus - creative should unlock new audiences
"""

        prompt = f"""
Create high-converting Meta ad copy for:

CLIENT: {self.client_name}
OFFER: {self.offer}
TARGET AUDIENCE PAIN POINTS: {json.dumps(self.research.get('target_audience', {}).get('pain_points', []))}
HOOKS: {json.dumps(self.research.get('hooks', []))}
TRANSFORMATION: {json.dumps(self.research.get('transformation', {}))}

{creative_expertise}

Generate 10 ad copy variations across these formats:

**FORMAT 1: Problem-Agitate-Solve (3 variations)**
- Hook with problem
- Agitate the pain
- Present solution

**FORMAT 2: Story-Based (3 variations)**
- Before story
- Transformation moment
- After results

**FORMAT 3: Direct Response (2 variations)**
- Clear hook
- Benefits
- Strong CTA

**FORMAT 4: Social Proof (2 variations)**
- Lead with results/testimonial
- Explain how
- CTA

For each ad include:
- Primary text (125 chars for feed, can be longer)
- Headline (40 chars)
- Description (30 chars)
- CTA button recommendation

Format as structured output I can directly use.
"""
        
        ad_copy = self.call_llm(prompt, max_tokens=4000)
        
        self.ad_copy = {
            "client": self.client_name,
            "variations": ad_copy,
            "generated_at": datetime.now().isoformat()
        }
        
        copy_file = self.output_dir / "03_ad_copy.md"
        copy_file.write_text(f"""# Ad Copy: {self.client_name}

**Offer:** {self.offer}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{ad_copy}
""", encoding="utf-8")
        
        self.log(f"Saved: {copy_file}")
        return self.ad_copy
    
    # =========================================================================
    # PHASE 4: AD IMAGE GENERATION
    # =========================================================================
    
    def phase_4_ad_images(self) -> dict:
        """Phase 4: Generate ad image prompts and images."""
        print("\n[PHASE 4/8] Ad Image Generation")
        print("-" * 40)
        
        self.log("Generating image prompts...")
        
        prompt = f"""
Create image generation prompts for Meta ads for:

CLIENT: {self.client_name}
OFFER: {self.offer}
TARGET AUDIENCE: {json.dumps(self.research.get('target_audience', {}).get('demographics', ''))}

Generate 5 ad image concepts with detailed prompts for AI image generation:

**IMAGE 1: Problem Visual**
- Show the pain point visually
- Prompt for DALL-E/Midjourney

**IMAGE 2: Solution/Transformation**
- Show the after state
- Prompt for DALL-E/Midjourney

**IMAGE 3: Social Proof Style**
- Results/numbers focused
- Prompt for DALL-E/Midjourney

**IMAGE 4: Pattern Interrupt**
- Scroll-stopping visual
- Prompt for DALL-E/Midjourney

**IMAGE 5: Lifestyle/Aspiration**
- Desired outcome visualization
- Prompt for DALL-E/Midjourney

For each include:
- Concept description
- Detailed image prompt (ready for DALL-E 3)
- Recommended dimensions (1080x1080, 1200x628, etc.)
- Text overlay suggestions
"""
        
        image_prompts = self.call_llm(prompt, max_tokens=3000)
        
        self.images["ad_prompts"] = image_prompts
        
        # Generate actual images if FAL_KEY available
        if os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY"):
            self.log("Generating images with Nano Banana Pro...")
            self._generate_images_nano_banana(image_prompts, "ad")
        else:
            self.log("Note: Set FAL_KEY to generate actual images")
        
        images_file = self.output_dir / "04_ad_images.md"
        images_file.write_text(f"""# Ad Image Prompts: {self.client_name}

**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{image_prompts}
""", encoding="utf-8")
        
        self.log(f"Saved: {images_file}")
        return self.images
    
    def _generate_images_nano_banana(self, prompts_text: str, prefix: str):
        """Generate images using fal.ai Nano Banana Pro."""
        fal_key = os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY")
        if not fal_key:
            self.log("FAL_KEY not set, skipping image generation")
            return
        
        # Extract prompts (simplified)
        import re
        prompt_matches = re.findall(r'Prompt[:\s]*["\']?([^"\']+)["\']?', prompts_text, re.IGNORECASE)
        
        images_dir = self.output_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        for i, prompt in enumerate(prompt_matches[:3], 1):  # Limit to 3 for cost
            try:
                self.log(f"  Generating image {i} with Nano Banana Pro...")
                response = requests.post(
                    "https://fal.run/fal-ai/nano-banana-pro",
                    headers={
                        "Authorization": f"Key {fal_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": prompt[:2000],
                        "aspect_ratio": "1:1",
                        "resolution": "2K"
                    },
                    timeout=180
                )
                
                if response.status_code == 200:
                    result = response.json()
                    images = result.get("images", [])
                    if images:
                        image_url = images[0].get("url")
                        if image_url:
                            img_response = requests.get(image_url, timeout=60)
                            if img_response.status_code == 200:
                                img_path = images_dir / f"{prefix}_image_{i}.png"
                                with open(img_path, "wb") as f:
                                    f.write(img_response.content)
                                self.log(f"    Saved: {img_path}")
                else:
                    self.log(f"    Error: {response.status_code} - {response.text[:100]}")
                
            except Exception as e:
                self.log(f"    Error generating image {i}: {e}")
    
    # =========================================================================
    # PHASE 5: LANDING PAGE GENERATION
    # =========================================================================
    
    def phase_5_landing_page(self) -> dict:
        """Phase 5: Generate landing page copy and structure."""
        print("\n[PHASE 5/8] Landing Page Generation")
        print("-" * 40)
        
        self.log("Generating landing page...")
        
        prompt = f"""
Create a high-converting landing page for:

CLIENT: {self.client_name}
OFFER: {self.offer}
TRANSFORMATION: {json.dumps(self.research.get('transformation', {}))}
PAIN POINTS: {json.dumps(self.research.get('target_audience', {}).get('pain_points', []))}
HOOKS: {json.dumps(self.research.get('hooks', []))}

Generate a complete landing page with these sections:

**ABOVE THE FOLD**
- Headline (attention-grabbing, benefit-focused)
- Subheadline (clarify the offer)
- Hero section copy
- Primary CTA button text
- Social proof element

**PROBLEM SECTION**
- Problem headline
- 3-5 pain point bullets
- Agitation copy

**SOLUTION SECTION**
- Solution headline
- How it works (3 steps)
- Mechanism explanation

**BENEFITS SECTION**
- 5-7 benefit bullets with icons
- Feature-to-benefit statements

**SOCIAL PROOF SECTION**
- Testimonial suggestions
- Case study outline
- Results/numbers to highlight

**FAQ SECTION**
- 5-7 common questions and answers

**FINAL CTA SECTION**
- Urgency/scarcity element
- Final headline
- CTA button text
- Risk reversal (guarantee)

**FORM FIELDS**
- Recommended fields to collect
- Application questions (if applicable)

Format as clean markdown ready for a designer/developer.
"""
        
        landing_page = self.call_llm(prompt, max_tokens=5000)
        
        self.landing_page = {
            "client": self.client_name,
            "content": landing_page,
            "generated_at": datetime.now().isoformat()
        }
        
        lp_file = self.output_dir / "05_landing_page.md"
        lp_file.write_text(f"""# Landing Page: {self.client_name}

**Offer:** {self.offer}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{landing_page}
""", encoding="utf-8")
        
        self.log(f"Saved: {lp_file}")
        return self.landing_page
    
    # =========================================================================
    # PHASE 6: LANDING PAGE IMAGES
    # =========================================================================
    
    def phase_6_landing_page_images(self) -> dict:
        """Phase 6: Generate landing page image prompts."""
        print("\n[PHASE 6/8] Landing Page Images")
        print("-" * 40)
        
        self.log("Generating landing page image prompts...")
        
        prompt = f"""
Create image prompts for landing page sections:

CLIENT: {self.client_name}
OFFER: {self.offer}

Generate prompts for:

**1. HERO IMAGE**
- Main above-the-fold visual
- Should convey transformation
- Detailed DALL-E prompt

**2. PROBLEM SECTION IMAGE**
- Visual representation of pain
- Before state
- Detailed DALL-E prompt

**3. SOLUTION SECTION IMAGE**
- Product/service in action
- The mechanism at work
- Detailed DALL-E prompt

**4. RESULTS/SOCIAL PROOF IMAGE**
- Success visualization
- Charts, graphs, or lifestyle
- Detailed DALL-E prompt

**5. ABOUT/TRUST IMAGE**
- Professional credibility
- Team or founder visual
- Detailed DALL-E prompt

For each provide:
- Section name
- Concept description
- Detailed DALL-E 3 prompt (be specific about style, composition, lighting)
- Recommended dimensions
"""
        
        lp_image_prompts = self.call_llm(prompt, max_tokens=3000)
        
        self.images["landing_page_prompts"] = lp_image_prompts
        
        if os.getenv("FAL_KEY") or os.getenv("FAL_API_KEY"):
            self.log("Generating landing page images with Nano Banana Pro...")
            self._generate_images_nano_banana(lp_image_prompts, "lp")
        
        lp_images_file = self.output_dir / "06_landing_page_images.md"
        lp_images_file.write_text(f"""# Landing Page Images: {self.client_name}

**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{lp_image_prompts}
""", encoding="utf-8")
        
        self.log(f"Saved: {lp_images_file}")
        return self.images
    
    # =========================================================================
    # PHASE 7: CRM SETUP
    # =========================================================================
    
    def phase_7_crm_setup(self) -> dict:
        """Phase 7: Generate CRM pipeline and automation setup."""
        print("\n[PHASE 7/8] CRM Pipeline Setup")
        print("-" * 40)
        
        self.log("Generating CRM configuration...")
        
        prompt = f"""
Create a complete CRM pipeline and automation setup for:

CLIENT: {self.client_name}
OFFER: {self.offer}

Generate:

**1. PIPELINE STAGES**
Define each stage with:
- Stage name
- Stage goal
- Automation triggers
- Time limits

Example stages:
- New Lead
- Contacted
- Qualified
- Appointment Set
- No Show
- Showed Up
- Proposal Sent
- Closed Won
- Closed Lost
- Nurture

**2. LEAD SCORING**
- Scoring criteria
- Point values
- Qualification threshold

**3. AUTOMATION TRIGGERS**
For each key event:
- New lead created
- Lead qualified
- Appointment booked
- No show
- Post-call follow up
- Nurture sequence trigger

**4. TAGS/LABELS**
- Lead source tags
- Status tags
- Interest level tags
- Custom tags

**5. CUSTOM FIELDS**
- Required fields for this business
- Field types (text, dropdown, date, etc.)

**6. INTEGRATION POINTS**
- Calendar integration
- Email integration
- SMS integration
- Payment integration

Format as implementation-ready JSON/configuration.
"""
        
        crm_setup = self.call_llm(prompt, max_tokens=4000)
        
        self.crm_config = {
            "client": self.client_name,
            "configuration": crm_setup,
            "generated_at": datetime.now().isoformat()
        }
        
        crm_file = self.output_dir / "07_crm_setup.md"
        crm_file.write_text(f"""# CRM Setup: {self.client_name}

**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{crm_setup}
""", encoding="utf-8")
        
        self.log(f"Saved: {crm_file}")
        return self.crm_config
    
    # =========================================================================
    # PHASE 8: FOLLOW-UP SEQUENCES
    # =========================================================================
    
    def phase_8_followup_sequences(self) -> dict:
        """Phase 8: Generate email/SMS follow-up sequences."""
        print("\n[PHASE 8/8] Follow-up Sequences")
        print("-" * 40)
        
        self.log("Generating follow-up sequences...")
        
        prompt = f"""
Create complete follow-up sequences for:

CLIENT: {self.client_name}
OFFER: {self.offer}
TRANSFORMATION: {json.dumps(self.research.get('transformation', {}))}
OBJECTIONS: {json.dumps(self.research.get('target_audience', {}).get('objections', []))}

Generate these sequences:

**SEQUENCE 1: WELCOME SEQUENCE (5 emails)**
After lead opts in:
- Email 1: Immediate - Welcome + deliver lead magnet
- Email 2: Day 1 - Story + credibility
- Email 3: Day 2 - Problem agitation
- Email 4: Day 3 - Solution mechanism
- Email 5: Day 4 - Case study + CTA

**SEQUENCE 2: PRE-CALL SEQUENCE (3 emails + 2 SMS)**
After booking call:
- Confirmation email
- Day before reminder
- Hour before reminder
- SMS reminders

**SEQUENCE 3: NO-SHOW SEQUENCE (4 emails + 2 SMS)**
If they miss the call:
- Immediate - Reschedule link
- Day 1 - Why they should reschedule
- Day 3 - FOMO/urgency
- Day 7 - Final attempt

**SEQUENCE 4: POST-CALL NURTURE (7 emails)**
If they don't close:
- Day 1 - Thank you + resources
- Day 3 - Address objection #1
- Day 5 - Case study
- Day 7 - Address objection #2
- Day 10 - Limited time offer
- Day 14 - Final value add
- Day 21 - Check in

**SEQUENCE 5: LONG-TERM NURTURE (ongoing)**
- Monthly newsletter framework
- Re-engagement triggers

For each email provide:
- Subject line (with A/B variant)
- Preview text
- Full email body
- CTA

For SMS provide:
- Message text (under 160 chars)
- Timing
"""
        
        sequences = self.call_llm(prompt, max_tokens=6000)
        
        self.email_sequence = {
            "client": self.client_name,
            "sequences": sequences,
            "generated_at": datetime.now().isoformat()
        }
        
        seq_file = self.output_dir / "08_followup_sequences.md"
        seq_file.write_text(f"""# Follow-up Sequences: {self.client_name}

**Offer:** {self.offer}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}

---

{sequences}
""", encoding="utf-8")
        
        self.log(f"Saved: {seq_file}")
        return self.email_sequence
    
    # =========================================================================
    # RUN FULL PIPELINE
    # =========================================================================
    
    def run(self, budget: float = 5000) -> dict:
        """Run the complete campaign pipeline."""
        start_time = time.time()
        
        print("=" * 60)
        print(f"FULL CAMPAIGN PIPELINE: {self.client_name}")
        print("=" * 60)
        print(f"Website: {self.website}")
        print(f"Offer: {self.offer}")
        print(f"Budget: ${budget}/month")
        print("=" * 60)
        
        results = {}
        
        # Phase 1: Research
        results["research"] = self.phase_1_research()
        
        # Phase 2: Meta Ads Setup
        results["meta_ads"] = self.phase_2_meta_ads_setup(budget)
        
        # Phase 3: Ad Copy
        results["ad_copy"] = self.phase_3_ad_copy()
        
        # Phase 4: Ad Images
        results["ad_images"] = self.phase_4_ad_images()
        
        # Phase 5: Landing Page
        results["landing_page"] = self.phase_5_landing_page()
        
        # Phase 6: Landing Page Images
        results["lp_images"] = self.phase_6_landing_page_images()
        
        # Phase 7: CRM Setup
        results["crm"] = self.phase_7_crm_setup()
        
        # Phase 8: Follow-up Sequences
        results["sequences"] = self.phase_8_followup_sequences()
        
        # Save master output
        master_file = self.output_dir / "00_campaign_master.json"
        with open(master_file, "w") as f:
            json.dump({
                "client": self.client_name,
                "website": self.website,
                "offer": self.offer,
                "budget": budget,
                "generated_at": datetime.now().isoformat(),
                "files": [str(f) for f in self.output_dir.glob("*.md")]
            }, f, indent=2)
        
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("CAMPAIGN PIPELINE COMPLETE")
        print("=" * 60)
        print(f"Time: {elapsed/60:.1f} minutes")
        print(f"\nOutput files in: {self.output_dir}")
        for f in sorted(self.output_dir.glob("*.md")):
            print(f"  - {f.name}")
        print("=" * 60)
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate complete campaign from research to follow-up"
    )
    
    parser.add_argument("--client", required=True, help="Client/company name")
    parser.add_argument("--website", required=True, help="Client website")
    parser.add_argument("--offer", required=True, help="Main offer/product")
    parser.add_argument("--budget", type=float, default=5000, help="Monthly ad budget (default: 5000)")
    parser.add_argument("--output-dir", default=".tmp/campaigns", help="Output directory")
    
    args = parser.parse_args()
    
    # Create output directory with client name
    safe_client = args.client.lower().replace(" ", "_")[:30]
    output_dir = Path(args.output_dir) / safe_client
    
    pipeline = CampaignPipeline(
        client_name=args.client,
        website=args.website,
        offer=args.offer,
        output_dir=output_dir
    )
    
    pipeline.run(budget=args.budget)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
