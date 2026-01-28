# AI Landing Page Generator (Droid/Claude Code)

## What This Workflow Is
**Master orchestrator** that generates beautiful, high-converting landing pages using AI (Claude/Droid) and automatically publishes them to Cloudflare Pages. Creates complete HTML/CSS landing pages with modern design, responsive layouts, and conversion-optimized copy.

## What It Does
1. Receives offer, product, or campaign details from user
2. Researches target audience and competitive landscape
3. Generates conversion-optimized copy using AI
4. Creates beautiful HTML/CSS landing page with modern design
5. Generates responsive mobile-first layouts
6. Deploys to Cloudflare Pages automatically
7. Returns live URL and backup files

## Prerequisites

### Required API Keys (add to .env)
```
OPENROUTER_API_KEY=your_openrouter_key     # AI generation (Claude)
CLOUDFLARE_API_TOKEN=your_cf_api_token     # Cloudflare Pages deployment
CLOUDFLARE_ACCOUNT_ID=your_cf_account_id   # Cloudflare account ID
PERPLEXITY_API_KEY=your_perplexity_key     # Market research (optional)
```

### Cloudflare Setup
1. Create API Token: https://dash.cloudflare.com/profile/api-tokens
2. Permissions needed: `Cloudflare Pages: Edit`
3. Get Account ID from dashboard URL or Zone Overview

### Installation
```bash
pip install requests python-dotenv jinja2
npm install -g wrangler  # Optional: for CLI deployment
```

## How to Run

### Option 1: Python Script (Recommended)
```bash
python3 execution/generate_landing_page.py \
  --product "AI Course for Marketers" \
  --headline "Master AI Marketing in 30 Days" \
  --price "$497" \
  --target-audience "Marketing professionals and agency owners" \
  --style "modern-gradient" \
  --deploy
```

### Option 2: Full Pipeline with Research
```bash
python3 execution/generate_landing_page.py \
  --product "Lead Generation System" \
  --website "https://example.com" \
  --research \
  --style "minimal-clean" \
  --deploy
```

### Option 3: Generate Only (No Deploy)
```bash
python3 execution/generate_landing_page.py \
  --product "Coaching Program" \
  --headline "Transform Your Business in 90 Days" \
  --price "$2,997" \
  --output-dir .tmp/landing_pages/coaching
```

## Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| product | string | Yes | Product/service name |
| headline | string | No | Main headline (AI generates if not provided) |
| subheadline | string | No | Supporting subheadline |
| price | string | No | Price point ($XXX) |
| target-audience | string | No | Who the page targets |
| website | string | No | Company website for research |
| style | enum | No | Design style (see styles below) |
| research | flag | No | Run market research first |
| deploy | flag | No | Auto-deploy to Cloudflare |
| project-name | string | No | Cloudflare Pages project name |
| output-dir | string | No | Local output directory |

### Available Design Styles (Anthropic Frontend Design Skill)
**Distinctive designs that avoid generic "AI slop" aesthetics:**

| Style | Fonts | Best For |
|-------|-------|----------|
| `neo-noir` | Clash Display + Satoshi | Dark dramatic, cinematic feel |
| `editorial-luxury` | Playfair Display + Source Sans 3 | Elegant, refined, high-ticket |
| `electric-tech` | Cabinet Grotesk + General Sans | Futuristic, SaaS, tech |
| `warm-organic` | Fraunces + Nunito Sans | Wellness, coaching, approachable |
| `neubrutalism` | Space Grotesk + Work Sans | Bold, raw, startups |
| `modern-gradient` | Syne + Outfit | Gradient backgrounds, glassmorphism |
| `minimal-clean` | Plus Jakarta Sans | White space, subtle shadows |
| `dark-mode` | Clash Display + Satoshi | Dark backgrounds, neon accents |
| `bold-colors` | DM Sans | Vibrant, high contrast CTAs |
| `professional` | System fonts | Corporate, trustworthy |

**Design System Features:**
- Unique, distinctive fonts (NOT Inter, Roboto, Arial)
- Bold color palettes with sharp accents
- Staggered animation reveals on page load
- Noise texture overlays (dark themes)
- Glass morphism effects
- Glow effects and dramatic shadows
- Neubrutalism option with harsh borders

