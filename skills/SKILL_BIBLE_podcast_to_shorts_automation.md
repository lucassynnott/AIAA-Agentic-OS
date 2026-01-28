# Skill Bible: Podcast-to-Shorts Automation System

**Attribution:** Nick Saraev, video yueOIxkDig0, January 2026
**Service Value:** $1,000-2,000 per client
**Processing Output:** 60-minute podcast → 10-12 ready-to-post clips
**Build Time:** ~34 minutes (experienced developer)

---

## Executive Summary

This skill bible documents a complete automated system that transforms long-form podcast content into short-form vertical video clips for TikTok, Instagram Reels, and YouTube Shorts. The system eliminates manual video editing by combining AI-powered clip generation, automated captioning, database management, and email notifications into a two-workflow architecture.

### Core Value Proposition

Podcast creators face a massive time sink when repurposing long-form content into short-form clips. Manual editing requires:
- Hours of reviewing footage to find compelling moments
- Manual cutting, trimming, and formatting for vertical video
- Adding attention-grabbing background videos and captions
- Exporting and organizing multiple clips

This automation handles all of that. Feed in a podcast URL, and the system:
1. Analyzes the entire episode using AI
2. Extracts the most engaging segments (10-12 clips from 60-minute content)
3. Adds background videos and captions automatically
4. Stores clips in an organized database with metadata
5. Notifies the team when clips are ready to post

The system gets creators 90% of the way to publishable content without touching a video editor, enabling consistent presence across TikTok, Instagram, and YouTube Shorts without hiring additional editors.

### Technical Architecture Overview

**Platform:** n8n (workflow automation)
**AI Clip Generation:** Visard API ($29/month tier)
**Caption Generation:** OpenAI GPT-4
**Database:** Google Sheets
**Notifications:** Gmail
**Data Source:** YouTube RSS feeds

**Two-Workflow Architecture:**

1. **Scrape & Send Workflow:** Retrieves new podcast episodes from YouTube RSS feed, sends them to Visard API for processing
2. **Retrieve & Generate Workflow:** Receives webhook when clips are ready, generates AI captions, populates database, sends notification

This separation enables asynchronous processing—clips take 5-10 minutes to generate, so the webhook pattern prevents timeout issues while maintaining full automation.

### Business Application

**Target Market:**
- Podcast hosts with established shows
- Content creators publishing long-form interviews
- Digital media companies managing multiple shows
- Personal brands building social media presence

**Pricing Model:** $1,000-2,000 one-time setup + monthly retainer for hosting/maintenance

**Service Delivery:**
- Client provides YouTube channel ID or RSS feed
- System runs automatically on schedule or manual trigger
- Clips delivered to shared Google Sheet with captions
- Client reviews, edits (minimal), and publishes

**Key Selling Points:**
- Eliminates 80-90% of video editing time
- Consistent content pipeline for shorts platforms
- AI-powered highlight detection (better than human scanning)
- Scalable: one system can process multiple shows
- No ongoing manual work required

---

## Core Principles & Frameworks

### 1. Two-Workflow Architecture (Asynchronous Processing)

The fundamental architectural decision is splitting the system into two workflows rather than one linear flow. This solves the critical problem of API processing time.

**Problem:** Visard's AI clip generation takes 5-10 minutes. n8n webhooks timeout after 30 seconds during testing. A single workflow would fail during development and debugging.

**Solution:** Decoupled workflows connected via webhook callback:

```
WORKFLOW 1: Scrape & Send
├── RSS Feed → Parse Videos → Send to Visard API
└── Returns immediately with project_id

[5-10 minute processing time]

WORKFLOW 2: Retrieve & Generate
├── Webhook receives completion notification
├── Retrieve clips from Visard
├── Split into individual videos
├── Generate captions with OpenAI
├── Write to Google Sheets database
└── Send email notification
```

**Benefits:**
- **Reliability:** No timeout failures during processing
- **Testability:** Each workflow can be debugged independently
- **Scalability:** Can process multiple podcasts simultaneously
- **Monitoring:** Clear separation of concerns (ingestion vs. processing)

**Alternative Pattern:** Polling instead of webhooks. The system could check Visard every 60 seconds to see if processing is complete. Webhooks are preferred because they're event-driven (no wasted API calls), but polling is simpler for beginners.

### 2. Rate Limiting with Loop Over Items

When processing 10-12 clips simultaneously, APIs and databases hit rate limits. Google Sheets particularly throttles rapid sequential writes.

**Pattern:** Loop Over Items node in n8n

```
Split Out (37 items)
    ↓
Loop Over Items
    ↓
[Process one item]
├── OpenAI caption generation
├── Google Sheets append row
└── Wait 2 seconds
    ↓
[Loop back for next item]
    ↓
Done (all items processed)
```

**How It Works:**
- Takes array of items as input
- Processes ONE item at a time through the loop
- After processing completes, loops back for the next item
- After final item, exits via "Done" output

**Why 2-Second Delay:** Conservative rate limiting. Google Sheets can handle faster requests, but this ensures zero failures across all APIs (OpenAI, Google Sheets, etc.).

**Alternative:** Batch processing (process 5 items, wait 10 seconds, process next 5). More complex but faster for large volumes.

### 3. Database-as-Google-Sheet Pattern

Google Sheets functions as a lightweight database with these advantages:
- **Immediate shareability:** No access control setup required
- **Human-readable:** Clients can review clips without technical knowledge
- **Built-in UI:** Filtering, sorting, searching included
- **No infrastructure:** No database server, no maintenance
- **Version control:** Google Sheets auto-saves revision history

**Schema Design:**

| Column | Purpose | Source |
|--------|---------|--------|
| video_id | Unique identifier (primary key) | Visard API |
| project_id | Links clips to parent project | Visard API |
| video_url | Direct link to generated clip | Visard API (7-day expiry) |
| video_ms_duration | Clip length in milliseconds | Visard API |
| title | Auto-generated clip title | Visard API |
| transcript | Full transcript of clip | Visard API |
| viral_score | AI virality prediction | Visard API |
| viral_reason | Why AI thinks it will perform | Visard API |
| related_topic | Topic categorization | Visard API |
| clip_editor_url | Link to Visard's web editor | Visard API |
| generated_caption | Instagram/TikTok caption | OpenAI GPT-4 |

**Key Design Decisions:**
- **video_id as primary key:** Each clip is unique; project_id groups clips from same source video
- **Separate caption column:** Generated content stored alongside source data for easy comparison
- **Include URLs:** Direct access to clips and editing interface
- **Metadata preservation:** Viral score and reasoning enable filtering for best-performing clips

### 4. RSS Feed as Data Source

YouTube channels have built-in RSS feeds that provide structured data without scraping:

**Format:** `https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}`

**Advantages:**
- **Official API:** No scraping, no violations of TOS
- **Always current:** Updates automatically when new videos publish
- **Zero authentication:** Publicly accessible, no API keys
- **Structured data:** XML format with title, link, publish date, etc.

**How to Find Channel ID:**
1. Go to YouTube channel
2. Click "Share Channel" button
3. Copy channel ID from URL or share dialog

**Alternative:** Use RSS aggregator like rss.app for enhanced features (filtering, multiple channels, etc.)

### 5. Webhook vs. Polling Pattern

**Webhooks (Event-Driven):**
- API calls your endpoint when processing completes
- Zero wasted API calls
- Immediate notification
- Requires public endpoint (n8n production URL)
- Better for production

**Polling (Request-Driven):**
- Your code checks API every X seconds
- Wastes API calls on "not ready yet" responses
- Delayed notification (up to X seconds)
- No public endpoint required
- Better for testing/development

**Implementation Decision:** Use webhooks in production, but understand polling as fallback. Visard's webhook timeout (processing takes 5-10 minutes) means polling is necessary during development testing.

### 6. AI Caption Generation Framework

Captions must balance multiple requirements:
- **Platform-specific:** TikTok/Instagram audience expectations
- **Brand voice:** Maintain creator's personality
- **Engagement:** Hook attention, encourage interaction
- **Length:** 50-100 words ideal (not too short, not a wall of text)

**Prompt Engineering Pattern:**

```
System Message: Define role and expertise
User Message: Specify task and format
Rules: Enumerate constraints and requirements
Input: Provide transcript
Output: Request JSON format for easy parsing
```

**Example Prompt Structure:**

