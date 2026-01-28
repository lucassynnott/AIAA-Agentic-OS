# SKILL BIBLE: YouTube Channel Automation (3 Complete Workflows)

## Executive Summary

YouTube content creation can be automated end-to-end using three interconnected agentic workflows: an AI video editor that removes silences and enhances quality, a cross-niche outlier detector that identifies high-performing content ideas, and an AI thumbnail generator that face-swaps proven thumbnails. These workflows reduce video production from hours to minutes while maintaining professional quality.

**Core Insight**: "Whatever your day-to-day is, you can probably automate 90% of it. AI is not capable of automating 100% of one person's job, but it is capable of automating 90% of 100,000 people's jobs."

This skill bible documents three production-ready workflows built using the Directive-Orchestration-Execution (DO) framework with Claude Code, requiring zero programming knowledge.

---

## 1. The Workflow Ecosystem (How All Three Connect)

### The Complete YouTube Production Loop

```
Phase 1: Content Ideation
└── Cross-Niche Outlier Detector
    ├── Identifies high-performing videos in related niches
    ├── Analyzes transcripts for content themes
    └── Generates title variants → OUTPUT: Google Sheet with ideas

Phase 2: Content Creation
└── Record raw footage (manual step)
    └── Use any recording software (OBS, etc.)

Phase 3: Post-Production
└── AI Video Editor
    ├── Removes silence gaps automatically
    ├── Detects and cuts mistakes
    ├── Enhances audio quality
    ├── Applies color grading
    └── Adds intro animation → OUTPUT: Final edited video

Phase 4: Publishing
└── AI Thumbnail Generator
    ├── Analyzes outlier thumbnails
    ├── Face-swaps with pose matching
    ├── Generates 3 variants per concept
    └── Iterative text/background edits → OUTPUT: Final thumbnail

Phase 5: Upload
└── Automated upload to YouTube (workflow extends to this)
```

**Key Integration Point**: The outlier detector feeds directly into thumbnail generator. High-performing thumbnails from step 1 become templates for step 4.

---

## 2. Workflow #1: AI Video Editor (Silence Removal + Enhancement)

### What It Does

Automatically edits talking-head videos by:
- Extracting audio from recorded video
- Running neural voice activity detection (Silero VAD)
- Removing silence gaps between speech (0.5-second threshold)
- Detecting verbal mistakes via trigger words
- Enhancing audio quality
- Applying color grading
- Adding intro animations (swivel effect)
- Using hardware acceleration for fast processing

**Processing Speed**: Faster than Premiere Pro due to hardware acceleration.

### Technical Architecture

```
Input: Raw video file (e.g., 1_cut_851.mp4)
       ↓
Step 1: Audio Extraction
       ↓
Step 2: Silero VAD Analysis (voice activity detection)
       ├── Identifies speech segments
       └── Flags silence gaps > 0.5 seconds
       ↓
Step 3: Silence Removal
       ├── Cuts non-speech segments
       └── Maintains natural pacing
       ↓
Step 4: Mistake Detection
       ├── Listens for trigger words (user-defined)
       └── Cuts from trigger point back to previous segment
       ↓
Step 5: Audio Enhancement
       ├── Noise reduction
       ├── Normalization
       └── Compression
       ↓
Step 6: Color Grading
       └── Applies preset color corrections
       ↓
Step 7: Intro Addition
       └── Adds swivel teaser animation
       ↓
Step 8: Hardware Acceleration Render
       └── Exports final video
       ↓
Output: Edited video ready for upload
```

### The Silero VAD Component

**What is Silero VAD?**
- Neural network-based voice activity detection
- Distinguishes speech from silence/noise
- More accurate than amplitude-based detection
- Handles varying audio levels

**Why VAD Over Simple Silence Detection?**
```
Traditional Approach: ffmpeg -af silencedetect
Problem: Misses low-volume speech, cuts mid-sentence

Silero VAD Approach: Neural voice recognition
Benefit: Understands speech patterns, preserves natural flow
```

**Configuration**:
- Threshold: 0.5 seconds (adjustable)
- Sensitivity: High (catches brief pauses)
- Post-processing: Smooth transitions between cuts

### The Mistake Detection System

**How It Works**:
1. User defines trigger phrases (e.g., "um, let me restart")
2. System monitors audio transcription in real-time
3. When trigger detected:
   - Identify timestamp of trigger
   - Find previous speech segment boundary
   - Cut from current point back to that boundary
4. Resume from corrected position

**Example Flow**:
```
Timeline:
0:00 - 0:45: Clean speech
0:45 - 0:48: "Actually, let me restart that"  ← TRIGGER
                                                  ↓
                                           CUT FROM 0:45
0:48 - 1:30: Re-recording of segment       ← KEEPS THIS
                                                  ↓
Final edit: 0:00-0:45 → 0:48-1:30 (seamless)
```

### Audio Enhancement Pipeline

**Step 1: Noise Reduction**
- Removes background hum/static
- Preserves voice clarity
- Uses spectral subtraction

**Step 2: Normalization**
- Evens out volume levels
- Target: -16 LUFS (YouTube standard)
- Prevents clipping

**Step 3: Compression**
- Reduces dynamic range
- Makes quiet parts audible
- Prevents sudden loud spikes

**Parameters** (auto-configured):
```python
# These are set by the workflow, user doesn't need to know them
noise_reduction: -20dB
normalization_target: -16 LUFS
compression_ratio: 3:1
compression_threshold: -18dB
```

### Building This Workflow (Step-by-Step)

**Phase 1: Initial Setup**
```
Prompt to Claude Code:
"I'd like to build a simple workflow that takes as input a video,
identifies the silence gaps, cuts those silence gaps, finds any
mistakes I make, cuts those too, then builds a little cool intro
animation (video swivel). This is a demo, so ignore any existing
workflows in my directives folder. Build from scratch. Start by
giving me three options we could use, look at pre-existing solutions,
and lay them out. If it makes sense, we can proceed."
```

