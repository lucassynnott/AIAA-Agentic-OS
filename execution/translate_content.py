#!/usr/bin/env python3
"""
Content Translator - Translate content to multiple languages.

Usage:
    python3 execution/translate_content.py \
        --content "Your content here" \
        --languages "spanish,french,german" \
        --output .tmp/translations.json
"""

import argparse, json, os, sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    if os.getenv("OPENROUTER_API_KEY"):
        return OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model():
    return "anthropic/claude-sonnet-4" if os.getenv("OPENROUTER_API_KEY") else "gpt-4o"

LANGUAGE_CODES = {
    "spanish": "es", "french": "fr", "german": "de", "italian": "it",
    "portuguese": "pt", "dutch": "nl", "russian": "ru", "japanese": "ja",
    "chinese": "zh", "korean": "ko", "arabic": "ar", "hindi": "hi"
}

def translate(client, content, target_language, preserve_formatting=True):
    """Translate content to target language."""
    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": f"You are a professional translator. Translate to {target_language}. Preserve tone, formatting, and meaning."},
            {"role": "user", "content": f"""Translate this content to {target_language}:

{content}

Rules:
- Preserve all formatting (headers, bullets, etc.)
- Maintain the original tone and style
- Localize idioms appropriately
- Keep proper nouns unchanged unless they have standard translations"""}
        ],
        temperature=0.3,
        max_tokens=4000
    ).choices[0].message.content
    return response

def main():
    parser = argparse.ArgumentParser(description="Translate content")
    parser.add_argument("--content", "-c", help="Content to translate")
    parser.add_argument("--file", "-f", help="File with content")
    parser.add_argument("--languages", "-l", required=True, help="Comma-separated target languages")
    parser.add_argument("--output", "-o", default=".tmp/translations.json")
    args = parser.parse_args()

    if args.file:
        content = Path(args.file).read_text()
    else:
        content = args.content or ""

    languages = [l.strip().lower() for l in args.languages.split(",")]

    print(f"\n🌍 Content Translator\n   Languages: {languages}\n")
    client = get_client()

    translations = {"original": content, "translations": {}}
    
    for lang in languages:
        print(f"   Translating to {lang}...", end=" ")
        translated = translate(client, content, lang)
        translations["translations"][lang] = {
            "language": lang,
            "code": LANGUAGE_CODES.get(lang, lang[:2]),
            "content": translated
        }
        print("✅")

    output = {
        "translated_at": datetime.now().isoformat(),
        "source_length": len(content),
        **translations
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Translated to {len(languages)} languages")
    print(f"   📄 Output: {args.output}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
