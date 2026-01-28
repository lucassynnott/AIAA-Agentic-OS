# Facebook Ad Library Analysis Automation

## What This Workflow Is
This workflow scrapes Facebook Ad Library for competitor ads, downloads media, and uses AI (Gemini) to analyze ad creative, copy, and strategies.

## What It Does
1. Receives search keyword via form
2. Scrapes Ad Library for matching ads
3. Downloads images/videos
4. AI analyzes each ad creative
5. Outputs summaries to Google Sheet

## Prerequisites

### Required API Keys (add to .env)
```
GEMINI_API_KEY=your_gemini_key            # For video/image analysis
GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

### Required Tools
- Python 3.10+
- Ad Library scraper access
- Google OAuth

### Installation
```bash
pip install google-generativeai google-api-python-client requests
```

## How to Run

### Via N8N Form
Submit form with:
- Facebook Ad Library Search Keyword

### Via Python Script
```bash
python3 execution/analyze_fb_ads.py \
  --keyword "skincare brand" \
  --output_sheet "[SHEET_URL]"
```

### Quick One-Liner
```bash
python3 execution/analyze_fb_ads.py --keyword "[KEYWORD]"
```

## Goal
[Describe the purpose of this workflow]

## Trigger
- **Type**: Form
- **Node**: On form submission

## Inputs
- **Facebook Ad Library Search Keyword**: text (required)

## Integrations Required
- Google Sheets

## Process
### 1. Switch
[Describe what this step does]

### 2. Filter For Likes
[Describe what this step does]

### 3. Wait
[Describe what this step does]

### 4. Wait1
[Describe what this step does]

### 5. Download Video
[Describe what this step does]

### 6. Upload Video to Drive
[Describe what this step does]

### 7. Wait2
[Describe what this step does]

### 8. Loop Over Image Ads
[Describe what this step does]

### 9. Loop Over Text Ads
[Describe what this step does]

### 10. Loop Over Video Ads
[Describe what this step does]

### 11. Begin Gemini Upload Session
[Describe what this step does]

### 12. Redownload Video
[Describe what this step does]

### 13. Upload Video to Gemini
[Describe what this step does]

### 14. Analyze Video with Gemini
[Describe what this step does]

### 15. Output Video Summary
[Describe what this step does]

### 16. Add as Type = Video
[Describe what this step does]

### 17. Analyze Image
[Describe what this step does]

### 18. Output Image Summary
[Describe what this step does]

### 19. Add as Type = Image
[Describe what this step does]

### 20. Output Text Summary
[Describe what this step does]

### 21. Add as Type = Text
[Describe what this step does]

### 22. Wait3
[Describe what this step does]

### 23. On form submission
Workflow is triggered via form.

### 24. Wait4
[Describe what this step does]

### 25. Download Image
[Describe what this step does]

### 26. Run Ad Library Scraper
[Describe what this step does]

### 27. Get Ad Library Scraper Results
[Describe what this step does]

## Output Schema
[Define expected output structure]

## Edge Cases
- Handle empty/missing input fields
- API rate limits for external services
- AI model failures or timeouts

## Related Skill Bibles

**[SKILL_BIBLE_meta_ads_manager_technical.md](../skills/SKILL_BIBLE_meta_ads_manager_technical.md)** (PRIMARY)
- Complete Meta Ads Manager technical mastery
- Persona-led creative diversification (90% success rate)
- Understanding what makes Meta ads perform
- Andromeda update impact analysis
- Creative development best practices

**[SKILL_BIBLE_hormozi_ad_analysis.md](../skills/SKILL_BIBLE_hormozi_ad_analysis.md)**
- Ad analysis and critique framework
- What makes ads convert vs fail
- Creative direction insights

## Original N8N Workflow
This directive was generated from: `N8N Workflows/Workflows/Funnels, Ads, & Copywriting Agency/Facebook Ad Library Analysis Automation.json`
Generated on: 2026-01-02