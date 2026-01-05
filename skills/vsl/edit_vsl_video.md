# Edit VSL Video: Complete Post-Production Workflow

## Purpose
Transform raw VSL footage into a polished, professional video asset that maximizes conversions through strategic editing, pacing, and post-production enhancements.

## When to Use
- After recording VSL footage
- Raw footage needs polishing for landing page
- Existing VSL needs refresh/optimization
- Creating multiple VSL variations for A/B testing
- Client needs professional video editing service

## Prerequisites
- Raw VSL footage recorded in OBS (1080p, 30fps)
- VSL script/transcript for reference
- Gamma presentation slides (or similar)
- Brand assets (logos, colors, fonts)
- Video editing software installed

## Editing Philosophy

**Goal**: Enhance, don't overdo. The VSL should feel professional but authentic.

**Key Principles:**
1. **Pacing is everything** - Keep viewers engaged through dynamic editing
2. **Authenticity > perfection** - Light mistakes humanize you
3. **Audio quality first** - Poor audio kills conversions faster than poor video
4. **Maintain congruency** - Match the energy and tone throughout
5. **Test before scaling** - Get feedback before heavy production

## Required Software & Tools

### Video Editing Software Options

**Option 1: DaVinci Resolve (FREE) - RECOMMENDED**
- **Cost**: Free (Professional version $295 one-time)
- **Best for**: Color grading, audio mixing, professional output
- **Pros**:
  - Industry-standard color correction
  - Built-in audio editing (Fairlight)
  - Free version is extremely capable
  - No watermarks
  - Professional delivery presets
- **Cons**:
  - Steeper learning curve
  - Resource intensive (needs good GPU)
- **Download**: blackmagicdesign.com/products/davinciresolve

**Option 2: Adobe Premiere Pro**
- **Cost**: $22.99/month (Creative Cloud)
- **Best for**: Integration with Adobe ecosystem
- **Pros**:
  - Industry standard
  - Integration with After Effects, Photoshop
  - Extensive plugins and presets
  - Familiar interface for many
- **Cons**:
  - Subscription cost
  - Can be buggy
  - Resource intensive
- **Use if**: Already have Creative Cloud subscription

**Option 3: Final Cut Pro (Mac Only)**
- **Cost**: $299.99 one-time
- **Best for**: Mac users wanting speed
- **Pros**:
  - Optimized for Mac hardware
  - Fast rendering
  - Magnetic timeline (easy to use)
  - One-time purchase
- **Cons**:
  - Mac only
  - Less industry-standard than Premiere/Resolve
- **Use if**: Mac user, want speed over advanced features

**Option 4: CapCut (FREE)**
- **Cost**: Free
- **Best for**: Beginners, quick edits
- **Pros**:
  - Very easy to use
  - Templates and presets
  - Auto-captions
  - Cloud-based option
- **Cons**:
  - Limited professional features
  - Watermark on free version
  - Less control over advanced settings
- **Use if**: Testing VSL concept, minimal editing needed

**This guide uses DaVinci Resolve** (most accessible + professional)

### Supporting Software

**Audio Cleanup:**
- **Audacity** (Free): Basic noise removal, EQ
- **Adobe Audition** ($22.99/mo): Professional audio restoration
- **iZotope RX** ($399): Industry-leading audio repair

**Motion Graphics:**
- **After Effects** ($22.99/mo): Professional motion graphics
- **Apple Motion** ($49.99): Mac alternative to AE
- **Canva** (Free/Pro): Simple animated text overlays

**Asset Creation:**
- **Canva Pro** ($12.99/mo): Graphics, thumbnails, lower thirds
- **Figma** (Free): UI/design elements
- **Photoshop** ($22.99/mo): Advanced graphics

## Pre-Edit Preparation

### 1. Review All Raw Footage

**Create Edit Notes Document:**
```
VSL EDIT NOTES - [Project Name]

RAW FOOTAGE:
- Take 1: 00:00-08:45 (good energy, fumbled at 3:20)
- Take 2: 00:00-09:10 (best take, use as primary)
- Take 3: 00:00-08:30 (backup, tired energy)

SECTIONS TO USE:
- Intro: Take 2 (00:00-01:15)
- Problem: Take 2 (01:15-03:45)
- Solution: Take 2 (03:45-05:20)
- Proof: Take 2 (05:20-07:30)
- CTA: Take 2 (07:30-09:10)

MISTAKES TO CUT:
- Take 2, 03:20-03:24: Word stumble, cut and smooth
- Take 2, 06:45: Long pause, tighten
- Take 2, 08:10: "Um" filler, remove

NOTES:
- Slide transitions need smoothing
- Audio levels drop at 04:30, needs boost
- Add lower third at intro
- Insert B-roll at proof section
```

### 2. Organize Project Assets

