# SKILL BIBLE: N8N Ad Creative Automation System ($70K Value)

## Executive Summary

A complete ad library scraper and AI image spinner system built entirely in N8N that automates 60-70% of a PPC agency's creative work. The system scrapes competitor ads from Facebook/Instagram, analyzes them with AI, generates multiple variations using GPT image editing, and organizes everything in Google Drive with a tracking spreadsheet. This eliminates the manual creative process of finding winning ads, recreating them, and testing variations.

**Core Insight**: "This could probably eliminate like 60 to 70% of an entire PPC agency's job. A lot of the time all you guys are really doing in a PPC agency is just spinning working ads—either ads that you guys have created in the past for yourself or you guys are informally or manually looking at competitor ads, finding what works, and then doing the spinning yourself."

This skill bible documents a live build with all detours, debugging, and real-world problem-solving included for maximum instructive value.

---

## 1. System Overview (The Complete Flow)

### What This System Does

```
Phase 1: Ad Discovery
├── Scrape Facebook/Instagram Ad Library via Apify
├── Filter: Static image ads only (no videos)
├── Extract: Ad images, text, metadata
└── Limit: Configurable (20 ads for testing, 100+ for production)

Phase 2: Organization Setup
├── Create Google Drive folder structure
│   ├── Parent folder: "PPC Thievery"
│   ├── Per-ad subfolders: Named by ad_archive_id
│   │   ├── "1_source_assets" folder
│   │   └── "2_spun_assets" folder
├── Create Google Sheet: "Scraped Ads" with headers
└── Initialize tracking database

Phase 3: Image Processing
├── Download source ad images
├── Upload to Google Drive (source folder)
├── Share images (make publicly accessible)
└── Generate direct download links

Phase 4: AI Analysis
├── Analyze images with OpenAI Vision (GPT-4)
├── Generate comprehensive descriptions
├── Create "change request" prompts for spinning
└── Generate 3 variants per ad

Phase 5: Image Generation
├── Loop through each variant
├── Send to GPT Image-1 edit endpoint
├── Apply style transformations
├── Generate spun versions
└── Rate limit handling (1-second delays)

Phase 6: Final Organization
├── Upload spun images to Google Drive
├── Log all data to Google Sheet:
│   ├── Timestamp, ad IDs, URLs
│   ├── Source/spun folder links
│   ├── Spin prompts used
│   └── Direct image links
└── Ready for team review/deployment

Output: Organized ad library + tracking sheet + automated variations
```

### The Value Proposition

**Manual Process** (Traditional PPC agency):
```
1. Browse competitor ad libraries (30-60 min)
2. Screenshot promising ads (10 min)
3. Brief designer on variations (15 min)
4. Designer creates 3 variants (2-4 hours)
5. Review/revisions (30 min)
6. Total: 4-6 hours per ad set

Cost: $50-150/hour designer × 4-6 hours = $200-900 per ad set
```

**Automated Process** (This system):
```
1. Run workflow (5 min setup)
2. System processes 20 ads → 60 variants (30 min automated)
3. Review results, select winners (15 min)
Total: 20 minutes active time

Cost: API fees ~$2-5 for 60 variations
```

**ROI**: 90-95% time reduction, 98% cost reduction

---

## 2. Prerequisites & Setup

### Required Accounts

**Apify** (Ad scraping):
- Purpose: Access to ad library scrapers
- Pricing: Pay-per-scrape (~$0.01-0.05 per ad)
- Setup: Create account, get API token

**OpenAI** (Image analysis + generation):
- Purpose: GPT-4 Vision for analysis, GPT Image-1 for generation
- Pricing:
  - Vision: ~$0.01 per image analyzed
  - Image generation: ~$0.02-0.04 per generated image
- Setup: API key with sufficient credits

**Google Cloud** (Drive + Sheets):
- Purpose: File storage and tracking
- Pricing: Free (within generous limits)
- Setup: OAuth credentials (covered in section 3)

**N8N** (Automation platform):
- Purpose: Workflow orchestration
- Options: Self-hosted (free) or N8N Cloud ($20/month)
- Setup: Instance running, credentials configured

### Total Setup Cost
- One-time: $0 (all services have free tiers for testing)
- Per-run: $2-10 depending on volume (20-100 ads)

---

## 3. Building The System (Live Build Process)

### Phase 1: Ad Library Scraper Setup

**Step 1: Research Available Scrapers**

Navigate to Apify marketplace:
```
1. Go to apify.com
2. Search: "ads" or "Facebook Ad Scraper"
3. Options found:
   - Facebook Ad Library Scraper (Curious Coder) ✓ CHOSEN
   - Google Ad Scraper
   - LinkedIn Ad Scraper
   - Twitter Ad Scraper
```

