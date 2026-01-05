# Podcast-to-Social Repurposer

## What This Workflow Is
This workflow transforms podcast episodes into multiple content pieces including short clips, Twitter threads, LinkedIn posts, blog articles, and Instagram carousels.

## What It Does
1. Transcribes podcast episode
2. Identifies highlight moments and quotes
3. Generates short video clips (30-60s)
4. Creates platform-specific content (threads, posts, carousels)
5. Outputs organized content package

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For transcription + content
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- ffmpeg (for video processing)
- OpenAI Whisper

### Installation
```bash
pip install openai yt-dlp pydub
brew install ffmpeg  # or apt-get install ffmpeg
```

## How to Run

### Step 1: Transcribe Episode
```bash
python3 execution/transcribe_podcast.py \
  --url "[PODCAST_URL]" \
  --output .tmp/transcript.txt
```

### Step 2: Generate All Content
```bash
python3 execution/repurpose_podcast.py \
  --transcript .tmp/transcript.txt \
  --platforms "twitter,linkedin,instagram" \
  --output_dir .tmp/episode_content/
```

### Quick One-Liner
```bash
python3 execution/transcribe_podcast.py --url "[URL]" && \
python3 execution/repurpose_podcast.py --transcript .tmp/transcript.txt --platforms all
```

## Goal
Transform podcast episodes into multiple content pieces for social media distribution.

## Inputs
- **Podcast URL**: YouTube, Spotify, or audio file
- **Episode Title**: For context
- **Target Platforms**: Twitter, LinkedIn, Instagram, TikTok

## Process

### 1. Transcribe Episode
```bash
python3 execution/transcribe_podcast.py \
  --url "[PODCAST_URL]" \
  --output .tmp/transcript.txt
```

### 2. Extract Content
```bash
python3 execution/repurpose_podcast.py \
  --transcript .tmp/transcript.txt \
  --platforms "twitter,linkedin,instagram"
```

### 3. Content Outputs

**Short Clips (3-5 per episode)**
- 30-60 second highlight clips
- Best quotes/insights
- Caption + hashtags included

**Twitter Thread**
- Key insights as thread
- 8-12 tweets
- Quote graphics

**LinkedIn Posts (2-3)**
- Long-form posts from main points
- Story-based or tip-based

**Instagram**
- Carousel summarizing episode
- Reel script from best moment
- Quote graphics

**Blog Post**
- Full episode summary
- Show notes
- SEO optimized

**Newsletter Section**
- Episode highlight
- Key takeaways
- Listen link

### 4. Output Structure
```
/episode_[name]/
  ├── clips/
  │   ├── clip_1.mp4
  │   ├── clip_2.mp4
  │   └── clip_3.mp4
  ├── twitter_thread.md
  ├── linkedin_posts.md
  ├── instagram_carousel.md
  ├── reel_script.md
  ├── blog_post.md
  └── quote_graphics/
```

### 5. Distribution Schedule
| Day | Platform | Content |
|-----|----------|---------|
| 1 | All | Episode announcement |
| 2 | Twitter | Thread |
| 3 | LinkedIn | Post 1 |
| 4 | Instagram | Reel |
| 5 | Twitter | Clip 1 |
| 6 | LinkedIn | Post 2 |
| 7 | Instagram | Carousel |

## Integrations
- Whisper (transcription)
- OpenAI (content generation)
- Video editing API (clips)

## Cost
- Transcription: ~$0.10/hour
- Content generation: ~$0.20/episode
- **Per episode: ~$0.50-1.00**