**Folder Structure:**
```
/[ProjectName]_VSL_Edit
  /01_Raw_Footage
    - Take1.mp4
    - Take2.mp4
    - Take3.mp4
  /02_Audio
    - Voiceover_cleaned.wav
    - Music_background.mp3
  /03_Graphics
    - Logo.png
    - Lower_thirds.png
    - Client_logos.png
    - Testimonial_graphics.png
  /04_B-Roll
    - Charts_animation.mp4
    - Screencast_dashboard.mp4
  /05_Project_Files
    - [ProjectName].drp (DaVinci Resolve project)
  /06_Exports
    - [ProjectName]_v1.mp4
    - [ProjectName]_v2.mp4
    - [ProjectName]_FINAL.mp4
```

### 3. Set Up Edit Project

**DaVinci Resolve Project Settings:**

1. **Create New Project**: File → New Project → "[ProjectName]_VSL"

2. **Set Timeline Resolution**:
   - Right-click in Media Pool → Timeline → Create New Timeline
   - Name: "Main Edit"
   - Timeline Resolution: 1920x1080 HD
   - Timeline Frame Rate: 30fps
   - Click Create

3. **Project Settings** (Gear icon):
   - **Master Settings Tab**:
     - Timeline Resolution: 1920x1080 HD
     - Timeline Frame Rate: 30
     - Playback Frame Rate: 30
   - **Color Management Tab**:
     - Color Science: DaVinci YRGB Color Managed
     - Timeline Color Space: Rec.709 Gamma 2.4
   - **Capture & Playback Tab**:
     - Audio Sample Rate: 48000 Hz
     - Bit Depth: 24-bit

## Editing Workflow

### Phase 1: Assembly Edit (Rough Cut)

**Goal**: Get all footage on timeline in correct order, no polish yet.

#### Step 1: Import Footage

1. Media Pool (top left) → Right-click → Import Media
2. Select all raw footage files
3. Drag "Take 2" (best take) to timeline
4. Scrub through and identify sections

#### Step 2: Mark In/Out Points

For each section of your VSL:
1. Play to start of good section
2. Press "I" key (Mark In)
3. Play to end of good section
4. Press "O" key (Mark Out)
5. Drag to timeline or press F9

**Structure your timeline by sections:**
```
TIMELINE VIEW:
[00:00-01:00] Intro/Hook
[01:00-02:30] Problem Agitation
[02:30-03:30] Solution Introduction
[03:30-06:00] Proof Stack (case studies)
[06:00-07:30] Process/How It Works
[07:30-08:00] Objection Handling
[08:00-09:00] CTA/Next Steps
```

#### Step 3: Remove Major Mistakes

**Using Blade Tool (B key):**
1. Scrub to mistake start
2. Press B (blade tool)
3. Click timeline to cut
4. Scrub to mistake end
5. Cut again
6. Press A (selection tool)
7. Click unwanted section
8. Press Delete (or Backspace)
9. Press Delete again to "ripple delete" (close gap)

**Common Cuts:**
- Stumbles/word fumbles
- Long pauses (>2 seconds)
- "Um", "uh", filler words
- False starts
- Off-script tangents

#### Step 4: Assembly Review

1. Play full timeline start to finish
2. Check:
   - [ ] All sections present
   - [ ] Logical flow maintained
   - [ ] Major mistakes removed
   - [ ] Approximate target length (3-5 min for most VSLs)
3. Take notes on:
   - Pacing issues (too slow/fast)
   - Energy inconsistencies
   - Audio problems
   - Visual issues

**Save**: File → Save Project (Cmd/Ctrl + S)

---

### Phase 2: Fine Cut (Detailed Edit)

**Goal**: Tighten pacing, smooth transitions, perfect the flow.

#### Step 1: Tighten Pacing

**Remove Dead Air:**
- Pauses between sentences should be 0.5-1 second max
- Pauses between sections can be 1-2 seconds
- Pauses before key points can be 1.5 seconds (for emphasis)

**How to Tighten:**
1. Zoom in on timeline (Cmd/Ctrl + Plus)
2. Find pauses in audio waveform (flat lines)
3. Cut out excess silence
4. Leave just enough for natural breath

**Breathing Room Formula:**
- Between words in sentence: 0.2-0.3 sec
- Between sentences: 0.5-0.8 sec
- Before important point: 1-1.5 sec
- Section transitions: 1.5-2 sec

**Pacing Cadence:**
- Intro/Hook: Fast pace, punchy
- Problem: Medium pace, let pain sink in
- Solution: Varied pace, build excitement
- Proof: Steady pace, let data speak
- CTA: Slow down slightly, clear and deliberate

#### Step 2: Smooth Jump Cuts

**The Problem**: When you cut within same shot, creates visual "jump"

**Solutions:**

**Option A: B-Roll Overlay**
1. Cut the audio as needed (tight pacing)
2. Add B-roll footage over the jump cut
3. B-roll covers the visual jump while audio flows smoothly

**B-Roll Sources:**
- Screen recordings of dashboard/software
- Animated charts/graphs
- Stock footage (relevant to point)
- Product images
- Text overlays with key points
- Client logos/testimonials

**How to Add B-Roll:**
1. Place playhead at jump cut location
2. Drag B-roll to track above (V2)
3. Trim B-roll to cover 1-2 seconds around jump
4. Adjust opacity if needed (usually 100%)

**Option B: Slide Transition**
- If slides change near jump cut, transition naturally
- Make sure slide change feels intentional
- Align audio with slide content

