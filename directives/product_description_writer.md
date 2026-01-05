# Product Description Writer

## What This Workflow Is
This workflow generates compelling e-commerce product descriptions optimized for SEO and conversions, including benefit-focused copy, meta tags, and platform-specific formatting.

## What It Does
1. Analyzes product features and images
2. Generates benefit-focused descriptions
3. Creates SEO meta titles and descriptions
4. Formats for specific platforms (Shopify, Amazon, Etsy)
5. Outputs ready-to-use HTML/copy

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For writing + vision
```

### Required Tools
- Python 3.10+
- OpenAI API access

### Installation
```bash
pip install openai
```

## How to Run

### Step 1: Analyze Product
```bash
python3 execution/analyze_product.py \
  --images product_photos/ \
  --features features.txt \
  --output .tmp/product_data.json
```

### Step 2: Generate Description
```bash
python3 execution/write_product_description.py \
  --data .tmp/product_data.json \
  --tone professional \
  --platform shopify \
  --output .tmp/description.html
```

### Quick One-Liner
```bash
python3 execution/write_product_description.py --product "Product Name" --features "Feature1, Feature2" --platform shopify
```

## Goal
Generate compelling e-commerce product descriptions optimized for SEO and conversions.

## Inputs
- **Product Name**: What you're selling
- **Category**: Product type
- **Features**: List of product features
- **Images**: Product photos (for AI analysis)
- **Tone**: Professional, Playful, Luxury, Technical

## Process

### 1. Analyze Product
```bash
python3 execution/analyze_product.py \
  --images product_photos/ \
  --features features.txt \
  --output .tmp/product_data.json
```

### 2. Generate Description
```bash
python3 execution/write_product_description.py \
  --data .tmp/product_data.json \
  --tone professional \
  --platform shopify
```

### 3. Description Structure
```
[HEADLINE]
[Benefit-focused tagline]

[OPENING]
[Hook that addresses customer need]

[FEATURES → BENEFITS]
• [Feature] → [What it means for customer]
• [Feature] → [What it means for customer]
• [Feature] → [What it means for customer]

[SOCIAL PROOF]
[Reviews, testimonials, or usage stats]

[SPECIFICATIONS]
- Size: X
- Material: X
- Weight: X

[CTA]
[Urgency/scarcity if applicable]
```

### 4. SEO Elements
- Meta title (50-60 chars)
- Meta description (150-160 chars)
- Alt text for images
- Keywords naturally integrated

### 5. Platform Formats
**Shopify/WooCommerce**: Full HTML description
**Amazon**: Bullet points + A+ content
**Etsy**: Story-driven, handmade focus

## Output
- Main description (HTML)
- Bullet points
- Meta title/description
- Image alt text
- Keywords list

## Integrations
- OpenAI (writing)
- Vision AI (image analysis)

## Cost
- ~$0.05-0.10 per description
