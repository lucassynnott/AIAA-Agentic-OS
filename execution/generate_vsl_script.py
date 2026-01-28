#!/usr/bin/env python3
"""VSL Script Generator - UPDATED with paragraph-based prompting"""

import argparse, json, os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def load_skill_bibles() -> str:
    """Load VSL skill bibles"""
    bibles = []
    paths = ["skills/SKILL_BIBLE_vsl_writing_production.md", "skills/SKILL_BIBLE_vsl_script_mastery_fazio.md", "skills/SKILL_BIBLE_funnel_copywriting_mastery.md"]
    for path in paths:
        try:
            with open(path) as f:
                bibles.append(f.read())
                print(f"✅ Loaded: {path}")
        except:
            print(f"⚠️  Not found: {path}")
    return "\n\n---\n\n".join(bibles)

def generate_hooks(research_data: dict, client: OpenAI) -> list:
    """Generate hook options"""
    print("🎯 Generating hooks...")
    model = "anthropic/claude-opus-4.5" if "openrouter" in str(client.base_url).lower() else "gpt-4o"
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": f"""Generate 3 VSL hooks for {research_data['company']['name']} - {research_data['offer']['name']}. Return as JSON: {{"hooks": [{{"type": "...", "text": "...", "whyItWorks": "..."}}]}}"""}],
        temperature=0.7
    )
    
    result = response.choices[0].message.content
    if "```json" in result:
        result = result.split("```json")[1].split("```")[0].strip()
    return json.loads(result)["hooks"]

def generate_vsl_script(research_data: dict, skill_bibles: str, vsl_length: str, client: OpenAI) -> str:
    """Generate VSL script with explicit paragraph requirements"""
    print(f"📝 Generating {vsl_length} VSL...")
    
    model = "anthropic/claude-opus-4.5" if "openrouter" in str(client.base_url).lower() else "gpt-4o"
    
    system_prompt = f"""You are an expert VSL scriptwriter.

FRAMEWORKS (use these):
{skill_bibles[:50000]}

Write COMPLETE scripts with FULL paragraphs (50-80 words each, 3-5 sentences).
WORD COUNT STANDARDS:
- Mini: MINIMUM 1,000 words (7-10 min)
- Medium (DEFAULT): MINIMUM 3,000 words (20-25 min)
- Long: MINIMUM 10,000 words (60-90 min)"""

    # Set minimum based on length
    min_words = {"mini": 1000, "medium": 3000, "long": 10000}.get(vsl_length, 3000)

    user_prompt = f"""Write COMPLETE VSL script for:

Company: {research_data['company']['name']}
Offer: {research_data['offer']['name']}
Details: {research_data['offer']['description'][:1000]}
Pain Points: {json.dumps(research_data.get('targetAudience', {}).get('painPoints', []))}
Social Proof: {research_data.get('socialProof', {}).get('caseStudies', [{}])[0][:800] if research_data.get('socialProof', {}).get('caseStudies') else 'N/A'}

⚠️⚠️⚠️ CRITICAL: MINIMUM {min_words} WORDS for {vsl_length.upper()} VSL ⚠️⚠️⚠️

10-PART STRUCTURE (write complete paragraphs for EACH):

1. HOOK (2-3 paragraphs, 100-150 words)
2. PROBLEM (4-5 paragraphs, 300-400 words) 
3. CREDIBILITY (3 paragraphs, 200-250 words)
4. SOLUTION (3 paragraphs, 200-250 words)
5. MECHANISM (6-8 paragraphs, 600-800 words) ← LONGEST SECTION
6. SOCIAL PROOF (5-6 paragraphs, 400-500 words)
7. OFFER (5-6 paragraphs, 400-500 words)
8. URGENCY (3 paragraphs, 200-250 words)
9. GUARANTEE (2-3 paragraphs, 150-200 words)
10. CTA (3 paragraphs, 200-250 words)

Format:
## HOOK (0:00-0:30)
[Write 2-3 FULL paragraphs here]

**Graphics:** [...]
**Tone:** [...]

## PROBLEM (0:30-2:00)
[Write 4-5 FULL paragraphs here]

[etc for all 10 sections]

DO NOT abbreviate. DO NOT outline. Write COMPLETE script paragraphs."""
    
    # Set max_tokens based on length (long VSLs need much more)
    max_tokens_map = {"mini": 5000, "medium": 16000, "long": 50000}
    max_tokens = max_tokens_map.get(vsl_length, 16000)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.7,
        max_tokens=max_tokens
    )
    
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--research", required=True)
    parser.add_argument("--length", default="medium", choices=["mini", "medium", "long"])
    parser.add_argument("--style", default="education")
    parser.add_argument("--output", required=True)
    parser.add_argument("--hooks-output")
    args = parser.parse_args()
    
    # Init client
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return 1
    
    client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1") if os.getenv("OPENROUTER_API_KEY") and not os.getenv("OPENAI_API_KEY") else OpenAI(api_key=api_key)
    
    print("🚀 VSL Script Generation...")
    
    with open(args.research) as f:
        research_data = json.load(f)
    
    skill_bibles = load_skill_bibles()
    hooks = generate_hooks(research_data, client)
    
    if args.hooks_output:
        Path(args.hooks_output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.hooks_output, "w") as f:
            f.write("# Hook Options\n\n" + "\n\n---\n\n".join([f"## Option {i+1}: {h['type']}\n\n{h['text']}\n\n**Why:** {h['whyItWorks']}" for i, h in enumerate(hooks)]))
    
    script = generate_vsl_script(research_data, skill_bibles, args.length, client)
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        f.write(script)
    
    word_count = len(script.split())
    print(f"\n✅ Generated: {word_count} words ({round(word_count/150, 1)} min)")
    
    return 0

if __name__ == "__main__":
    exit(main())
