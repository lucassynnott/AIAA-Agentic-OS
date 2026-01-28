#!/usr/bin/env python3
"""
Insert Swivel Teaser into Video

Inserts a "swivel teaser" at a specified point in a video - a fast-forward
preview of video content starting at 1 minute with 3D rotation effects.
Original audio continues playing throughout.

See: directives/pan_3d_transition.md for effect parameters.

Usage:
    # Insert 5-second swivel teaser at 3 seconds (previews from 1:00 to end)
    python execution/insert_3d_transition.py input.mp4 output.mp4

    # Custom teaser content start point
    python execution/insert_3d_transition.py input.mp4 output.mp4 \
        --teaser-start 90  # Preview starts at 1:30

    # With background image
    python execution/insert_3d_transition.py input.mp4 output.mp4 \
        --bg-image .tmp/background.png

Timeline Result:
    Video: [0-3s original] [3-8s swivel teaser showing content from 1:00 onwards] [8s+ original]
    Audio: [original audio plays continuously throughout]
"""

import subprocess
import tempfile
import os
import argparse
import json
import sys
from pathlib import Path

# Add execution directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the transition creator
from pan_3d_transition import create_transition, get_video_info
# Import hardware encoding functions
from jump_cut_vad import get_cached_encoder_args

DEFAULT_INSERT_AT = 3.0    # Insert transition at 3 seconds
DEFAULT_DURATION = 5.0     # 5-second transition
DEFAULT_TEASER_START = 60.0  # Teaser content starts at 1 minute
MAX_PLAYBACK_RATE = 100.0  # Cap teaser speed at 100x for readability


