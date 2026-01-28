# 3D Pan Transition Effect

Create fast-forward "preview" style transitions with subtle 3D rotation, similar to Premiere Pro's Basic 3D effect. Used for intros, scene transitions, or "coming up" previews.

## Execution Script

`execution/pan_3d_transition.py`

---

## Quick Start

```bash
# Basic 1-second transition (uses tuned defaults)
python3 execution/pan_3d_transition.py input.mp4 output.mp4

# 5-second transition with background image
python3 execution/pan_3d_transition.py input.mp4 output.mp4 \
    --output-duration 5 \
    --bg-image .tmp/background.png

# Custom 3D effect parameters
python3 execution/pan_3d_transition.py input.mp4 output.mp4 \
    --swivel-start 5 --swivel-end -5 \
    --tilt-start 2 --tilt-end 2 \
    --speed 10
```

---

## What It Does

1. **Extracts frames** from source video at native FPS
2. **Applies 3D CSS transforms** (rotateY, rotateX, scale) via Remotion
3. **Fast-forwards playback** (default 7x speed)
4. **Renders final video** at source resolution/FPS

The effect creates a subtle "floating card" look where the video appears to rotate in 3D space while playing at high speed.

---

## CLI Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `input` | required | Input video file path |
| `output` | required | Output video file path |
| `--start` | 0 | Start time in source video (seconds) |
| `--source-duration` | auto | Duration of source to use (auto = output-duration × speed) |
| `--output-duration` | 1.0 | Final output duration (seconds) |
| `--swivel-start` | 3.5 | Starting Y-axis rotation (degrees, positive = left side closer) |
| `--swivel-end` | -3.5 | Ending Y-axis rotation (degrees, negative = right side closer) |
| `--tilt-start` | 1.7 | Starting X-axis rotation (degrees, positive = top tilted back) |
| `--tilt-end` | 1.7 | Ending X-axis rotation (constant = no tilt animation) |
| `--perspective` | 1000 | 3D perspective depth (lower = more dramatic) |
| `--speed` | 7 | Playback speed multiplier (7 = 700% speed) |
| `--easing` | linear | Animation easing: `linear`, `easeOut`, `easeInOut`, `spring` |
| `--bg-color` | #2d3436 | Background color (hex) when video edges are visible |
| `--bg-image` | none | Background image path (overrides --bg-color) |

---

## Tuned Default Values

These defaults were calibrated for subtle, professional-looking transitions:

```python
SWIVEL: 3.5° → -3.5°    # Gentle left-to-right rotation
TILT: 1.7° (constant)    # Slight upward tilt, no animation
ZOOM: 1.5% out           # Hardcoded in render (scale 0.985)
SPEED: 7x                # Fast but readable
EASING: linear           # Smooth, predictable motion
```

### Parameter Tuning Guide

| Effect | Parameter | Range | Notes |
|--------|-----------|-------|-------|
| More dramatic rotation | `--swivel-start/end` | ±5-15° | Keep symmetric (e.g., 10 → -10) |
| Subtle rotation | `--swivel-start/end` | ±2-4° | Current default is 3.5° |
| Constant tilt | `--tilt-start` = `--tilt-end` | 1-3° | No tilt animation |
| Tilt animation | Different start/end | 0-5° | Tilts during playback |
| Faster preview | `--speed` | 10-15 | For longer source content |
| Slower, readable | `--speed` | 3-5 | For shorter clips |
| Bouncy feel | `--easing spring` | - | Overshoots then settles |
| Smooth deceleration | `--easing easeOut` | - | Fast start, slow end |

---

## Background Options

### Solid Color (default)
```bash
python3 execution/pan_3d_transition.py input.mp4 output.mp4 --bg-color "#1a1a2e"
```

### Background Image
```bash
python3 execution/pan_3d_transition.py input.mp4 output.mp4 --bg-image .tmp/bg.png
```

The background is visible at the edges when the video rotates in 3D space. Use an image that complements your content (nature scenes, abstract textures, etc.).

---

## Performance

| Resolution | Output Duration | Render Time |
|------------|-----------------|-------------|
| 4K 60fps | 1 second | ~15-20s |
| 4K 60fps | 5 seconds | ~80s |
| 1080p 30fps | 1 second | ~5-8s |
| 1080p 30fps | 5 seconds | ~25-30s |

**Bottlenecks:**
1. FFmpeg frame extraction (disk I/O + decoding)
2. Remotion rendering (3D transforms on each frame)

---

## Technical Details

### How It Works