**Why Facebook Ad Library Scraper**:
- Previously tested, reliable
- Includes ad metadata
- Supports filtering by keyword
- Returns structured JSON

**Step 2: Test Scraper on Apify**

Before building N8N workflow, validate on Apify:
```
1. Open scraper page
2. Input: Facebook Ad Library search URL
   Example: https://www.facebook.com/ads/library/?q=agency
3. Settings:
   - Scrape ad details: ON
   - Max records: 20 (testing)
4. Run scraper
5. Verify output contains:
   - original_image_url
   - ad_archive_id
   - page_name
   - body (ad copy)
   - start_date
```

**Step 3: Get Apify API Token**

```
1. Apify dashboard → Settings
2. API tokens → Create new token
3. Name: "PPC Thievery" (or any name)
4. Copy token (save securely)
```

**Step 4: Build N8N HTTP Request**

N8N doesn't have native Apify node, so use HTTP request:

```
Node: HTTP Request
Method: POST
URL: https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items

Authentication:
- Type: Header Auth
- Name: Authorization
- Value: Bearer {YOUR_API_TOKEN}

Body (JSON):
{
  "urls": ["https://www.facebook.com/ads/library/?q=agency"],
  "scrapeAdDetails": true,
  "maxRecords": 20
}
```

**Finding the Actor ID**:
```
Method 1: URL inspection
- In Apify, open scraper page
- URL: https://apify.com/curious_coder/facebook-ad-library-scraper
- Actor ID is between "apify.com/" and "/"
- Example: curious_coder~facebook-ad-library-scraper

Method 2: Copy from API docs
- Scraper page → API tab
- Copy actor ID directly
```

**Step 5: Test & Validate**

Execute N8N node:
```
Expected output: JSON array with 20 items
Each item contains:
- ad_archive_id
- page_id
- page_name
- images: { original_image_url }
- body (ad text)
- start_date
```

**Debugging Common Issues**:

Issue: "Authentication failed"
```
Fix: Check Authorization header format
Should be: Bearer YOUR_TOKEN (with space after "Bearer")
```

Issue: "Actor not found"
```
Fix: Verify actor ID format
Correct: curious_coder~facebook-ad-library-scraper
Incorrect: curious_coder/facebook-ad-library-scraper
```

Issue: "URLs" undefined
```
Fix: Check JSON body formatting
Ensure URLs is array: ["url"] not "url"
```

### Phase 2: Filtering Static Image Ads

**The Problem**: Ad libraries contain videos, carousels, text-only ads.

**The Solution**: Filter for ads with `original_image_url`.

**N8N Node**: Filter

```
Configuration:
- Conditions: Keep if...
- Field: {{ $json.images.original_image_url }}
- Operation: Is Not Empty

Result: Removes 7-10 items typically (video/carousel ads)
From 20 scraped → 10-13 static image ads
```

**Why Filter Early**:
- Saves processing time
- Avoids API calls for unusable ads
- Cleaner downstream logic

**Optional: Add Limit Node**

For testing, add Limit node after Filter:
```
Node: Limit
Max items: 2

Reasoning: Test with 2 ads first
- Validates full flow
- Avoids wasting API credits
- Faster iteration during build
```

**Pro Tip**: Always test with small batches (2-5 items) when building. Scale up after validation.

### Phase 3: Google Drive Folder Structure

**The Folder Hierarchy**:

```
PPC Thievery (Parent - created once)
├── ad_archive_217728 (Per-ad folder)
│   ├── 1_source_assets (Original ad)
│   └── 2_spun_assets (Generated variations)
├── ad_archive_217729
│   ├── 1_source_assets
│   └── 2_spun_assets
└── [More ad folders...]
```

**Why This Structure**:
- **Parent folder**: Keeps all campaigns organized
- **Ad-specific subfolders**: Isolates each ad's assets
- **Numbered prefixes** (1_, 2_): Ensures consistent sorting
- **Source/spun separation**: Easy visual comparison

**Building the Structure**:

**Step 1: One-Time Parent Folder Creation**

```
Node: Google Drive - Create Folder
Folder name: "PPC Thievery"
Parent folder: Root (or specify)

Output: folder_id (save to variable)
```

**Step 2: Store Parent Folder ID**

```
Node: Set (Edit Fields)
Field name: google_drive_folder_id
Value: {{ $json.id }} (from previous node)

Purpose: Reference this ID throughout workflow
```

**Step 3: Per-Ad Folder Creation**