**Option C: Camera Angle Change**
- If you have multiple camera angles, switch angles
- Covers jump cut with intentional camera change
- Requires multi-cam recording setup

**Option D: Zoom/Crop**
- Duplicate video clip
- Zoom in 10-15% on second clip
- Creates "camera push" effect
- Covers jump cut
- Don't overuse (max 2-3 times per VSL)

**How to Zoom in DaVinci:**
1. Select clip
2. Inspector panel (top right)
3. Transform → Zoom: 1.15
4. Adjust Position X/Y to reframe

**Option E: Embrace the Jump**
- For fast-paced, energetic VSLs
- Quick jump cuts can add energy
- Works well for younger audiences
- Use sparingly in B2B VSLs (can look amateurish)

#### Step 3: Add Slide Transitions

**Goal**: Smooth transitions between slide changes

**Preset Transitions (Use Sparingly):**
- Effects Library → Video Transitions → Dissolve
- Drag "Cross Dissolve" between clips
- Duration: 0.5-0.75 seconds (subtle)

**Better Option - Slide Motion:**
1. When slide changes, add slight zoom or pan to slide
2. Creates dynamic feel without cheesy transitions
3. Keyframe slide position/scale

**Slide Motion Example:**
1. Select slide clip at change point
2. Inspector → Transform → Enable keyframes
3. First frame: Zoom 1.0, Position centered
4. Last frame (20 frames later): Zoom 1.05, Position slight left
5. Creates subtle push-in effect

**Best Practice**:
- Most transitions should be straight cuts (immediate)
- Use cross dissolve only when:
  - Time passing
  - Major section change
  - Want softer feel

#### Step 4: Match Audio Levels

**Goal**: Consistent volume throughout, no sudden jumps

**Using Fairlight Page (Audio Tab):**
1. Click "Fairlight" at bottom of Resolve
2. View audio waveforms
3. Identify volume inconsistencies

**Normalize Audio:**
1. Select all audio clips
2. Right-click → Normalize Audio Levels
3. Target: -16 LUFS (for web video)
4. Click Normalize

**Manual Level Adjustment:**
1. Select clip with quiet audio
2. Inspector → Volume: +3dB to +6dB
3. Or drag volume line up in timeline

**Remove Plosives (P/B pops):**
1. Find plosive in waveform (large spike)
2. Zoom in on spike
3. Add keyframe before spike
4. Add keyframe on spike (reduce volume -6dB)
5. Add keyframe after spike
6. Creates volume "dip" only on plosive

**Compression for Even Dynamics:**
1. Select audio track
2. Effects Library → Dynamics → Compressor
3. Settings:
   - Ratio: 3:1
   - Threshold: -20dB
   - Attack: 6ms
   - Release: 60ms
   - Make-up Gain: +4dB

**Save**: Cmd/Ctrl + S

---

### Phase 3: Enhancements (Polish)

**Goal**: Add professional touches that increase credibility

#### Enhancement 1: Opening Title Card

**Why**: Sets professional tone, includes branding

**Create in Canva:**
1. Size: 1920x1080px
2. Background: Brand color or black
3. Text:
   - "[Your Company]"
   - "Presents"
4. Logo: Center or corner
5. Duration: 2-3 seconds
6. Export as PNG or short video

**Add to Timeline:**
1. Drag title card to start of timeline
2. Duration: 2 seconds
3. Add fade in (1 frame) and fade out (12 frames)

**Alternative - Animated Title:**
- Use Fusion page in Resolve
- Or create in After Effects
- Simple fade-in text animation
- Avoid overly flashy (feels dated)

#### Enhancement 2: Lower Third (Name Tag)

**When to Show**:
- First 5-10 seconds of VSL
- When introducing yourself
- Duration: 5-8 seconds

**Create Lower Third:**

**Option A: Canva**
1. Size: 1920x1080px (full frame)
2. Keep bottom 1/3 only (rest transparent)
3. Design:
   - Name: [Your Name]
   - Title: [Founder/CEO, Company]
   - Background: Semi-transparent box or solid bar
   - Colors: Brand colors
4. Export as PNG with transparency

**Option B: DaVinci Resolve Text Tool**
1. Effects Library → Titles → Lower Third
2. Drag to timeline above video (at intro)
3. Inspector → Text:
   - Line 1: Your Name
   - Line 2: Your Title, Company
4. Inspector → Settings:
   - Font: Clean sans-serif (Montserrat, Inter, Helvetica)
   - Size: 48pt (name), 32pt (title)
   - Color: White or brand color
   - Background: None or subtle box

**Placement**:
- Start: 10-15 seconds into VSL (after you introduce yourself)
- Duration: 6-8 seconds
- Fade in: 12 frames
- Fade out: 12 frames

#### Enhancement 3: Text Overlays (Key Points)

**Purpose**: Reinforce key statements, increase retention

**When to Use**:
- Important statistics: "847 Agencies Served"
- Key claims: "3X Your Revenue in 90 Days"
- Bullet points: "Strategy, Implementation, Optimization"
- CTAs: "Book Your Call Below"

