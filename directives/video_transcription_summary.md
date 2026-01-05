# Video Transcription + Summary

## What This Workflow Is
This workflow transcribes videos from YouTube, Google Drive, or local files and generates AI summaries with key points, timestamps, and action items.

## What It Does
1. Downloads/extracts audio from video
2. Transcribes using Whisper
3. Generates summary with key points
4. Creates timestamp markers
5. Extracts action items and quotes

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For transcription + summary
```

### Required Tools
- Python 3.10+
- ffmpeg
- OpenAI API access

### Installation
```bash
pip install openai yt-dlp pydub
brew install ffmpeg
```

## How to Run

### Step 1: Extract Audio
```bash
python3 execution/extract_audio.py --url "[VIDEO_URL]" --output .tmp/audio.mp3
```

### Step 2: Transcribe
```bash
python3 execution/transcribe_video.py \
  --audio .tmp/audio.mp3 \
  --output .tmp/transcript.txt
```

### Step 3: Generate Summary
```bash
python3 execution/summarize_video.py \
  --transcript .tmp/transcript.txt \
  --format detailed \
  --output .tmp/summary.md
```

### Quick One-Liner
```bash
python3 execution/extract_audio.py --url "[URL]" && \
python3 execution/transcribe_video.py --audio .tmp/audio.mp3 && \
python3 execution/summarize_video.py --transcript .tmp/transcript.txt
```

## Goal
Transcribe videos and generate summaries, key points, and action items.

## Inputs
- **Video Source**: YouTube URL, Google Drive, or file upload
- **Output Format**: Summary, full transcript, or both
- **Summary Length**: Brief (1 para), Standard (3-5 points), Detailed

## Process

### 1. Extract Audio
```bash
python3 execution/extract_audio.py --url "[VIDEO_URL]" --output .tmp/audio.mp3
```

### 2. Transcribe
```bash
python3 execution/transcribe_video.py \
  --audio .tmp/audio.mp3 \
  --output .tmp/transcript.txt
```

### 3. Generate Summary
```bash
python3 execution/summarize_video.py \
  --transcript .tmp/transcript.txt \
  --format detailed \
  --output .tmp/summary.md
```

### 4. Output Structure
```markdown
# Video Summary: [Title]

**Duration:** [X minutes]
**Source:** [URL]

## TL;DR
[2-3 sentence summary]

## Key Points
1. [Main point 1]
2. [Main point 2]
3. [Main point 3]

## Detailed Summary
[Section-by-section breakdown]

## Timestamps
- 0:00 - Intro
- 2:30 - [Topic 1]
- 8:45 - [Topic 2]

## Quotes
> "[Notable quote 1]"
> "[Notable quote 2]"

## Action Items
- [ ] [Action 1]
- [ ] [Action 2]
```

### 5. Use Cases
- Meeting recordings
- Webinar summaries
- Podcast notes
- Tutorial documentation
- Research videos

## Integrations
- OpenAI Whisper (transcription)
- OpenAI/Anthropic (summarization)

## Cost
- Transcription: ~$0.006/minute
- Summary: ~$0.03-0.05
- **1-hour video: ~$0.40**
