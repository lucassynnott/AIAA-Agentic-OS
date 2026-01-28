# AI Objection Handler Reference

## What This Workflow Is
This workflow provides AI-powered objection handling responses for sales conversations based on context and proven frameworks.

## What It Does
1. Receives objection and context
2. Matches to objection framework
3. Generates tailored response
4. Provides alternative approaches
5. Logs for training

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key
```

### Required Tools
- Python 3.10+

### Installation
```bash
pip install openai
```

## How to Run

### Step 1: Get Objection Response
```bash
python3 execution/handle_objection.py \
  --objection "It's too expensive" \
  --context '{"deal_value": 5000, "competitor": "Acme"}' \
  --output .tmp/response.json
```

### Quick One-Liner
```bash
python3 execution/handle_objection.py --objection "[OBJECTION]"
```

## Goal
Provide AI-powered objection handling suggestions and scripts for sales conversations.

## Inputs
- **Objection**: What the prospect said
- **Context**: Deal stage, product, prospect info
- **Tone**: Consultative, direct, empathetic

## Process

### 1. Get Objection Response
```bash
python3 execution/handle_objection.py \
  --objection "It's too expensive" \
  --context '{"deal_value": 5000, "competitor": "Acme"}' \
  --output .tmp/response.json
```

### 2. Common Objections + Responses

**"It's too expensive"**
```
Framework: Acknowledge → Reframe → Value

"I hear you - budget is always a consideration. 
Let me ask: if you could [achieve result], 
what would that be worth to your business?

[Calculate ROI together]

So the investment is $X, but the return is $Y. 
Does that change how you're thinking about it?"
```

**"We're using [Competitor]"**
```
Framework: Acknowledge → Differentiate → Curiosity

"Great - [Competitor] is solid for [their strength]. 
Out of curiosity, how's [specific area we're better at] 
working for you?

[If they mention pain point]

That's actually where we see the biggest difference. 
Would it be worth seeing how we approach that differently?"
```

**"We don't have budget right now"**
```
Framework: Validate → Explore → Options

"Totally understand. When you say 'right now' - 
is budget something that opens up at a specific time, 
or is it more about priorities?

[If timing]: Let's pencil in a conversation for [date].
[If priorities]: Help me understand what's taking 
priority - maybe there's a way we fit."
```

**"I need to talk to my team/boss"**
```
Framework: Support → Prepare → Next Step

"Of course - important decisions like this should 
involve the right people. 

What questions do you think they'll have? 
I can help you prepare.

Would it help if I put together a summary you 
could share with them?"
```

**"We tried something like this before"**
```
Framework: Empathize → Differentiate → Proof

"I appreciate you sharing that - bad experiences 
make it hard to consider new options.

What specifically didn't work? [Listen]

That's actually why we [differentiator]. 

Here's how [similar client] had the same concern 
and what their experience was..."
```

### 3. Response Format
```json
{
  "objection": "It's too expensive",
  "category": "price",
  "confidence": 0.95,
  "responses": [
    {
      "approach": "ROI reframe",
      "script": "[Full script]",
      "follow_up": "[Next question to ask]"
    },
    {
      "approach": "Value stack",
      "script": "[Alternative script]"
    }
  ],
  "questions_to_ask": [
    "What's your current cost of [problem]?",
    "What would solving this be worth?"
  ]
}
```

### 4. Training Mode
- Input real objections from calls
- Get AI response suggestions
- Rate and refine responses
- Build custom playbook

## Integrations
- OpenAI/Anthropic
- Call transcription
- CRM notes

## Cost
- ~$0.02 per objection handled

## Related Skill Bibles

**[SKILL_BIBLE_hormozi_sales_training.md](../skills/SKILL_BIBLE_hormozi_sales_training.md)**
- Ultimate sales training framework
- Objection handling psychology
- Closing techniques

**[SKILL_BIBLE_hormozi_closing_deals.md](../skills/SKILL_BIBLE_hormozi_closing_deals.md)**
- 4000+ sales closing methodology
- Objection crusher frameworks
- Deal acceleration

**[SKILL_BIBLE_hormozi_sales_concepts.md](../skills/SKILL_BIBLE_hormozi_sales_concepts.md)**
- 9 core sales concepts
- Buyer psychology
- Reframe techniques

**[SKILL_BIBLE_hormozi_influence_psychology.md](../skills/SKILL_BIBLE_hormozi_influence_psychology.md)**
- Get anyone to do anything framework
- Persuasion psychology
- Response optimization