**Phase 2: Research Phase**
Claude Code will:
1. Search for existing solutions/libraries
2. Present 3 approaches:
   - **Pure Local Stack**: ffmpeg + custom scripts
   - **Hybrid Cloud**: Some API calls for processing
   - **VAD-First Approach**: Silero VAD + moviepy (RECOMMENDED)

**Example Output**:
```
Option 1: Pure Local Stack
- ffmpeg for silence detection
- Python for orchestration
- Pros: Fully local, free
- Cons: Less accurate silence detection

Option 2: Hybrid Cloud
- Use cloud transcription API
- Local video processing
- Pros: Better mistake detection
- Cons: API costs, slower

Option 3: VAD-First Approach (RECOMMENDED)
- Silero VAD for voice detection
- moviepy for video editing
- Hardware acceleration support
- Pros: Best accuracy, fast processing
- Cons: Requires Python dependencies
```

**Phase 3: Selection & Testing**
```
User: "Let's go with Option 3 (VAD-First)"

Claude Code will:
1. Install dependencies (silero-vad, moviepy, etc.)
2. Create directive file: directives/smart_video_edit.md
3. Create execution scripts in execution/ folder
4. Set up configuration files
```

**Phase 4: Testing**
```
Prompt: "Run the video editing workflow on 1_cut_851.mp4"

System will:
1. Check directives/smart_video_edit.md
2. Find execution scripts listed
3. Run scripts in sequence
4. Output edited video
```

### The Directive File Structure

**Location**: `directives/smart_video_edit.md`

**Contents** (auto-generated, but user can edit):
```markdown
# Smart Video Edit Workflow

## Description
Automatically edit talking head videos by removing silences,
detecting mistakes, and enhancing quality.

## Inputs
- video_file: Path to raw video (MP4, MOV, etc.)
- silence_threshold: Seconds of silence to remove (default: 0.5)
- trigger_words: List of mistake indicators (optional)

## Steps
1. Extract audio from video
2. Run Silero VAD analysis
3. Identify silence gaps > threshold
4. Cut silence segments
5. Detect trigger words in transcript
6. Remove mistake segments
7. Apply audio enhancements:
   - Noise reduction
   - Normalization to -16 LUFS
   - Compression (3:1 ratio)
8. Apply color grading preset
9. Add intro animation (swivel effect)
10. Render with hardware acceleration

## Execution Scripts
- execution/extract_audio.py
- execution/silero_vad_analysis.py
- execution/cut_silences.py
- execution/detect_mistakes.py
- execution/enhance_audio.py
- execution/apply_color_grade.py
- execution/add_intro_animation.py
- execution/render_video.py

## Outputs
- Edited video: output/edited_{original_filename}.mp4
- Processing log: output/edit_log_{timestamp}.txt

## Edge Cases
- Very short videos (<30 seconds): Skip silence removal
- No speech detected: Warn user, output original
- Trigger words in legitimate context: Manual review suggested
```

### Execution Scripts (What They Do)

User **never writes these**. Claude Code generates them. But understanding helps:

**execution/silero_vad_analysis.py**:
```
Purpose: Analyzes audio to find speech vs silence
Inputs: Extracted audio file
Process:
  1. Load Silero VAD model
  2. Process audio in chunks
  3. Generate timestamps for speech segments
Output: JSON with speech segment timestamps
```

**execution/cut_silences.py**:
```
Purpose: Removes silence gaps from video
Inputs: Original video + speech timestamps
Process:
  1. Read timestamp JSON
  2. Extract video segments matching speech
  3. Concatenate segments seamlessly
Output: Video with silences removed
```

**execution/enhance_audio.py**:
```
Purpose: Improves audio quality
Inputs: Video with cut silences
Process:
  1. Extract audio track
  2. Apply noise reduction filter
  3. Normalize to -16 LUFS
  4. Apply compression
  5. Re-attach to video
Output: Video with enhanced audio
```

### Real-World Usage

**Command**:
```
"Run the video editing workflow on my_recording.mp4"
```

**What Happens**:
1. Claude Code reads `directives/smart_video_edit.md`
2. Finds listed execution scripts
3. Runs them in sequence
4. Monitors for errors
5. If error occurs: attempts fix, retries
6. Outputs final video to `output/` folder

**Time Comparison**:
- Manual editing in Premiere Pro: 1-2 hours for 10-minute video
- This workflow: 5-10 minutes (mostly processing time)

---

## 3. Workflow #2: Cross-Niche Outlier Detector

### What It Does

Identifies high-performing YouTube videos in related (but not identical) niches to inspire content ideas. Uses "outlier score" to find videos that performed significantly above channel average.

**Outlier Score Formula**:
```
Base Score = Video Views / Channel Average Views

Recency Boost = Multiplier for recent videos (decay function)

Cross-Niche Modifiers:
- +30% if title mentions money
- +20% if title mentions time
- +15% if title mentions specific numbers

Final Score = Base Score × Recency Boost × Modifiers
```

**Example**: Video with 6.81 outlier score performed 681% better than channel average.

### The Complete System Architecture

```
Input: User defines related niches (e.g., "business but not AI")
       ↓
Step 1: API Selection (TubeLab chosen)
       ↓
Step 2: Scrape Videos from Related Channels
       ├── Filters: Published in last month
       ├── Volume: 100 videos per run
       └── Criteria: Related niche, not direct competitor
       ↓
Step 3: Calculate Outlier Scores
       ├── Video views / channel average
       ├── Apply recency boost
       └── Apply cross-niche modifiers
       ↓
Step 4: Fetch Transcripts
       └── Download full transcripts via YouTube API
       ↓
Step 5: AI Summarization
       ├── Summarize video content
       ├── Extract key themes
       └── Identify hook strategies
       ↓
Step 6: Generate Title Variants
       ├── Analyze original title
       ├── Adapt to user's channel style
       └── Create 3 alternative versions
       ↓
Step 7: Output to Google Sheet
       ├── Video link
       ├── Thumbnail
       ├── Original title
       ├── Outlier score
       ├── Summary
       └── 3 title variants
       ↓
Output: Google Sheet with ranked content ideas
```

