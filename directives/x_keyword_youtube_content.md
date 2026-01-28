# X Keyword Search to YouTube Content Generator

## What This Workflow Is

Automated content research workflow that searches X (Twitter) for high-performing posts matching specified keywords, analyzes engagement patterns, and generates YouTube video ideas with full outlines optimized for the @thelucassynnott channel.

## What It Does

1. Uses Grok-4-fast (via OpenRouter) to search X for trending/high-performing posts
2. Filters posts by engagement metrics (likes, retweets, replies)
3. Extracts content themes and viral angles
4. Generates 5 YouTube video ideas based on trending topics
5. Creates detailed video outlines using YouTube script writing best practices
6. Outputs to formatted Google Doc
7. Sends Slack notification with document link

## Prerequisites

### Required API Keys
- `OPENROUTER_API_KEY` - For Grok-4-fast access
- `SLACK_WEBHOOK_URL` - For notifications
- Google OAuth configured (`client_secrets.json` + `token.pickle`)

### Required Skill Bibles
- `skills/SKILL_BIBLE_youtube_script_writing.md`
- `skills/SKILL_BIBLE_youtube_growth.md`

### Installation
```bash
pip install openai requests python-dotenv google-auth-oauthlib google-api-python-client
```

## How to Run

### Manual Execution
```bash
python3 execution/x_keyword_youtube_content.py
```

### With Custom Keywords
```bash
python3 execution/x_keyword_youtube_content.py \
    --keywords "AI agents" "Claude Code" "automation workflows" "agentic AI" \
    --min_engagement 100 \
    --num_videos 5
```

### Scheduled (Every 3 Hours)
```bash
# Add to crontab
0 */3 * * * cd /path/to/AIAA-Agentic-OS && python3 execution/x_keyword_youtube_content.py >> .tmp/logs/x_youtube_cron.log 2>&1
```

## Inputs

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| keywords | list | No | ["AI", "automations", "claude code", "agentic workflows"] | Keywords to search on X |
| min_engagement | int | No | 50 | Minimum likes+retweets to consider "high performing" |
| num_videos | int | No | 5 | Number of video ideas to generate |
| time_range | str | No | "24h" | How far back to search (24h, 7d, 30d) |
| channel_handle | str | No | "@thelucassynnott" | YouTube channel for context |

## Process

### Step 1: X Search via Grok-4-fast
Use Grok's native X search capabilities to find high-performing posts:
- Search each keyword
- Filter by engagement metrics
- Extract post content, author, metrics
- Identify common themes and viral angles

**Grok Prompt Structure:**
```
Search X for posts about [KEYWORD] from the last 24 hours.
Find posts with high engagement (100+ likes or 20+ retweets).
For each post, extract:
- Post content
- Author handle
- Likes, retweets, replies
- Why this resonated (analysis)
```

### Step 2: Aggregate and Analyze
- Combine results from all keyword searches
- Remove duplicates
- Rank by engagement score
- Identify top 10-15 posts
- Extract common themes and patterns

### Step 3: Generate Video Ideas
Using YouTube skill bibles, transform trending topics into video concepts:
- Apply packaging principles (title + thumbnail concept)
- Ensure searchability + curiosity gap
- Map to proven video formats (tutorial, case study, list, story)
- Consider @thelucassynnott's existing content style

### Step 4: Create Full Outlines
For each video idea, generate:
- **Title**: Optimized for CTR (under 60 chars)
- **Thumbnail Concept**: Visual direction
- **Hook** (0-30s): Using the 5-part framework
- **Body Structure**: With retention tactics
- **Key Talking Points**: Bullet format
- **CTA**: What viewers should do next
- **Estimated Length**: Based on content depth

### Step 5: Format and Deliver
- Compile all content into formatted markdown
- Create Google Doc with proper formatting
- Send Slack notification with:
  - Number of posts analyzed
  - Top trending themes
  - Google Doc link
  - Timestamp

## Outputs

### Local Files
- `.tmp/x_youtube_content/[timestamp]_posts.json` - Raw X posts data
- `.tmp/x_youtube_content/[timestamp]_video_ideas.md` - Markdown output

### Google Doc
Formatted document with:
- Executive summary of trending topics
- 5 video ideas with full outlines
- Source posts referenced

### Slack Notification
- Workflow status
- Document link
- Key metrics

## Quality Gates

- [ ] Minimum 10 high-performing posts found
- [ ] All 5 video ideas have complete outlines
- [ ] Each outline includes hook, body, and CTA
- [ ] Google Doc created successfully
- [ ] Slack notification sent

## Edge Cases

| Scenario | Solution |
|----------|----------|
| Few posts found | Lower engagement threshold, expand time range |
| Grok API error | Retry with exponential backoff (3 attempts) |
| Duplicate topics | Ensure variety across 5 ideas |
| Google Doc fails | Save locally, notify without link |

## Related Directives
- `twitter_thread_writer.md` - For creating X content
- `youtube_script_generator.md` - For full video scripts

## Self-Annealing Notes

### 2026-01-27: Initial Creation
- **Issue**: Grok model ID was incorrect (`grok-3-fast` vs `grok-4-fast`)
- **Fix**: Updated to use `x-ai/grok-4-fast` which is the correct OpenRouter model ID
- **Learning**: Always verify model IDs via OpenRouter API: `curl https://openrouter.ai/api/v1/models`
- **Test Result**: Successfully generated 5 video ideas with full outlines