```
Node: Google Drive - Create Folder
Folder name: {{ $json.ad_archive_id }}
Parent folder ID: {{ $('Set_Variables').item.json.google_drive_folder_id }}

Runs: Once per filtered ad
Creates: One folder per ad (e.g., "ad_archive_217728")
```

**Step 4: Source Assets Subfolder**

```
Node: Google Drive - Create Folder
Folder name: "1_source_assets"
Parent folder ID: {{ $json.id }} (from step 3)

Purpose: Stores original downloaded ad
```

**Step 5: Spun Assets Subfolder**

```
Node: Google Drive - Create Folder
Folder name: "2_spun_assets"
Parent folder ID: {{ $('Create_Asset_Parent_Folder').item.json.id }}

Purpose: Stores AI-generated variations
```

**Complete Node Sequence**:
```
HTTP Request (scrape)
→ Filter (static ads only)
→ Limit (testing only)
→ Create Parent Folder (once)
→ Set Variables (store parent ID)
→ Create Per-Ad Folder
→ Create Source Subfolder
→ Create Spun Subfolder
```

### Phase 4: Image Download & Upload

**The Challenge**: Images are hosted on Facebook CDN. We need to:
1. Download them
2. Upload to our Google Drive
3. Make them accessible to OpenAI

**Step 1: Download Source Image**

```
Node: HTTP Request
URL: {{ $json.images.original_image_url }}
Response format: File (binary)

Output: Binary image data
```

**Why This Works**:
- `original_image_url` from scraper is public CDN link
- HTTP GET downloads file directly
- N8N stores as binary data automatically

**Step 2: Upload to Google Drive**

```
Node: Google Drive - Upload File
File: {{ $binary.data }} (from download node)
File name: {{ $binary.data.fileName }}
Folder ID: {{ $('Create_Source_Subfolder').item.json.id }}

Result: Uploaded to "1_source_assets" folder
```

**Binary Data Note**:
When working with files in N8N, data flows as "binary" type. Nodes expecting files automatically read from `$binary.data`.

**Step 3: Share File (Critical for OpenAI)**

```
Node: Google Drive - Share
File ID: {{ $json.id }} (from upload)
Role: Reader
Type: Anyone with link

Why: OpenAI Vision needs public URL to analyze
```

**Step 4: Generate Direct Download Link**

**The Problem**: Google Drive share links look like:
```
https://drive.google.com/file/d/FILE_ID/view
```

But OpenAI needs direct image URLs. We must reconstruct:
```
https://drive.google.com/uc?export=download&id=FILE_ID
```

**N8N Implementation**:

```
Node: Set (Edit Fields)
Field: direct_image_url
Value: https://drive.google.com/uc?export=download&id={{ $json.id }}

This creates a URL OpenAI can directly access
```

**Complete Image Flow**:
```
Download (HTTP)
→ Upload to Drive
→ Share File
→ Generate Direct URL
```

### Phase 5: AI Image Analysis

**Goal**: Generate comprehensive description for spinning.

**Node**: OpenAI - Chat with Vision

```
Configuration:
Model: gpt-4-vision-preview (or gpt-4o)
Max tokens: 1000

Prompt:
"What's in this image? Describe it extremely comprehensively.
Leave nothing out."

Image URL: {{ $json.direct_image_url }}
```

**Example Output**:
```
"The image depicts a scenic and serene outdoor setting featuring
a burnt orange or copper colored SUV parked near what appears to
be a mountainous overlook. The vehicle is positioned against a
backdrop of dramatic rocky cliffs and a cloudy sky suggesting
either early morning or late afternoon lighting. The composition
emphasizes adventure and exploration with the SUV as the central
subject positioned in the lower third of the frame..."
```

**Why Comprehensive Descriptions**:
- More detail = better spinning options
- Captures layout, colors, text placement
- Identifies elements to preserve vs modify

**Performance Note**: This step is fast (~2-3 seconds per image).

### Phase 6: Prompt Spinning (The Secret Sauce)

**The Concept**: Don't just copy the ad. Create "change request" prompts that transform it while maintaining effectiveness.

**The System Prompt**:

```
You're a helpful intelligent prompt assistant. You help rewrite prompts.

I've generated an image description. I want you to take that image
description and give me a simple change request prompt I could use
to tell an image editor what changes to make.

Generate exactly 3 change requests, no more, no less.

Output as JSON:
{
  "variants": [
    "Change request 1...",
    "Change request 2...",
    "Change request 3..."
  ]
}
```

**Example Training Data** (include in prompt):