See: `skills/SKILL_BIBLE_frontend_design_mastery.md`

## Process

### Step 1: Input Validation & Research
**Quality Gate:**
- [ ] Product name provided
- [ ] Either headline or website provided
- [ ] API keys configured

**If research flag enabled:**
- Use Perplexity to research:
  - Target audience pain points
  - Competitor messaging
  - Industry-specific language
  - Social proof elements

### Step 2: Generate Landing Page Copy (PROPS Formula)
**AI Prompt Framework:**
Using PROPS formula (327% conversion increase) from skill bibles:

**P - Problem Amplification (3-Layer Deep):**
- Layer 1: Surface problem ("can't get clients")
- Layer 2: Tried everything ("courses, ads, cold outreach - nothing works")
- Layer 3: Starting to believe ("maybe I'm not cut out for this")
- Future pace: Where this leads if not fixed

**R - Result Demonstration (Triple R Formula):**
- **Real**: Specific numbers ("close 3 new clients in 30 days")
- **Relatable**: Paint life change ("imagine finally taking that vacation")
- **Reachable**: Break into chunks ("just one client every 10 days")

**O - Objection Removal:**
- Time: "Only 27 minutes a day"
- Money: ROI testimonials
- Past failure: "Those methods were designed to fail"
- Skepticism: Skeptic testimonials

**P - Proof Stacking (Pyramid Structure):**
- Base: Hard data, statistics, studies
- Middle: Journey testimonials (skeptic, imperfect user, home run)
- Top: Home run case study

**S - Simple Next Step:**
- Single CTA focus, no competing links

**Copy Fields Generated:**
| Field | Purpose |
|-------|---------|
| social_proof_header | Badge above headline ("Join 10,000+ professionals") |
| headline | 4-8 word desire-based with action verb |
| subheadline | Specific outcome + timeframe |
| hero_description | 2-3 sentences showing you understand their world |
| trust_badges | Array of trust elements |
| problem_headline | Agitation headline |
| problem_points | 3-layer deep pain points |
| unique_mechanism | The specific system/method name |
| solution_description | How mechanism solves root cause |
| features | 6 outcome-focused benefits |
| testimonials | Trio pattern (skeptic, imperfect, home run) |
| offer_stack | Value items with crossed-out prices |
| total_value | Value stack total |
| guarantee | Specific risk reversal |
| urgency_text | Legitimate scarcity reason |
| final_cta_headline | Urgency close headline |

**Quality Gate:**
- [ ] Headlines pass clarity test (under 10 words)
- [ ] Problem points follow 3-layer structure
- [ ] Unique mechanism is named and differentiated
- [ ] Offer stack shows value breakdown
- [ ] CTA is clear and action-oriented

### Step 3: Generate HTML/CSS Design (PROPS Page Structure)
**Page Structure (from Video Research):**

```
┌─────────────────────────────────────────────────────────────┐
│  HERO: Audience Callout + Big Promise + Social Proof        │
│  - "ATTENTION: [TARGET AUDIENCE]" callout                   │
│  - Social proof badge                                       │
│  - Main headline + subheadline                              │
│  - Trust badges row                                         │
│  - Primary CTA                                              │
├─────────────────────────────────────────────────────────────┤
│  P: PROBLEM AMPLIFICATION (3-Layer Deep)                    │
│  - "Sound Familiar?" intro                                  │
│  - 3 problem cards with emoji + color-coded borders         │
│  - Future pace warning box                                  │
├─────────────────────────────────────────────────────────────┤
│  R: RESULT DEMONSTRATION (Triple R Formula)                 │
│  - "INTRODUCING" label                                      │
│  - Unique Mechanism as section headline                     │
│  - Solution description                                     │
│  - Features grid (outcome-focused)                          │
│  - Mid-page CTA                                             │
├─────────────────────────────────────────────────────────────┤
│  P: PROOF PYRAMID (Testimonials)                            │
│  - "Real Results From Real People" headline                 │
│  - Testimonials grid with result badges                     │
├─────────────────────────────────────────────────────────────┤
│  O: OBJECTION HANDLING (FAQ)                                │
│  - "Still Have Questions?" headline                         │
│  - FAQ accordion (objections disguised as questions)        │
├─────────────────────────────────────────────────────────────┤
│  S: SIMPLE NEXT STEP (Offer Stack)                          │
│  - "Everything You Get Today" headline                      │
│  - Offer stack card with checkmarks + strikethrough values  │
│  - Total value vs. price comparison                         │
│  - Large CTA button                                         │
│  - Guarantee badge (green highlight)                        │
├─────────────────────────────────────────────────────────────┤
│  URGENCY CLOSE                                              │
│  - Final CTA headline                                       │
│  - Urgency/scarcity text                                    │
│  - CTA button                                               │
│  - Social proof reinforcement                               │
└─────────────────────────────────────────────────────────────┘
```