### 2026-01-27: Google Doc Service Account Limitation
- **Issue**: Service accounts without Google Workspace have 0 GB storage quota
- **Error**: `403 - The user's Drive storage quota has been exceeded`
- **Root Cause**: Personal Gmail service accounts cannot create files in Drive/Docs - they have zero storage allocation
- **Attempted Fixes**:
  - Shared folder approach (still counts against creator's quota)
  - `supportsAllDrives=True` parameter (no effect)
  - Drive API vs Docs API (same limitation)
- **Workaround Implemented**: Fallback delivery chain:
  1. Try Google Doc (will fail for service accounts)
  2. Try GitHub Gist if `GITHUB_TOKEN` is set
  3. Send content directly in Slack as fallback
- **Permanent Fix Options**:
  - Use Google Workspace with domain-wide delegation
  - Use OAuth2 user flow with refresh tokens (`token.pickle`)
  - Add `GITHUB_TOKEN` to Railway for Gist delivery

### 2026-01-27: OAuth2 Token Fix (RESOLVED)
- **Solution**: Used existing `token.pickle` with OAuth2 user credentials
- **Implementation**: Base64 encoded pickle stored as `GOOGLE_OAUTH_TOKEN_PICKLE` env var in Railway
- **Result**: Google Docs now created successfully using user's storage quota
- **Token refresh**: Code automatically refreshes expired tokens using refresh_token
- **Test**: Successfully created doc at https://docs.google.com/document/d/1OlXQ-DQdD_k2CEQ7VXraV9JDeFTb3KWPTCHcFs4Wcpc/edit

### 2026-01-27: Google Docs Formatting Fix
- **Issue**: Raw markdown was inserted as plain text (`# Heading`, `**bold**` visible as literal text)
- **Solution**: Created `markdown_to_docs_requests()` function that converts markdown to Google Docs API formatting
- **Implementation**:
  - Parses markdown and tracks formatting positions
  - Strips markdown syntax from display text
  - Applies native Google Docs styles (HEADING_1, HEADING_2, bold, etc.)
  - Uses unicode horizontal line for `---` dividers
- **Result**: Documents now have proper headings, bold text, and visual formatting
- **AGENTS.md Updated**: Added Rule 5 documenting Google Docs formatting requirements for all workflows
- **Test**: https://docs.google.com/document/d/1mZ3c5Y4epGlVNTEaA0ttYEEoltu3sgdy6KETzMTnObU/edit

### Model ID Reference
Current valid Grok models on OpenRouter:
- `x-ai/grok-4-fast` (recommended - fast and capable)
- `x-ai/grok-4` (full model)
- `x-ai/grok-3` / `x-ai/grok-3-mini`

## Scheduling Notes

This workflow is designed to run automatically every 3 hours to capture fresh trending content.

**Crontab Entry:**
```
0 */3 * * * cd /Users/lucasnolan/Agentic\ OS/AIAA-Agentic-OS && /usr/bin/python3 execution/x_keyword_youtube_content.py >> .tmp/logs/x_youtube_cron.log 2>&1
```

**Launchd Alternative (macOS):**
See `com.aiaa.x_youtube_content.plist` in project root.

### 2026-01-28: Dashboard Cron Toggle Implementation
- **Feature**: Added ability to toggle cron on/off from dashboard without removing deployment
- **Implementation**: Uses Railway GraphQL `serviceInstanceUpdate` mutation
- **Critical Gotcha**: `cronSchedule: ""` (empty string) causes "Problem processing request" error
- **Solution**: Use `cronSchedule: null` to disable, restore original schedule to enable
- **API Endpoint**: `https://backboard.railway.app/graphql/v2`
- **Required**: Dashboard needs `RAILWAY_API_TOKEN` env var to make Railway API calls
- **Mutation Used**:
  ```graphql
  mutation {
    serviceInstanceUpdate(
      serviceId: "5fbf1961-5c49-41ec-a776-fb4c7723bf69",
      environmentId: "951885c9-85a5-46f5-96a1-2151936b0314",
      input: { cronSchedule: null }  # or "0 */3 * * *" to restore
    )
  }
  ```
- **AGENTS.md Updated**: Added Rules 6 & 7 for Railway GraphQL API and dashboard token
- **New Directive**: Created `directives/deploy_workflow_to_dashboard.md` with complete deployment guide

### 2026-01-28: Schedule Editor Implementation
- **Feature**: Granular cron schedule editor replacing simple dropdown
- **UI Components**:
  - Interval input (1-24) for frequency
  - Unit selector ("hours" or "days")
  - Minute input (0-59) for timing within the hour
  - Save button to apply changes to Railway
  - Live cron expression display showing actual pattern
- **Dynamic "Schedule:" Text**: Header now updates automatically when schedule changes
  - `initScheduleTexts()` syncs display on page load from actual cron
  - `updateScheduleText()` called after successful save
- **cronToText Conversion**: Human-readable schedule display
  - `0 */3 * * *` → "Every 3 hours"
  - `30 * * * *` → "Every hour at :30"
  - `0 0 * * *` → "Daily at 00:00"
- **RAILWAY_API_TOKEN Fix**: Discovered token was missing from dashboard
  - Symptom: UI showed success but cron didn't change in Railway
  - Root cause: Silent API failures due to missing auth
  - Fix: Set token via GraphQL variableUpsert mutation
- **AGENTS.md Updated**: Added Rule 8 for Schedule Editor details
