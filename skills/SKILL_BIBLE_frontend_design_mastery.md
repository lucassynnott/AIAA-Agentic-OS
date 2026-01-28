# SKILL BIBLE: Frontend Design Mastery

> Source: Anthropic Claude Code Frontend Design Skill
> Adapted for: AIAA Agentic OS Landing Page & Funnel Builders
> Purpose: Create distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics

---

## Executive Summary

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Every landing page and funnel must be visually striking, memorable, and cohesive with a clear aesthetic point-of-view. The goal is to implement real working code with exceptional attention to aesthetic details and creative choices.

---

## Core Design Philosophy

### The Anti-AI-Slop Manifesto

**NEVER use generic AI-generated aesthetics:**
- ❌ Overused font families (Inter, Roboto, Arial, system fonts)
- ❌ Cliched color schemes (purple gradients on white backgrounds)
- ❌ Predictable layouts and component patterns
- ❌ Cookie-cutter design lacking context-specific character
- ❌ Safe, boring, forgettable interfaces

**ALWAYS create distinctive designs:**
- ✅ Unexpected, characterful font choices
- ✅ Bold color palettes with sharp accents
- ✅ Asymmetric, grid-breaking layouts
- ✅ Context-specific visual personality
- ✅ Memorable, unforgettable interfaces

---

## Design Thinking Process

Before coding ANY frontend, answer these questions:

### 1. Purpose
- What problem does this interface solve?
- Who uses it?
- What action should they take?

### 2. Tone (Pick ONE and commit fully)
Choose an extreme aesthetic direction:

| Aesthetic | Characteristics | Best For |
|-----------|----------------|----------|
| **Brutally Minimal** | Stark, lots of whitespace, single accent | Luxury, premium |
| **Maximalist Chaos** | Dense, layered, overwhelming detail | Creative, bold |
| **Retro-Futuristic** | 80s/90s meets sci-fi | Tech, innovation |
| **Organic/Natural** | Flowing shapes, earth tones | Wellness, eco |
| **Luxury/Refined** | Elegant, subtle, prestigious | High-ticket |
| **Playful/Toy-like** | Bright, bouncy, fun | Consumer, youth |
| **Editorial/Magazine** | Grid-based, typography-heavy | Content, media |
| **Brutalist/Raw** | Exposed structure, harsh | Tech, authentic |
| **Art Deco/Geometric** | Patterns, gold accents | Events, premium |
| **Soft/Pastel** | Gentle, approachable | Wellness, feminine |
| **Industrial/Utilitarian** | Functional, no-nonsense | B2B, tools |
| **Neo-Noir** | Dark, dramatic shadows | Gaming, tech |
| **Glassmorphism** | Frosted glass, depth | Modern SaaS |
| **Neubrutalism** | Bold borders, shadows | Startups, bold |

### 3. Differentiation
- What makes this UNFORGETTABLE?
- What's the one thing someone will remember?
- What visual element will stick in their mind?

---

## Typography Excellence

### Font Selection Rules

**Display Fonts (Headlines):**
Choose distinctive, characterful options:
- Clash Display
- Cabinet Grotesk
- Satoshi
- General Sans
- Switzer
- Outfit
- Plus Jakarta Sans
- DM Sans (only if styled uniquely)
- Syne
- Space Mono (for tech/code aesthetic)
- Playfair Display (editorial)
- Fraunces (quirky serif)
- Bebas Neue (bold impact)
- Monument Extended
- PP Neue Montreal

**Body Fonts (Readable):**
- Source Sans 3
- Work Sans
- Nunito Sans
- Public Sans
- Manrope
- IBM Plex Sans
- Libre Franklin

**Font Pairing Examples:**
```css
/* Editorial Luxury */
--font-display: 'Playfair Display', serif;
--font-body: 'Source Sans 3', sans-serif;

/* Modern Tech */
--font-display: 'Clash Display', sans-serif;
--font-body: 'Satoshi', sans-serif;

/* Bold Startup */
--font-display: 'Cabinet Grotesk', sans-serif;
--font-body: 'General Sans', sans-serif;

/* Playful Creative */
--font-display: 'Fraunces', serif;
--font-body: 'Nunito Sans', sans-serif;
```

### Typography Styling
```css
/* Headlines that command attention */
h1 {
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -0.03em;
}

/* Subheadlines with breathing room */
h2 {
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    font-weight: 500;
    line-height: 1.2;
    letter-spacing: -0.01em;
}
```

---

## Color & Theme Systems

### Bold Color Strategy

**Dominant + Accent Approach:**
Don't distribute colors evenly. Pick ONE dominant color and use sharp accents.