```
User: "The image features a promotional graphic with a bright blue background."

Assistant Output (variants):
[
  "Make the background bright orange instead of blue",
  "Change design to minimalist black and white",
  "Transform into ultra-maximalist style with patterns"
]
```

**The Change Request Template**:

This is what gets injected into variants (set via Set Variables node):

```
Spin this ad so that it features bright blue stylized ultra-maximalism
design. If there is any text on the page, replace it with something like
"Get your AI automation today" or "Get your systems optimized today".
If there are any assets on the page, leave them as is. Add a logo and
company name "LeftClick" in the bottom right hand corner along with a
little stylized mouse pointer icon.

Also, adjust the copy so that it's relevant to an audience that wants
AI automation. Make sure your generated copy is similar in length to
the copy of the original.
```

**User-Customizable**: You edit this template in Set Variables node to match your brand/style.

**The Spinning Node** (OpenAI):

```
Node: OpenAI - Chat
Model: gpt-4 or gpt-4-turbo
Temperature: 0.7 (allows creativity)

System Prompt: [See above - the full prompt assistant instructions]

User Input:
- Original description from Vision analysis
- Change request template from variables

Output: JSON with 3 variants
```

**Step 7: Split Out Variants**

```
Node: Split Out (Item Lists)
Field to split: variants

Input: 1 item with 3 variants array
Output: 3 separate items (one per variant)

Why: Allows looping through each variant for image generation
```

### Phase 7: Looping Over Variants

**The Problem**: We have 3 variants per ad. Need to generate an image for each.

**The Solution**: Loop Over Items node with batch processing.

**N8N Setup**:

```
Node: Loop Over Items
Batch size: 1

Connects to:
├── Download Static Image (re-download for each variant)
├── Generate Image (GPT Image-1 edit)
├── Wait (1 second - rate limit protection)
└── Loop back to start
```

**Why Re-Download Image**:
Each variant needs the original image as input to GPT Image-1 edit endpoint. Since we're in a loop context, we need the image binary data available. Solution: Add image URL to each variant item, re-download in loop.

**Adding Image URL to Variants**:

```
Node: Edit Fields (before splitting variants)
Field: image_ad_url
Value: {{ $('Download_Static_Image_Ad').item.json.images.original_image_url }}

Result: Each variant now has original image URL attached
```

**Inside the Loop**:

```
1. HTTP Request: Download image from image_ad_url
2. Generate Image: Send to GPT Image-1 with variant prompt
3. Wait: 1 second delay
4. Loop continues to next variant
```

### Phase 8: GPT Image-1 Edit Endpoint

**The Challenge**: N8N has no built-in node for GPT image editing. Must use HTTP request.

**API Endpoint**:
```
POST https://api.openai.com/v1/images/edits
```

**Authentication**:

```
N8N Trick: Use Predefined Credential Type
Instead of: Manual header auth
Use: OpenAI credential (created for other nodes)

Setup:
1. Authentication: Predefined Credential Type
2. Credential Type: OpenAI API
3. Select: (Your existing OpenAI credential)

N8N automatically adds: Authorization: Bearer {token}
```

**Request Body** (Form Data - Critical):

```
Content-Type: multipart/form-data

Fields:
1. model: "gpt-image-1" (text field)
2. image: binary file (from download node)
3. prompt: {{ $json.variant }} (from loop)
4. size: "1024x1024" (text field)
```

**How to Set Binary File in N8N**:

```
Body Content Type: Form-Data (Multipart)

Add Parameter:
- Name: image
- Type: n:binaryFile
- Input Data Field Name: data
- File Name: image

N8N automatically attaches binary from previous node
```

**The Prompt Field**:

```
Parameter: prompt
Value: {{ $json.variant }}

This injects the change request like:
"Make background bright orange instead of blue..."
```

**Full HTTP Request Configuration**:

```
Method: POST
URL: https://api.openai.com/v1/images/edits
Auth: Predefined (OpenAI API)

Body Parameters:
├── model: gpt-image-1
├── image: [binary file]
├── prompt: {{ $json.variant }}
└── size: 1024x1024

Response Format: JSON
```

**Expected Response**:

```json
{
  "data": [
    {
      "b64_json": "iVBORw0KGgo..."
    }
  ]
}
```

**Problem**: Response is base64, not viewable image.

**Solution**: Convert base64 to file.

### Phase 9: Base64 to File Conversion

```
Node: Convert to File
Input: {{ $json.data[0].b64_json }}
Output format: Auto (detects PNG/JPEG)
File name: generated_{{ $now }}.png

Result: Binary image file ready for upload
```

### Phase 10: Upload Spun Images