### Why Outlier Score > Absolute Views

**Problem with absolute views**:
```
Video A: 1M views on 10M subscriber channel = Underperformed
Video B: 100K views on 50K subscriber channel = Massive outlier
```

**Outlier score corrects for channel size**:
```
Video A: 1M / (avg 2M per video) = 0.5 score (poor)
Video B: 100K / (avg 15K per video) = 6.67 score (excellent)
```

**Why this matters**: Small channels can have breakthrough videos. These formulas work regardless of your size.

### The TubeLab API Integration

**Why TubeLab**:
- Outlier calculation built-in
- Affordable pricing ($0.001 per video analyzed)
- Includes transcript access
- Supports cross-niche filtering

**Alternative APIs Considered**:
1. Apify YouTube Scraper (more expensive)
2. Knox Influencer (enterprise pricing)
3. Custom scraping (unreliable, against TOS)

**TubeLab Chosen**: Best balance of features, cost, reliability.

### The Recency Boost Algorithm

**Problem**: Old viral videos aren't relevant to current trends.

**Solution**: Decay function that prioritizes recent content.

```
Recency Multiplier = 1 + (0.5 × e^(-days_old / 30))

Examples:
- 1 day old: 1.49× boost
- 7 days old: 1.39× boost
- 30 days old: 1.18× boost
- 90 days old: 1.03× boost
- 180 days old: 1.0× (no boost)
```

**Why exponential decay**: Reflects how quickly YouTube trends change.

### Cross-Niche Modifier System

**Hook Type Analysis**:

```markdown
Money Hooks (+30%):
- "I made $X"
- "How to earn..."
- "$X per month"
- "Passive income"

Time Hooks (+20%):
- "in 24 hours"
- "in 7 days"
- "30-day challenge"
- "Before 30"

Number Hooks (+15%):
- Specific metrics (e.g., "127 clients")
- Percentages ("300% growth")
- Rankings ("#1 strategy")
```

**Why these modifiers**:
- Money: Universal motivator across niches
- Time: Creates urgency, relatable
- Numbers: Specificity = credibility

**Stacking**: Modifiers multiply, not add.
```
Title: "I made $26,000 in 24 hours"
Base score: 5.2
Money boost: 5.2 × 1.30 = 6.76
Time boost: 6.76 × 1.20 = 8.11
Final score: 8.11 (outlier detector flags this)
```

### Building This Workflow

**Phase 1: API Research**
```
Prompt:
"I'd like to build a workflow that finds outliers on YouTube.
Before we proceed, please look comprehensively across the internet
to see if there are any APIs out there that are easily web accessible
that we could use that have already done this for us. Look for at least three."
```

**Phase 2: API Comparison**
Claude Code will research and present:
```
Option 1: TubeLab API
- Pricing: $0.001/video, ~$1 for 100 videos
- Features: Outlier score built-in, transcript access
- Ease: REST API, good documentation
- Verdict: RECOMMENDED

Option 2: Apify YouTube Scraper
- Pricing: $0.02/video, ~$2 for 100 videos
- Features: Comprehensive data
- Ease: More complex setup
- Verdict: Good alternative

Option 3: Knox Influencer
- Pricing: Enterprise (expensive)
- Features: Advanced analytics
- Ease: Requires account approval
- Verdict: Skip unless at scale
```

**Phase 3: Build Command**
```
Prompt:
"Hi, I'd like to build a workflow that uses TubeLab to scrape
outliers in niches that are similar to mine but not related.
Once done, I'd like you to analyze the transcripts of the videos
and then return a summary, all of the fields from TubeLab, and
then three alternative titles based off of my own YouTube channel
that would apply to the video content that I create."
```

**Phase 4: Configuration Questions**
Claude Code will ask:
1. What's your YouTube channel URL?
2. What are related niches? (e.g., "business but not AI")
3. Where to output? (Google Sheet)
4. How many videos per run? (e.g., 100)
5. Filters? (e.g., "published in last month")

**Phase 5: Execution**
```
Prompt: "Find me 50 outliers and dump to a Google sheet"

System:
1. Calls TubeLab API with filters
2. Calculates enhanced outlier scores
3. Fetches transcripts
4. Summarizes with Claude
5. Generates 3 title variants per video
6. Outputs to Google Sheet with thumbnails
```

### The Output Google Sheet Structure

| Column | Content | Purpose |
|--------|---------|---------|
| **Thumbnail** | Video thumbnail image | Visual reference |
| **Original Title** | Exact title from video | Source material |
| **Channel** | Channel name | Context |
| **Views** | View count | Validation |
| **Outlier Score** | Calculated score (e.g., 6.81) | Ranking metric |
| **Summary** | AI-generated summary | Quick understanding |
| **Theme** | Content category | Grouping |
| **Hook Strategy** | What made it work | Learning |
| **Title Variant 1** | Your-style adaptation | Ready to use |
| **Title Variant 2** | Alternative angle | Options |
| **Title Variant 3** | Different approach | Variety |
| **Video Link** | YouTube URL | Source access |

### Real-World Usage Example

**Input**:
```
Channel: Nick Saraev (AI/Automation)
Related niches: Business, entrepreneurship, productivity (NOT AI)
Filters: Last 30 days, min 50K views
Volume: 100 videos
```

**Sample Output**:
```
Video: "The Spirit of Excellence" - Pastor Matt Hagee
Score: 6.81
Views: 2.1M (channel avg: 308K)
Summary: Motivational talk on maintaining excellence in work
Hook: Authority figure + aspirational concept
Theme: Personal development

Your Title Variants:
1. "The Spirit of Excellence in AI Automation"
2. "Why Excellence Matters More Than Speed (Automation Paradox)"
3. "Building Excellent Systems: What Pastors Teach About Workflows"
```