```css
/* Neo-Noir Dark */
:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #141414;
    --text-primary: #fafafa;
    --text-secondary: #a1a1a1;
    --accent: #ff3366; /* Sharp, memorable accent */
    --accent-glow: rgba(255, 51, 102, 0.4);
}

/* Warm Luxury */
:root {
    --bg-primary: #1a1612;
    --bg-secondary: #2d2620;
    --text-primary: #f5f0e8;
    --text-secondary: #b8a898;
    --accent: #d4a574;
    --accent-gold: #c9a962;
}

/* Electric Blue Tech */
:root {
    --bg-primary: #020617;
    --bg-secondary: #0f172a;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --accent: #3b82f6;
    --accent-cyan: #06b6d4;
}

/* Soft Pastel */
:root {
    --bg-primary: #fef7f0;
    --bg-secondary: #fff5eb;
    --text-primary: #3d3d3d;
    --text-secondary: #6b6b6b;
    --accent: #e07a5f;
    --accent-soft: #81b29a;
}

/* Brutalist Raw */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f0f0f0;
    --text-primary: #000000;
    --text-secondary: #333333;
    --accent: #ff0000;
    --border: 3px solid #000000;
}
```

---

## Motion & Animation

### High-Impact Animation Strategy

Focus on orchestrated moments, not scattered micro-interactions:

```css
/* Staggered Page Load Reveal */
@keyframes fadeSlideUp {
    from {
        opacity: 0;
        transform: translateY(40px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-title {
    animation: fadeSlideUp 0.8s ease-out forwards;
    animation-delay: 0.1s;
    opacity: 0;
}

.hero-subtitle {
    animation: fadeSlideUp 0.8s ease-out forwards;
    animation-delay: 0.2s;
    opacity: 0;
}

.hero-cta {
    animation: fadeSlideUp 0.8s ease-out forwards;
    animation-delay: 0.4s;
    opacity: 0;
}

/* Hover States That Surprise */
.cta-button {
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.cta-button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
}

.cta-button:hover::before {
    transform: translateX(100%);
}

.cta-button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Scroll-Triggered Reveals */
.reveal-on-scroll {
    opacity: 0;
    transform: translateY(60px);
    transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.reveal-on-scroll.visible {
    opacity: 1;
    transform: translateY(0);
}
```

### Micro-Interactions
```css
/* Card Hover with Depth */
.feature-card {
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    transform-style: preserve-3d;
}

.feature-card:hover {
    transform: translateY(-8px) rotateX(2deg);
    box-shadow: 
        0 25px 50px -12px rgba(0, 0, 0, 0.25),
        0 0 0 1px rgba(255, 255, 255, 0.1);
}

/* Button Magnetic Effect */
.magnetic-button {
    transition: transform 0.2s ease-out;
}
```

---

## Spatial Composition

### Layout Breaking Techniques

**Asymmetric Grids:**
```css
.hero-grid {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 4rem;
    align-items: center;
}

/* Offset elements */
.hero-image {
    transform: translateX(10%) translateY(-5%);
}
```

**Overlapping Elements:**
```css
.overlap-section {
    position: relative;
}

.overlap-card {
    position: relative;
    z-index: 2;
    margin-top: -80px;
}

.background-shape {
    position: absolute;
    top: -20%;
    right: -10%;
    width: 60%;
    height: 120%;
    background: var(--accent);
    opacity: 0.1;
    border-radius: 50%;
    filter: blur(100px);
}
```

**Diagonal Flow:**
```css
.diagonal-section {
    clip-path: polygon(0 5%, 100% 0, 100% 95%, 0 100%);
    padding: 8rem 0;
}
```

**Grid-Breaking Hero:**
```css
.hero {
    min-height: 100vh;
    display: grid;
    grid-template-rows: 1fr auto 1fr;
    place-items: center;
    position: relative;
}

.hero-content {
    grid-row: 2;
    max-width: 80ch;
    text-align: center;
}

.floating-element {
    position: absolute;
    /* Place decorative elements at unexpected positions */
}
```

---

## Backgrounds & Visual Details

### Atmospheric Backgrounds

**Gradient Mesh:**
```css
.gradient-mesh {
    background: 
        radial-gradient(at 40% 20%, var(--accent) 0px, transparent 50%),
        radial-gradient(at 80% 0%, var(--secondary) 0px, transparent 50%),
        radial-gradient(at 0% 50%, var(--tertiary) 0px, transparent 50%),
        radial-gradient(at 80% 50%, var(--accent) 0px, transparent 50%),
        radial-gradient(at 0% 100%, var(--secondary) 0px, transparent 50%);
    background-color: var(--bg-primary);
}
```

**Noise Texture Overlay:**
```css
.noise-overlay::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    opacity: 0.03;
    pointer-events: none;
}
```

**Geometric Patterns:**
```css
.geo-pattern {
    background-image: 
        linear-gradient(30deg, var(--accent) 12%, transparent 12.5%, transparent 87%, var(--accent) 87.5%, var(--accent)),
        linear-gradient(150deg, var(--accent) 12%, transparent 12.5%, transparent 87%, var(--accent) 87.5%, var(--accent)),
        linear-gradient(30deg, var(--accent) 12%, transparent 12.5%, transparent 87%, var(--accent) 87.5%, var(--accent)),
        linear-gradient(150deg, var(--accent) 12%, transparent 12.5%, transparent 87%, var(--accent) 87.5%, var(--accent));
    background-size: 80px 140px;
    background-position: 0 0, 0 0, 40px 70px, 40px 70px;
}
```