def composite_with_transition(
    input_path: str,
    output_path: str,
    insert_at: float = DEFAULT_INSERT_AT,
    duration: float = DEFAULT_DURATION,
    teaser_start: float = DEFAULT_TEASER_START,
    bg_color: str = "#2d3436",
    bg_image: str = None,
) -> None:
    """
    Insert a swivel teaser into video while preserving original audio.

    The swivel teaser shows video content from teaser_start to end,
    compressed into the specified duration with 3D rotation effects.

    Args:
        input_path: Source video file
        output_path: Output video file
        insert_at: Where to insert teaser in timeline (seconds)
        duration: Teaser duration (seconds)
        teaser_start: Where to start sourcing teaser content (seconds, default 60)
        bg_color: Background color for teaser
        bg_image: Optional background image for teaser
    """
    # Get video info
    info = get_video_info(input_path)
    total_duration = info["duration"]

    # Validate teaser_start
    if teaser_start >= total_duration:
        raise ValueError(f"Teaser start ({teaser_start}s) must be less than video duration ({total_duration}s)")

    # Calculate content to preview (from teaser_start to end)
    # Cap playback rate at MAX_PLAYBACK_RATE for readability
    available_content = total_duration - teaser_start
    uncapped_rate = available_content / duration

    if uncapped_rate > MAX_PLAYBACK_RATE:
        # Cap at max speed, take only as much content as fits
        playback_rate = MAX_PLAYBACK_RATE
        teaser_content = duration * MAX_PLAYBACK_RATE  # e.g., 5s × 100x = 500s of content
        print(f"   ⚠️  Capping speed at {MAX_PLAYBACK_RATE}x (would have been {uncapped_rate:.1f}x)")
    else:
        playback_rate = uncapped_rate
        teaser_content = available_content

    print(f"🎬 Insert Swivel Teaser")
    print(f"   Input: {input_path}")
    print(f"   Insert at: {insert_at}s")
    print(f"   Teaser duration: {duration}s")
    print(f"   Teaser content: {teaser_start}s → {total_duration:.1f}s ({teaser_content:.1f}s at {playback_rate:.1f}x speed)")
    print()

    if insert_at + duration > total_duration:
        raise ValueError(f"Insert point + duration ({insert_at + duration}s) exceeds video duration ({total_duration}s)")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Step 1: Generate the swivel teaser (content from teaser_start to end)
        transition_path = os.path.join(tmpdir, "transition.mp4")
        print(f"📐 Generating swivel teaser...")

        create_transition(
            input_path=input_path,
            output_path=transition_path,
            start=teaser_start,  # Start sourcing from teaser_start (default 60s)
            source_duration=teaser_content,  # Content from teaser_start to end
            output_duration=duration,
            playback_rate=playback_rate,  # Calculated to fit all content
            bg_color=bg_color,
            bg_image=bg_image,
        )

        # Step 2: Extract segments from original video (video only)
        print(f"\n✂️  Extracting video segments...")

        # Get encoder args (hardware if available)
        encoder_args = get_cached_encoder_args()

        # Segment 1: 0 to insert_at
        seg1_path = os.path.join(tmpdir, "seg1.mp4")
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-t", str(insert_at),
            "-an",  # No audio
        ] + encoder_args + [
            "-loglevel", "error",
            seg1_path
        ]
        subprocess.run(cmd, check=True)
        print(f"   Segment 1: 0s - {insert_at}s")

        # Segment 2 is the transition (already has no audio from Remotion)
        # But we need to ensure it's in the right format
        seg2_path = os.path.join(tmpdir, "seg2.mp4")
        cmd = [
            "ffmpeg", "-y", "-i", transition_path,
            "-an",  # No audio
        ] + encoder_args + [
            "-loglevel", "error",
            seg2_path
        ]
        subprocess.run(cmd, check=True)
        print(f"   Segment 2: transition ({duration}s)")

        # Segment 3: insert_at + duration to end
        seg3_path = os.path.join(tmpdir, "seg3.mp4")
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-ss", str(insert_at + duration),
            "-an",  # No audio
        ] + encoder_args + [
            "-loglevel", "error",
            seg3_path
        ]
        subprocess.run(cmd, check=True)
        remaining = total_duration - (insert_at + duration)
        print(f"   Segment 3: {insert_at + duration}s - end ({remaining:.1f}s)")

        # Step 3: Concatenate video segments
        print(f"\n🔗 Concatenating video segments...")
        concat_video_path = os.path.join(tmpdir, "concat_video.mp4")

        concat_list = os.path.join(tmpdir, "concat.txt")
        with open(concat_list, "w") as f:
            f.write(f"file '{seg1_path}'\n")
            f.write(f"file '{seg2_path}'\n")
            f.write(f"file '{seg3_path}'\n")

        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy",  # Stream copy since segments are already encoded
            "-loglevel", "error",
            concat_video_path
        ]
        subprocess.run(cmd, check=True)

        # Step 4: Extract original audio
        print(f"🎵 Extracting original audio...")
        audio_path = os.path.join(tmpdir, "audio.aac")
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-vn", "-c:a", "aac", "-b:a", "192k",
            "-loglevel", "error",
            audio_path
        ]
        subprocess.run(cmd, check=True)

        # Step 5: Merge video and audio
        print(f"🎞️  Merging video and audio...")
        cmd = [
            "ffmpeg", "-y",
            "-i", concat_video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "copy",
            "-shortest",  # In case of tiny duration mismatches
            "-loglevel", "error",
            output_path
        ]
        subprocess.run(cmd, check=True)

    print(f"\n✅ Output saved to {output_path}")
    print(f"   Timeline: [0-{insert_at}s] [swivel teaser {duration}s] [{insert_at+duration}s-end]")
    print(f"   Teaser shows: {teaser_start}s → {total_duration:.1f}s ({teaser_content:.1f}s at {playback_rate:.1f}x speed)")
    print(f"   Audio: Original audio preserved throughout")


def main():
    parser = argparse.ArgumentParser(
        description="Insert 3D transition into video while preserving audio"
    )
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output video file")
    parser.add_argument("--insert-at", type=float, default=DEFAULT_INSERT_AT,
                        help=f"Insert point in seconds (default: {DEFAULT_INSERT_AT})")
    parser.add_argument("--duration", type=float, default=DEFAULT_DURATION,
                        help=f"Transition duration in seconds (default: {DEFAULT_DURATION})")
    parser.add_argument("--teaser-start", type=float, default=DEFAULT_TEASER_START,
                        help=f"Where to start sourcing teaser content (default: {DEFAULT_TEASER_START}s = 1 minute)")
    parser.add_argument("--bg-color", type=str, default="#2d3436",
                        help="Background color (hex, default: #2d3436)")
    parser.add_argument("--bg-image", type=str, default=None,
                        help="Background image path (overrides --bg-color)")

    args = parser.parse_args()

    composite_with_transition(
        input_path=args.input,
        output_path=args.output,
        insert_at=args.insert_at,
        duration=args.duration,
        teaser_start=args.teaser_start,
        bg_color=args.bg_color,
        bg_image=args.bg_image,
    )


if __name__ == "__main__":
    main()
