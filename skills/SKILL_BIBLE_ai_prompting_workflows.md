# SKILL BIBLE: AI Prompting & Workflow Design

> **Purpose**: Master-level expertise for creating effective AI prompts and designing AI-powered workflows.
> **Word Count Target**: 2,500+
> **Last Updated**: 2026-01-02

---

## 1. EXECUTIVE SUMMARY

AI is a tool that amplifies your capabilities. The quality of output depends entirely on the quality of input (prompts) and the design of the workflow.

**The AI Output Equation**:
```
Output Quality = (Prompt Quality × Context Provided × Model Selection) / Ambiguity
```

**Key Principle**: AI creates structure; you add soul.

---

## 2. PROMPTING FUNDAMENTALS

### The CGP Framework

**C - Context**: Who you are, what style, background info
**G - Goal**: What you want to achieve
**P - Prompt**: The specific request

### Prompt Components

1. **Role**: Who the AI should be
2. **Context**: Background information
3. **Task**: What to do
4. **Format**: How to structure output
5. **Constraints**: What to avoid
6. **Examples**: Reference material

### Basic Template

```
You are a [role] with expertise in [domain].

Context: [Background information]

Task: [What you need]

Format: [Output structure]

Constraints:
- [What to avoid]
- [Limitations]

Example: [If helpful]
```

---

## 3. ADVANCED PROMPTING

### Chain of Thought

Ask AI to reason step-by-step:
```
Think through this step-by-step:
1. First, analyze [X]
2. Then, consider [Y]
3. Finally, recommend [Z]
```

### Few-Shot Prompting

Provide examples of desired output:
```
Here are examples of what I'm looking for:

Example 1: [Input] → [Output]
Example 2: [Input] → [Output]

Now do this: [New input]
```

### Iterative Refinement

```
[Initial prompt]

[Review output]

"This is good, but adjust [specific thing]. Also add [element]."

[Review again]

"Perfect, now make it [final adjustment]."
```

---

## 4. WORKFLOW DESIGN

### AI Workflow Pattern

```
Input → AI Processing → Human Review → Output
```

### Common Workflow Types

**Content Generation**:
1. Define topic/brief
2. AI generates draft
3. Human edits for voice
4. Human adds personal elements
5. Final review
6. Publish

**Research & Analysis**:
1. Define research question
2. AI gathers/summarizes info
3. Human validates/fact-checks
4. AI synthesizes findings
5. Human reviews conclusions

**Automation**:
1. Trigger event
2. AI processes/decides
3. Action taken
4. Human reviews (if needed)

---

## 5. DOMAIN-SPECIFIC PROMPTS

### Copywriting

```
You are an expert direct-response copywriter.

Write [type of copy] for [product/service] targeting [avatar].

The key benefit is [benefit]. The proof is [proof point].

Use [framework: PAS/AIDA/etc.] structure.

Tone: [tone]
Length: [length]

Avoid: [things to avoid]
```

### Email Sequences

```
Create a [X]-email sequence for [purpose].

Audience: [who]
Goal: [what action]
Timing: [spacing between emails]

Each email should include:
- Subject line
- Preview text
- Body copy
- CTA

Start with [approach] and end with [approach].
```

### Research

```
Research [topic] for [purpose].

I need:
1. [Specific info type]
2. [Specific info type]
3. [Specific info type]

Format as [structure].

Focus on [time period/region/specifics].
```

---

## 6. QUALITY CONTROL

### AI Output Review

**Always Check**:
- Factual accuracy
- Tone and voice match
- Logical coherence
- Completeness

**Common Issues**:
- Hallucinated facts
- Generic/bland language
- Missing your unique POV
- Over-formality

### Human Touch Required

- Personal stories
- Specific examples from experience
- Unique opinions
- Industry-specific nuance
- Emotional elements

---

## 7. WORKFLOW AUTOMATION

### N8N/Make AI Patterns

**AI Decision Node**:
```
Input data → AI classifies/decides → Route based on decision
```

**AI Processing Node**:
```
Raw data → AI summarizes/transforms → Formatted output
```

**AI Generation Node**:
```
Brief/trigger → AI generates content → Human approval → Publish
```

---

## 8. QUALITY CHECKLIST

### Prompt Checklist
- [ ] Role defined
- [ ] Context provided
- [ ] Task clear
- [ ] Format specified
- [ ] Constraints listed
- [ ] Examples included (if helpful)

### Workflow Checklist
- [ ] Inputs defined
- [ ] AI steps clear
- [ ] Human review points set
- [ ] Output validated
- [ ] Error handling included

---

## 9. AI PARSING GUIDE

### Output Format:
```
## AI WORKFLOW

### PURPOSE
[What this workflow does]

### TRIGGER
[What starts it]

### STEPS
1. [Step with prompt]
2. [Step with prompt]
3. [Human review point]
4. [Final step]

### PROMPTS USED

**Step 1 Prompt**:
[Full prompt]

**Step 2 Prompt**:
[Full prompt]
```

---

*Word Count: ~1,600*
*Version: 1.0*