**Best Practices**:
- Use sparingly (3-5 times max in 5-min VSL)
- On screen for 3-5 seconds
- Animated entrance (fade or slide in)
- Large, readable font (72-96pt)
- High contrast (white on dark, dark on light)

**Create Text Overlay:**
1. Effects Library → Titles → Text
2. Drag to timeline above video
3. Inspector → Text: Type your text
4. Inspector → Settings:
   - Font: Bold sans-serif
   - Size: 84pt
   - Color: White (or brand color)
   - Stroke: 4px black outline (for readability)
   - Alignment: Center
5. Position center of frame

**Animation:**
1. Select text clip
2. Effects Library → Transitions → Move (Slide In)
3. Duration: 0.3 seconds
4. Hold for 3-4 seconds
5. Fade out: 0.5 seconds

**Example Placement**:
- "We've worked with 847 agencies" → Show "847 Agencies"
- "Our 3-step process" → Show "3-Step Process"
- "Book your call below" → Show "Book Your Call" + arrow down

#### Enhancement 4: Background Music

**Why**: Adds energy, fills silence, professional feel

**Cautions**:
- Music should be QUIET (barely noticeable)
- Never overpower voice (-30dB to -25dB below voice)
- Wrong music ruins VSL (too upbeat, too dramatic)

**Music Selection:**

**For B2B VSLs:**
- Corporate/Inspiring (Artlist, Epidemic Sound)
- Uplifting but not cheesy
- Medium tempo (100-120 BPM)
- Minimal lyrics (preferably instrumental)
- Consistent energy (no dramatic builds)

**Recommended Tracks:**
- Artlist: Search "corporate inspiring background"
- Epidemic Sound: "Ambient Corporate" category
- YouTube Audio Library: "Ambient" genre (free)
- Uppbeat: "Corporate" category (free)

**How to Add:**
1. Import music track
2. Drag to audio track below voice (A2)
3. Trim to match VSL length
4. Fade in (2 seconds) at start
5. Fade out (3 seconds) at end
6. Adjust volume: -28dB (should be barely audible)

**Volume Ducking (Auto-lower music when speaking):**
1. Fairlight page
2. Select music track
3. Effects → Dynamics → Compressor
4. Sidechain: Voice track
5. Settings:
   - Ratio: 10:1
   - Threshold: -30dB
   - Attack: 10ms
   - Release: 200ms
- Music automatically lowers when you speak

**When to Skip Music**:
- Very serious/high-ticket B2B (legal, finance, enterprise)
- Short VSLs (<2 minutes)
- If unsure about music choice (better no music than wrong music)

#### Enhancement 5: B-Roll and Visual Interest

**Purpose**: Maintain visual engagement, illustrate points

**When to Insert B-Roll**:
- During case study mentions (show results, dashboards)
- When discussing process (show screens, steps)
- Over jump cuts (as mentioned earlier)
- During proof sections (client logos, testimonials)
- Long talking sections (break up static camera)

**B-Roll Types:**

**1. Screen Recordings (Screencast)**
- Record dashboard, software, results, analytics
- Shows proof and process
- Use QuickTime (Mac) or OBS (any platform)
- 30-45 seconds max per clip

**2. Stock Footage**
- Pexels.com (free)
- Pixabay.com (free)
- Artgrid.io (paid, high quality)
- Keep it relevant (no random coffee shots)

**3. Motion Graphics**
- Animated charts/graphs
- Kinetic typography (text animation)
- Transitions
- Use After Effects or templates from Envato

**4. Product/Service Screenshots**
- Your offering in action
- Before/after comparisons
- Client results
- Testimonials

**How to Insert B-Roll:**
1. Identify section that needs visual interest
2. Cut main footage at that point (or overlay)
3. Insert B-roll on video track above (V2)
4. Duration: 3-8 seconds per B-roll clip
5. Add subtle cross dissolve (0.3 sec) on edges
6. Ensure audio continues uninterrupted

