# Multi-Language Content Translator

## What This Workflow Is
This workflow translates content into multiple languages using AI, preserving tone, idioms, and cultural context.

## What It Does
1. Takes source content in any format
2. Detects or uses specified source language
3. Translates to all target languages
4. Validates grammar and cultural appropriateness
5. Outputs organized translation files

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For AI translation
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai
```

## How to Run

### Step 1: Translate Content
```bash
python3 execution/translate_content.py \
  --input content.md \
  --source en \
  --targets "es,fr,de,pt" \
  --tone casual \
  --output .tmp/translations/
```

### Quick One-Liner
```bash
python3 execution/translate_content.py --input "[FILE]" --targets "es,fr,de"
```

## Goal
Translate content into multiple languages while preserving tone and context.

## Inputs
- **Source Content**: Text, document, or URL
- **Source Language**: Original language
- **Target Languages**: Languages to translate to
- **Tone**: Formal, casual, technical

## Process

### 1. Translate Content
```bash
python3 execution/translate_content.py \
  --input content.md \
  --source en \
  --targets "es,fr,de,pt" \
  --tone casual \
  --output .tmp/translations/
```

### 2. Translation Types

**Literal:**
Word-for-word accurate translation.

**Localized:**
Adapted for cultural context and idioms.

**Transcreation:**
Recreated to achieve same emotional impact.

### 3. Quality Checks
- Grammar validation
- Idiom appropriateness
- Cultural sensitivity
- Brand voice consistency
- Technical accuracy

### 4. Output Structure
```
translations/
├── content_es.md (Spanish)
├── content_fr.md (French)
├── content_de.md (German)
├── content_pt.md (Portuguese)
└── translation_notes.md
```

### 5. Use Cases
- Website localization
- Marketing materials
- Product documentation
- Email campaigns
- Social media posts
- Support articles

### 6. Review Process
1. AI translation
2. Native speaker review (optional)
3. Back-translation check
4. Final approval

## Integrations
- OpenAI/Anthropic (translation)
- DeepL (alternative)
- Google Translate API

## Cost
- ~$0.02/1000 characters
- Full article: ~$0.10-0.30