**Glass Effect (Glassmorphism):**
```css
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
}
```

**Dramatic Shadows:**
```css
.dramatic-shadow {
    box-shadow: 
        0 1px 1px rgba(0,0,0,0.08),
        0 2px 2px rgba(0,0,0,0.08),
        0 4px 4px rgba(0,0,0,0.08),
        0 8px 8px rgba(0,0,0,0.08),
        0 16px 16px rgba(0,0,0,0.08),
        0 32px 32px rgba(0,0,0,0.08);
}
```

---

## Design System Templates

### Template 1: Neo-Noir Dark
```css
:root {
    --font-display: 'Clash Display', sans-serif;
    --font-body: 'Satoshi', sans-serif;
    
    --bg-primary: #0a0a0a;
    --bg-card: #141414;
    --text-primary: #fafafa;
    --text-secondary: #737373;
    --accent: #ff3366;
    --accent-glow: 0 0 60px rgba(255, 51, 102, 0.3);
    
    --border-radius: 16px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Template 2: Editorial Luxury
```css
:root {
    --font-display: 'Playfair Display', serif;
    --font-body: 'Source Sans 3', sans-serif;
    
    --bg-primary: #faf9f7;
    --bg-card: #ffffff;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --accent: #b8860b;
    
    --border-radius: 4px;
    --transition: all 0.4s ease;
}
```

### Template 3: Electric Tech
```css
:root {
    --font-display: 'Cabinet Grotesk', sans-serif;
    --font-body: 'General Sans', sans-serif;
    
    --bg-primary: #020617;
    --bg-card: rgba(30, 41, 59, 0.5);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --accent: #3b82f6;
    --accent-secondary: #06b6d4;
    
    --border-radius: 12px;
    --border-glow: 0 0 0 1px rgba(59, 130, 246, 0.5);
}
```

### Template 4: Warm Organic
```css
:root {
    --font-display: 'Fraunces', serif;
    --font-body: 'Nunito Sans', sans-serif;
    
    --bg-primary: #fef7f0;
    --bg-card: #ffffff;
    --text-primary: #3d3229;
    --text-secondary: #7d7067;
    --accent: #e07a5f;
    --accent-secondary: #81b29a;
    
    --border-radius: 24px;
    --transition: all 0.5s ease;
}
```

### Template 5: Neubrutalism
```css
:root {
    --font-display: 'Space Grotesk', sans-serif;
    --font-body: 'Work Sans', sans-serif;
    
    --bg-primary: #fffef0;
    --bg-card: #ffffff;
    --text-primary: #000000;
    --text-secondary: #333333;
    --accent: #ff5757;
    --accent-secondary: #5271ff;
    
    --border: 3px solid #000000;
    --border-radius: 0;
    --shadow: 8px 8px 0 #000000;
}
```

---

## Implementation Checklist

### Before Writing Code
- [ ] Defined the PURPOSE clearly
- [ ] Committed to ONE aesthetic direction
- [ ] Identified the MEMORABLE element
- [ ] Selected distinctive fonts (NOT Inter, Roboto, Arial)
- [ ] Chose bold color palette with sharp accent

### During Implementation
- [ ] Typography creates hierarchy and character
- [ ] Colors are cohesive with dominant + accent approach
- [ ] Layout has intentional asymmetry or grid-breaking
- [ ] Backgrounds create atmosphere and depth
- [ ] Animations are orchestrated, not scattered
- [ ] Every detail is intentional

### Quality Check
- [ ] Would I remember this design tomorrow?
- [ ] Does it look like a human designer made it?
- [ ] Is there a clear visual personality?
- [ ] Are there zero generic AI patterns?
- [ ] Would a creative director approve this?

---

## Quick Reference: Font + Color Combos

| Aesthetic | Display Font | Body Font | Dominant | Accent |
|-----------|--------------|-----------|----------|--------|
| Neo-Noir | Clash Display | Satoshi | #0a0a0a | #ff3366 |
| Luxury | Playfair Display | Source Sans 3 | #faf9f7 | #b8860b |
| Tech | Cabinet Grotesk | General Sans | #020617 | #3b82f6 |
| Organic | Fraunces | Nunito Sans | #fef7f0 | #e07a5f |
| Brutal | Space Grotesk | Work Sans | #fffef0 | #ff5757 |
| Editorial | Syne | Libre Franklin | #ffffff | #000000 |
| Pastel | DM Serif Display | Manrope | #f8f4ff | #9b8afb |
| Industrial | IBM Plex Mono | IBM Plex Sans | #1c1c1c | #00ff88 |

---

*Remember: Claude is capable of extraordinary creative work. Don't hold back - show what can truly be created when thinking outside the box and committing fully to a distinctive vision.*
