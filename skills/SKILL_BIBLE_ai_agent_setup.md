# SKILL BIBLE: AI Agent Architecture & Implementation in N8N

## Executive Summary

This skill bible provides comprehensive guidance for building production-ready AI agents in N8N with integrated tools, memory management, and sophisticated prompt engineering. The document covers everything from basic agent setup to advanced multi-agent orchestration patterns, enabling automation professionals to create intelligent workflows that can research prospects, generate personalized content, analyze data, and execute complex multi-step processes.

The skill encompasses critical components including chat model configuration across multiple providers (OpenRouter, direct APIs), system prompt engineering for specific use cases, tool integration (Perplexity, Reddit, custom functions), memory management for conversational context, and advanced patterns like sequential agent chains and parallel processing. This knowledge is essential for anyone looking to implement AI-powered automation at scale while maintaining quality, cost-effectiveness, and reliability.

## Source
- **Type:** Internal SOP/Skill Document
- **Category:** ai-workflows
- **Original File:** setup_ai_agent.md

## Core Principles

### 1. Modular Agent Architecture
AI agents should be built with clear separation of concerns: chat model selection, system prompts, tool integration, memory management, and error handling. This modular approach enables easier debugging, optimization, and scaling while maintaining flexibility to swap components as needed.

### 2. Strategic Model Selection
Choose AI models based on task complexity and cost considerations. Use free models (Gemini 2.0 Flash, DeepSeek R1) for simple tasks, mid-tier models (GPT-4 Turbo, Claude 3.5 Haiku) for medium complexity, and premium models (Claude 3.5 Sonnet) for complex reasoning and analysis.

### 3. Prompt Engineering Excellence
System prompts must be specific, structured, and include clear role definition, responsibilities, context, output requirements, and success criteria. Generic prompts produce inconsistent results; detailed prompts with examples drive reliable performance.

### 4. Tool Integration Strategy
Integrate external tools (Perplexity for research, Reddit for community insights, custom functions for data processing) to expand agent capabilities beyond the base model's training data. Each tool should have clear descriptions and specific use cases.

### 5. Memory Management for Context
Implement appropriate memory strategies based on use case: session-based memory for multi-turn conversations, persistent memory for cross-workflow context, and buffer window memory for maintaining recent conversation history.

### 6. Fallback and Error Handling
Always implement fallback models and error handling strategies. Primary model failures should automatically route to backup models, and timeout/retry logic should prevent workflow failures from temporary service issues.

### 7. Cost Optimization Through Intelligence
Monitor token usage, execution time, and model costs. Implement intelligent routing where simple tasks use cheaper models and complex tasks justify premium model costs. Track performance metrics to optimize over time.

### 8. Quality Assurance Integration
Build quality checks into agent workflows through QA agents, validation steps, and output formatting requirements. Automated quality control prevents poor outputs from reaching end users.

## Step-by-Step Process

### Phase 1: Foundation Setup

#### Step 1: Configure Chat Model Provider
1. **Choose Primary Provider**
   - For unified access: Sign up at openrouter.ai
   - For direct access: Use provider-specific APIs (Anthropic, OpenAI)
   - Generate API key from provider dashboard

2. **Set Up N8N Credentials**
   - In N8N AI Agent node, select chat model type
   - Add new credential
   - For OpenRouter: Use Header Authentication
     - Header: `Authorization`
     - Value: `Bearer YOUR_API_KEY`
   - For direct providers: Paste API key directly

3. **Select Primary Model**
   - **Claude 3.5 Sonnet** (`anthropic/claude-3.5-sonnet`): Complex writing, analysis, reasoning
   - **GPT-4 Turbo** (`openai/gpt-4-turbo`): Structured tasks, JSON output
   - **Gemini 2.0 Flash** (`google/gemini-2.0-flash-exp:free`): Fast operations, testing
   - **DeepSeek R1 Free** (`deepseek/deepseek-r1`): Simple operations, high volume

#### Step 2: Configure Fallback Model
1. Enable fallback model in AI Agent advanced options
2. Select cost-effective backup (typically Gemini 2.0 Flash)
3. Set timeout to 60 seconds
4. Configure retry logic: 2 retries with 3-second wait