### Integration with Thumbnail Generator

**Critical Connection**:
```
Outlier Detector Output (Google Sheet)
         ↓
Contains thumbnail URLs
         ↓
Feed directly to Thumbnail Generator
         ↓
"Create thumbnails like [URL] using our workflow"
         ↓
Generates face-swapped versions
```

This creates a closed loop: Research → Ideation → Production.

---

## 4. Workflow #3: AI Thumbnail Generator (Pose-Matched Face Swapping)

### What It Does

Face-swaps existing high-performing YouTube thumbnails to feature you, using advanced pose matching to avoid uncanny valley effects. Generates 3 variations per concept with iterative editing capability.

**Key Innovation**: Pose matching via facial angle analysis.

### The Uncanny Valley Problem (And Solution)

**Why Most AI Thumbnails Fail**:
```
Common Approach:
1. Find thumbnail you like
2. Upload to Midjourney/Stable Diffusion
3. Say "put my face here"
4. Result: Weird, off-angle, uncanny valley

Problem: Face direction mismatch
```

**Example**:
```
Source thumbnail: Subject looking left at 45° angle
Your reference photo: Looking straight at camera
AI must infer: What you look like from that angle
Result: Distorted, unnatural face
```

**The Solution**: Pose matching via MediaPipe.

### The MediaPipe Pose Detection System

**What MediaPipe Does**:
- Analyzes facial landmarks (468 points on face)
- Calculates 3D orientation:
  - **Yaw**: Left-right rotation
  - **Pitch**: Up-down rotation
  - **Roll**: Head tilt

**The Matching Process**:
```
Step 1: Analyze source thumbnail
├── Extract face
├── Run MediaPipe detection
└── Output: Yaw -45°, Pitch 10°, Roll 0°

Step 2: Analyze your reference photos
├── Process all reference images in folder
├── Calculate pose for each
└── Library:
    - photo1.jpg: Yaw 0°, Pitch 0°, Roll 0° (straight on)
    - photo2.jpg: Yaw -40°, Pitch 5°, Roll -2° (slight left)
    - photo3.jpg: Yaw 45°, Pitch -10°, Roll 0° (right angle)
    - etc.

Step 3: Find closest match via Euclidean distance
├── Calculate distance in pose space:
│   distance = √[(yaw_diff)² + (pitch_diff)² + (roll_diff)²]
├── For each reference photo:
│   - photo1: distance = 47.17° (too different)
│   - photo2: distance = 6.40° (CLOSEST MATCH)
│   - photo3: distance = 90.55° (opposite direction)
└── Select: photo2.jpg

Step 4: Use photo2.jpg as reference for face swap
└── AI only needs to swap similar angles = natural result
```

**Why This Works**: AI is much better at face-swapping when angles match. Less inference = less distortion.

### The Face Swap Pipeline (Using Midjourney/Flux Pro)

**Technical Flow**:
```
Inputs:
- Source thumbnail (URL or image)
- Best-match reference photo (from pose analysis)
- Secondary reference photo (for consistency)

Process:
1. Load source thumbnail
2. Detect face region (bounding box)
3. Load reference photos
4. Send to Midjourney/Flux with prompt:
   "Face swap the person in this image with the person
    in these reference photos. Maintain exact pose, lighting,
    and background. Only change the face."
5. Generate 3 variations (slight randomness for options)
6. Post-process:
   - Color matching (match skin tone to reference)
   - Edge blending (smooth transition)
   - Quality enhancement

Output: 3 thumbnail variants
```

**Generation Time**: 20-40 seconds per variant with Flux Pro.

### The Reference Photo Library Strategy

**Setup**:
```
Create folder: reference_photos/
├── straight_on_01.jpg     (Yaw: 0°, Pitch: 0°)
├── straight_on_02.jpg     (Yaw: 0°, Pitch: 5°)
├── left_45_01.jpg         (Yaw: -45°, Pitch: 0°)
├── left_45_02.jpg         (Yaw: -40°, Pitch: -5°)
├── right_45_01.jpg        (Yaw: 45°, Pitch: 0°)
├── right_45_02.jpg        (Yaw: 50°, Pitch: 5°)
├── up_angle_01.jpg        (Yaw: 0°, Pitch: -20°)
├── down_angle_01.jpg      (Yaw: 0°, Pitch: 20°)
└── etc.
```

**Coverage Strategy**:
- 8 cardinal angles (0°, 45°, 90°, etc.)
- 3 pitch variations (up, straight, down)
- 2-3 photos per angle
- Total: ~30 reference photos covers 95% of thumbnails

**One-Time Setup**: Spend 30 minutes taking these photos, use forever.

### Building This Workflow

**Phase 1: Initial Concept**
```
Prompt:
"Hi, I'd like to make a thumbnail generator. I want to use
Midjourney/Flux Pro. Please assist me."
```

**Phase 2: Approach Selection**
Claude Code presents options:
```
Option 1: Simple Face Swap (Standard)
- Take any reference photo
- Swap faces directly
- Fast, easy
- Result: Often uncanny valley

Option 2: Pose-Matched Face Swap (RECOMMENDED)
- Analyze source thumbnail pose
- Find matching reference photo
- Swap with similar angles
- Result: Natural, professional

Option 3: Full AI Generation
- Describe thumbnail concept
- Generate from scratch
- No face swap needed
- Result: Less control, hit-or-miss
```

**Phase 3: Implementation**
```
Choose: Option 2 (Pose-Matched)

Claude Code will:
1. Install MediaPipe
2. Create reference photo analyzer
3. Set up Flux Pro API integration
4. Build directive: directives/thumbnail_generator.md
5. Create execution scripts
```

**Phase 4: Reference Photo Setup**
```
Prompt: "Analyze my reference photos and build a pose library"

System will:
1. Scan reference_photos/ folder
2. Run MediaPipe on each photo
3. Calculate yaw, pitch, roll
4. Store in pose_library.json
5. Ready for matching
```