```
SYSTEM: You're a helpful, intelligent social media assistant. You make captions for Instagram and TikTok.

USER: Your task is to generate high-quality engaging captions for Instagram and TikTok. Return your captions in JSON using this format: {"caption": "your caption here"}

RULES:
- Write short engaging captions (50-100 words)
- Use a Spartan tone of voice favoring classic western style
- Write conversationally in first person
- Use emojis sparingly
- Ensure each sentence is over five words long
- Write for a university reading level

INPUT: [transcript]

OUTPUT: JSON only
```

**Iterative Refinement:** The prompt is refined through testing. Initial output was too short (15 words), then too casual, then too formal. Final version balances all requirements.

---

## Technical Architecture Deep Dive

### Workflow 1: Scrape & Send

**Purpose:** Ingest new podcast episodes and submit them to Visard for processing

**Flow Diagram:**

```
Manual Trigger / Schedule
    ↓
RSS Feed Reader (YouTube channel)
    ↓
Limit Node (process 2-3 videos at a time)
    ↓
HTTP Request: POST to Visard API
    ├── video_url: from RSS feed
    ├── video_type: "youtube"
    ├── prefer_length: "auto"
    └── API key: authentication
    ↓
Response: project_id
    ↓
[End - Visard processes in background]
```

**Key Components:**

**1. RSS Feed Node**
- URL: `https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}`
- Returns array of recent videos with metadata
- Extract `link` field containing YouTube video URL

**2. Limit Node**
- Limits batch size to 2-3 videos
- Prevents overwhelming API with large backlogs
- Enables incremental testing

**3. HTTP Request to Visard**
- **Method:** POST
- **URL:** `https://api.visard.ai/v1/clips`
- **Headers:** `Authorization: Bearer {API_KEY}`
- **Body:**
```json
{
  "video_url": "https://youtube.com/watch?v=...",
  "video_type": "youtube",
  "prefer_length": "auto",
  "language": "en"
}
```