#### Step 3: Design System Prompt Architecture
1. **Define Agent Role**: Specific expertise area and responsibilities
2. **Set Context Parameters**: Available data, constraints, success criteria
3. **Specify Output Requirements**: Format (JSON/Markdown/Text), length, style
4. **Include Quality Standards**: Professional tone, accuracy requirements
5. **Add Dynamic Variables**: Use `{{$json["fieldName"]}}` for context injection

### Phase 2: Tool Integration

#### Step 4: Configure Perplexity Search Tool
1. Sign up at perplexity.ai and generate API key
2. In AI Agent node, add Perplexity tool:
   - **Name**: `web_search`
   - **Description**: "Search the web for current information"
   - **Model**: `sonar-pro` for detailed research
   - **Return sources**: Yes
   - **Max tokens**: 4000+
   - **Recency**: auto

#### Step 5: Set Up Reddit Search Tool
1. Add Reddit tool in AI Agent (no API key required)
2. Configure settings:
   - **Name**: `community_insights`
   - **Description**: "Search Reddit for community discussions"
   - **Subreddits**: auto or specify relevant ones
   - **Sort**: relevance

#### Step 6: Implement Custom Function Tools
1. Create Code node before AI Agent
2. Define custom functions:
```javascript
function analyzeData(input) {
  // Custom logic for data processing
  return {
    result: processedData,
    insights: generatedInsights
  };
}

return [{
  json: {
    toolName: "analyze_data",
    toolDescription: "Analyze data and generate insights",
    toolFunction: analyzeData.toString()
  }
}];
```

### Phase 3: Memory Configuration

#### Step 7: Implement Session Management
1. **Generate Unique Session IDs**:
```javascript
const sessionId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
return [{
  json: {
    sessionId: sessionId,
    timestamp: new Date().toISOString(),
    userInput: $json["userInput"]
  }
}];
```

2. **Configure Buffer Window Memory**:
   - Type: Window Buffer Memory
   - Session ID: `{{$json['sessionId']}}`
   - Context Window: 5-10 messages for multi-turn conversations

#### Step 8: Set Up Persistent Memory (Optional)
1. **Create Google Sheets Storage**:
   - Columns: SessionID, Timestamp, UserMessage, AgentResponse, Context
   - Use Google Sheets nodes for append/lookup operations

2. **Implement Context Loading**:
```javascript
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

### Phase 4: Advanced Implementation

#### Step 9: Build Agent Chains (Sequential Processing)
1. **Design Agent Sequence**:
   - Research Agent → Analysis Agent → Writing Agent → QA Agent
2. **Configure Each Agent**:
   - Specialized system prompts for each stage
   - Pass output from previous agent as input to next
   - Implement error handling at each stage

#### Step 10: Implement Parallel Agent Processing
1. **Set Up Parallel Branches**:
   - Split input to multiple specialized agents
   - Process simultaneously for different output formats
   - Merge results in final compilation step

#### Step 11: Add Quality Assurance Loop
1. **Create QA Agent**:
```
You are a quality assurance reviewer for [CONTENT TYPE].

Review this content and check:
1. Grammar and spelling errors
2. Brand voice consistency
3. Factual accuracy
4. Call-to-action clarity
5. Length requirements

If all checks pass, respond with: "APPROVED"
If issues found, provide specific corrections.
```

2. **Implement Revision Loop**:
   - QA Agent reviews output
   - If issues found, route back to Correction Agent
   - Re-check until approved or max iterations reached

### Phase 5: Production Optimization

#### Step 12: Implement Error Handling
1. **Configure Timeout Settings**:
   - Timeout: 60-90 seconds for complex operations
   - Retry on fail: Yes
   - Max retries: 2
   - Retry wait: 3 seconds

2. **Add Error Detection**:
```javascript
if ($json["error"]) {
  return [{
    json: {
      status: "failed",
      error: $json["error"],
      fallbackAction: "notify_admin"
    }
  }];
}
```

#### Step 13: Set Up Performance Monitoring
1. **Track Execution Metrics**:
```javascript
const startTime = Date.now();
// ... AI Agent execution ...
const endTime = Date.now();
const duration = endTime - startTime;

