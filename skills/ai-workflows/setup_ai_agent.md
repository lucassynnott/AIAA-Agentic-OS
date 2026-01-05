# Setting Up AI Agents with Tools in N8N

## Overview

Learn how to configure powerful AI agents in N8N with integrated tools like Perplexity, Reddit search, and custom functions. This guide covers system prompt engineering, tool integration, memory management, and fallback strategies for production-ready AI agents.

## Table of Contents

1. [AI Agent Architecture](#ai-agent-architecture)
2. [Chat Model Configuration](#chat-model-configuration)
3. [System Prompt Engineering](#system-prompt-engineering)
4. [Tool Integration](#tool-integration)
5. [Memory Configuration](#memory-configuration)
6. [Advanced Agent Patterns](#advanced-agent-patterns)

---

## AI Agent Architecture

### Basic Agent Structure

```
AI Agent Node Configuration:
├── Chat Model: OpenRouter (or direct provider)
├── System Prompt: Define role and expertise
├── Tools:
│   ├── Perplexity (Research)
│   ├── Reddit Search (Community insights)
│   ├── Custom functions
├── Memory: Window Buffer Memory
├── Output: JSON or Text
└── Error Handling: Fallback model
```

### Key Components

**1. Chat Model Selection**
- Primary model for main operations
- Fallback model for errors/rate limits
- Cost vs capability balance

**2. System Prompt**
- Defines agent behavior and expertise
- Sets output format requirements
- Establishes quality standards

**3. Tools**
- External information sources
- Custom function execution
- API integrations

**4. Memory**
- Session-based context
- Multi-turn conversations
- Persistent storage options

---

## Chat Model Configuration

### OpenRouter Setup

**Purpose**: Access multiple AI models through one unified API

**Configuration Steps**:

1. **Sign up at openrouter.ai**
2. **Generate API key** from dashboard
3. **In N8N AI Agent node**:
   - Select "OpenRouter" as chat model
   - Add credential
   - Use Header Authentication
   - Header: `Authorization`
   - Value: `Bearer YOUR_API_KEY`

**Model Selection Guide**:

```
Primary Models:
├── Claude 3.5 Sonnet (anthropic/claude-3.5-sonnet)
│   - Best for: Complex writing, analysis, reasoning
│   - Cost: ~$0.015-0.04 per execution
│   - Context: 200K tokens
│
├── GPT-4 Turbo (openai/gpt-4-turbo)
│   - Best for: Structured tasks, JSON output
│   - Cost: ~$0.01-0.03 per execution
│   - Context: 128K tokens
│
├── Gemini 2.0 Flash (google/gemini-2.0-flash-exp:free)
│   - Best for: Fast operations, testing
│   - Cost: FREE
│   - Context: 1M tokens
│
└── DeepSeek R1 Free (deepseek/deepseek-r1)
    - Best for: Simple operations, high volume
    - Cost: FREE
    - Context: 32K tokens
```

### Direct Provider Setup

**Claude Direct**:
- Get API key from console.anthropic.com
- Select "Anthropic" chat model in N8N
- Paste API key

**OpenAI Direct**:
- Get API key from platform.openai.com
- Select "OpenAI" chat model in N8N
- Paste API key

### Fallback Model Configuration

**Purpose**: Automatic retry with different model if primary fails

**Setup**:
```
AI Agent Node Settings:
├── Primary Model: Claude 3.5 Sonnet
├── Advanced Options
│   └── Enable fallback model: Yes
│   └── Fallback Model: Gemini 2.0 Flash Pro
└── Timeout: 60 seconds
```

**Use Cases**:
- Primary model hits rate limit
- Token context exceeded
- Service temporary outage
- Cost optimization for retry attempts

---

## System Prompt Engineering

### Effective Prompt Structure

```
You are a [ROLE] specializing in [EXPERTISE].

Your responsibilities:
1. [Primary Task]
2. [Secondary Task]
3. [Quality Standards]

Context:
- [Relevant Information]
- [Constraints]
- [Success Criteria]

Output Requirements:
- Format: [JSON/Markdown/Text]
- Length: [Specific range]
- Style: [Professional/Casual/Technical]
- Must include: [Required elements]
```

### Prompt Templates by Use Case

#### Research Agent

```
You are an expert B2B prospect research analyst specializing in creating comprehensive meeting preparation documents for business professionals.

Your responsibilities:
1. Analyze LinkedIn profiles and professional backgrounds
2. Identify key business challenges and opportunities
3. Research company context and market position
4. Generate actionable insights for sales conversations

You receive:
- Name: {{$json["prospectName"]}}
- Company: {{$json["companyName"]}}
- Position: {{$json["position"]}}
- LinkedIn URL: {{$json["linkedinUrl"]}}
- Previous Experience: {{$json["experience"]}}
- Education: {{$json["education"]}}

Research Focus:
- Current company trajectory and recent news
- Industry challenges and trends
- Personal career journey and achievements
- Potential pain points related to our solution
- Conversation starters and rapport-building topics

Output Format:
Generate a comprehensive meeting prep document with:
1. Executive Summary (3-4 sentences)
2. Professional Background
3. Company Context
4. Potential Pain Points
5. Recommended Talking Points
6. Questions to Ask

Maintain professional tone and cite sources where relevant.
```

#### Cold Email Icebreaker Writer

```
You are an expert cold email icebreaker writer for B2B outreach campaigns.

Your goal is to write a highly personalized first line that:
1. References specific, recent activity or achievement
2. Shows genuine research (not generic compliments)
3. Creates curiosity and relevance
4. Flows naturally into the email body
5. Is 1-2 sentences maximum

You receive:
- Prospect Name: {{$json["prospectName"]}}
- Company: {{$json["companyName"]}}
- Research Analysis: {{$json["researchReport"]}}
- Email Body Context: {{$json["emailBody"]}}

Research Analysis Format:
The research analysis contains specific information about:
- Recent company news or achievements
- Prospect's content (podcasts, posts, articles)
- Professional background and expertise
- Company initiatives and projects

Writing Guidelines:
- Be specific, not generic ("saw your company" is weak)
- Reference something recent (last 3 months)
- Show you understand their world
- Create natural transition to email body
- Avoid over-the-top flattery
- No asking questions in icebreaker

GOOD Examples:
"Loved your breakdown on scaling agencies to 10K MRR in 6 months on The Sauce podcast - the content flywheel strategy especially resonated."

"Noticed you just launched the new AI-powered analytics dashboard last week - the real-time cohort analysis feature looks game-changing."

BAD Examples:
"I love what you're doing at [Company]" (too generic)
"Your company is amazing!" (no specificity)
"Can I ask you about [topic]?" (don't ask in icebreaker)

Output:
Provide only the icebreaker text, no explanation or formatting.
```

#### Content Writing Agent

```
You are an expert content strategist who creates engaging professional content for [PLATFORM].

Transform this input into [CONTENT TYPE] that:
1. Hooks attention in first line
2. Delivers value and insights
3. Uses [FORMATTING STYLE]
4. Maintains [TONE]
5. Optimal length: [LENGTH]

Input: {{$json["content"]}}

Format Requirements:
- [Specific formatting rules]
- [Structure requirements]
- [Call-to-action guidelines]

Output: [Specific output format]
```

### Dynamic Prompt Variables

**Inject Context from Previous Nodes**:

```javascript
const systemPrompt = `You are a ${$json["agentRole"]} specializing in ${$json["expertise"]}.

Brand Voice: ${$json["brandVoice"]}
Tone: ${$json["toneStyle"]}
Keywords to include: ${$json["keywords"]}

Generate content that matches this brand identity.`;

return [{
  json: {
    systemPrompt: systemPrompt
  }
}];
```

---

## Tool Integration

### Perplexity Search Tool

**Purpose**: AI-powered web search and research

**Setup**:
1. Sign up at perplexity.ai
2. Get API key from settings
3. In N8N AI Agent node, add Perplexity tool

**Configuration**:
```
Perplexity Tool Settings:
├── Name: web_search
├── Description: "Search the web for current information"
├── Model: sonar-pro (for detailed research)
├── Return sources: Yes
├── Max tokens: 4000+
└── Recency: auto
```

**Use Cases**:
- Company research
- Industry trends
- Recent news and updates
- Competitive analysis
- Market insights

**Example Usage in Prompt**:
```
Research the company {{$json["companyName"]}} and provide:
1. Recent news and updates (last 3 months)
2. Key competitors and market position
3. Notable achievements or challenges
4. Leadership team information

Use web search to find the most current information.
```

### Reddit Search Tool

**Purpose**: Community insights and discussions

**Setup**:
- Built into N8N AI Agent
- No API key required
- Configure in Tools section

**Configuration**:
```
Reddit Tool Settings:
├── Name: community_insights
├── Description: "Search Reddit for community discussions"
├── Subreddits: auto (or specify specific ones)
└── Sort: relevance
```

**Use Cases**:
- Pain point discovery
- Community sentiment
- Real user feedback
- Product reviews
- Industry discussions

**Example Usage**:
```
Search Reddit for discussions about [TOPIC] in the [INDUSTRY] space.
Focus on:
- Common pain points mentioned
- Solutions people are looking for
- Frustrations with current tools
- Feature requests
```

### Custom Function Tool

**Purpose**: Execute custom JavaScript functions

**Setup**:
```javascript
// Define custom function in Code node
function analyzeData(input) {
  // Custom logic
  return {
    result: processedData,
    insights: generatedInsights
  };
}

// Make available to AI Agent
return [{
  json: {
    toolName: "analyze_data",
    toolDescription: "Analyze data and generate insights",
    toolFunction: analyzeData.toString()
  }
}];
```

### Multi-Tool Agent Configuration

**Complete Setup Example**:

```
AI Agent Configuration:
├── Chat Model: OpenRouter (Claude 3.5 Sonnet)
├── System Prompt: {{$json['systemPrompt']}}
├── Tools:
│   ├── Perplexity
│   │   ├── Name: "web_search"
│   │   └── Description: "Search web for current info"
│   ├── Reddit
│   │   ├── Name: "community_insights"
│   │   └── Description: "Find Reddit discussions"
│   └── Custom Function
│       ├── Name: "data_analyzer"
│       └── Description: "Analyze structured data"
├── Memory:
│   ├── Type: Window Buffer Memory
│   ├── Session ID: {{$json['sessionId']}}
│   └── Context Length: 5
└── Output Parser: Auto-detect
```

---

## Memory Configuration

### Session Management

**Generate Unique Session IDs**:

```javascript
// Code node before AI Agent
const sessionId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

return [{
  json: {
    sessionId: sessionId,
    timestamp: new Date().toISOString(),
    userInput: $json["userInput"]
  }
}];
```

### Buffer Window Memory

**Purpose**: Keep recent conversation context

**Configuration**:
```
Memory Settings:
├── Type: Window Buffer Memory
├── Session ID: {{$json['sessionId']}}
├── Context Window: 5-10 messages
└── Use Case: Multi-turn conversations
```

**When to Use**:
- Interactive chat agents
- Iterative refinement workflows
- Follow-up question handling
- Context-dependent responses

**Example Flow**:
```
User: "Research Microsoft"
Agent: [Provides research]
User: "What about their competitors?"
Agent: [Remembers we're discussing Microsoft, provides competitor info]
```

### Persistent Memory

**Purpose**: Remember information across workflow runs

**Implementation**:

```javascript
// Save to Google Sheets
const conversationHistory = {
  sessionId: $json["sessionId"],
  timestamp: new Date().toISOString(),
  userMessage: $json["userMessage"],
  agentResponse: $json["agentResponse"],
  context: $json["relevantContext"]
};

// Google Sheets: Append Row
// Columns: SessionID, Timestamp, UserMessage, AgentResponse, Context
```

**Load Context on Start**:
```javascript
// Google Sheets: Lookup
// Search for: SessionID = {{$json["sessionId"]}}
// Return: Last 10 messages

const previousContext = $json["sheetsData"].map(row => ({
  role: row.role,
  content: row.content
}));

return [{
  json: {
    conversationHistory: previousContext,
    currentInput: $json["newMessage"]
  }
}];
```

---

## Advanced Agent Patterns

### Sequential Agent Chain

**Use Case**: Complex tasks requiring specialized expertise at each stage

**Structure**:
```
Input Data
    ↓
Research Agent (Gather information)
    ↓
Analysis Agent (Process findings)
    ↓
Writing Agent (Create output)
    ↓
Quality Check Agent (Review)
    ↓
Final Output
```

**Implementation**:
- Each agent has specialized system prompt
- Output from one becomes input to next
- Error handling at each stage
- Progress tracking via status updates

**Example: VSL Script Creation**:
```
1. Hook Agent → Creates 3 opening hook variations
2. Story Agent → Builds narrative architecture
3. Objection Handler → Addresses common concerns
4. CTA Agent → Crafts compelling call-to-action
5. Compiler → Assembles complete script
```

### Parallel Agent Pattern

**Use Case**: Generate multiple content pieces simultaneously

**Structure**:
```
Input Transcript
    ↓
    ├── YouTube Script Agent → Doc Creation
    ├── LinkedIn Post Agent → Doc Creation
    ├── Twitter Thread Agent → Doc Creation
    └── Newsletter Agent → Doc Creation
```

**Benefits**:
- Faster execution (parallel processing)
- Multiple content formats at once
- Consistent source material
- Time-efficient scaling

### Agent with QA Loop

**Use Case**: Ensure quality before final output

**Structure**:
```
Content Generation Agent
    ↓
QA Agent Reviews:
├── Grammar and spelling
├── Brand voice consistency
├── Factual accuracy
├── CTA clarity
└── Length requirements
    ↓
IF Issues Found:
    → Correction Agent → Re-check
ELSE:
    → Publish/Deliver
```

**QA Agent Prompt**:
```
You are a quality assurance reviewer for [CONTENT TYPE].

Review this content and check:
1. Grammar and spelling errors
2. Brand voice consistency with: {{$json["brandVoice"]}}
3. Factual accuracy
4. Call-to-action clarity
5. Length requirements: {{$json["targetLength"]}}

If all checks pass, respond with: "APPROVED"
If issues found, provide specific corrections in this format:
{
  "status": "NEEDS_REVISION",
  "issues": [
    {"type": "grammar", "location": "paragraph 2", "fix": "suggestion"},
    {"type": "brand_voice", "location": "paragraph 3", "fix": "suggestion"}
  ]
}
```

### Conditional Routing Agent

**Use Case**: Route to different agents based on input type

**Structure**:
```
Switch Node:
Mode: "Expression"

Rules:
├── Case 1: {{$json["contentType"]}} === "blog"
│   → Route to Blog Writer Agent
├── Case 2: {{$json["contentType"]}} === "social"
│   → Route to Social Media Agent
├── Case 3: {{$json["contentType"]}} === "email"
│   → Route to Email Writer Agent
└── Default:
    → Error: Unknown content type
```

---

## Error Handling and Best Practices

### Timeout Configuration

```
AI Agent Node Settings:
├── Timeout: 60000 (60 seconds)
├── Retry on Fail: Yes
├── Max Retries: 2
└── Retry Wait: 3000 (3 seconds)
```

### Fallback Strategies

**1. Model Fallback**:
- Primary: Claude 3.5 Sonnet
- Fallback: Gemini 2.0 Flash

**2. Error Handling**:
```javascript
// Code node after AI Agent
if ($json["error"]) {
  return [{
    json: {
      status: "failed",
      error: $json["error"],
      fallbackAction: "notify_admin"
    }
  }];
} else {
  return [{
    json: {
      status: "success",
      output: $json["output"]
    }
  }];
}
```

### Cost Optimization

**Model Selection Strategy**:
```
Simple Tasks (classification, extraction):
└── Use: DeepSeek R1 Free or Gemini 2.0 Flash

Medium Complexity (content generation):
└── Use: GPT-4 Turbo or Claude 3.5 Haiku

Complex Tasks (deep analysis, long-form writing):
└── Use: Claude 3.5 Sonnet or GPT-4
```

### Performance Monitoring

**Track Agent Performance**:
```javascript
// Before AI Agent
const startTime = Date.now();

// After AI Agent
const endTime = Date.now();
const duration = endTime - $json["aiStartTime"];

// Log to Google Sheets
{
  agentName: "Prospect Research Agent",
  model: "claude-3.5-sonnet",
  duration: duration,
  tokensUsed: $json["usage"]["totalTokens"],
  cost: $json["usage"]["totalCost"],
  timestamp: new Date().toISOString()
}
```

---

## Common Use Cases

### 1. Prospect Research Agent

**Components**:
- Perplexity for company research
- LinkedIn data from Explorium
- System prompt for meeting prep docs
- Output: Formatted Google Doc

### 2. Content Generation Agent

**Components**:
- Input: Transcript or brief
- Tools: Web search for current info
- Memory: Track user preferences
- Output: Multiple content formats

### 3. Email Personalization Agent

**Components**:
- Input: Lead data + email template
- Tools: Perplexity for prospect research
- Prompt: Icebreaker writer
- Output: Personalized emails

### 4. Data Analysis Agent

**Components**:
- Input: Structured data (JSON/CSV)
- Custom functions for calculations
- Prompt: Generate insights
- Output: Executive summary

---

## Troubleshooting

### Issue: Agent Timeout

**Solutions**:
1. Increase timeout setting to 90-120 seconds
2. Reduce input text length
3. Use model with larger context window
4. Split into smaller requests
5. Enable fallback model

### Issue: Inconsistent Responses

**Solutions**:
1. Make system prompt more specific
2. Add output format examples
3. Use JSON mode if structured output needed
4. Reduce temperature setting (0.3-0.5)
5. Add validation step after agent

### Issue: Tool Not Working

**Solutions**:
1. Verify API keys are correct
2. Check tool description is clear
3. Ensure agent prompt mentions tool usage
4. Test tool in isolation first
5. Check rate limits on tool API

### Issue: Memory Not Persisting

**Solutions**:
1. Verify session ID is consistent
2. Check context window length
3. Ensure memory type is correct
4. Test with simple conversation first
5. Verify memory node is connected

---

## Next Steps

After mastering AI agent setup:

1. **Implement specific workflows**:
   - Mass personalization workflow
   - Prospect research automation
   - Meeting summarization

2. **Optimize for production**:
   - Add error handling
   - Implement monitoring
   - Set up cost tracking
   - Create fallback strategies

3. **Scale operations**:
   - Batch processing patterns
   - Rate limit management
   - Multi-agent orchestration
   - Performance optimization

**Related Skills**:
- `mass_personalize_with_ai.md` - Scale personalization
- `ai_prospect_research.md` - Automated research
- `ai_meeting_summarization.md` - Meeting intelligence

---

## Resources

**N8N Documentation**:
- AI Agent Node: docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent
- Memory Types: docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.memory

**Model Providers**:
- OpenRouter: openrouter.ai/docs
- Anthropic: docs.anthropic.com
- OpenAI: platform.openai.com/docs

**Tool APIs**:
- Perplexity: docs.perplexity.ai
- Reddit API: reddit.com/dev/api

---

Ready to build production AI agents that automate intelligent work at scale.