```
Node: Google Drive - Upload
File: {{ $binary.data }}
File name: {{ $binary.data.fileName }}
Folder ID: {{ $('Create_Spun_Subfolder').item.json.id }}

Uploads to: "2_spun_assets" folder for each ad
```

### Phase 11: Google Sheets Tracking

**Why Track**: Need centralized view of all ads + spun variants for team review.

**Sheet Structure**:

| Column | Purpose | Source |
|--------|---------|--------|
| timestamp | Unique ID | {{ $now.toUnixInteger() }} |
| ad_archive_id | Ad identifier | From scraper |
| page_id | Advertiser ID | From scraper |
| original_image_url | Source ad link | From scraper |
| page_name | Advertiser name | From scraper |
| ad_body | Ad copy text | From scraper |
| date_scraped | When scraped | From scraper (start_date) |
| spun_prompt | Variant used | From loop (variant) |
| asset_folder | Parent folder link | Drive link |
| source_folder | Original ad folder | Drive link |
| spun_folder | Variants folder | Drive link |
| direct_spun_image_link | Quick access | Drive direct link |

**Initialization** (Run once):

```
Node 1: Google Sheets - Create Spreadsheet
Name: "PPC Thievery"
Location: Inside parent Google Drive folder

Node 2: Google Sheets - Create Sheet
Spreadsheet ID: {{ $json.spreadsheetId }}
Sheet name: "Scraped Ads"

Node 3: Edit Fields - Add Headers
Creates fields matching column names above

Node 4: Google Sheets - Append Row
Appends header row to sheet
```

**Ongoing Logging** (Per variant):

```
Node: Google Sheets - Append Row
Spreadsheet: By ID (from initialization)
Sheet: "Scraped Ads"
Mapping: Manual

Fields mapped:
- timestamp: {{ $now.toUnixInteger() }}
- ad_archive_id: {{ $('Run_Ad_Library_Scraper').item.json.ad_archive_id }}
- page_id: {{ $('Run_Ad_Library_Scraper').item.json.page_id }}
- [etc. for all columns]
```

**Google Drive Link Construction**:

```
Asset folder: https://drive.google.com/drive/folders/{{ $('Create_Asset_Parent_Folder').item.json.id }}
Source folder: https://drive.google.com/drive/folders/{{ $('Create_Source_Subfolder').item.json.id }}
Spun folder: https://drive.google.com/drive/folders/{{ $('Create_Spun_Subfolder').item.json.id }}
```

**Why Clickable Links**: Team can instantly navigate to assets from spreadsheet.

---

## 4. The Complete N8N Canvas

### Node-by-Node Flow

```
[Manual Trigger]
    ↓
[Set Variables] ← User configures folder ID, change request
    ↓
[HTTP Request: Apify Scraper] ← 20 ads from Facebook
    ↓
[Filter: Static Ads Only] ← Removes videos
    ↓
[Limit: 2 Items] ← Testing only (remove for production)
    ↓
[Google Drive: Create Parent Folder] ← "PPC Thievery"
    ↓
[Google Sheets: Create Spreadsheet] ← Tracking database
    ↓
[Google Sheets: Create Sheet] ← "Scraped Ads" tab
    ↓
[Edit Fields: Add Headers] ← Column names
    ↓
[Google Sheets: Append Headers] ← First row
    ↓
[Google Drive: Create Ad Folder] ← Per ad (loops automatically)
    ↓
[Google Drive: Create Source Folder] ← "1_source_assets"
    ↓
[Google Drive: Create Spun Folder] ← "2_spun_assets"
    ↓
[HTTP Request: Download Image] ← From Facebook CDN
    ↓
[Google Drive: Upload to Source] ← Save original
    ↓
[Google Drive: Share File] ← Make public
    ↓
[OpenAI Vision: Analyze Image] ← Comprehensive description
    ↓
[OpenAI Chat: Generate Variants] ← 3 change requests
    ↓
[Split Out: Variants Array] ← 1 item → 3 items
    ↓
[Edit Fields: Add Image URL] ← Attach original URL
    ↓
[Loop Over Items] ← Batch size 1
    ├→ [HTTP Request: Re-download Image]
    ├→ [HTTP Request: GPT Image-1 Edit]
    ├→ [Convert to File: Base64 → PNG]
    ├→ [Google Drive: Upload Spun Image]
    ├→ [Google Sheets: Append Row] ← Log this variant
    ├→ [Wait: 1 Second]
    └→ [Loop Back]
```

### Visual Complexity Note

**From the video**: "This is getting pretty sexy in so far that it's getting kind of complex. And I mean that not in a good way. The sexier your flow gets, like the more complex that it gets, typically the less valuable it actually is. The simpler a flow is, the more maintainable it is."