// Log to monitoring sheet
{
  agentName: "Prospect Research Agent",
  model: "claude-3.5-sonnet",
  duration: duration,
  tokensUsed: $json["usage"]["totalTokens"],
  cost: $json["usage"]["totalCost"],
  timestamp: new Date().toISOString()
}
```

#### Step 14: Optimize for Cost and Performance
1. **Implement Intelligent Model Routing**:
   - Simple tasks → Free models (DeepSeek R1, Gemini Flash)
   - Medium complexity → Mid-tier models (GPT-4 Turbo)
   - Complex tasks → Premium models (Claude 3.5 Sonnet)

2. **Monitor and Adjust**:
   - Track cost per execution
   - Measure quality vs. cost trade-offs
   - Optimize model selection based on performance data

## Frameworks & Templates

### System Prompt Framework

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

### Research Agent Template

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

### Cold Email Icebreaker Template

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

Writing Guidelines:
- Be specific, not generic
- Reference something recent (last 3 months)
- Show you understand their world
- Create natural transition to email body
- Avoid over-the-top flattery
- No asking questions in icebreaker

GOOD Examples:
"Loved your breakdown on scaling agencies to 10K MRR in 6 months on The Sauce podcast - the content flywheel strategy especially resonated."

"Noticed you just launched the new AI-powered analytics dashboard last week - the real-time cohort analysis feature looks game-changing."

Output: Provide only the icebreaker text, no explanation or formatting.
```

### QA Agent Template

```
You are a quality assurance reviewer for {{$json["contentType"]}}.

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

### Agent Architecture Framework

```
AI Agent Node Configuration:
├── Chat Model: [Primary] (Fallback: [Secondary])
├── System Prompt: {{$json['systemPrompt']}}
├── Tools:
│   ├── Perplexity (web_search)
│   ├── Reddit (community_insights)
│   └── Custom Function (data_analyzer)
├── Memory:
│   ├── Type: Window Buffer Memory
│   ├── Session ID: {{$json['sessionId']}}
│   └── Context Length: 5-10
├── Output Parser: Auto-detect
└── Error Handling: Fallback model enabled
```

### Model Selection Framework

```
Task Complexity Assessment:
├── Simple (classification, extraction)
│   └── Models: DeepSeek R1 Free, Gemini 2.0 Flash
│   └── Cost: FREE - $0.001 per execution
├── Medium (content generation, basic analysis)
│   └── Models: GPT-4 Turbo, Claude 3.5 Haiku
│   └── Cost: $0.01 - $0.03 per execution
└── Complex (deep analysis, long-form writing)
    └── Models: Claude 3.5 Sonnet, GPT-4
    └── Cost: $0.015 - $0.04 per execution