**Design System:**
- Unique fonts from Fontshare/Google Fonts (NOT Inter, Roboto)
- Staggered fade-slide-up animations on hero elements
- Color-coded problem cards (red → orange → yellow)
- Noise texture overlay for dark themes
- Glass morphism effects
- Glow effects on hover

**Quality Gate:**
- [ ] PROPS structure followed in correct order
- [ ] Audience callout appears above headline
- [ ] Problem section has 3-layer visual hierarchy
- [ ] "INTRODUCING" label precedes unique mechanism
- [ ] Offer stack shows value breakdown
- [ ] Guarantee in highlighted box
- [ ] Mobile responsive (tested at 375px, 768px, 1024px)

### Step 4: Local Build & Preview
**Save to output directory:**
```
.tmp/landing_pages/{project_slug}/
├── index.html
├── styles.css (inlined in production)
├── assets/
│   ├── hero-bg.svg
│   └── icons/
├── metadata.json
└── preview.png (screenshot)
```

### Step 5: Deploy to Cloudflare Pages
**Deployment Method: Direct Upload API**

```bash
# Using Wrangler CLI
npx wrangler pages deploy .tmp/landing_pages/{project_slug} \
  --project-name {project_name}
```

**Or via API:**
```python
# Create project if not exists
POST https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects
{
  "name": "landing-page-{slug}",
  "production_branch": "main"
}

# Upload files via Direct Upload
POST https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{project_name}/deployments
# With form data containing files
```

**Quality Gate:**
- [ ] Deployment successful (HTTP 200)
- [ ] Live URL accessible
- [ ] SSL certificate active
- [ ] Page loads correctly

### Step 6: Return Results
**Output:**
```json
{
  "success": true,
  "product": "AI Course for Marketers",
  "liveUrl": "https://ai-course-landing.pages.dev",
  "previewUrl": "https://abc123.ai-course-landing.pages.dev",
  "localFiles": ".tmp/landing_pages/ai_course/",
  "deploymentId": "abc123",
  "metadata": {
    "headline": "Master AI Marketing in 30 Days",
    "style": "modern-gradient",
    "generatedAt": "2026-01-08T12:00:00Z"
  }
}
```

## Design Templates

### Modern Gradient Style
```css
:root {
  --primary: #6366f1;
  --secondary: #8b5cf6;
  --accent: #f59e0b;
  --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
}
```
Features: Glassmorphism cards, gradient CTAs, floating elements

### Minimal Clean Style
```css
:root {
  --primary: #0f172a;
  --secondary: #3b82f6;
  --accent: #10b981;
  --bg-main: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #64748b;
}
```
Features: Maximum white space, subtle shadows, clean typography

### Dark Mode Style
```css
:root {
  --primary: #7c3aed;
  --secondary: #06b6d4;
  --accent: #f43f5e;
  --bg-main: #0f172a;
  --bg-card: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
}
```
Features: Dark backgrounds, neon accents, glow effects

## Quality Gates (Master Workflow)

### Pre-Deployment Checklist
- [ ] Copy passes conversion review
- [ ] Design matches selected style
- [ ] All sections complete
- [ ] Mobile responsive verified
- [ ] Images optimized
- [ ] CTA buttons work

### Post-Deployment Validation
- [ ] Live URL accessible
- [ ] Page loads under 3 seconds
- [ ] SSL active
- [ ] No console errors
- [ ] Forms functional (if applicable)

## Error Handling

| Error Type | Strategy |
|------------|----------|
| AI generation fails | Retry once → Use fallback templates |
| Cloudflare API error | Check credentials → Retry → Save locally |
| Invalid HTML | Auto-fix with fallback structure |
| Image generation fails | Use placeholder SVGs |
| Rate limiting | Exponential backoff (10s, 30s, 60s) |