**Simplification Opportunities**:
- Could remove Edit Fields nodes by hardcoding some values
- Could skip re-downloading images (more complex data passing)
- Could remove limit node in production
- Could batch Google Sheets updates (append once at end)

**Trade-off**: This build prioritizes **learnability** over **simplicity**. Every step is explicit and debuggable.

---

## 5. Advanced Debugging Techniques

### Issue 1: Item Matching Hell

**The Problem**: N8N processes items in batches. Sometimes nodes expect 1 item but receive 20.

**The Symptom**:
```
Error: "Cannot read property 'id' of undefined"
Cause: Node expects $json.id but receives array of items
```

**The Fix**: Use Item Linking

```
Bad:
{{ $json.id }} ← Fails with multiple items

Good:
{{ $('Specific_Node_Name').item.json.id }} ← Specifies exact source

Best:
{{ $('Run_Ad_Library_Scraper').item.json.ad_archive_id }}
    ↑ Node name              ↑ Field path
```

**Pro Tip**: Always reference upstream nodes by name, never rely on implicit $json when multiple items flow through.

### Issue 2: Binary Data Pinning

**The Problem**: Can't pin binary data for testing.

**The Symptom**:
```
Error: "Input data field 'data' doesn't exist"
Cause: Tried to pin a node with binary, then execute downstream
```

**The Fix**: Don't pin binary nodes during testing.

```
Workflow:
Download Image → Upload to Drive
       ↑              ↑
    (Binary)      (Needs binary)

Testing approach:
1. Execute Download Image (don't pin)
2. Immediately execute Upload to Drive
3. Both run together, binary flows correctly

Don't:
1. Execute Download Image
2. Pin output
3. Execute Upload to Drive ← FAILS
```

### Issue 3: Google Drive Folder IDs

**The Problem**: Creating nested folders requires parent IDs, but which node has the ID?

**The Solution**: Use Set Variables as central state.

```
Pattern:
[Create Folder A]
    ↓ (ID: abc123)
[Set Variables] ← Store: parent_folder_id = abc123
    ↓
[Create Folder B]
    Parent ID: {{ $('Set_Variables').item.json.parent_folder_id }}
```

**Why This Works**: Set Variables outputs never change. Safe to reference from anywhere.

### Issue 4: OpenAI Rate Limits

**The Symptom**:
```
Error: "Rate limit exceeded"
Cause: Generating 60 images too fast
```

**The Fix**: Add Wait nodes.

```
Inside loop:
Generate Image
    ↓
[Wait: 1 second] ← Slows requests to 60/min (under 100/min limit)
    ↓
Loop continues
```

**Advanced**: Exponential backoff on errors.

```
If error code 429:
- Wait 2 seconds
- Retry
- If fails again: Wait 4 seconds
- Max retries: 3
```

(N8N supports this via Error Workflow + Set + If nodes)

### Issue 5: JSON Output Viewing

**The Trick**: Always view JSON output, not Table/Schema.

```
Table view: Hides nested arrays
Schema view: Hides multiple items
JSON view: Shows EVERYTHING

To switch:
Output panel → Dropdown → "JSON"
```

**Why**: You need to see ALL items (e.g., 20 ads) to understand data flow.

---

## 6. Scaling & Optimization

### Production Configuration

**Change these values for real campaigns**:

```
1. Remove Limit node (or set to 100+)
2. Increase Apify scraper max records: 100-500
3. Adjust batch size in Loop: 3-5 (generate multiple images simultaneously)
4. Add error handling: Error Workflow that retries failed items
5. Enable workflow logs: Settings → Save Execution Data → Success & Error
```

### Cost at Scale

**Example**: Process 100 ads, 3 variants each = 300 generated images

```
Apify scraping: 100 ads × $0.02 = $2.00
OpenAI Vision (analysis): 100 × $0.01 = $1.00
GPT Image-1 (generation): 300 × $0.04 = $12.00
Google Drive: Free (well under limits)
Google Sheets: Free

Total: ~$15 for 300 ad variants
```

**Traditional cost**: $50-150/designer × 100 ads = $5,000-15,000

**ROI**: 333× - 1000× cost reduction

### Performance Optimization

**Bottlenecks**:
1. Image generation (slowest): 10-20 sec per image
2. Image download: 1-2 sec per image
3. Google Drive uploads: 1-2 sec per file
4. Everything else: <1 sec

**Optimization 1: Parallel Loops**

```
Current: 1 variant at a time
Optimized: 3 variants in parallel

Method:
Replace Loop Over Items with Split In Batches (size: 3)
Add 3 parallel paths (one per variant)
All generate simultaneously

Result: 3× faster (30 images in 10 min vs 30 min)
```