### Iterative Editing Capability

**Initial Generation**:
```
Prompt: "Generate thumbnails like [URL] using our workflow"

Output: 3 variants of face-swapped thumbnail
```

**Refinement Loop**:
```
Prompt 1: "Change the text from 'Pastor Matt' to 'Nick Saraev'"
→ System regenerates with text change

Prompt 2: "Make the hair darker and the shirt brown"
→ System applies color edits

Prompt 3: "Remove background blur, increase contrast"
→ System applies post-processing

Prompt 4: "Generate 3 more variants with different expressions"
→ System creates alternatives
```

**Iteration Speed**: 20-30 seconds per change.

### The Directive File Structure

**Location**: `directives/thumbnail_generator.md`

**Contents**:
```markdown
# AI Thumbnail Generator

## Description
Face-swap YouTube thumbnails using pose-matched reference photos
for natural results. Generate 3 variants per concept.

## Inputs
- source_url: YouTube video URL or direct thumbnail URL
- num_variants: Number of variations (default: 3)
- custom_text: Optional text overlay changes
- style_modifications: Optional style adjustments

## Steps
1. Download source thumbnail
2. Run MediaPipe face detection on source
3. Calculate source pose (yaw, pitch, roll)
4. Load pose_library.json
5. Find closest matching reference photo by Euclidean distance
6. Select top 2 reference photos for consistency
7. Call Flux Pro API with face swap prompt
8. Generate 3 variants
9. Apply post-processing:
   - Color matching
   - Edge blending
   - Sharpness enhancement
10. Save to thumbnails/ folder
11. Display for user review

## Execution Scripts
- execution/download_thumbnail.py
- execution/analyze_pose.py
- execution/find_best_reference.py
- execution/flux_face_swap.py
- execution/post_process_thumbnail.py

## Outputs
- 3 thumbnail variants in thumbnails/ folder
- Metadata: pose angles, reference photos used
- Preview: Display all 3 for selection

## Edge Cases
- No face detected in source: Warn user, try AI enhancement
- No matching reference photo: Use closest available + warn
- API failure: Retry 3x, then fail gracefully
```

### Real-World Usage

**Example 1: Simple Generation**
```
Input: "Generate thumbnails like https://youtube.com/... using our workflow"

Output:
- thumbnail_variant_1.jpg (closest to original)
- thumbnail_variant_2.jpg (slightly different expression)
- thumbnail_variant_3.jpg (alternative angle)
```

**Example 2: Parallel Generation**
```
Input:
"Run the thumbnail generator on these 3 URLs:
- https://youtube.com/watch?v=ABC
- https://youtube.com/watch?v=DEF
- https://youtube.com/watch?v=GHI"

Output: 9 total thumbnails (3 per source)
Processing time: ~2 minutes (parallel execution)
```

**Example 3: Iterative Refinement**
```
Step 1: Generate base thumbnails
Step 2: "Change Pastor Matt Hagee to Nick Saraev"
Step 3: "Change 'Spirit of Excellence' to 'Workflows with Claude Code'"
Step 4: "Swap profile pic with mine"
Step 5: "Change text from 'How I make $26K/day' to 'How I Make Agent Flows'"

Final result: Fully customized thumbnail in < 3 minutes
```

---

## 5. The DO Framework (Directive-Orchestration-Execution)

### Why This Framework Matters

**The Problem**: AI is probabilistic, business needs deterministic.

**The Solution**: Three-layer architecture that separates concerns.

```
Layer 1: DIRECTIVE (What to do)
├── Natural language instructions
├── Lives in directives/ folder
├── No code, just SOPs
└── Examples: directives/smart_video_edit.md

Layer 2: ORCHESTRATION (Decision making)
├── AI agent (Claude Code)
├── Reads directives
├── Chooses which tools to call
├── Handles errors and retries
└── Adapts to situations

Layer 3: EXECUTION (How to do it)
├── Python scripts
├── Lives in execution/ folder
├── Deterministic, reliable
├── One script = one job
└── Examples: execution/cut_silences.py
```

### Why Separation of Concerns Works

**Probabilistic AI Issue**:
```
Task: "Sort this list of 1000 items"

Without framework:
- AI attempts to sort via reasoning
- Takes 30 seconds
- 90% accurate (100 errors)
- Expensive (lots of tokens)

With framework:
- AI calls sort_list.py
- Takes 0.05 seconds
- 100% accurate (0 errors)
- Free (local execution)
```

**The Rule**: Push deterministic work to code, reserve AI for judgement.

### Folder Structure

```
workspace/
├── directives/
│   ├── smart_video_edit.md
│   ├── cross_niche_outlier.md
│   ├── thumbnail_generator.md
│   └── [other workflows].md
│
├── execution/
│   ├── silero_vad_analysis.py
│   ├── cut_silences.py
│   ├── enhance_audio.py
│   ├── scrape_tubelab.py
│   ├── analyze_pose.py
│   ├── flux_face_swap.py
│   └── [other scripts].py
│
├── reference_photos/
│   ├── straight_on_01.jpg
│   ├── left_45_01.jpg
│   └── [other angles].jpg
│
├── thumbnails/
│   └── [generated thumbnails]
│
├── output/
│   └── [edited videos]
│
├── .env
│   └── API keys stored here
│
├── agents.md
│   └── System prompt (framework explanation)
│
└── pose_library.json
    └── Reference photo metadata
```

### Creating Directives (Natural Language SOPs)

**Format** (Markdown):
```markdown
# [Workflow Name]

## Description
[One sentence: what this does]

## Inputs
- input_1: Description
- input_2: Description

## Steps
1. Step one description
2. Step two description
3. Call execution/script_name.py
4. Step four description

## Execution Scripts
- execution/script1.py
- execution/script2.py

## Outputs
- output_1: Description
- output_2: Description

## Edge Cases
- Case 1: How to handle
- Case 2: How to handle
```

