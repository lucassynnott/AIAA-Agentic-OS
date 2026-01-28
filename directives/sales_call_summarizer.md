# Sales Call Transcription + Summary

## What This Workflow Is
This workflow transcribes sales call recordings and uses AI to generate structured summaries including key points, objections raised, action items, and deal assessment.

## What It Does
1. Takes audio/video recording as input
2. Transcribes using Whisper or AssemblyAI
3. Identifies speakers (diarization)
4. Generates structured summary with AI
5. Exports to CRM, Google Docs, or Slack

## Prerequisites

### Required API Keys (add to .env)
```
OPENAI_API_KEY=your_openai_key            # For transcription + summary
ASSEMBLYAI_API_KEY=your_assemblyai_key    # Alternative for transcription
GOOGLE_APPLICATION_CREDENTIALS=credentials.json  # For Google Docs
```

### Required Tools
- Python 3.10+
- OpenAI API access (Whisper)
- ffmpeg (for audio processing)

### Installation
```bash
pip install openai google-api-python-client pydub
brew install ffmpeg  # or apt-get install ffmpeg
```

## How to Run

### Step 1: Transcribe Recording
```bash
python3 execution/transcribe_call.py \
  --input recording.mp3 \
  --output .tmp/transcript.txt
```

### Step 2: Generate Summary
```bash
python3 execution/summarize_call.py \
  --transcript .tmp/transcript.txt \
  --call_type discovery \
  --output .tmp/summary.json
```

### Step 3: Export to Google Doc
```bash
python3 execution/export_call_summary.py \
  --summary .tmp/summary.json \
  --format gdoc \
  --title "Call Summary - Acme Corp - Jan 15"
```

### Quick One-Liner
```bash
python3 execution/transcribe_call.py --input recording.mp3 && \
python3 execution/summarize_call.py --transcript .tmp/transcript.txt --call_type discovery
```

### Process Zoom Recording URL
```bash
python3 execution/transcribe_call.py --url "https://zoom.us/rec/xxx" --output .tmp/transcript.txt
```

## Goal
Automatically transcribe sales calls and generate AI summaries with action items, objections, and next steps.

## Inputs
- **Audio/Video File**: Call recording (MP3, MP4, WAV)
- **Recording URL**: Zoom/Google Meet recording link
- **Call Type**: Discovery, Demo, Closing, Follow-up

## Tools/Scripts
- `execution/transcribe_call.py` - Audio transcription
- `execution/summarize_call.py` - AI summary generation

## Process

### 1. Transcribe Recording
```bash
python3 execution/transcribe_call.py \
  --input recording.mp3 \
  --output .tmp/transcript.txt
```

Uses: OpenAI Whisper or AssemblyAI

### 2. Generate Summary
```bash
python3 execution/summarize_call.py \
  --transcript .tmp/transcript.txt \
  --call_type discovery \
  --output .tmp/summary.json
```

### 3. Summary Structure

```markdown
# Call Summary
**Date:** [Date]
**Duration:** [Length]
**Participants:** [Names]
**Call Type:** Discovery

## Quick Overview
[2-3 sentence summary of the call]

## Key Discussion Points
1. [Topic 1]
   - [Key details]
2. [Topic 2]
   - [Key details]

## Pain Points Identified
- [Pain point 1]
- [Pain point 2]
- [Pain point 3]

## Objections Raised
| Objection | Response Given | Resolved? |
|-----------|----------------|-----------|
| [Objection 1] | [Response] | Yes/No |
| [Objection 2] | [Response] | Yes/No |

## Budget/Timeline Discussion
- Budget: [Mentioned/Not discussed]
- Timeline: [Urgency level]
- Decision maker: [Identified/Unknown]

## Competitor Mentions
- [Competitor 1]: [Context]
- [Competitor 2]: [Context]

## Action Items
### For Us
- [ ] [Action 1] - Due: [Date]
- [ ] [Action 2] - Due: [Date]

### For Prospect
- [ ] [Action 1]
- [ ] [Action 2]

## Next Steps
- [Next meeting/action]
- Follow-up date: [Date]

## Deal Assessment
- **Interest Level:** High/Medium/Low
- **Fit Score:** [X/10]
- **Close Probability:** [X%]
- **Recommended Action:** [Proceed/Nurture/Disqualify]

## Notable Quotes
> "[Impactful quote from prospect]"
```

### 4. Output Destinations
- Google Doc (shareable)
- CRM note (HubSpot, Salesforce)
- Slack notification
- Email to team

## Integration Options

### Auto-Capture from Zoom
Webhook triggers on recording ready.

### Auto-Capture from Fireflies/Otter
Pull transcripts via API.

### Manual Upload
Drag-drop recording to process.

## Integrations Required
- OpenAI Whisper or AssemblyAI (transcription)
- OpenAI/Anthropic (summarization)
- CRM API (optional)
- Google Docs API (optional)

## Cost Estimate
- Transcription: ~$0.006/minute (Whisper)
- Summary: ~$0.05/call
- **30-min call: ~$0.25**

## Use Cases
- Sales call documentation
- Client meeting notes
- Coaching and training
- Deal review prep

## Edge Cases
- Poor audio quality: Flag for manual review
- Multiple speakers: Use diarization
- Long calls (60+ min): Chunk processing

## Related Skill Bibles

Load these skill bibles for better call analysis and insights:

**[SKILL_BIBLE_hormozi_sales_training.md](../skills/SKILL_BIBLE_hormozi_sales_training.md)**
- Ultimate Sales Training 2025 framework
- Objection handling patterns to identify
- Sales psychology and buying signals

**[SKILL_BIBLE_hormozi_closing_deals.md](../skills/SKILL_BIBLE_hormozi_closing_deals.md)**
- 4000+ sales closing methodology
- Deal acceleration techniques
- Close probability indicators

**[SKILL_BIBLE_hormozi_sales_concepts.md](../skills/SKILL_BIBLE_hormozi_sales_concepts.md)**
- 9 core sales concepts
- Framework for understanding buyer behavior
- Sales conversation patterns

**[SKILL_BIBLE_agency_sales_system.md](../skills/SKILL_BIBLE_agency_sales_system.md)**
- Agency-specific sales frameworks
- Discovery call structure
- Deal qualification criteria