**Optimization 2: Batch Google Sheets**

```
Current: Append row per variant (300 API calls)
Optimized: Aggregate data, append once (1 API call)

Method:
After loop completes, use Aggregate node
Build array of all rows
Append to Google Sheets in bulk

Result: Faster, fewer API calls
```

**Optimization 3: Cached Image Downloads**

```
Current: Re-download image for each variant
Optimized: Download once, pass binary through loop

Method:
Use Function node to attach binary to all variant items
Loop accesses binary from item data

Result: 2-3× faster image processing
```

### Monitoring & Alerts

**Set up Slack/Email notifications**:

```
Node: Slack (or Email)
Trigger: On workflow completion

Message:
"PPC Thievery complete!
- Ads processed: {{ $('Filter').item.json.count }}
- Variants generated: {{ $('Loop_Over_Items').item.json.count }}
- Spreadsheet: [link]
- Drive folder: [link]"
```

**Error alerts**:

```
Error Workflow:
If: Generation fails
Then: Send alert with error details
Retry: 3 times before alerting
```

---

## 7. Real-World Application

### Use Case 1: Agency Client Deliverables

**Scenario**: Client needs 50 ad variations for Meta campaign.

**Process**:
1. Run workflow with client's competitor search terms
2. System generates 150 variants (50 ads × 3 each)
3. Review spreadsheet, flag top 50
4. Send Google Drive folder to client
5. Client selects finals for deployment

**Time**: 2 hours (mostly automated processing)

### Use Case 2: Internal Creative Testing

**Scenario**: Your agency needs fresh creative ideas.

**Process**:
1. Weekly workflow run: Scrape your niche
2. Generate variants with your brand style (modify change request)
3. A/B test top variants
4. Iterate based on performance

**Time**: 30 min/week

### Use Case 3: White-Label Service

**Scenario**: Sell "AI-powered creative generation" as service.

**Process**:
1. Client provides: Search terms, brand guidelines
2. Customize change request template with their brand
3. Run workflow
4. Deliver: Spreadsheet + organized Drive folder
5. Charge: $500-2000 per batch (100 variants)

**Profit**: $485-1985 per batch (cost: $15)

---

## 8. Ethical & Legal Considerations

### Copyright & Ad Inspiration

**Important**: This system scrapes competitor ads for **inspiration**, not **copying**.

**Legal gray areas**:
- Ad libraries are public (Meta requirement)
- Using as reference/inspiration: Generally okay
- Direct copying: Copyright infringement
- AI-generated variations: New derivative works

**Best practices**:
1. Always modify significantly (style, colors, layout)
2. Never copy brand names/logos exactly
3. Use as starting point, not final deliverable
4. Have designer review/refine AI outputs

**Disclaimer**: Consult legal counsel for your jurisdiction.

### Platform Terms of Service

**Meta Ad Library**: Public data, scraping allowed (via official API).

**Apify**: Legal scraping service, handles TOS compliance.

**OpenAI**: Generated images are yours to use commercially (per OpenAI TOS as of Jan 2025).

**Google Drive**: No issues for business use.

---

## 9. Troubleshooting Guide

### Error: "No image URL found"

**Cause**: Ad is video/carousel, not static image.

**Fix**: Filter node should catch this. If not:
```
Filter condition:
{{ $json.images }} AND {{ $json.images.original_image_url }}
```

### Error: "OpenAI cannot access image"

**Cause**: Google Drive file not shared publicly.

**Fix**: Verify share step:
```
Google Drive - Share
Role: Reader
Type: Anyone with link
```

Also verify direct URL construction:
```
https://drive.google.com/uc?export=download&id=FILE_ID
```

### Error: "Invalid JSON response"

**Cause**: OpenAI returned non-JSON (happened with vision model).

**Fix**: Add JSON validation:
```
Function node after OpenAI:
try {
  return JSON.parse($input.item.json.message.content);
} catch (e) {
  return { variants: [] }; // Fallback
}
```

### Error: "Loop never completes"

**Cause**: Loop Over Items not connected back correctly.

**Fix**: Ensure loop output connects to loop input node (forms circuit).

### Error: "Google Sheets not finding columns"

**Cause**: No header row, or trying to map before sheet exists.

**Fix**: Initialize spreadsheet with headers first (section 11).

---

## 10. Extensions & Variations

### Extension 1: Video Ad Scraping

**Current**: Filters out videos.
**Extension**: Process videos with AI.