**Key Principles**:
1. No code in directives (only natural language)
2. Clear step-by-step instructions
3. Reference execution scripts by name
4. Include edge case handling
5. Specify expected inputs/outputs

### How Orchestration Works

**The Decision Loop**:
```
1. User sends message: "Edit my video"
                ↓
2. AI reads agents.md (knows about DO framework)
                ↓
3. AI searches directives/ folder
                ↓
4. Finds: directives/smart_video_edit.md
                ↓
5. Reads directive, understands steps
                ↓
6. Sees: "Call execution/cut_silences.py"
                ↓
7. Loads execution/cut_silences.py
                ↓
8. Executes script with parameters
                ↓
9. Script returns result
                ↓
10. AI evaluates: Success or error?
                ↓
    If error: Fix and retry
    If success: Continue to next step
                ↓
11. Repeats for all steps in directive
                ↓
12. Returns final result to user
```

**Error Handling**:
```
Script fails → AI reads error message
              ↓
         Diagnoses problem
              ↓
         Attempts fix
              ↓
         Retries (up to 3x)
              ↓
         If still failing: Report to user
```

### Execution Scripts (Deterministic Tools)

**One Script = One Job**:
```python
# execution/cut_silences.py

Purpose: Remove silence gaps from video
Input: video_file, speech_timestamps.json
Process:
  1. Load video
  2. Load timestamps
  3. Extract segments matching timestamps
  4. Concatenate segments
  5. Save output
Output: video_no_silences.mp4

Always produces same output for same input.
```

**Why One Job Per Script**:
- Easy to test
- Easy to debug
- Easy to replace/improve
- Modular (mix and match)

### Building Workflows in Practice

**The Meta Loop** (Using AI to build AI workflows):

```
You → Claude Code (via voice/text)
        ↓
   "Build me a workflow that does X"
        ↓
   Claude Code researches
        ↓
   Presents 3 options
        ↓
   You choose one
        ↓
   Claude Code builds:
   - Directive file
   - Execution scripts
   - Configuration
        ↓
   You test it
        ↓
   It works? Done.
   It breaks? Claude Code fixes it.
        ↓
   Iterate until perfect
        ↓
   Now you have a reusable workflow
```

**Time Investment**:
- Simple workflow: 15-30 minutes
- Complex workflow: 1-2 hours
- One-time investment, infinite reuse

---

## 6. Integration Strategy (Using All Three Together)

### The Content Production System

**Weekly Workflow**:

```
Monday: Content Research (30 minutes)
├── Run outlier detector: "Find 50 outliers, dump to sheet"
├── Review Google Sheet
├── Flag 3-5 promising concepts
└── Select top concept for this week's video

Tuesday: Pre-Production (1 hour)
├── Feed outlier thumbnail URLs to thumbnail generator
├── Generate 9 thumbnail variants (3 per concept)
├── Select best thumbnail
├── Write script based on outlier summary
└── Prepare recording setup

Wednesday: Recording (30-60 minutes)
└── Record raw video (no editing needed)

Thursday: Post-Production (15 minutes active, 30 minutes processing)
├── Run video editor: "Edit my_recording.mp4"
├── While processing: Create thumbnail variants
├── Review edited video
├── Make final thumbnail text adjustments
└── Export final assets

Friday: Upload
├── Upload video to YouTube
├── Set thumbnail
└── Schedule release
```

**Total Active Time**: ~2.5 hours/week
**Automated Time Saved**: ~8-10 hours/week

### The Parallel Processing Strategy

**Batch Operations**:
```
Instead of:
1. Edit video 1 (wait 30 min)
2. Edit video 2 (wait 30 min)
3. Edit video 3 (wait 30 min)
Total: 90 minutes sequential

Do this:
1. Start video 1 edit (background)
2. Start video 2 edit (background)
3. Start video 3 edit (background)
4. Work on thumbnails while all process
Total: 35 minutes (30 processing + 5 active)
```

**Claude Code Command**:
```
"Edit these 3 videos in parallel:
- monday_recording.mp4
- wednesday_recording.mp4
- friday_recording.mp4

Also generate thumbnails for each using the outlier sheet."
```

System will handle parallelization automatically.

### Data Flow Between Workflows

```
Outlier Detector
    ↓
Outputs Google Sheet with:
- High-performing thumbnails
- Titles that work
- Content themes
- Transcript summaries
    ↓
Human Decision Layer:
- Select which concepts to pursue
- Choose thumbnail styles
    ↓
Thumbnail Generator
    ↓
Inputs from Outlier Sheet:
- Thumbnail URLs for face-swapping
- Title text for overlays
    ↓
Outputs:
- 3 custom thumbnails per concept
    ↓
Video Recording
    ↓
Outputs:
- Raw video file
    ↓
Video Editor
    ↓
Inputs:
- Raw video
    ↓
Outputs:
- Polished, edited video
    ↓
Final Upload:
- Video + Thumbnail + Title (from outlier research)
```

### Scaling Strategy

**Phase 1: Single Video/Week** (Current system)
- 1 video recorded
- 1 outlier detection run/week
- 3 thumbnail concepts tested
- Total time: 2.5 hours

**Phase 2: 2-3 Videos/Week** (Same system, more volume)
- 3 videos recorded
- 1 outlier detection run/week (generates 50+ ideas)
- Batch video editing
- Batch thumbnail generation
- Total time: 5 hours

**Phase 3: Daily Content** (Requires team)
- 7 videos/week
- Continuous outlier monitoring
- Hire video editor to QA AI output
- Hire thumbnail designer to refine AI output
- Your role: Strategy and recording only
- Total time: 10 hours (your time)

---

## 7. Cost Analysis

### One-Time Setup Costs

**Software/Tools**:
```
Claude Code: Free (or $20/month for Pro)
OBS (recording): Free
Silero VAD: Free (open source)
MediaPipe: Free (open source)
Reference photo library: Free (30 min of your time)
```

