# Video-to-Shorts Clip Extractor

## What This Workflow Is
This workflow uses AI to analyze long-form videos, identify viral-worthy moments, and automatically extract vertical short clips for YouTube Shorts, TikTok, and Instagram Reels.

## What It Does
1. Analyzes video for high-engagement moments
2. Identifies quotable statements and visual highlights
3. Extracts and crops clips to vertical format
4. Adds auto-captions/subtitles
5. Outputs clips with titles, descriptions, hashtags

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For analysis + captions
```

### Required Tools
- Python 3.10+
- ffmpeg
- yt-dlp (for YouTube downloads)

### Installation
```bash
pip install openai yt-dlp
brew install ffmpeg
```

## How to Run

### Step 1: Analyze Video
```bash
python3 execution/analyze_video.py \
  --url "[YOUTUBE_URL]" \
  --output .tmp/analysis.json
```

### Step 2: Extract Clips
```bash
python3 execution/extract_clips.py \
  --video "[VIDEO_FILE]" \
  --timestamps .tmp/analysis.json \
  --format vertical \
  --output .tmp/clips/
```

### Quick One-Liner
```bash
python3 execution/analyze_video.py --url "[URL]" && \
python3 execution/extract_clips.py --video .tmp/video.mp4 --timestamps .tmp/analysis.json
```

## Goal
Automatically extract viral-worthy short clips from long-form videos for YouTube Shorts, TikTok, and Reels.

## Inputs
- **Video URL**: YouTube or local file
- **Clip Count**: Number of clips to extract
- **Clip Length**: 15s, 30s, 60s
- **Style**: Vertical (9:16) or Square (1:1)

## Process

### 1. Analyze Video
```bash
python3 execution/analyze_video.py \
  --url "[YOUTUBE_URL]" \
  --output .tmp/analysis.json
```

AI identifies:
- High-engagement moments
- Quotable statements
- Visual highlights
- Emotional peaks
- Story arcs

### 2. Extract Clips
```bash
python3 execution/extract_clips.py \
  --video "[VIDEO_FILE]" \
  --timestamps .tmp/analysis.json \
  --format vertical \
  --output .tmp/clips/
```

### 3. Clip Enhancement
- Auto-crop to vertical
- Add captions/subtitles
- Add progress bar
- Optimize audio levels
- Add hook text overlay

### 4. Output Per Clip
```
clip_[X]/
  ├── clip.mp4 (processed)
  ├── thumbnail.jpg
  ├── title_options.txt
  ├── description.txt
  └── hashtags.txt
```

### 5. Clip Selection Criteria
| Factor | Weight |
|--------|--------|
| Standalone value | High |
| Hook strength | High |
| Visual interest | Medium |
| Quote-worthy | Medium |
| Controversy/debate | Medium |

## Best Practices
- First 1-2 seconds must hook
- Clear single takeaway per clip
- Captions increase watch time 40%
- Post 3-5 clips per long video

## Integrations
- YouTube API
- FFmpeg (video processing)
- Whisper (captions)
- OpenAI (analysis)

## Cost
- ~$0.20-0.50 per video analyzed
- Processing: Local/free