**B-Roll Pacing**:
- Change every 5-8 seconds (keeps eyes moving)
- Don't overdo (every 10-15 seconds is often enough)
- Let important moments breathe (don't cut away during key proof)

#### Enhancement 6: Color Grading (Advanced)

**Goal**: Consistent, professional color throughout

**Basic Color Correction:**
1. Switch to Color page (bottom of Resolve)
2. Select first clip
3. Adjust:
   - Lift (shadows): Brighten if too dark
   - Gamma (midtones): Overall exposure
   - Gain (highlights): Prevent overexposure
   - Saturation: Slight boost (+5 to +10)

**Automatic Color Balance:**
1. Select clip
2. Color → Auto Color
3. Resolve analyzes and corrects
4. Review and adjust if needed

**Apply Grade to All Clips:**
1. Right-click graded clip
2. "Grab Still" (Alt/Option + S)
3. Select other clips
4. Right-click graded still
5. "Apply Grade"

**Simple "Cinematic" Look:**
1. Color page → Select clip
2. Curves:
   - Slight S-curve (contrast boost)
3. Hue vs Sat:
   - Desaturate oranges slightly
   - Boost blue/teal slightly
4. Subtle (don't overdo - this isn't a Hollywood film)

**When to Skip**: If camera footage looks good, color grading isn't essential for VSL

---

### Phase 4: Audio Enhancement

**Goal**: Crystal-clear, professional audio quality

#### Step 1: Noise Reduction

**If Background Noise Present:**

**Using Fairlight in Resolve:**
1. Fairlight page
2. Select audio clip
3. Effects → Noise Reduction
4. Click "Sample Noise" → Select section where only noise (no voice)
5. Adjust:
   - Noise Reduction: 12-18dB
   - Threshold: -30dB
6. Preview and adjust

**Using Audacity (External):**
1. Export audio from Resolve: File → Export → Audio Only → WAV
2. Open in Audacity
3. Effect → Noise Reduction and Repair → Noise Reduction
4. Select noise sample (silence section)
5. Click "Get Noise Profile"
6. Select entire track (Cmd/Ctrl + A)
7. Effect → Noise Reduction → Apply
8. Settings: Reduction 12dB, Sensitivity 6, Frequency Smoothing 3
9. Export cleaned audio
10. Re-import to Resolve, replace original audio

#### Step 2: EQ (Equalization)

**Goal**: Enhance voice clarity, remove mud

**Standard Voice EQ:**
1. Fairlight page → Audio track
2. Effects → EQ → Parametric EQ
3. Apply these adjustments:
   - **High-pass filter at 80Hz**: Remove low rumble
   - **Cut 200-400Hz (-3dB)**: Remove muddiness
   - **Boost 3-5kHz (+3dB)**: Add presence/clarity
   - **Slight boost 10kHz (+2dB)**: Add air/sparkle

**Preset Alternative:**
- Effects Library → "Voice Over" preset
- Apply and tweak as needed

#### Step 3: De-Esser

**Purpose**: Reduce harsh "S" sounds (sibilance)

**Apply De-Esser:**
1. Fairlight page
2. Effects → De-Esser
3. Settings:
   - Frequency: 6000-8000 Hz (where S sounds live)
   - Threshold: -20dB
   - Ratio: 6:1
4. Play and adjust until S sounds softened

#### Step 4: Final Compressor + Limiter

**For Even, Loud Audio:**

**Compressor (Already applied in Phase 2, verify settings):**
- Ratio: 3:1
- Threshold: -20dB
- Attack: 6ms
- Release: 60ms
- Make-up Gain: +4dB

**Limiter (Prevent Clipping):**
1. Fairlight page
2. Effects → Limiter (after compressor)
3. Settings:
   - Threshold: -1dB
   - Release: 60ms
- Prevents audio from ever exceeding -1dB (no distortion)

#### Step 5: Check Loudness Standards

**Target Loudness for Web Video:**
- **Integrated Loudness**: -16 LUFS (standard for social media, YouTube, web)

**Check Loudness in Resolve:**
1. Fairlight page
2. Meters (right side) → Loudness
3. Play timeline from start
4. Check "Integrated" reading at end
5. Should read -16 LUFS

**If Too Quiet**:
- Add more make-up gain to compressor (+2 to +4dB)
- Or increase track volume

**If Too Loud**:
- Reduce make-up gain or track volume

**Most platforms auto-normalize anyway**, but targeting -16 LUFS ensures consistency.

---

### Phase 5: Final Review & QA

**Goal**: Catch any errors before export

#### Final Review Checklist

**Technical Quality:**
- [ ] Audio clear throughout (no distortion, clipping)
- [ ] Audio levels consistent (no sudden jumps)
- [ ] Video in focus entire time
- [ ] No black frames or glitches
- [ ] All B-roll placed correctly
- [ ] Text overlays readable and timed correctly
- [ ] Lower third appears at right time
- [ ] Background music balanced (not overpowering)
- [ ] Color grade consistent across clips

**Content Quality:**
- [ ] Opening hook grabs attention (first 10 sec)
- [ ] Story flows logically (problem → solution → proof → CTA)
- [ ] Pacing feels dynamic (not too slow or rushed)
- [ ] All key proof points included
- [ ] CTA is crystal clear
- [ ] No awkward long pauses
- [ ] Jump cuts feel natural (or covered with B-roll)
- [ ] Energy consistent (or intentionally varied)

**Length & Timing:**
- [ ] Total length appropriate (3-5 min for VSL funnel, 8-12 min for webinar VSL)
- [ ] No section drags on too long
- [ ] Intro under 30 seconds
- [ ] CTA repeated at end

**Branding:**
- [ ] Logo/company name appears
- [ ] Brand colors present (graphics/text)
- [ ] Professional appearance throughout

#### Get External Feedback

**Before finalizing**, show to:

1. **Teammate/partner**: Fresh eyes catch errors
2. **Target customer (if possible)**: Does messaging resonate?
3. **Non-expert friend**: Is it clear to someone unfamiliar?

**Feedback Questions:**
- Did you stay engaged the whole time?
- What part was confusing (if any)?
- Did the CTA make sense?
- Would you book a call after watching? Why or why not?
- Any technical issues (audio, video, pacing)?

**Iterate if Needed:**
- If 2+ people mention same issue, fix it
- Don't over-obsess on minor details
- Perfect is the enemy of done

---

## Export Settings

### Exporting from DaVinci Resolve

**Step 1: Deliver Page**
1. Click "Deliver" at bottom of Resolve
2. Select "YouTube" preset (best for web)

**Step 2: Customize Settings**

**Format Tab:**
- Format: MP4
- Codec: H.264
- Quality: Automatic (or set bitrate to 15000 Kbps)

**Video Tab:**
- Resolution: 1920x1080
- Frame Rate: 30
- Quality: Restrict to 15000 Kbps

**Audio Tab:**
- Codec: AAC
- Sample Rate: 48000 Hz
- Channels: Stereo
- Bitrate: 256 kbps

**File Tab:**
- Filename: [ProjectName]_VSL_v1.mp4
- Location: Browse to /06_Exports folder

**Step 3: Add to Render Queue**
- Click "Add to Render Queue"

**Step 4: Render**
- Click "Render All"
- Wait for completion (progress bar shows)

**Step 5: Verify Export**
1. Navigate to export folder
2. Play exported video in VLC or QuickTime
3. Check:
   - [ ] Plays smoothly
   - [ ] Audio synced with video
   - [ ] No visual glitches
   - [ ] Quality looks good
   - [ ] Length correct

### Export Presets for Different Uses

**1. High-Quality Master (Archive)**
- Codec: H.264
- Bitrate: 25000 Kbps
- Resolution: 1920x1080
- Use: Master backup, can re-encode later

**2. Web/Landing Page Optimized (Primary)**
- Codec: H.264
- Bitrate: 10000-15000 Kbps
- Resolution: 1920x1080
- Use: Upload to Vimeo, YouTube, Wistia for embedding

**3. Social Media (Optional)**
- Codec: H.264
- Bitrate: 8000 Kbps
- Resolution: 1080x1920 (9:16 for stories) or 1080x1080 (1:1 for feed)
- Use: Instagram, Facebook, LinkedIn feed posts

**4. Low-Bandwidth Version (Optional)**
- Codec: H.264
- Bitrate: 5000 Kbps
- Resolution: 1280x720 (720p)
- Use: Email attachments, slow connections, secondary backup

### File Naming Convention

```
[ProjectName]_VSL_[Version]_[Date]_[Variant].mp4

Examples:
- AAA_VSL_v1_2025-01-20_Master.mp4
- AAA_VSL_v2_2025-01-22_WebOptimized.mp4
- AAA_VSL_v2_2025-01-22_9x16_Social.mp4
- AAA_VSL_FINAL_2025-01-25.mp4
```

---

## Advanced Editing Techniques

### Multi-Camera Editing

**If you recorded from multiple angles:**

1. **Sync Cameras:**
   - Import all camera angles
   - Right-click in timeline → "Auto-Sync Audio"
   - Resolve aligns all angles by audio waveform

2. **Multi-Cam Clip:**
   - Right-click synced clips → "Create New Multicam Clip"
   - Name it "VSL Multi-Cam"

3. **Cut Between Angles:**
   - Double-click multi-cam clip to open
   - Play through and press 1, 2, 3 keys to switch between Camera 1, 2, 3
   - Creates dynamic cutting between angles
   - Keeps viewer engaged

**When to Cut:**
- Wide shot: Intro, CTA, big statements
- Medium shot: Main content delivery (most of video)
- Close-up: Emotional moments, key proof points

### Animated Text and Graphics (Fusion)

**DaVinci Resolve Fusion Page** = Built-in motion graphics

**Simple Animated Lower Third:**
1. Fusion page → Create new Fusion composition
2. Add "Text+" node
3. Add "Transform" node
4. Keyframe position: Starts off-screen left → Animates to position → Holds → Animates off right
5. Export as compound clip
6. Use in timeline

**Or Use Templates:**
- Envato Elements: Download Fusion title templates
- Import into Resolve
- Customize text and colors

### Green Screen Background Replacement

**If recorded on green screen:**

1. Add camera footage to timeline
2. Effects Library → OpenFX → Color → 3D Keyer
3. Drag onto clip
4. Select green color with eyedropper
5. Adjust "Matte Finesse" settings until green removed
6. Add background image/video below camera layer
7. Can be: Office background, logo wall, motion graphics

**Tip**: Requires good green screen lighting for clean key

### Captions and Subtitles (Critical for Social)

**Why Add Captions:**
- 85% of social videos watched without sound
- Increases watch time
- Accessibility
- Helps SEO

**Auto-Generate Captions in DaVinci Resolve:**
1. Timeline → Right-click clip → "Transcribe Audio"
2. Language: English
3. Click "Transcribe"
4. Resolve auto-generates subtitles
5. Review and fix errors (always has some)
6. Export:
   - Subtitle → Export → SRT file
   - Or burn-in to video (Timeline → Subtitles → "Create Captions Track")

**Or Use External Tools:**
- **Rev.com**: Manual transcription ($1.50/min) - most accurate
- **Otter.ai**: Auto transcription - good accuracy
- **Descript**: Transcription + video editing in one
- **Kapwing**: Free auto-captions (online)

**Burned-in Caption Style (Social Media):**
- Large font (72-96pt)
- Bold, sans-serif
- Yellow or white
- Black stroke/outline
- 2-3 words at a time
- Centered on screen

### Sound Effects (Subtle)

**When to Add SFX:**
- Whoosh: On text animation entrance
- Pop: When stat/number appears
- Click: On button/CTA appearance
- Ambient: Very subtle background ambience

**Where to Find SFX:**
- Epidemic Sound (subscription)
- Artlist (subscription)
- Freesound.org (free, Creative Commons)
- YouTube Audio Library (free)

**How to Add:**
1. Import SFX
2. Place on audio track (A3)
3. Trim to exact moment (e.g., text appears)
4. Volume: -20dB to -15dB (subtle, not overpowering)

**Caution**: Don't overdo. B2B VSLs should be clean, not gimmicky.

---

## Optimization for Different Platforms

### Landing Page VSL (Primary Use Case)

**Best Practices:**
- **Length**: 3-5 minutes (absolute max 8 minutes)
- **Format**: 16:9 (landscape)
- **Quality**: 1080p, 10-15 Mbps
- **Hosting**: Vimeo Pro, Wistia, or YouTube (unlisted)
- **Settings**:
  - Autoplay: Yes (if platform allows)
  - Controls: Minimal (hide if possible)
  - Loop: No
  - Related videos: None (if YouTube, use embed API to hide)

**Vimeo Embed Code (Recommended):**
```html
<iframe src="https://player.vimeo.com/video/YOUR_VIDEO_ID?autoplay=1&loop=0&autopause=0&muted=0&title=0&byline=0&portrait=0"
  width="1280" height="720" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>
```

**Settings Breakdown:**
- `autoplay=1`: Starts playing immediately
- `title=0&byline=0&portrait=0`: Hides Vimeo branding
- `loop=0`: Don't replay (want them to CTA)
- `muted=0`: Audio on (unless required by browser policy)

**Wistia Advantages:**
- Best analytics (heatmaps showing drop-off)
- Email capture gates
- CTAs within video
- A/B testing
- Worth $79/mo if running paid traffic

### Social Media Adaptation

**LinkedIn (Organic Posts):**
- **Length**: 1-2 minutes (attention span shorter)
- **Format**: 16:9 or 1:1 (square)
- **Captions**: Burned-in (most watch muted)
- **Hook**: First 3 seconds MUST stop scroll
- **CTA**: Comment for link (platform favors engagement)

**Instagram Feed:**
- **Length**: 60-90 seconds max
- **Format**: 1:1 (square) or 4:5 (vertical)
- **Captions**: Burned-in
- **Hook**: First 1-2 seconds
- **CTA**: Link in bio

**Instagram Stories/Reels:**
- **Length**: 15-60 seconds
- **Format**: 9:16 (vertical)
- **Captions**: Large, centered
- **Edit**: Fast-paced jump cuts
- **Hook**: Immediate (0.5 seconds)

**YouTube:**
- **Length**: 3-8 minutes (can be longer)
- **Format**: 16:9
- **Thumbnail**: Custom, eye-catching (create in Canva)
- **Title**: SEO-optimized with keywords
- **Description**: Full context, timestamps, links
- **End screen**: Channel subscribe, related video

**Facebook:**
- **Length**: 1-3 minutes
- **Format**: 1:1 (square) performs best
- **Captions**: Burned-in (90% muted viewing)
- **Upload native**: Don't share YouTube link

### Email VSL

**Different from Landing Page VSL:**
- Shorter: 2-3 minutes max (lower commitment)
- Faster hook: 5 seconds to grab attention
- Often: Thumbnail with play button (not autoplay)
- CTA: Clear next step (reply, book call, click link)

**Hosting**: Use Vimeo/Wistia/Loom, embed video thumbnail in email that links to full video on landing page or Loom share link.

---

## VSL Editing Best Practices Summary

### Do's:
✅ **Prioritize audio quality** over video quality
✅ **Tighten pacing** - Remove unnecessary pauses
✅ **Use B-roll** to cover jump cuts and add visual interest
✅ **Add subtle background music** (-28dB, barely noticeable)
✅ **Include proof elements** - Show results, testimonials, logos
✅ **Reinforce key points** with text overlays (sparingly)
✅ **Test on target audience** before finalizing
✅ **Keep it authentic** - Minor imperfections are humanizing
✅ **Optimize for platform** - Different cuts for landing page vs social
✅ **Include clear CTA** - Tell them exactly what to do next

### Don'ts:
❌ **Over-edit** - Don't make it feel sterile or overly produced
❌ **Use cheesy effects** - No spinning transitions, lens flares, etc.
❌ **Make it too long** - Every minute past 5 min, drop-off increases
❌ **Hide your face** - People buy from people, show yourself
❌ **Use distracting music** - Should be barely audible
❌ **Skip audio enhancement** - Bad audio = instant credibility loss
❌ **Forget captions** - Essential for social, helpful for accessibility
❌ **Use template intros** - Generic intros scream "cheap"
❌ **Leave in major mistakes** - Stumbles and "ums" hurt credibility
❌ **Ignore analytics** - Watch drop-off data, optimize accordingly

---

## Post-Production Workflow Summary

**Estimated Time Investment:**

| Phase | Time (5-min VSL) | Priority |
|-------|------------------|----------|
| Pre-Edit Prep | 30 min | Critical |
| Assembly Edit | 1 hour | Critical |
| Fine Cut | 2 hours | Critical |
| Enhancements | 1-2 hours | High |
| Audio Polish | 1 hour | High |
| Final Review | 30 min | Critical |
| Export & Upload | 30 min | Critical |
| **TOTAL** | **6-8 hours** | — |

**First VSL may take 10-15 hours** as you learn. Each subsequent VSL gets faster.

---

## Analytics and Iteration

**After Publishing, Track:**

**Vimeo/Wistia Analytics:**
- **Play rate**: % of page visitors who press play
- **Engagement graph**: Where people drop off
- **Conversion rate**: Play → CTA click

**Key Metrics:**
- Play rate >60% = Good
- Average watch time >50% = Good
- CTA click rate 5-15% = Good (for B2B VSL funnel)

**Optimization Based on Data:**

**If drop-off in first 10 seconds:**
- Hook isn't strong enough
- Re-cut intro to be more compelling
- Test different opening line

**If drop-off around 2-3 min mark:**
- VSL too long, losing attention
- Cut out slower sections
- Increase pacing

**If high watch rate but low CTA clicks:**
- CTA not clear enough
- Add stronger urgency
- Test different CTA wording

**A/B Test:**
- Create 2 versions with different hooks
- 50% traffic to each
- Measure which converts better

---

## Software & Resources

### Essential Tools
- **DaVinci Resolve** (Free): Primary editing software
- **Canva Pro** ($12.99/mo): Graphics, thumbnails, lower thirds
- **Audacity** (Free): Audio cleanup
- **Handbrake** (Free): Video compression/conversion

### Stock Assets
- **Stock Video**: Pexels, Pixabay (free), Artgrid (paid)
- **Music**: Artlist, Epidemic Sound, YouTube Audio Library
- **Sound Effects**: Freesound.org, Epidemic Sound
- **Fonts**: Google Fonts (free), Adobe Fonts (with CC)

### Video Hosting
- **Vimeo Pro** ($20/mo): Clean, professional, good analytics
- **Wistia** ($79/mo): Best analytics, built for marketing
- **YouTube** (Free): Unlisted option, good for testing
- **Loom** ($12.50/mo): Quick video messages, email VSLs

### Learning Resources
- **DaVinci Resolve Training**: blackmagicdesign.com/products/davinciresolve/training
- **Casey Faris (YouTube)**: DaVinci Resolve tutorials
- **Film Editing Pro**: Pacing and storytelling techniques

---

## Troubleshooting Common Issues

### Issue: Choppy Playback in Timeline

**Cause**: High-resolution footage, computer can't handle real-time playback

**Solution**:
1. Playback → Proxy Mode → Half Resolution
2. Or: Generate optimized media (right-click clip → Generate Optimized Media)
3. Edit with optimized, export with original quality

### Issue: Audio/Video Out of Sync

**Cause**: Frame rate mismatch or dropped frames

**Solution**:
1. Right-click clip → Synchronize Clips → Audio
2. Or manually adjust: Inspector → Retime → Speed (adjust by 0.1% until synced)
3. Prevent: Always record at consistent frame rate (30fps)

### Issue: Exported Video Looks Worse Than Timeline

**Cause**: Export settings too compressed

**Solution**:
1. Increase bitrate to 15000-20000 Kbps
2. Use H.264 High Profile codec
3. Disable hardware encoding if artifacts present

### Issue: Colors Look Different After Export

**Cause**: Color space mismatch

**Solution**:
1. Project Settings → Color Management → Rec.709
2. Deliver page → Video → Data Levels: Auto
3. Test export on multiple devices/browsers

---

## Related Skills
- write_vsl_script.md (create compelling script first)
- record_vsl.md (capture high-quality raw footage)
- design_sales_funnel_structure.md (where VSL fits in funnel)
- optimize_vsl_performance.md (analyze and improve conversions)

---

## Final Notes

**Philosophy**: Your VSL editing should enhance your message, not overshadow it. The goal is to remove distractions (mistakes, bad audio, poor pacing) while maintaining authenticity.

**First VSL**: Won't be perfect. Ship it, gather data, improve the next one.

**Iteration**: Every VSL you edit teaches you something. Document what works, refine your process.

**Investment**: Spending 8 hours editing a VSL that generates $50K+ in revenue is time well spent.

---

**Training References:**
- `/trainings/Website & VSL/VSL (Advanced)/`
  - #8- Setting Up OBS To Record Your VSL.srt
  - Finished VSL Example #1-3.srt (study editing techniques)
  - BONUS- Behind The Scenes Of A High End VSL Production.srt

**Version**: 1.0
**Last Updated**: 2025-01-19
**Created By**: Claude Sonnet 4.5
**Based On**: Antigravity Agents VSL Training + Industry Best Practices