**Total One-Time Cost**: $0-20

### Ongoing API Costs

**Per Video Production Cycle**:

```
Outlier Detection (100 videos analyzed):
- TubeLab API: $1.00
- Claude API (summarization): $0.50
Total: $1.50 per research session (weekly)

Video Editing:
- All local processing: $0.00
- No API calls needed

Thumbnail Generation (3 variants):
- Flux Pro API: $0.60 (3 × $0.20)
- MediaPipe: Free (local)
Total: $0.60 per video

Weekly Total (1 video):
- Research: $1.50
- Editing: $0.00
- Thumbnails: $0.60
Total: $2.10/week = $109/year
```

### Cost vs Value

**Traditional Approach**:
```
Video editor: $50-100/video
Thumbnail designer: $25-50/thumbnail
Research time: 2-3 hours @ $50/hr = $100-150

Per video cost: $175-300
Per year (52 videos): $9,100-15,600
```

**Automated Approach**:
```
Per video cost: $2.10 in API fees
Per year (52 videos): $109

Savings: $9,000-15,500/year
ROI: 8,257%-14,220%
```

**Plus time saved**: ~8 hours/week = 416 hours/year

---

## 8. Common Issues & Solutions

### Issue 1: Video Editor Cuts Too Aggressively

**Symptom**: Removes pauses that should stay (for emphasis).

**Solution**:
```
Edit directives/smart_video_edit.md:

Change:
silence_threshold: 0.5

To:
silence_threshold: 0.8  (allows longer natural pauses)
```

**Alternative Solution**:
```
Add to directive:
"Preserve pauses after questions (marked by rising intonation)"
```

### Issue 2: Thumbnail Face Looks Unnatural

**Symptom**: Face swap has uncanny valley effect.

**Root Cause**: No matching reference photo for that angle.

**Solution**:
```
1. Check pose_library.json for coverage gaps
2. Take new reference photos at needed angles
3. Run: "Analyze my reference photos and rebuild pose library"
4. Regenerate thumbnail
```

**Quick Fix**:
```
"Generate thumbnail again but use straight-on reference photo
and adjust source thumbnail angle to match"
```

### Issue 3: Outlier Detector Returns Irrelevant Videos

**Symptom**: Videos from completely unrelated niches.

**Solution**:
```
Refine search criteria:

Instead of:
"Find outliers in business niche"

Use:
"Find outliers in [specific sub-niche] such as:
- B2B SaaS marketing
- Agency operations
- Productivity tools
Exclude: Crypto, real estate, e-commerce"
```

### Issue 4: Video Editor Fails on Long Videos (>2 hours)

**Symptom**: Processing crashes or takes forever.

**Solution 1**: Chunk processing
```
Add to directive:
"For videos >90 minutes, split into 30-minute chunks,
process separately, then concatenate"
```

**Solution 2**: Hardware acceleration
```
Enable in directive:
"Use GPU acceleration for encoding (NVIDIA NVENC or AMD VCE)"
```

### Issue 5: Thumbnail Text Overlaps Face

**Symptom**: Generated text placement blocks face.

**Solution**:
```
Iterative edit:
"Move text to top-left corner and reduce size by 20%"

Or add to directive:
"Text placement rules:
- Never place text over face region
- Use rule of thirds for positioning
- Ensure high contrast with background"
```

### Issue 6: API Rate Limits

**Symptom**: TubeLab or Flux Pro returns rate limit error.

**Solution**:
```
Add to execution script:
- Implement exponential backoff
- Retry with delay: 1s, 2s, 4s, 8s
- If still failing after 4 retries, queue for later

Or batch operations:
"Process 25 videos now, wait 1 hour, process next 25"
```

---

## 9. Advanced Techniques

### Technique 1: Multi-Stage Video Processing

**Beyond basic editing**:
```
Stage 1: Silence removal (current workflow)
Stage 2: Add B-roll insertion points
         └── AI identifies topics needing visual examples
         └── Suggests timestamps for B-roll
Stage 3: Auto-generate B-roll
         └── Use AI image generation for concepts
         └── Or pull from stock footage APIs
Stage 4: Add captions/subtitles
         └── Transcribe with Whisper
         └── Generate SRT file
         └── Burn into video
```

**Build this**:
```
"Extend my video editing workflow to:
1. Identify topics that need B-roll
2. Generate B-roll suggestions with timestamps
3. Auto-transcribe and add captions"
```

### Technique 2: Style Transfer for Thumbnails

**Beyond face-swapping**:
```
Current: Face swap exact thumbnail
Advanced: Apply artistic style

Example:
"Take this high-performing thumbnail, swap my face,
but apply [channel name]'s visual style:
- Color palette: [colors]
- Font: [font name]
- Background pattern: [description]"
```

**Build this**:
```
"Add style transfer to thumbnail generator:
1. Analyze my last 10 thumbnails
2. Extract style patterns (colors, fonts, composition)
3. Apply this style to new thumbnails automatically"
```

### Technique 3: Predictive Outlier Scoring

**Current**: Analyze existing videos (retrospective).

**Advanced**: Predict which concepts will perform (prospective).

```
Extension:
"Train a model on:
- 1000+ outlier videos from my niche
- Extract patterns: titles, topics, hooks
- Predict outlier score for new concepts before creating

Usage:
'Will this title work: [proposed title]'
→ Returns predicted outlier score + suggestions"
```

### Technique 4: Automated A/B Testing

**Workflow**:
```
Phase 1: Generate 3 thumbnail variants (current workflow)
Phase 2: Upload video with thumbnail A
Phase 3: After 2 hours, check CTR
Phase 4: If CTR < 6%, swap to thumbnail B
Phase 5: After 2 more hours, check again
Phase 6: Keep winner, archive losers
```

**Build this**:
```
"Create auto A/B testing workflow:
1. Generate 3 thumbnails
2. Upload video with thumbnail 1
3. Monitor CTR every 2 hours
4. Auto-swap to better performing thumbnail
5. Report final winner"
```