1. **FFmpeg** extracts JPEG frames from source video segment
2. Frames are copied to Remotion's `public/frames/` directory
3. **Remotion** (React-based video renderer) generates a dynamic composition:
   - CSS `perspective` for 3D depth
   - CSS `transform: rotateY() rotateX() scale()` for 3D effect
   - Frame interpolation based on playback rate
4. Remotion renders final MP4 at source resolution/FPS
5. Temp frames are cleaned up

### CSS Transform Order

```css
transform: translateY(0%) rotateY(Xdeg) rotateX(Ydeg) scale(0.985)
```

- `translateY`: Vertical offset (currently 0)
- `rotateY`: Swivel (left/right rotation)
- `rotateX`: Tilt (up/down rotation)
- `scale`: Zoom (0.985 = 1.5% zoom out)

### Easing Functions

| Type | Behavior |
|------|----------|
| `linear` | Constant speed throughout |
| `easeOut` | Fast start, gradual slowdown |
| `easeInOut` | Slow start, fast middle, slow end |
| `spring` | Overshoots target, bounces back |

---

## Dependencies

### System Requirements
```bash
brew install ffmpeg node  # macOS
```

### Remotion Setup (one-time)
```bash
cd execution/video_effects
npm install
```

The script uses `npx remotion render` which handles Remotion execution.

---

## Example Workflow

### Creating an Intro Transition

```bash
# 1. Place source video in .tmp/
cp ~/Desktop/my_video.mp4 .tmp/source.mp4

# 2. Generate 3-second intro transition
python3 execution/pan_3d_transition.py \
    .tmp/source.mp4 \
    .tmp/intro_transition.mp4 \
    --output-duration 3 \
    --bg-image .tmp/background.jpg \
    --easing easeOut

# 3. Preview result
open .tmp/intro_transition.mp4
```

### Creating a "Coming Up" Preview

```bash
# Start 2 minutes into the video, create 5-second preview
python3 execution/pan_3d_transition.py \
    .tmp/full_video.mp4 \
    .tmp/coming_up.mp4 \
    --start 120 \
    --output-duration 5 \
    --speed 10
```

---

## Troubleshooting

### Remotion render fails
```
Render error: Cannot find module 'remotion'
```
**Fix:** Run `npm install` in `execution/video_effects/`

### Video looks too zoomed out
The zoom is hardcoded at 1.5% (scale 0.985). To change, edit `pan_3d_transition.py` line ~196:
```python
const scaleVal = 0.985; // Change this value
```

### Background image not showing
- Ensure image path is correct and file exists
- Supported formats: PNG, JPG, JPEG
- Image is copied to Remotion's public folder during render

### Render is slow
- Lower resolution source = faster render
- Shorter output duration = fewer frames
- The 4K 60fps source extracts 2100 frames for a 5s transition at 7x speed

---

## Output

- **Deliverable:** Video file at specified output path
- **Format:** MP4 (H.264)
- **Resolution:** Matches source video
- **FPS:** Matches source video

---

## Related Tool: Insert Swivel Teaser

Use `execution/insert_3d_transition.py` to insert a **swivel teaser** into an existing video. The swivel teaser shows content **starting at 1 minute** (by default) compressed into a short preview with 3D rotation effects, while preserving original audio throughout.

```bash
# Insert 5-second swivel teaser at 3 seconds (previews from 1:00 to end)
python3 execution/insert_3d_transition.py input.mp4 output.mp4

# With background image
python3 execution/insert_3d_transition.py input.mp4 output.mp4 \
    --bg-image .tmp/background.png

# Custom teaser content start point (preview from 1:30 onwards)
python3 execution/insert_3d_transition.py input.mp4 output.mp4 \
    --teaser-start 90 --bg-image .tmp/background.png
```

**CLI Arguments:**

| Argument | Default | Description |
|----------|---------|-------------|
| `--insert-at` | 3.0 | Where to insert teaser in timeline (seconds) |
| `--duration` | 5.0 | Teaser duration (seconds) |
| `--teaser-start` | 60.0 | Where to start sourcing teaser content (seconds) |
| `--bg-color` | #2d3436 | Background color (hex) |
| `--bg-image` | none | Background image path |

**Timeline Result:**
```
Video: [0-3s original] [3-8s swivel teaser] [8s+ original]
Audio: [original audio plays continuously throughout]
```

**Example:** For a 6-minute video:
- Teaser content: 60s → 360s (300 seconds)
- Teaser duration: 5 seconds
- Playback speed: 60x (automatically calculated)
- Result: Content from 1:00 onwards previewed in 5-second swivel teaser

**Why start at 1 minute?** The first minute typically contains intro/branding that doesn't make for interesting preview content. Starting at 1 minute shows the "meat" of the video in the teaser.