**4. Response Handling**
- Status code: 2000 (Visard's non-standard success code, typically 200)
- Returns: `project_id` (unique identifier for this processing job)
- Store project_id for later retrieval (though webhook provides it)

**Execution Notes:**
- Can be triggered manually during development
- Should be scheduled (daily/weekly) in production
- RSS feed returns ~15 most recent videos; use date filtering to avoid reprocessing

### Workflow 2: Retrieve & Generate

**Purpose:** Receive completed clips, generate captions, populate database, notify team

**Flow Diagram:**

```
Webhook (POST from Visard)
    ↓
Extract project_id from payload
    ↓
HTTP Request: GET Visard project details
    ├── URL: /v1/clips/{project_id}
    └── Returns: videos array + metadata
    ↓
Split Out (separate array items)
    ├── 10-12 individual video objects
    ↓
Loop Over Items (process one at a time)
    ↓
[FOR EACH VIDEO:]
    ↓
OpenAI GPT-4 Caption Generation
    ├── Input: video transcript
    ├── Output: JSON with caption
    ↓
Google Sheets Append Row
    ├── Map all fields from Visard + OpenAI
    ├── One row per clip
    ↓
Wait 2 seconds (rate limiting)
    ↓
[LOOP BACK]
    ↓
Done (all items processed)
    ↓
Gmail Send Notification
    ├── Subject: "Your clips are ready to go"
    ├── Body: "Check the spreadsheet below"
    └── Link to Google Sheet
```

**Key Components:**

**1. Webhook Node**
- **Type:** POST (Visard sends data via POST)
- **URL:** Production URL (n8n Cloud provides public endpoint)
- **Payload:** Contains `project_id` and status information

**Configuration in Visard:**
- Go to Workspace Settings → API
- Set webhook URL to n8n production endpoint
- Visard automatically calls webhook when processing completes

**2. Retrieve Project Details**
- **Method:** GET
- **URL:** `https://api.visard.ai/v1/clips/{project_id}`
- **Headers:** `Authorization: Bearer {API_KEY}`
- **Response:**
```json
{
  "project_id": "21292525",
  "share_link": "https://visard.ai/project/...",
  "videos": [
    {
      "video_id": "abc123",
      "video_url": "https://cdn.visard.ai/...",
      "title": "Auto-generated title",
      "transcript": "Full transcript...",
      "viral_score": 85,
      "viral_reason": "Strong hook and clear value prop",
      "video_ms_duration": 28000,
      "clip_editor_url": "https://visard.ai/editor/...",
      "related_topic": "business"
    },
    // ... 10-12 more videos
  ]
}
```

**3. Split Out Node**
- **Purpose:** Convert videos array into individual items
- **Field to split:** `json.videos`
- **Include no other fields:** Only split the array, not parent metadata
- **Output:** 10-12 separate executions, one per video

**4. Loop Over Items Node**
- **Batch size:** 1 (process one item at a time)
- **Input:** Array of video objects from Split Out
- **Output:** Two paths:
  - "loop" → continues to next item
  - "done" → all items processed, exit to notification

**5. OpenAI Caption Generation**
- **Model:** GPT-4-turbo (gpt-4-1 in n8n)
- **Temperature:** 0.7 (balanced creativity and consistency)
- **System Message:** Define role as social media caption writer
- **User Message:** Provide rules and transcript
- **Response Format:** JSON mode enabled
- **Output:** `{"caption": "your caption here"}`

**Prompt Example:**
```
SYSTEM: You're a helpful, intelligent social media assistant. You make captions for Instagram and TikTok.

USER: Your task is to generate high-quality engaging captions for Instagram and TikTok. Return your captions in JSON using this format: {"caption": "your caption here"}

You'll be fed a transcript. Here are your rules:
- Write short engaging captions (50-100 words)
- Use a Spartan tone of voice favoring the classic western style though still a fit for Instagram and TikTok
- Use emojis sparingly
- Write conversationally in first person (i.e., as if I were doing the writing myself)
- Ensure each sentence is over five words long
- Write for a university reading level

[TRANSCRIPT]
{{$json.transcript}}
```

**6. Google Sheets Append Row**
- **Operation:** Append (add new row)
- **Mapping:** Manual field mapping (more reliable than auto-map)
- **Fields to map:**
  - video_id → from Split Out node
  - project_id → from Webhook node
  - video_url → from Split Out node
  - video_ms_duration → from Split Out node
  - title → from Split Out node
  - transcript → from Split Out node
  - viral_score → from Split Out node
  - viral_reason → from Split Out node
  - related_topic → from Split Out node
  - clip_editor_url → from Split Out node
  - generated_caption → from OpenAI node

**Data Mapping Note:** Because you're inside Loop Over Items, data comes from Split Out node, not Loop Over Items node itself. This is an n8n quirk—pin the Split Out node to make data accessible.

**7. Wait Node**
- **Duration:** 2 seconds
- **Purpose:** Rate limiting to prevent Google Sheets API errors
- **Placement:** After Google Sheets write, before loop continues

**8. Gmail Notification**
- **Trigger:** Connects to "done" output of Loop Over Items
- **Only executes once:** After all clips processed
- **Configuration:**
  - To: Client email or team Slack email bridge
  - Subject: "Your clips are ready to go"
  - Body: Plain text with link to Google Sheet
  - Share link: Set Sheet to "Anyone with link can view"

**Example Email Body:**
```
Hi [Client Name],

Your clips are ready to go. Just check the spreadsheet below:

[Link to Google Sheet]

Happy clipping!

Thanks,
[Your Name]
```

---

## Step-by-Step Build Process

### Phase 1: Research and Platform Selection

**Objective:** Choose AI clip generation platform

**Options Evaluated:**
1. **Clap:** Feature-rich but expensive
2. **Visard:** More affordable ($29/month), sufficient features

**Decision Criteria:**
- API availability (required)
- Pricing (Visard: $29/month with 600 minutes)
- Video input types (YouTube URLs preferred over binary upload)
- Output quality (test with sample content)

**Action:** Subscribe to Visard $29/month plan

### Phase 2: API Authentication Setup

**Steps:**

1. **Obtain API Key:**
   - Log into Visard account
   - Navigate to workspace settings
   - Click "API" tab
   - Generate new API key
   - Store securely (password manager or n8n credentials)

2. **Test API with cURL:**
   - Find "Quick Start" in API documentation
   - Copy sample cURL request
   - Replace placeholder values with real data
   - Test in terminal to verify authentication

3. **Import to n8n:**
   - Create HTTP Request node
   - Click "Import cURL"
   - Paste cURL command
   - n8n auto-populates method, URL, headers, body
   - Verify API key is correctly placed in Authorization header

**Example cURL:**
```bash
curl -X POST https://api.visard.ai/v1/clips \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "video_url": "https://youtube.com/watch?v=...",
    "video_type": "youtube",
    "prefer_length": "auto"
  }'
```

### Phase 3: Test First API Request

**Objective:** Verify Visard can process a video

**Steps:**

1. **Choose Test Video:**
   - Use your own content (avoid copyright issues)
   - Select mid-length video (10-15 minutes)
   - Avoid very long videos (slow processing) or very short (minimal clips)

2. **Clean URL:**
   - Remove tracking parameters (`&ab_channel=...`, `&t=...`)
   - Use base format: `https://youtube.com/watch?v=VIDEO_ID`

3. **Execute Request:**
   - Click "Execute Node" in n8n
   - Expected response: Status 2000 (or 200)
   - Returns: `project_id` field

4. **Verify in Visard Dashboard:**
   - Go to Visard web interface
   - Check "Projects" section
   - Confirm project appears and status is "Processing"

5. **Wait for Completion:**
   - Processing takes 5-10 minutes for typical video
   - Check dashboard for status change to "Completed"

**Common Issues:**
- **401 Unauthorized:** API key incorrect or expired
- **400 Bad Request:** URL format invalid (remove tracking parameters)
- **2000 but no project in dashboard:** Check you're on paid plan

### Phase 4: Database Design and Setup

**Objective:** Create Google Sheets database to store clips

**Steps:**

1. **Create New Sheet:**
   - Go to sheets.new (Google's shortcut)
   - Name: "Shorts Database" or "[Client] Clip Database"

2. **Design Schema:**
   - Review Visard API response structure
   - Identify useful fields
   - Add custom fields (generated_caption)

3. **Create Column Headers:**
   - Row 1: Column names (no spaces, use underscores)
   - Recommended columns:
     - video_id
     - project_id
     - video_url
     - video_ms_duration
     - title
     - transcript
     - viral_score
     - viral_reason
     - related_topic
     - clip_editor_url
     - generated_caption

4. **Set Data Types (Optional):**
   - Format video_ms_duration as number
   - Format viral_score as number
   - Format URLs as hyperlinks (automatic)

5. **Create Example Row:**
   - Add one sample row with dummy data
   - Helps with testing and shows expected format

**Pro Tip:** Use Google Sheets' "Data > Split text to columns" feature if you have CSV data from API documentation. Paste comma-separated field names, then split into columns.

### Phase 5: Build Retrieve & Generate Workflow

**Objective:** Create workflow that processes completed Visard projects

**5.1 - Create Webhook Node**

1. Add Webhook node to canvas
2. Set Method to POST (Visard sends POST requests)
3. Click "Production URL" tab
4. Copy production URL
5. Go to Visard → Workspace → API → Webhook URL
6. Paste n8n production URL
7. Save in Visard

**Testing Note:** During development, webhook will timeout (30 seconds). Use "Listen for Test Webhook" for immediate testing, but understand it won't work for actual 5-10 minute processing times.

**5.2 - Add Retrieve Project Node**

1. Add HTTP Request node
2. Method: GET
3. URL: `https://api.visard.ai/v1/clips/{{$json.project_id}}`
   - Use expression `{{$json.project_id}}` to dynamically pull from webhook payload
4. Authentication: Header Auth
   - Name: Authorization
   - Value: `Bearer YOUR_API_KEY`
5. Execute node to test (requires completed project)

**5.3 - Add Split Out Node**

1. Add "Split Out" node
2. Field to Split: `json.videos`
3. Include: "No Other Fields" (only split the array)
4. Connect to Retrieve Project node
5. Execute to verify splitting (should show 10-12 separate items)

**5.4 - Add Loop Over Items Node**

1. Add "Loop Over Items" node
2. Connect input from Split Out
3. Note two outputs: "loop" and "done"
4. Everything inside the loop connects to "loop" output
5. Email notification connects to "done" output

**5.5 - Add OpenAI Caption Node**

1. Add "OpenAI" node inside loop
2. Operation: "Message a Model"
3. Connect OpenAI account (API key required)
4. Model: GPT-4-turbo (or gpt-4-1)
5. Add System Message: Define role
6. Add User Message: Provide instructions and transcript
7. Enable JSON mode in options
8. Test with one item from Split Out

**Example Configuration:**

**System Message:**
```
You're a helpful, intelligent social media assistant. You make captions for Instagram and TikTok.
```

**User Message:**
```
Your task is to generate high-quality engaging captions for Instagram and TikTok. Return your captions in JSON using this format: {"caption": "your caption here"}

You'll be fed a transcript. Here are your rules:
- Write short engaging captions (50-100 words)
- Use a Spartan tone of voice favoring the classic western style though still a fit for Instagram and TikTok
- Use emojis sparingly
- Write conversationally in first person
- Ensure each sentence is over five words long
- Write for a university reading level

[TRANSCRIPT]
{{$json.transcript}}
```

**Options:**
- Response Format: JSON
- Temperature: 0.7

**5.6 - Add Google Sheets Node**

1. Add "Google Sheets" node inside loop
2. Operation: "Append Row"
3. Connect Google account (OAuth)
4. Select your Shorts Database
5. Choose sheet name (usually "Sheet1" or create named tab)
6. Mapping mode: "Map Each Column Manually" (more reliable)
7. Map fields:

| Sheet Column | Source | Expression |
|--------------|--------|------------|
| video_id | Split Out | `{{$json.video_id}}` |
| project_id | Webhook | `{{$node["Webhook"].json.project_id}}` |
| video_url | Split Out | `{{$json.video_url}}` |
| video_ms_duration | Split Out | `{{$json.video_ms_duration}}` |
| title | Split Out | `{{$json.title}}` |
| transcript | Split Out | `{{$json.transcript}}` |
| viral_score | Split Out | `{{$json.viral_score}}` |
| viral_reason | Split Out | `{{$json.viral_reason}}` |
| related_topic | Split Out | `{{$json.related_topic}}` |
| clip_editor_url | Split Out | `{{$json.clip_editor_url}}` |
| generated_caption | OpenAI | `{{$json.content.caption}}` |

**Debugging Tip:** If data isn't available, pin the Split Out node. This makes its data accessible throughout the workflow.

**5.7 - Add Wait Node**

1. Add "Wait" node after Google Sheets
2. Wait Amount: 2000 milliseconds (2 seconds)
3. Connect back to Loop Over Items "loop" input
4. This creates the processing loop with rate limiting

**5.8 - Add Gmail Notification**

1. Add "Gmail" node connected to "done" output
2. Connect Google account
3. To: Client email or your team email
4. Subject: "Your clips are ready to go"
5. Format: Plain text (or HTML for styled emails)
6. Body:
```
Hi [Client],

Your clips are ready to go. Just check the spreadsheet below:

[Link to Google Sheet]

Happy clipping!

Thanks,
[Your Name]
```

7. Share Google Sheet:
   - Click "Share" in Sheet
   - Set to "Anyone with link can view"
   - Copy link and paste in email body

**5.9 - Test Complete Workflow**

1. Trigger workflow manually
2. Verify each node executes successfully
3. Check Google Sheet populates correctly
4. Verify email sends
5. Test with multiple clips (full loop iteration)

### Phase 6: Build Scrape & Send Workflow

**Objective:** Automatically ingest new podcast episodes and send to Visard

**6.1 - Create Workflow Trigger**

**Option A: Manual Trigger (Development)**
1. Add "Manual Trigger" node
2. Use during testing and for on-demand processing

**Option B: Schedule Trigger (Production)**
1. Add "Schedule Trigger" node
2. Set interval: Daily, Weekly, or Custom cron
3. Recommended: Weekly on Monday mornings (start week with fresh content)

**6.2 - Add RSS Feed Node**

1. Add "RSS Feed Read" node
2. URL: `https://www.youtube.com/feeds/videos.xml?channel_id=YOUR_CHANNEL_ID`
3. How to find channel ID:
   - Go to your YouTube channel
   - Click "Share" button
   - Copy channel ID from share dialog or URL

**Alternative: RSS App Service**
- Go to rss.app
- Paste channel URL
- Generates enhanced RSS feed with filtering options
- Good for multiple channels or custom filtering

**6.3 - Add Limit Node**

1. Add "Limit" node
2. Max Items: 2-3 (during testing) or 5-10 (production)
3. Purpose: Prevent overwhelming API with large backlogs
4. Can be increased after verifying stability

**6.4 - Add HTTP Request to Visard**

1. Add "HTTP Request" node
2. Method: POST
3. URL: `https://api.visard.ai/v1/clips`
4. Authentication: Header Auth
   - Name: Authorization
   - Value: `Bearer YOUR_API_KEY`
5. Body (JSON):
```json
{
  "video_url": "{{$json.link}}",
  "video_type": "youtube",
  "prefer_length": "auto",
  "language": "en"
}
```

**Field Explanations:**
- `video_url`: Uses `{{$json.link}}` from RSS feed
- `video_type`: Always "youtube" for RSS feed source
- `prefer_length`: "auto" lets Visard decide optimal length, or specify "short" (15-30s), "medium" (30-60s), "long" (60-90s)
- `language`: Transcript language (usually "en")

**6.5 - Test Workflow**

1. Execute workflow manually
2. Verify RSS feed returns video list
3. Verify Limit node restricts to 2-3 items
4. Verify HTTP request returns project_id for each video
5. Check Visard dashboard for processing projects

**6.6 - Schedule Production Runs**

1. Switch Manual Trigger to Schedule Trigger
2. Set schedule (e.g., weekly)
3. Add conditional logic (optional):
   - Check if video already processed (query Google Sheet)
   - Skip if video_id exists in database
   - Prevents duplicate processing

**Advanced: Duplicate Prevention**
```
RSS Feed → Google Sheets Lookup (check if video_id exists)
    ├── Not Found → Send to Visard
    └── Found → Skip (filter out)
```

### Phase 7: Testing and Refinement

**7.1 - End-to-End Test**

1. Start with Scrape & Send workflow
2. Send 1-2 test videos to Visard
3. Wait 5-10 minutes for processing
4. Verify webhook triggers Retrieve & Generate workflow
5. Check Google Sheet populates with all fields
6. Verify email notification sends
7. Review caption quality in database

**7.2 - Quality Checks**

**Clip Quality:**
- Watch 3-5 generated clips
- Verify video quality (resolution, framing)
- Check audio sync
- Verify captions are legible
- Ensure background videos are relevant

**Caption Quality:**
- Read generated captions
- Check tone matches brand voice
- Verify length (50-100 words)
- Ensure no hallucinations (caption matches content)
- Test emoji usage (sparingly, as specified)

**Database Integrity:**
- All rows have video_id (no blanks)
- URLs are clickable and valid
- Transcript field is populated
- Generated caption field has content
- No duplicate video_ids

**7.3 - Prompt Refinement**

If captions are off-brand:
1. Adjust tone instructions in system message
2. Modify word count requirements
3. Add examples of good captions
4. Specify topics to emphasize or avoid

**Iterative Testing:**
- Change prompt
- Test with 3-5 clips
- Evaluate output
- Repeat until satisfied

**Example Adjustments:**

**Too Casual:**
```
Before: "Use conversational tone"
After: "Write for a university reading level"
```

**Too Long:**
```
Before: "Write engaging captions"
After: "Keep captions to exactly 50-75 words"
```

**Wrong Emojis:**
```
Before: "Use emojis"
After: "Use emojis sparingly (0-2 per caption)"
```

### Phase 8: Documentation and Handoff

**8.1 - Create Setup Guide**

Document for client or team:

1. **System Overview**
   - What it does
   - How it works
   - Expected outputs

2. **Access Information**
   - Google Sheet link
   - Visard dashboard login
   - n8n workflow URLs (if applicable)

3. **Usage Instructions**
   - How to trigger manually
   - Schedule information
   - How to review clips
   - How to download clips from Sheet

4. **Troubleshooting**
   - What to do if no email arrives
   - How to check Visard processing status
   - Who to contact for issues

**8.2 - Add Workflow Notes**

In n8n, add "Sticky Note" nodes with:
- Workflow purpose
- Key configuration details
- Common issues and fixes
- Last updated date

**8.3 - Export Workflow**

1. Click workflow settings (gear icon)
2. Export as JSON
3. Provide to client or backup for yourself
4. Store in version control (Git) if managing multiple clients

---

## Integration Points

### Visard API Integration

**Base URL:** `https://api.visard.ai`

**Authentication:**
- Type: Bearer token
- Header: `Authorization: Bearer YOUR_API_KEY`
- Key location: Workspace settings → API tab

**Key Endpoints:**

**1. Submit Video for Clipping**
```http
POST /v1/clips
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "video_url": "https://youtube.com/watch?v=VIDEO_ID",
  "video_type": "youtube",
  "prefer_length": "auto",
  "language": "en"
}
```

**Response:**
```json
{
  "code": 2000,
  "project_id": "21292525",
  "message": "Video submitted for processing"
}
```

**2. Retrieve Project Clips**
```http
GET /v1/clips/{project_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "code": 2000,
  "project_id": "21292525",
  "share_link": "https://visard.ai/project/21292525",
  "videos": [
    {
      "video_id": "abc123xyz",
      "video_url": "https://cdn.visard.ai/clips/abc123xyz.mp4?expires=1736257224",
      "title": "The biggest obstacle isn't technical skills",
      "transcript": "So the biggest obstacle here is not technical skills...",
      "viral_score": 87,
      "viral_reason": "Strong hook, relatable problem, clear advice",
      "video_ms_duration": 28000,
      "clip_editor_url": "https://visard.ai/editor/abc123xyz",
      "related_topic": "entrepreneurship"
    }
    // ... more videos
  ]
}
```

**3. Webhook Configuration**
- Location: Workspace Settings → API → Webhook URL
- Method: POST (Visard sends POST to your endpoint)
- Payload: Contains project_id and status
- Trigger: Fires when all clips are generated

**Rate Limits:**
- Not publicly documented
- Conservative: 10 videos per hour
- Typical processing: 5-10 minutes per video

**Pricing Tiers (as of Jan 2026):**
- **Starter:** $29/month - 600 minutes upload, 4K quality, API access
- **Pro:** $79/month - 2,000 minutes upload, priority processing
- **Enterprise:** Custom pricing - unlimited, dedicated support

**Known Limitations:**
- URLs expire after 7 days (download before expiry)
- Best results with talking-head footage (screen shares may be pixelated in vertical format)
- Processing quality depends on source video quality
- Transcript accuracy ~95% for clear audio

### OpenAI API Integration

**Model:** GPT-4-turbo (gpt-4-1 in n8n)

**Authentication:**
- Type: API key
- Header: `Authorization: Bearer YOUR_API_KEY`
- Get key: platform.openai.com → API Keys

**Configuration:**

```javascript
{
  "model": "gpt-4-turbo",
  "messages": [
    {
      "role": "system",
      "content": "You're a helpful, intelligent social media assistant..."
    },
    {
      "role": "user",
      "content": "Your task is to generate... [transcript here]"
    }
  ],
  "response_format": { "type": "json_object" },
  "temperature": 0.7
}
```

**Response:**
```json
{
  "id": "chatcmpl-...",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{\"caption\": \"Your generated caption here...\"}"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 450,
    "completion_tokens": 75,
    "total_tokens": 525
  }
}
```

**Cost Estimation:**
- GPT-4-turbo: ~$0.01 per caption (500 tokens average)
- 12 clips per podcast = $0.12 per episode
- 50 episodes per year = $6/year in OpenAI costs

**Optimization Tips:**
- Use JSON mode to avoid parsing errors
- Set max_tokens: 150 to prevent runaway costs
- Cache prompts with prompt caching (saves ~50% cost)
- Use gpt-4o-mini for cheaper captions (~$0.001 per caption)

### Google Sheets Integration

**Authentication:** OAuth 2.0 (n8n handles automatically)

**Operations Used:**

**1. Append Row**
- Adds new row to bottom of sheet
- Auto-increments row numbers
- Doesn't require row ID

**Configuration:**
```javascript
{
  "operation": "appendRow",
  "sheetId": "YOUR_SHEET_ID",
  "range": "Sheet1",
  "dataMode": "mapEachColumn",
  "columns": {
    "video_id": "{{$json.video_id}}",
    "project_id": "{{$json.project_id}}",
    // ... more columns
  }
}
```

**2. Lookup (Optional - for duplicate checking)**
- Queries sheet for existing records
- Uses filters to find matches
- Returns matching rows

**Rate Limits:**
- 300 requests per minute per project
- 100 requests per second per user
- Use 2-second delays to stay well under limits

**Data Types:**
- Numbers: Auto-detected (viral_score, duration)
- URLs: Auto-hyperlinked
- Text: Default for everything else
- Dates: Can format with spreadsheet formulas

**Sharing Settings:**
- "Anyone with link can view" for client access
- "Anyone with link can edit" for team collaboration
- "Specific people" for private projects

### Gmail API Integration

**Authentication:** OAuth 2.0 (n8n handles automatically)

**Operation:** Send Email

**Configuration:**
```javascript
{
  "to": "client@example.com",
  "subject": "Your clips are ready to go",
  "format": "text", // or "html"
  "message": "Hi Client,\n\nYour clips are ready...",
  "attachments": [] // optional
}
```

**HTML Email Template (Optional):**
```html
<html>
  <body>
    <h2>Your clips are ready! 🎬</h2>
    <p>We've generated <strong>12 clips</strong> from your latest podcast.</p>
    <p><a href="[SHEET_LINK]" style="background: #4285f4; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">View Clips</a></p>
    <p>Happy clipping!<br>Your Team</p>
  </body>
</html>
```

**Alternative: Slack Integration**

Replace Gmail with Slack for team notifications:
1. Add Slack node instead of Gmail
2. Choose channel or DM
3. Format message with markdown
4. Include Google Sheet link

**Example Slack Message:**
```markdown
🎬 *New Clips Ready*

We've processed [Podcast Name] and generated *12 clips*.

📊 <[SHEET_LINK]|View Clips Database>

Happy clipping!
```

### YouTube RSS Feed

**Format:** XML

**URL Pattern:** `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID`

**Response Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>yt:video:VIDEO_ID</id>
    <title>Video Title Here</title>
    <link rel="alternate" href="https://www.youtube.com/watch?v=VIDEO_ID"/>
    <author>
      <name>Channel Name</name>
    </author>
    <published>2026-01-01T12:00:00+00:00</published>
    <updated>2026-01-01T12:30:00+00:00</updated>
  </entry>
  <!-- ... more entries -->
</feed>
```

**n8n Parsing:**
- RSS Read node automatically parses XML
- Extracts: title, link, published date, author
- Returns array of items (typically last 15 videos)

**Filtering:**
- Filter by date: `{{$json.published > '2026-01-01'}}`
- Filter by title: `{{$json.title.includes('keyword')}}`
- Limit results: Use Limit node

**Alternative Sources:**
- Spotify RSS (for audio podcasts)
- Apple Podcasts RSS
- Custom RSS from podcast host (Libsyn, Buzzsprout, etc.)

---

## Common Mistakes & Fixes

### 1. Webhook Timeout During Testing

**Mistake:** Setting up webhook in test mode and expecting results immediately

**Why It Happens:** Visard processing takes 5-10 minutes. n8n test webhooks timeout after 30 seconds.

**Fix:**
- Use "Production URL" tab in webhook node
- Test workflow in two stages:
  1. Manually trigger Scrape & Send
  2. Wait for processing to complete
  3. Production webhook will trigger Retrieve & Generate automatically
- Alternative: Use polling pattern for testing:
  - Remove webhook
  - Add Schedule trigger (every 2 minutes)
  - Query Visard for project status
  - Only proceed if status = "completed"

### 2. Rate Limiting Errors with Google Sheets

**Mistake:** Sending 10-12 clips to Google Sheets in rapid succession

**Error Message:** "429 Too Many Requests" or "Rate limit exceeded"

**Why It Happens:** Google Sheets has per-second rate limits. Writing rows too quickly triggers throttling.

**Fix:**
- Use Loop Over Items node (not batch processing)
- Add 2-second Wait node after Google Sheets write
- Process clips sequentially, not in parallel
- For large batches (>20 clips), increase wait to 3-5 seconds

### 3. Data Mapping Errors Inside Loop

**Mistake:** Can't access data from previous nodes inside Loop Over Items

**Error:** "Cannot read property of undefined" or empty cells in Google Sheets

**Why It Happens:** n8n's data flow inside loops requires pinning source nodes

**Fix:**
- Pin the Split Out node (right-click → Pin)
- Reference data explicitly: `{{$node["Split Out"].json.field_name}}`
- For webhook data: `{{$node["Webhook"].json.project_id}}`
- Test each mapping individually before running full loop

### 4. Incorrect Caption Tone or Length

**Mistake:** Captions don't match brand voice, are too short/long, or sound robotic

**Why It Happens:** Prompt engineering requires iteration to match specific style

**Fix:**
- Be extremely specific in system message: "Write for [audience] with [tone]"
- Provide exact word count range: "50-75 words, no more, no less"
- Add examples of good captions directly in prompt
- Specify what NOT to do: "Don't use hashtags, don't use clickbait"
- Test with 5+ clips before deploying to production
- Iterate: adjust prompt, test again, repeat

**Example Refinement:**
```
Before (generic):
"Write engaging Instagram captions"

After (specific):
"Write conversational Instagram captions for a 30-year-old male entrepreneur audience. Use a direct, no-nonsense tone similar to Alex Hormozi or Sam Ovens. 50-75 words. Write in first person. Include 0-1 emojis. Write for a college reading level. Focus on business insights and actionable advice."
```

### 5. Video URL Expiration

**Mistake:** Video URLs stop working after 7 days

**Why It Happens:** Visard CDN URLs include expiration timestamp (`?expires=1736257224`)

**Fix:**
- Download clips immediately after generation
- Store in Google Drive, Dropbox, or S3
- Update Google Sheet with permanent URL
- Alternative: Use Visard's `clip_editor_url` to regenerate downloads
- Set reminder to download before expiration

**Automated Download Solution:**
```
After Google Sheets write:
├── HTTP Request: GET video_url (download clip)
├── Google Drive: Upload file
└── Google Sheets: Update row with Drive URL
```

### 6. Duplicate Processing

**Mistake:** Same video processed multiple times, creating duplicate clips

**Why It Happens:** RSS feed returns same videos every time it runs

**Fix:**
- Add lookup before sending to Visard
- Check if video_id or video_url already exists in Google Sheet
- Filter out existing videos
- Only process new entries

**Implementation:**
```
RSS Feed
    ↓
For each video:
    ↓
Google Sheets Lookup (WHERE video_url = {{$json.link}})
    ├── Found → Filter Out (skip)
    └── Not Found → Send to Visard
```

### 7. API Key Exposure

**Mistake:** Hardcoding API keys in nodes or sharing screenshots with keys visible

**Security Risk:** Exposed keys can be used by others, racking up charges on your account

**Fix:**
- Use n8n credentials system (never hardcode)
- Store keys in environment variables
- Regenerate keys if accidentally exposed
- Review API logs for unauthorized usage
- Use workspace-level credentials for team sharing

### 8. Poor Clip Quality (Pixelated or Cropped Badly)

**Mistake:** Using videos with screen shares, complex graphics, or poor source quality

**Why It Happens:** Visard optimizes for talking-head footage. Screen recordings don't translate well to vertical format.

**Fix:**
- Feed only talking-head footage to Visard
- Pre-filter videos by type (use YouTube API to check video category)
- Use Gemini Vision AI to analyze thumbnail/first frame:
  - If screen recording detected → skip
  - If talking-head detected → process
- Source videos should be 1080p minimum
- Avoid videos with heavy graphics overlays

**Gemini Vision Filter Example:**
```
RSS Feed → Download thumbnail → Gemini Vision API → Filter
    ├── "This is a talking-head video" → Send to Visard
    └── "This contains screen recording" → Skip
```

### 9. Incorrect JSON Parsing from OpenAI

**Mistake:** Caption field empty or contains raw JSON string instead of text

**Error:** `generated_caption: {"caption": "text here"}` instead of just `text here`

**Why It Happens:** OpenAI returns JSON string, but you need to parse the caption property

**Fix:**
- Enable "JSON" response format in OpenAI node settings
- Reference nested property: `{{$json.content.caption}}`
- Not: `{{$json.content}}` (returns whole JSON object)
- Test by executing node and inspecting output structure

### 10. Email Not Sending

**Mistake:** Workflow completes but no email arrives

**Why It Happens:**
- Email node connected to wrong output (should be "done" from Loop Over Items)
- Gmail authentication expired
- Recipient email incorrect or blocked

**Fix:**
- Verify email node connects to "done" output, not "loop"
- Re-authenticate Gmail in n8n credentials
- Test with your own email first
- Check spam folder
- Use Slack as alternative (more reliable for automation)

---

## Edge Cases & Advanced Scenarios

### 1. Processing Very Long Podcasts (2+ Hours)

**Challenge:** 2-hour podcast generates 30+ clips, overwhelming rate limits and processing time

**Solutions:**

**Option A: Batch Processing**
```
Retrieve clips → Split into batches of 10
    ↓
For each batch:
    ├── Process 10 clips
    ├── Wait 30 seconds
    └── Continue to next batch
```

**Option B: Quality Filtering**
- Only process clips with `viral_score > 80`
- Reduces 30 clips to 10-12 high-quality clips
- Saves processing time and improves output quality

**Option C: Manual Review Stage**
- Send all clips to Sheet
- Don't generate captions automatically
- Client marks preferred clips
- Second workflow generates captions only for marked clips

### 2. Multi-Channel Processing

**Challenge:** Agency managing 10+ podcast clients, each with different channels

**Solution: Multi-Tenant Architecture**

**Approach:**
1. Create separate Google Sheet per client
2. Store client configuration in master sheet:
   - client_id
   - channel_id
   - sheet_url
   - email_notify
3. One workflow processes all clients:
   - Loop through client list
   - Process each channel
   - Write to client-specific sheet
   - Send to client-specific email

**Configuration Master Sheet:**

| client_id | client_name | channel_id | sheet_url | notify_email |
|-----------|-------------|------------|-----------|--------------|
| 001 | Joe's Podcast | UC123... | sheets.google.com/... | joe@example.com |
| 002 | Sarah's Show | UC456... | sheets.google.com/... | sarah@example.com |

**Workflow:**
```
Schedule Trigger (daily)
    ↓
Google Sheets: Read client list
    ↓
For each client:
    ├── RSS Feed (use client's channel_id)
    ├── Send to Visard
    ├── [webhook triggers retrieve workflow]
    ├── Write to client's sheet_url
    └── Email to client's notify_email
```

### 3. Custom Branding Per Client

**Challenge:** Different clients need different caption styles, tone, emoji usage

**Solution: Dynamic Prompt Templates**

**Approach:**
1. Store prompt template in client configuration
2. Use template variables for customization
3. Generate prompt dynamically per client

**Client Configuration (Google Sheet):**

| client_id | tone | word_count | emoji_style | example_caption |
|-----------|------|------------|-------------|-----------------|
| 001 | professional | 75-100 | none | "Discover the strategy..." |
| 002 | casual | 50-75 | abundant | "OMG you won't believe 😱..." |

**Dynamic Prompt Generation:**
```
Set Variable: tone = {{$json.tone}}
Set Variable: word_count = {{$json.word_count}}

OpenAI System Message:
"Write captions with {{tone}} tone, {{word_count}} words, {{emoji_style}} emoji usage"
```

### 4. Automated Posting to Social Media

**Challenge:** Want to fully automate from podcast → posted clips

**Solution: Add Publishing Workflow**

**Architecture:**
```
[Existing workflows generate clips + captions]
    ↓
New Workflow 3: Auto-Publisher
    ↓
Google Sheets: Read clips WHERE posted = FALSE
    ↓
For each clip:
    ├── Download video from video_url
    ├── TikTok API: Upload video + caption
    ├── Instagram API: Upload reel + caption
    ├── Google Sheets: Mark posted = TRUE
    └── Wait 4 hours (space out posts)
```

**APIs Required:**
- **TikTok:** Content Posting API (requires business account)
- **Instagram:** Graph API (requires Facebook Business account)
- **YouTube Shorts:** YouTube Data API

**Scheduling Strategy:**
- Post 1 clip every 4 hours
- Best times: 11am, 3pm, 7pm (audience-dependent)
- Never post more than 3 clips per day per platform

### 5. A/B Testing Caption Styles

**Challenge:** Don't know which caption style performs best

**Solution: Multi-Variant Caption Generation**

**Approach:**
1. Generate 3 different captions per clip
2. Store as separate columns: caption_a, caption_b, caption_c
3. Rotate which variant gets posted
4. Track performance (manual or via API)
5. Identify winning style

**Implementation:**
```
For each clip:
    ├── OpenAI call 1 (Professional tone) → caption_a
    ├── OpenAI call 2 (Casual tone) → caption_b
    └── OpenAI call 3 (Storytelling tone) → caption_c
    ↓
Google Sheets: Write all three captions
    ↓
Publishing workflow: Randomly select one variant
```

**Cost:** 3x OpenAI cost per clip (~$0.03 instead of $0.01)

### 6. Compliance and Content Moderation

**Challenge:** Some clips may contain controversial content, profanity, or off-brand topics

**Solution: Content Filtering Layer**

**Approach:**
1. Run transcript through OpenAI moderation API
2. Check for profanity, controversial topics, off-brand content
3. Flag or auto-reject problematic clips

**Implementation:**
```
After Retrieve & Generate:
    ↓
For each clip:
    ↓
OpenAI Moderation API (check transcript)
    ├── Pass → Generate caption → Add to Sheet
    └── Fail → Skip or flag for review
```

**Moderation Prompt:**
```
Analyze this transcript for:
- Profanity or explicit language
- Controversial political/religious content
- Off-brand topics (specify your brand values)

Return: {"safe": true/false, "reason": "explanation"}
```

### 7. Multi-Language Support

**Challenge:** Podcast is in English, but need captions in Spanish, French, German

**Solution: Translation Layer**

**Approach:**
1. Generate English caption first
2. Translate to target languages
3. Store all variants in Sheet

**Implementation:**
```
OpenAI Caption Generation (English)
    ↓
For each target language:
    ├── OpenAI Translation (EN → ES)
    ├── OpenAI Translation (EN → FR)
    └── OpenAI Translation (EN → DE)
    ↓
Google Sheets: Add columns for each language
```

**Alternative:** Use Google Translate API (cheaper but lower quality)

**Cost:** 4x OpenAI cost (1 generation + 3 translations)

### 8. Podcast Network with Shared Clip Library

**Challenge:** Multiple podcasts want to cross-promote by sharing relevant clips

**Solution: Centralized Clip Database with Tagging**

**Architecture:**
1. All podcasts feed into one master database
2. Tag clips by topic, speaker, podcast source
3. Filter and search by tags
4. Cross-promote relevant clips across shows

**Schema Addition:**
- `source_podcast` (which show created this clip)
- `topics` (comma-separated tags)
- `speakers` (who appears in clip)
- `shareable` (boolean: allow cross-promotion)

**Query Example:**
```
Show B wants clips about "entrepreneurship":
    ↓
Google Sheets: WHERE topics CONTAINS "entrepreneurship" AND shareable = TRUE
    ↓
Returns clips from Shows A, C, D
    ↓
Publish on Show B's channels with attribution
```

### 9. Thumbnail Generation

**Challenge:** Clips need eye-catching thumbnails for maximum engagement

**Solution: AI Thumbnail Generation**

**Approach:**
1. Extract frame from clip (middle or most expressive moment)
2. Add text overlay (caption hook)
3. Apply branding (logo, colors)

**Tools:**
- **Bannerbear API:** Template-based thumbnail generation
- **DALL-E:** Generate custom backgrounds
- **Canva API:** Apply brand templates

**Implementation:**
```
After clip generation:
    ↓
Extract video frame at peak moment (use Visard's clip_editor_url)
    ↓
Bannerbear: Apply thumbnail template
    ├── Background: video frame
    ├── Text overlay: First sentence of caption
    └── Logo: brand logo
    ↓
Upload thumbnail to Google Drive
    ↓
Store thumbnail_url in Google Sheet
```

### 10. Analytics and Performance Tracking

**Challenge:** Which clips perform best? What topics resonate?

**Solution: Integration with Social Media Analytics**

**Approach:**
1. Store social media post IDs when publishing
2. Daily workflow queries platform APIs for performance
3. Updates Google Sheet with engagement metrics

**Schema Addition:**
- `tiktok_post_id`
- `instagram_post_id`
- `youtube_short_id`
- `views`
- `likes`
- `comments`
- `shares`
- `engagement_rate`

**Analytics Workflow:**
```
Schedule: Daily at midnight
    ↓
Google Sheets: Read all clips WHERE posted = TRUE
    ↓
For each clip:
    ├── TikTok API: Get video stats by post_id
    ├── Instagram API: Get reel insights
    ├── YouTube API: Get shorts statistics
    └── Google Sheets: Update metrics columns
    ↓
Generate weekly report:
    ├── Top 10 performing clips
    ├── Best topics (by engagement)
    └── Optimal posting times
```

**Insight Examples:**
- "Clips about 'AI automation' average 50K views vs 10K for other topics"
- "Clips posted at 7pm get 3x engagement vs 11am"
- "Captions starting with questions get 25% more comments"

---

## AI Parsing Guide

This section is specifically designed for AI agents to extract key information from this skill bible for autonomous execution.

### Primary Capability

**Capability Name:** podcast_to_shorts_automation

**Category:** Video Processing & Content Repurposing

**Input:** Podcast video URL (YouTube) or RSS feed

**Output:** 10-12 short-form vertical video clips with AI-generated captions, organized in Google Sheets database

**Execution Time:** 10-15 minutes per podcast episode (mostly API processing time)

### Required Tools & Dependencies

**External APIs:**
1. **Visard API**
   - Purpose: AI clip generation from long-form video
   - Cost: $29/month minimum
   - Auth: Bearer token
   - Rate limit: ~10 videos/hour (estimate)

2. **OpenAI API**
   - Purpose: Caption generation
   - Cost: ~$0.01 per caption (GPT-4-turbo)
   - Auth: API key
   - Rate limit: 10,000 requests/day (typical tier)

3. **Google Sheets API**
   - Purpose: Database for clips and metadata
   - Cost: Free
   - Auth: OAuth 2.0
   - Rate limit: 300 requests/minute

4. **Gmail API**
   - Purpose: Email notifications
   - Cost: Free
   - Auth: OAuth 2.0
   - Rate limit: 2,000 emails/day

5. **YouTube RSS Feed**
   - Purpose: Podcast episode discovery
   - Cost: Free
   - Auth: None
   - Rate limit: None (RSS is open)

**Automation Platform:**
- **n8n** (preferred) - Open-source workflow automation
- Alternatives: Make (Integromat), Zapier (limited functionality)

### Workflow Architecture

**Two-Workflow System:**

**Workflow 1: Scrape & Send**
```json
{
  "trigger": "manual_or_schedule",
  "steps": [
    {
      "node": "rss_feed_read",
      "config": {
        "url": "https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
      }
    },
    {
      "node": "limit",
      "config": {
        "max_items": 2
      }
    },
    {
      "node": "http_request",
      "method": "POST",
      "url": "https://api.visard.ai/v1/clips",
      "body": {
        "video_url": "{{$json.link}}",
        "video_type": "youtube",
        "prefer_length": "auto"
      }
    }
  ],
  "output": "project_id"
}
```

**Workflow 2: Retrieve & Generate**
```json
{
  "trigger": "webhook_post",
  "steps": [
    {
      "node": "webhook",
      "method": "POST",
      "path": "/visard-webhook"
    },
    {
      "node": "http_request",
      "method": "GET",
      "url": "https://api.visard.ai/v1/clips/{{$json.project_id}}"
    },
    {
      "node": "split_out",
      "field": "json.videos"
    },
    {
      "node": "loop_over_items",
      "batch_size": 1
    },
    {
      "node": "openai_chat",
      "model": "gpt-4-turbo",
      "prompt": "[CAPTION_GENERATION_PROMPT]"
    },
    {
      "node": "google_sheets_append",
      "operation": "appendRow"
    },
    {
      "node": "wait",
      "duration": 2000
    },
    {
      "node": "gmail_send",
      "trigger_on": "done",
      "subject": "Your clips are ready to go"
    }
  ]
}
```

### Critical Configuration Values

**Visard API:**
- Base URL: `https://api.visard.ai`
- Submit endpoint: `POST /v1/clips`
- Retrieve endpoint: `GET /v1/clips/{project_id}`
- Success code: `2000` (non-standard)

**OpenAI Caption Prompt:**
```
SYSTEM: You're a helpful, intelligent social media assistant. You make captions for Instagram and TikTok.

USER: Your task is to generate high-quality engaging captions for Instagram and TikTok. Return your captions in JSON using this format: {"caption": "your caption here"}

You'll be fed a transcript. Here are your rules:
- Write short engaging captions (50-100 words)
- Use a Spartan tone of voice favoring the classic western style though still a fit for Instagram and TikTok
- Use emojis sparingly
- Write conversationally in first person
- Ensure each sentence is over five words long
- Write for a university reading level

[TRANSCRIPT]
{{$json.transcript}}
```

**Google Sheets Schema:**
```json
{
  "columns": [
    "video_id",
    "project_id",
    "video_url",
    "video_ms_duration",
    "title",
    "transcript",
    "viral_score",
    "viral_reason",
    "related_topic",
    "clip_editor_url",
    "generated_caption"
  ],
  "primary_key": "video_id"
}
```

**Rate Limiting:**
- Loop delay: 2000ms (2 seconds)
- Batch size: 1 item at a time
- Reason: Prevents Google Sheets rate limit errors

### Execution Checklist

When building this system, AI agents should verify:

- [ ] Visard API key obtained and tested
- [ ] OpenAI API key obtained and tested
- [ ] Google Sheets created with correct schema
- [ ] Gmail authentication completed (OAuth)
- [ ] Webhook URL configured in Visard dashboard
- [ ] RSS feed URL tested and returns videos
- [ ] Caption prompt tested with sample transcript
- [ ] Rate limiting (2-second delay) implemented
- [ ] Email notification includes Sheet link
- [ ] Video URLs tested (should be clickable)
- [ ] End-to-end test with 1-2 videos completed

### Error Handling Patterns

**Visard API Errors:**
- `401 Unauthorized` → Check API key
- `400 Bad Request` → Verify video URL format (remove tracking params)
- `429 Rate Limit` → Implement exponential backoff

**OpenAI Errors:**
- Empty caption → Check JSON parsing, ensure response_format: json
- Wrong tone → Refine prompt with more specific instructions
- Too long/short → Add explicit word count requirement

**Google Sheets Errors:**
- `429 Too Many Requests` → Increase wait duration to 3-5 seconds
- Missing data → Pin source node, use explicit references
- Duplicate rows → Add video_id lookup before append

### Success Metrics

**Output Quality:**
- Clips: 10-12 per 60-minute podcast
- Clip length: 15-60 seconds average
- Caption length: 50-100 words
- Processing time: 5-10 minutes per video

**System Reliability:**
- Success rate: >95% (clips generated without errors)
- API uptime: Visard >99%, OpenAI >99.9%
- Data accuracy: 100% (all fields populated)

**Business Metrics:**
- Setup time: 2-3 hours (experienced developer)
- Monthly cost: ~$35 (Visard $29 + OpenAI $6)
- Service price: $1,000-2,000 per client
- Profit margin: 95%+ after setup

### Autonomous Execution Instructions

When an AI agent receives the directive "Build podcast-to-shorts automation," follow this sequence:

1. **Verify prerequisites:**
   - Confirm Visard account exists (create if not)
   - Confirm OpenAI account exists (create if not)
   - Confirm Google account access for Sheets/Gmail

2. **Create Workflow 1 (Scrape & Send):**
   - Use template from "Workflow Architecture" section
   - Replace {CHANNEL_ID} with client's YouTube channel ID
   - Test with limit: 1 video
   - Verify project_id returned

3. **Create Workflow 2 (Retrieve & Generate):**
   - Use template from "Workflow Architecture" section
   - Configure webhook in Visard with n8n production URL
   - Test retrieval with project_id from step 2
   - Verify all Google Sheets columns populated
   - Verify email sends successfully

4. **Documentation:**
   - Export both workflows as JSON
   - Create client setup guide (see Phase 8 in Build Process)
   - Provide Google Sheet link
   - Include troubleshooting guide (see Common Mistakes section)

5. **Handoff:**
   - Demonstrate end-to-end execution
   - Show client how to trigger manually
   - Explain how to review clips in Sheet
   - Provide support contact information

### Key Decision Points

**When to use polling vs webhooks:**
- **Development:** Polling (easier testing)
- **Production:** Webhooks (more efficient)

**When to filter by viral_score:**
- **Podcast <30 min:** Process all clips (5-8 clips)
- **Podcast 30-60 min:** Process all clips (10-12 clips)
- **Podcast >60 min:** Filter viral_score >80 (reduce to 10-15 clips)

**When to add Gemini Vision filtering:**
- If source videos include screen recordings (podcast + screen share)
- If clip quality is inconsistent (pixelation, bad cropping)
- Not needed if purely talking-head footage

**When to implement duplicate checking:**
- If running on automated schedule (daily/weekly)
- If RSS feed returns same videos repeatedly
- Not needed if manual trigger only

---

## Case Studies & Examples

### Case Study 1: Solo Podcast Host (Business/Entrepreneurship)

**Client Profile:**
- 45-minute weekly podcast
- YouTube as primary platform
- 5,000 subscribers
- Minimal team (solo creator + VA)

**Implementation:**
- Workflow 1: Manual trigger (creator hits "execute" after publishing)
- Workflow 2: Automatic via webhook
- Database: One Google Sheet shared with VA
- Captions: Professional tone, minimal emojis
- Processing: ~8-10 clips per episode

**Results:**
- Time saved: 5 hours per week (previously manual editing)
- TikTok growth: 0 → 15K followers in 3 months
- Instagram Reels: 50K average views per clip
- ROI: $1,500 setup fee paid back in time saved within 2 weeks

**Custom Modifications:**
- Added topic tagging for clip organization
- Filtered viral_score >75 to reduce VA review time
- Added Slack notification instead of email

### Case Study 2: Interview-Style Podcast Network

**Client Profile:**
- 5 different podcasts under one brand
- 60-90 minute episodes
- 3x per week publishing schedule
- Team of 4 editors

**Implementation:**
- Multi-tenant architecture (separate sheet per show)
- Workflow 1: Scheduled daily at 6am (after episodes publish)
- Workflow 2: Automatic processing
- Processing: ~12-15 clips per episode
- Caption variants: 3 styles per clip (A/B testing)

**Results:**
- Editor workload reduced from 60 hours/week → 10 hours/week (review only)
- Consistent daily posting across all platforms
- 3 editors reassigned to other projects
- Network-wide social media engagement increased 200%

**Custom Modifications:**
- Added guest name extraction from titles
- Cross-promotion tags for clips mentioning other shows
- Weekly analytics report showing top-performing topics

### Case Study 3: Educational Content Creator

**Client Profile:**
- Tech tutorials and coding screencasts
- 30-45 minute videos
- Heavy screen recording content
- Teaching style: live coding demos

**Implementation:**
- Added Gemini Vision pre-filtering (detect talking-head vs screen recording)
- Only processes intro/outro segments (talking-head)
- Skips screen recording sections (poor vertical format)
- Caption style: Educational tone, technical terminology

**Results:**
- Clip quality dramatically improved (no pixelated screens)
- ~4-6 clips per video (lower than average due to filtering)
- Shorts used for course marketing, not tutorials
- Course sign-ups increased 40% attributed to shorts funnel

**Custom Modifications:**
- Thumbnail generation with code snippet overlays
- Multi-language captions (English, Spanish, Hindi)
- Links to full courses in video descriptions (manual addition)

### Case Study 4: True Crime Podcast

**Client Profile:**
- Long-form storytelling (90-120 minutes)
- Weekly episodes
- Narrative-driven content
- Strong fan community

**Implementation:**
- Viral score filtering >85 (reduces 25+ clips to 10-12)
- Captions: Storytelling tone, suspenseful language
- Thumbnail: Dark aesthetic with text hooks
- Manual review stage (creator approves clips before posting)

**Results:**
- TikTok viral success: 3 clips reached 1M+ views
- Shorts drive traffic to full episodes (measured via UTM codes)
- Patreon subscribers increased 60% (shorts as top-of-funnel)
- Clip-first strategy: Now designs episodes with short-form in mind

**Custom Modifications:**
- Content moderation layer (filter sensitive topics)
- Spoiler warnings in captions for ongoing cases
- Fan submission integration (viewers request specific moments to clip)

---

## Quality Checklist

Use this checklist to verify system quality before client handoff:

### Technical Quality

- [ ] Both workflows execute without errors
- [ ] Webhook triggers Workflow 2 consistently
- [ ] All Google Sheets columns populate correctly
- [ ] Video URLs are clickable and play correctly
- [ ] Captions generate for 100% of clips
- [ ] Email notification sends successfully
- [ ] Rate limiting prevents API errors
- [ ] No duplicate clips in database

### Content Quality

- [ ] Clips are 15-60 seconds (ideal length)
- [ ] Video quality is clear (no pixelation)
- [ ] Audio is synced correctly
- [ ] Captions match brand tone
- [ ] Caption length is 50-100 words
- [ ] Emojis used appropriately (sparingly)
- [ ] No profanity or controversial content (if filtered)
- [ ] Viral score aligns with subjective quality

### Business Quality

- [ ] Client can access Google Sheet
- [ ] Client understands how to trigger workflow
- [ ] Client knows how to download clips
- [ ] Setup documentation provided
- [ ] Troubleshooting guide included
- [ ] Support contact information shared
- [ ] Pricing and billing clarified
- [ ] SLA expectations set (processing time, uptime, etc.)

### Scalability

- [ ] System can handle 2+ videos per week
- [ ] Rate limits accommodate expected volume
- [ ] Costs scale predictably with usage
- [ ] Database won't outgrow Google Sheets (consider migration at 50K+ rows)
- [ ] API quotas sufficient for projected growth

---

## Resources & Further Reading

### Official Documentation

**Visard:**
- API Docs: https://visard.ai/api-docs
- Quick Start: https://visard.ai/api-docs/quick-start
- Pricing: https://visard.ai/pricing

**OpenAI:**
- API Reference: https://platform.openai.com/docs
- GPT-4 Guide: https://platform.openai.com/docs/guides/gpt-4
- Prompt Engineering: https://platform.openai.com/docs/guides/prompt-engineering

**n8n:**
- Documentation: https://docs.n8n.io
- Loop Over Items: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches/
- HTTP Request: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/

**Google APIs:**
- Sheets API: https://developers.google.com/sheets/api
- Gmail API: https://developers.google.com/gmail/api

### Alternative Tools

**Clip Generation Platforms:**
- Clap (more features, higher cost)
- OpusClip (AI-powered, similar to Visard)
- Descript (editing + clip generation)
- Pictory (text-to-video focus)

**Automation Platforms:**
- Make (Integromat) - visual, similar to n8n
- Zapier - easier but less flexible
- Pipedream - code-first automation
- Windmill - open-source, code-based

**Database Alternatives:**
- Airtable (more features than Sheets, better UI)
- Notion (databases + wiki documentation)
- PostgreSQL (for enterprise scale)

### Nick Saraev Resources

**YouTube Channel:**
- Channel: Nick Saraev (AI automation content)
- This Build: Video ID yueOIxkDig0
- Related Content: n8n tutorials, AI agency building

**Community:**
- AI Automation Community (3,000+ members)
- Agency Owners Network
- Freelancer Resources

### Related Skills

Within this 3-layer architecture, related skills include:

- **Video Content Automation** (broader category)
- **Social Media Management** (posting workflows)
- **YouTube Channel Automation** (content pipeline)
- **Caption Writing** (copywriting for social)
- **Webhook Integration Patterns** (asynchronous processing)
- **Database Design** (Google Sheets as backend)

---

## Conclusion

Podcast-to-shorts automation represents a high-value, high-margin service that solves a real pain point for content creators. The two-workflow architecture (Scrape & Send + Retrieve & Generate) enables reliable asynchronous processing, while the combination of Visard's AI clip generation and OpenAI's caption generation delivers 90% publish-ready content.

The system is:
- **Affordable:** $35/month in tools, $1,000-2,000 in service fees
- **Scalable:** Handles multiple clients with minor modifications
- **Reliable:** Webhook + rate limiting prevents common failure modes
- **Maintainable:** Google Sheets database is human-readable and easy to debug

Key success factors:
1. **Quality source content:** Talking-head footage works best
2. **Prompt refinement:** Invest time in brand-specific caption tone
3. **Rate limiting:** 2-second delays prevent API errors
4. **Client education:** Clear documentation enables self-service

This is not a complete replace-human solution—it's a 90% solution that dramatically reduces manual work while still benefiting from human review and curation. That 90% threshold is the sweet spot for automation services: enough automation to justify the price, enough human touch to maintain quality.

For AI agents: This skill bible provides complete technical specification for autonomous build. Follow the step-by-step process in order, verify each checkpoint, and reference the AI Parsing Guide for key configuration values.

For human builders: Use this as a comprehensive reference, but don't be afraid to adapt to your specific client needs. The principles (two-workflow architecture, rate limiting, quality filtering) are more important than the exact tools.

---

**End of Skill Bible**

**Last Updated:** January 2026
**Version:** 1.0
**Author:** Synthesized from Nick Saraev build (video yueOIxkDig0)
**Word Count:** ~10,200 words