### Technique 5: Voice Cloning for Mistake Correction

**Current**: Cut mistakes, lose content.

**Advanced**: Re-voice mistakes without re-recording.

```
Workflow:
1. Detect mistake segment
2. Extract script from context
3. Generate corrected audio with your cloned voice
4. Splice in corrected audio
5. Result: Seamless fix without re-recording
```

**Build this**:
```
"Extend video editor with voice cloning:
1. Train on my voice (10 min of audio)
2. When mistake detected, extract what I meant to say
3. Generate corrected audio in my voice
4. Replace mistake segment"
```

---

## 10. Scaling Beyond YouTube

### Adaptation 1: Podcast Production

**Similar workflows apply**:
```
Outlier Detection → Top podcast episodes in niche
Video Editor → Audio editor (remove silence, enhance quality)
Thumbnail Generator → Podcast cover art generator
```

**Build command**:
```
"Adapt my YouTube workflows for podcast production:
- Outlier detector for podcast episodes (Spotify/Apple)
- Audio editor (remove silences, enhance, add intro/outro)
- Cover art generator (text-based, no faces)"
```

### Adaptation 2: Social Media Clips

**Workflow**:
```
Input: Edited long-form video
       ↓
AI analyzes transcript for:
- High-engagement moments
- Self-contained segments
- Viral-worthy quotes
       ↓
Automatically cut clips:
- 15s, 30s, 60s versions
- Portrait (9:16) and landscape (16:9)
- Add captions
       ↓
Generate thumbnails for each
       ↓
Output: 10-20 clips ready for TikTok/IG/Twitter
```

### Adaptation 3: Email Newsletter

**Content repurposing**:
```
Outlier Detector output (summaries of videos)
       ↓
Weekly digest:
- "Top 5 business videos this week"
- Each with summary + key takeaway
- Link to full video
       ↓
Auto-send via email API
```

### Adaptation 4: Client Services

**Sell these workflows**:
```
Service 1: "YouTube Automation Package"
- Setup: $2,000 one-time
- Includes: All 3 workflows customized
- Training: 2-hour session
- Result: Client can produce videos 10× faster

Service 2: "Monthly Video Production"
- Recurring: $500/month
- You run workflows on their content
- They record, you handle everything else
- Scalable: 20 clients = $10K/month with minimal time

Service 3: "Workflow Development"
- Custom: $150/hour
- Build custom workflows for client needs
- Example: "Automate my podcast editing"
- Recurring revenue through maintenance
```

---

## AI PARSING GUIDE

### Primary Objective
When building video production workflows, use the DO framework (Directives-Orchestration-Execution) to separate natural language instructions from deterministic code execution.

### Critical Decision Points

**If User Says**: "I want to automate my video editing"
**Action Sequence**:
1. Ask about current workflow (what's manual?)
2. Identify repetitive tasks (silence removal, color grading, etc.)
3. Research existing tools/APIs
4. Present 3 approaches
5. Build directive + execution scripts
6. Test and iterate

**If User Says**: "The video editor cuts too much"
**Ask**:
- Where does it cut incorrectly? (timestamps)
- What should it preserve? (pauses, emphasis, etc.)
- Adjust silence_threshold or add rules to directive

**If User Says**: "Thumbnails look weird"
**Diagnose**:
1. Check pose matching (are angles similar?)
2. Review reference photo library (any gaps?)
3. Test with different reference photo
4. Adjust post-processing settings

### Integration Points

**Connects to**:
- Content Strategy (outlier detection feeds ideation)
- Video Production (editing pipeline)
- Growth Marketing (thumbnail optimization)
- Automation Infrastructure (DO framework foundation)
- API Integration (TubeLab, Flux Pro, YouTube)

### Output Quality Standards

When helping build these workflows:
1. ✅ Directive file created (natural language, no code)
2. ✅ Execution scripts in execution/ folder
3. ✅ One script = one job (modular)
4. ✅ Error handling in place
5. ✅ Reference materials organized (photos, configs)
6. ✅ Test on sample before production use

### Red Flags (Anti-Patterns)

❌ Code mixed into directive files
❌ Monolithic scripts that do multiple jobs
❌ No error handling
❌ Hardcoded paths/values (use config files)
❌ No reference photo library for thumbnails
❌ Skipping test phase

### Workflow Building Template

For any new automation workflow:
```
1. Define: What manual task to automate?
2. Research: What tools/APIs exist?
3. Design: 3 possible approaches
4. Choose: Best balance of quality/speed/cost
5. Build: Directive + execution scripts
6. Test: On sample data
7. Iterate: Fix issues
8. Deploy: Use in production
9. Monitor: Track performance
10. Improve: Refine based on results
```

---

## SOURCE ATTRIBUTION

**Primary Source**: Nick Saraev - "f*ck it. Here's how I automated my youtube channel in 24 mins (I show everything)"
- **Video ID**: S3kdxriOESk
- **Duration**: 23 minutes 17 seconds
- **Context**: Complete walkthrough of 3 production YouTube workflows with live demonstrations
- **Key Contribution**: Practical implementation of DO framework for video production automation
- **Authority Basis**: Built two AI agencies to $160K/month combined revenue, consultant for billion-dollar businesses
- **Technical Detail Level**: Shows actual directives, execution scripts, API integrations, and real output
- **Unique Innovation**: Pose-matched face swapping via MediaPipe for natural thumbnails
- **Capture Date**: January 2026 (via MCP YouTube Transcript)

**Supporting Context**: References to 6-hour Agentic Workflows course for DO framework fundamentals (video MxyRjL7NG18)

**Synthesis Approach**: This skill bible extracts three complete, production-ready workflows from a single tutorial video where Nick demonstrates his actual YouTube automation system. Each workflow is documented with full technical architecture, build instructions, real-world usage, and integration strategies.

---

**END SKILL BIBLE: YouTube Channel Automation (3 Complete Workflows)**