```

## Best Practices

### Prompt Engineering Excellence

1. **Be Hyper-Specific**: Replace generic instructions with specific requirements, examples, and constraints. Instead of "write a good email," specify "write a 150-word email with a personalized first line, value proposition in paragraph 2, and clear CTA."

2. **Use Dynamic Context Injection**: Leverage `{{$json["fieldName"]}}` to inject relevant data from previous workflow steps, making each agent execution contextually aware and personalized.

3. **Provide Examples**: Include both good and bad examples in system prompts to establish clear quality standards and expected output formats.

4. **Structure Output Requirements**: Clearly define expected format (JSON, Markdown, plain text), length constraints, tone requirements, and mandatory elements to include.

5. **Test Iteratively**: Start with simple prompts and gradually add complexity, testing each modification to understand its impact on output quality and consistency.

### Tool Integration Optimization

1. **Tool Description Clarity**: Write clear, specific descriptions for each tool that explain when and how the agent should use them. Vague descriptions lead to poor tool utilization.

2. **Strategic Tool Selection**: Choose tools that complement each other - Perplexity for current information, Reddit for community sentiment, custom functions for data processing.

3. **Rate Limit Management**: Implement delays and retry logic for external tool APIs to handle rate limiting gracefully without workflow failures.

4. **Tool Result Validation**: Add validation steps after tool usage to ensure results meet quality standards before proceeding to next workflow steps.

5. **Cost-Aware Tool Usage**: Monitor tool API costs and implement usage limits or approval workflows for expensive operations.

### Memory Management Strategies

1. **Session ID Consistency**: Generate unique, persistent session IDs that remain consistent across workflow executions for the same conversation or user.

2. **Context Window Optimization**: Balance memory window size with performance - larger windows provide more context but increase token costs and processing time.

3. **Memory Cleanup**: Implement periodic cleanup of old conversation data to prevent memory stores from growing indefinitely.

4. **Context Relevance**: Store only relevant conversation elements in memory, filtering out system messages and irrelevant data.

5. **Cross-Workflow Memory**: For agents that need to remember information across different workflows, implement persistent storage using Google Sheets or databases.

### Error Handling and Reliability

1. **Graceful Degradation**: Design workflows to continue functioning even when secondary tools or features fail, providing reduced functionality rather than complete failure.

2. **Comprehensive Logging**: Log all agent interactions, errors, and performance metrics to enable debugging and optimization.

3. **Timeout Configuration**: Set appropriate timeouts based on task complexity - simple tasks need 30-60 seconds, complex research may need 90-120 seconds.

4. **Fallback Model Strategy**: Always configure fallback models that are faster and cheaper than primary models to handle retries cost-effectively.

5. **User-Friendly Error Messages**: Convert technical errors into actionable user messages that explain what went wrong and potential next steps.

### Performance Optimization

1. **Model Selection Intelligence**: Route tasks to appropriate models based on complexity, cost, and quality requirements rather than using premium models for all tasks.

2. **Parallel Processing**: Where possible, run independent agent operations in parallel to reduce total execution time.

3. **Caching Strategies**: Cache frequently requested information (company research, common analyses) to avoid repeated API calls.

4. **Batch Processing**: Group similar operations together to optimize API usage and reduce per-operation overhead.

5. **Performance Monitoring**: Track execution time, token usage, and cost per operation to identify optimization opportunities.

### Quality Assurance Integration

1. **Automated QA Agents**: Build dedicated QA agents that review outputs for grammar, brand voice, factual accuracy, and completeness.

2. **Multi-Stage Validation**: Implement validation at multiple workflow stages rather than only at the end to catch issues early.

3. **Human-in-the-Loop**: For critical operations, include human review steps before final output delivery.

4. **Quality Metrics Tracking**: Monitor quality scores over time to identify degradation and optimization opportunities.

5. **Feedback Loops**: Implement mechanisms to capture user feedback and incorporate it into agent improvement processes.

## Common Mistakes to Avoid

### Prompt Engineering Pitfalls

1. **Generic System Prompts**: Using vague prompts like "You are a helpful assistant" instead of specific role definitions with clear responsibilities and expertise areas.

2. **Missing Output Format Specifications**: Failing to specify exact output format requirements, leading to inconsistent response structures that break downstream processing.

3. **Overloading Single Prompts**: Trying to accomplish too many tasks in one agent instead of breaking complex operations into specialized agent chains.

4. **Ignoring Context Injection**: Hard-coding information in prompts instead of using dynamic variables to inject relevant context from workflow data.

5. **No Examples or Guidelines**: Providing instructions without examples of good vs. bad outputs, leading to unpredictable quality.

### Tool Integration Errors

1. **Poor Tool Descriptions**: Writing unclear tool descriptions that don't help the agent understand when and how to use each tool effectively.

2. **Tool Overload**: Adding too many tools to a single agent, causing confusion and poor tool selection decisions.

3. **Missing API Key Management**: Failing to properly secure and manage API keys, leading to security vulnerabilities or service interruptions.

4. **No Rate Limit Handling**: Not implementing proper rate limiting and retry logic for external APIs, causing workflow failures during high usage.

5. **Tool Result Blindness**: Not validating or processing tool results before using them, leading to poor quality outputs based on incomplete or incorrect tool data.

### Memory Management Mistakes

1. **Inconsistent Session IDs**: Using different session ID generation methods across workflows, breaking conversation continuity.

2. **Memory Window Extremes**: Setting memory windows too small (losing important context) or too large (excessive token costs and processing time).

3. **No Memory Cleanup**: Allowing memory stores to grow indefinitely without cleanup, leading to performance degradation and storage costs.

4. **Context Pollution**: Storing irrelevant information in memory that confuses the agent and wastes tokens.

5. **Cross-User Memory Leakage**: Accidentally sharing memory between different users or sessions, creating privacy and accuracy issues.

### Architecture and Scaling Issues

1. **Monolithic Agent Design**: Building single agents that try to handle all tasks instead of creating specialized agents for specific functions.

2. **No Error Handling**: Failing to implement proper error handling and fallback strategies, causing complete workflow failures from minor issues.

3. **Ignoring Cost Optimization**: Using expensive models for all tasks regardless of complexity, leading to unsustainable operational costs.

4. **No Performance Monitoring**: Running agents without tracking performance metrics, missing optimization opportunities and cost overruns.

5. **Synchronous Processing**: Processing everything sequentially when parallel processing could significantly improve performance.

### Production Deployment Errors

1. **Insufficient Testing**: Deploying agents without thorough testing across different scenarios and edge cases.

2. **No Monitoring or Alerting**: Running production agents without monitoring for failures, performance issues, or quality degradation.

3. **Hard-Coded Configuration**: Embedding configuration values in workflows instead of using variables, making updates and maintenance difficult.

4. **No Backup Strategies**: Failing to implement backup models or manual processes for when AI agents fail.

5. **Ignoring User Experience**: Focusing only on technical functionality without considering user experience, response times, and error messaging.

## Tools & Resources

### AI Model Providers

**OpenRouter (Unified Access)**
- **URL**: openrouter.ai
- **Purpose**: Access multiple AI models through single API
- **Key Models**: Claude 3.5 Sonnet, GPT-4 Turbo, Gemini 2.0 Flash, DeepSeek R1
- **Pricing**: Pay-per-use, competitive rates
- **Setup**: Header authentication with Bearer token

**Anthropic (Direct)**
- **URL**: console.anthropic.com
- **Purpose**: Direct access to Claude models
- **Key Models**: Claude 3.5 Sonnet, Claude 3.5 Haiku
- **Pricing**: $0.003-0.015 per 1K tokens
- **Setup**: API key authentication

**OpenAI (Direct)**
- **URL**: platform.openai.com
- **Purpose**: Direct access to GPT models
- **Key Models**: GPT-4 Turbo, GPT-4, GPT-3.5 Turbo
- **Pricing**: $0.001-0.03 per 1K tokens
- **Setup**: API key authentication

**Google AI (Direct)**
- **URL**: ai.google.dev
- **Purpose**: Access to Gemini models
- **Key Models**: Gemini 2.0 Flash Pro, Gemini 1.5 Pro
- **Pricing**: Free tier available, then pay-per-use
- **Setup**: API key authentication

### Research and Data Tools

**Perplexity AI**
- **URL**: perplexity.ai
- **Purpose**: AI-powered web search and research
- **Models**: sonar-pro (detailed), sonar-online (fast)
- **Features**: Real-time information, source citations
- **Pricing**: $20/month for Pro, API pricing separate
- **Integration**: Built-in N8N tool

**Reddit API**
- **URL**: reddit.com/dev/api
- **Purpose**: Community discussions and sentiment analysis
- **Features**: Subreddit search, comment analysis
- **Pricing**: Free with rate limits
- **Integration**: Built-in N8N tool

**Explorium (LinkedIn Data)**
- **URL**: explorium.ai
- **Purpose**: Professional profile and company data
- **Features**: LinkedIn profile enrichment, company insights
- **Pricing**: Contact for enterprise pricing
- **Integration**: API integration via HTTP Request nodes

### Workflow and Automation Tools

**N8N**
- **URL**: n8n.io
- **Purpose**: Workflow automation platform
- **Key Features**: AI Agent nodes, visual workflow builder
- **Pricing**: Free self-hosted, cloud plans from $20/month
-