```
Add after filter:
If video: Extract thumbnail as static image
Process thumbnail as regular ad
Note in spreadsheet: "Video thumbnail"
```

### Extension 2: Multi-Platform Scraping

**Current**: Facebook/Instagram only.
**Extension**: Add LinkedIn, Twitter, Google scrapers.

```
Add parallel paths:
├─ Facebook scraper
├─ LinkedIn scraper
├─ Twitter scraper
└─ Merge results → Process identically
```

### Extension 3: Automated A/B Testing

**Current**: Manual review of variants.
**Extension**: Auto-deploy top variants to Meta.

```
Add at end:
1. Upload variants to Meta Business Suite (via API)
2. Create A/B test campaigns
3. Monitor performance (24-48 hours)
4. Report winners back to sheet
```

### Extension 4: Brand Safety Checks

**Current**: No filtering for inappropriate content.
**Extension**: Add content moderation.

```
After vision analysis:
1. Send description to moderation API
2. Check for:
   - Inappropriate imagery
   - Competitor brands
   - Off-brand messaging
3. Flag or auto-reject problematic ads
```

### Extension 5: Style Transfer

**Current**: Text-based prompt spinning.
**Extension**: Image-to-image style transfer.

```
Instead of GPT Image-1 edit:
Use: Stable Diffusion img2img
Benefit: More dramatic style changes
Process:
  - Same ad layout
  - Applied artistic styles (oil painting, sketch, etc.)
```

---

## AI PARSING GUIDE

### Primary Objective
When building ad creative automation, use N8N for visual workflow construction combined with external APIs (Apify, OpenAI) for specialized tasks that don't have native integrations.

### Critical Decision Points

**If User Says**: "I want to automate ad creative generation"
**Action Sequence**:
1. Determine ad platform (Facebook, LinkedIn, etc.)
2. Find scraper on Apify marketplace
3. Build N8N flow: Scrape → Analyze → Generate → Organize
4. Test with 2-5 ads before scaling

**If User Says**: "The images look weird/distorted"
**Diagnose**:
1. Check source image quality (low-res originals?)
2. Review change request prompts (too dramatic?)
3. Adjust GPT Image-1 parameters
4. Generate more variants (3 → 10) for better selection

**If User Says**: "This is too expensive"
**Optimize**:
1. Reduce variants per ad (3 → 1-2)
2. Use smaller image sizes (1024 → 512)
3. Batch process (100 ads once/week vs daily)
4. Pre-filter ads manually (only scrape top performers)

### Integration Points

**Connects to**:
- Ad Library Research (outlier detection)
- Creative Strategy (brand guidelines)
- Campaign Management (deployment pipelines)
- Performance Tracking (A/B test results)
- Design Systems (brand consistency)

### Output Quality Standards

When helping build ad creative automation:
1. ✅ Source ads filtered (static images only)
2. ✅ Folder structure organized (source/spun separation)
3. ✅ Tracking spreadsheet with all metadata
4. ✅ Change requests customized to brand
5. ✅ Rate limiting implemented (no API overages)
6. ✅ Error handling for failed generations

### Red Flags (Anti-Patterns)

❌ No filtering (processing videos wastes money)
❌ Hardcoded folder IDs (breaks when re-running)
❌ No rate limiting (hits OpenAI limits, workflow fails)
❌ Missing header row in Google Sheets (mapping breaks)
❌ Pinning binary data nodes (testing impossible)
❌ Generic change requests (outputs look identical)

---

## SOURCE ATTRIBUTION

**Primary Source**: Nick Saraev - "can't believe i built a $70k ai creative team in 66mins using only N8N"
- **Video ID**: GNmlnt52aSM
- **Duration**: 1 hour 6 minutes
- **Context**: Complete live build of production ad creative system with all debugging and iteration
- **Key Contribution**: Demonstrates real-world N8N workflow construction including all mistakes, fixes, and problem-solving
- **Authority Basis**: Built two AI agencies to $160K/month, formerly owned PPC agency
- **Technical Detail Level**: Every node configuration, API endpoint, data transformation, and debugging step shown
- **Unique Value**: Unedited live build showing how to actually construct complex automations (not just polished demos)
- **Teaching Philosophy**: "Keep in any detours I encounter along the way—this is the most instructive way of showing people how to build systems"
- **Capture Date**: January 2026 (via MCP YouTube Transcript)

**Synthesis Approach**: This skill bible extracts the complete $70K ad creative automation system from an unedited 66-minute live build. Every component is documented: from initial API research through final Google Sheets integration, including all debugging, iteration, and optimization decisions made during construction.

---

**END SKILL BIBLE: N8N Ad Creative Automation System ($70K Value)**