## Edge Cases

### No Headline Provided
**Solution:** AI generates 3 headline options, uses best one, saves others for A/B testing

### Complex Product (Multiple Offers)
**Solution:** Focus on single primary offer, add secondary offers in features section

### No Price Point
**Solution:** Use "Book a Call" or "Get Started" CTA instead of price-focused copy

### International Audience
**Solution:** Detect from inputs, adjust language/cultural references

## Cost Estimates

| Component | Cost |
|-----------|------|
| Claude (copy + code) | ~$0.05-0.15 per page |
| Perplexity research | ~$0.01 per query |
| Cloudflare Pages | Free (up to 500 deployments/month) |
| **Total per page** | ~$0.06-0.20 |

## Success Metrics

- **Generation Time:** Under 2 minutes
- **Deployment Success Rate:** 99%+
- **Page Load Speed:** Under 2 seconds
- **Mobile Score:** 90+ (PageSpeed Insights)
- **Conversion Rate:** Benchmark against industry (3-5%)

## Related Directives

- [landing_page_cro_analyzer.md](./landing_page_cro_analyzer.md) - Analyze existing pages
- [vsl_funnel_orchestrator.md](./vsl_funnel_orchestrator.md) - Full funnel creation
- [funnel_copywriter.md](./funnel_copywriter.md) - Advanced copywriting

## Related Skill Bibles

**Core Funnel Knowledge (LOAD THESE):**
- `SKILL_BIBLE_funnel_copywriting_mastery.md` - Complete funnel psychology & VSL structure
- `SKILL_BIBLE_vsl_script_mastery.md` - Daniel Fazio VSL method (data-driven Q&A)
- `SKILL_BIBLE_sales_funnel_structure.md` - 7 funnel types & architecture
- `SKILL_BIBLE_vsl_funnel_structure_sales_pag.md` - Latest research (Jan 2026)

**Frontend & Design:**
- `SKILL_BIBLE_frontend_design_mastery.md` - Anthropic anti-AI-slop design principles
- `SKILL_BIBLE_landing_page_ai_mastery.md` - AI landing page design framework
- `SKILL_BIBLE_high_converting_landing_pages_.md` - Conversion optimization

**Copywriting:**
- `SKILL_BIBLE_landing_page_copywriting.md` - Copywriting principles
- `SKILL_BIBLE_copywriting_fundamentals.md` - Direct response basics

## Self-Annealing Notes

### What Works Well (Validated Jan 2026)
- AI-generated copy is highly tailored and conversion-focused
- Design styles produce visually distinct pages (9 styles with unique fonts)
- ~25-35 seconds generation time per page
- Self-contained HTML (no external dependencies)
- Mobile-responsive out of the box
- Copy data saved separately for A/B testing variations
- **NEW:** VSL funnel structure integrated (Hero → Problem → Solution → Proof → Offer Stack → Close)
- **NEW:** Social proof headers and trust badges in hero section
- **NEW:** Offer stack section with value breakdown (total value vs price)
- **NEW:** Unique mechanism positioning in solution section
- **NEW:** Staggered reveal animations on page load

### Funnel Structure Improvements (Jan 2026)
Based on `SKILL_BIBLE_funnel_copywriting_mastery.md` and YouTube research:
1. Added social_proof_header field for above-headline badge
2. Added trust_badges array for hero section
3. Added unique_mechanism field for differentiation
4. Added offer_stack array with value/item pairs
5. Added total_value and final_cta_headline fields
6. Copy prompt now includes VSL funnel structure guidelines
7. Emotion-first, logic-second approach enforced in prompt

### Improvements to Consider
- Add image generation integration (Midjourney/DALL-E for hero images)
- Implement screenshot generation for preview thumbnails
- Add A/B testing built-in (multiple headline variants)
- Create video section support for VSL integration
- Add form integration (ConvertKit, Mailchimp, etc.)

### Knowledge Sources Mined
- YouTube channels: AI Expert (485K subs), Elementor (364K), DesignCode (342K)
- Topics: AI website builders, landing page copywriting, conversion optimization
- Tools referenced: Lovable, Elementor, Bubble, Webflow
