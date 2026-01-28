#!/usr/bin/env python3
"""
Hybrid Jump Cut Editor

1. FFmpeg silence detection (fast) to find gaps
2. Whisper transcription to snap cuts to word boundaries
3. FFmpeg to concatenate kept segments

Usage:
    python execution/jump_cut_editor.py input.mp4 output.mp4
    python execution/jump_cut_editor.py input.mp4 output.mp4 --silence-thresh -35 --min-silence 0.4
"""

import subprocess
import json
import re
import sys
import tempfile
import os
from pathlib import Path

# Configurable parameters
SILENCE_THRESH_DB = -30  # dB threshold for silence detection
MIN_SILENCE_DURATION = 0.5  # Minimum silence duration to cut (seconds)
PADDING_MS = 100  # Padding around speech segments (milliseconds)
WHISPER_MODEL = "base"  # tiny, base, small, medium, large
MIN_SEGMENT_DURATION = 1.0  # Minimum segment length - shorter ones get merged


def run_cmd(cmd: list, capture=True) -> str:
    """Run a command and return output."""
    print(f"  → {' '.join(cmd[:5])}...")
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if result.returncode != 0 and capture:
        print(f"Error: {result.stderr}")
    return result.stdout if capture else ""


def detect_silences(input_path: str, thresh_db: float, min_duration: float) -> list[tuple[float, float]]:
    """
    Use FFmpeg to detect silent segments.
    Returns list of (start, end) tuples for SILENT regions.
    """
    print(f"🔇 Detecting silences (threshold={thresh_db}dB, min={min_duration}s)...")

    cmd = [
        "ffmpeg", "-i", input_path,
        "-af", f"silencedetect=n={thresh_db}dB:d={min_duration}",
        "-f", "null", "-"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stderr  # FFmpeg outputs to stderr

    # Parse silence_start and silence_end from output
    silences = []
    starts = re.findall(r"silence_start: ([\d.]+)", output)
    ends = re.findall(r"silence_end: ([\d.]+)", output)

    for start, end in zip(starts, ends):
        silences.append((float(start), float(end)))

    print(f"   Found {len(silences)} silent regions")
    return silences


def get_speech_segments(duration: float, silences: list[tuple[float, float]], padding_s: float) -> list[tuple[float, float]]:
    """
    Convert silence regions to speech regions (inverse).
    Add padding around speech.
    """
    if not silences:
        return [(0, duration)]

    speech = []
    prev_end = 0

    for silence_start, silence_end in silences:
        if silence_start > prev_end:
            # Speech segment before this silence
            start = max(0, prev_end - padding_s)
            end = min(duration, silence_start + padding_s)
            speech.append((start, end))
        prev_end = silence_end

    # Final segment after last silence
    if prev_end < duration:
        start = max(0, prev_end - padding_s)
        speech.append((start, duration))

    # Merge overlapping segments
    merged = merge_overlapping(speech)

    return merged


def merge_overlapping(segments: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Merge overlapping or adjacent segments."""
    if not segments:
        return []

    merged = []
    for seg in sorted(segments):
        if merged and seg[0] <= merged[-1][1]:
            # Overlapping - extend the previous segment
            merged[-1] = (merged[-1][0], max(merged[-1][1], seg[1]))
        else:
            merged.append(seg)

    return merged


def merge_short_segments(segments: list[tuple[float, float]], min_duration: float) -> list[tuple[float, float]]:
    """
    Merge segments shorter than min_duration with their neighbors.
    This prevents tiny fragments from being created (like 0.46s intro pieces).
    """
    if not segments or len(segments) <= 1:
        return segments

    result = []
    i = 0

    while i < len(segments):
        start, end = segments[i]
        duration = end - start

        # If segment is too short and there's a next segment, merge with next
        if duration < min_duration and i + 1 < len(segments):
            # Extend to include next segment (bridge the gap)
            next_start, next_end = segments[i + 1]
            result.append((start, next_end))
            i += 2  # Skip the next segment since we merged it
        else:
            result.append((start, end))
            i += 1

    # Run merge_overlapping to clean up any overlaps created
    return merge_overlapping(result)


def transcribe_segment(input_path: str, start: float, end: float) -> list[dict]:
    """
    Transcribe a segment with Whisper to get word-level timestamps.
    Returns list of {word, start, end} dicts.
    """
    import whisper

    # Extract audio segment to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        cmd = [
            "ffmpeg", "-y", "-ss", str(start), "-i", input_path,
            "-t", str(end - start), "-vn", "-ar", "16000", "-ac", "1", tmp_path
        ]
        subprocess.run(cmd, capture_output=True)

        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(tmp_path, word_timestamps=True)

        words = []
        for segment in result.get("segments", []):
            for word_info in segment.get("words", []):
                words.append({
                    "word": word_info["word"],
                    "start": start + word_info["start"],  # Adjust to absolute time
                    "end": start + word_info["end"]
                })
        return words
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def snap_to_word_boundaries(segments: list[tuple[float, float]], input_path: str, model_name: str = "base") -> list[tuple[float, float]]:
    """
    Use Whisper to snap segment boundaries to word boundaries.
    Only transcribes ~1s around each cut point.
    """
    print(f"🎯 Snapping cuts to word boundaries with Whisper ({model_name})...")

    import whisper
    model = whisper.load_model(model_name)

    snapped = []

    for i, (seg_start, seg_end) in enumerate(segments):
        print(f"   Segment {i+1}/{len(segments)}: {seg_start:.2f}s - {seg_end:.2f}s")

        # Transcribe around the start boundary (expand window by 1s each side)
        window_start = max(0, seg_start - 1)
        window_end = seg_start + 1

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            cmd = [
                "ffmpeg", "-y", "-ss", str(window_start), "-i", input_path,
                "-t", str(window_end - window_start), "-vn", "-ar", "16000", "-ac", "1",
                "-loglevel", "error", tmp_path
            ]
            subprocess.run(cmd, capture_output=True)

            result = model.transcribe(tmp_path, word_timestamps=True)

            # For segment START: snap to word START (beginning of speech)
            # We want to start at the beginning of a word, not mid-word
            best_start = seg_start
            min_dist = float('inf')

            for segment in result.get("segments", []):
                for word_info in segment.get("words", []):
                    word_start = window_start + word_info["start"]

                    # Only consider word STARTS for segment start boundary
                    dist = abs(word_start - seg_start)
                    if dist < min_dist:
                        min_dist = dist
                        best_start = word_start

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Similar for end boundary
        window_start = seg_end - 1
        window_end = seg_end + 1

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            cmd = [
                "ffmpeg", "-y", "-ss", str(max(0, window_start)), "-i", input_path,
                "-t", str(window_end - window_start), "-vn", "-ar", "16000", "-ac", "1",
                "-loglevel", "error", tmp_path
            ]
            subprocess.run(cmd, capture_output=True)

            result = model.transcribe(tmp_path, word_timestamps=True)

            # For segment END: find the word END closest to seg_end
            # Then add a buffer to ensure we don't clip the word
            WORD_END_BUFFER = 0.20  # 200ms buffer after word end
            best_end = seg_end
            min_dist = float('inf')

            for segment in result.get("segments", []):
                for word_info in segment.get("words", []):
                    word_end = max(0, window_start) + word_info["end"]
                    dist = abs(word_end - seg_end)
                    if dist < min_dist:
                        min_dist = dist
                        best_end = word_end

            # Add buffer to prevent clipping
            best_end = best_end + WORD_END_BUFFER
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        snapped.append((best_start, best_end))

    # Merge any overlapping segments created by snapping
    return merge_overlapping(snapped)


def concatenate_segments(input_path: str, segments: list[tuple[float, float]], output_path: str):
    """
    Use FFmpeg to extract and concatenate segments.
    """
    print(f"✂️  Concatenating {len(segments)} segments...")

    with tempfile.TemporaryDirectory() as tmpdir:
        segment_files = []

        # Extract each segment (re-encode for frame-accurate cuts)
        for i, (start, end) in enumerate(segments):
            seg_path = os.path.join(tmpdir, f"seg_{i:04d}.mp4")
            duration = end - start

            # Put -ss AFTER -i for frame-accurate seeking (slower but precise)
            cmd = [
                "ffmpeg", "-y",
                "-i", input_path,
                "-ss", str(start),
                "-t", str(duration),
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k",
                "-loglevel", "error", seg_path
            ]
            subprocess.run(cmd, capture_output=True)
            segment_files.append(seg_path)

        # Create concat file
        concat_path = os.path.join(tmpdir, "concat.txt")
        with open(concat_path, "w") as f:
            for seg_path in segment_files:
                f.write(f"file '{seg_path}'\n")

        # Concatenate
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_path,
            "-c", "copy", "-loglevel", "error", output_path
        ]
        subprocess.run(cmd, capture_output=True)

    print(f"✅ Output saved to {output_path}")


def get_duration(input_path: str) -> float:
    """Get video duration in seconds."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", input_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Hybrid jump cut editor")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output video file")
    parser.add_argument("--silence-thresh", type=float, default=SILENCE_THRESH_DB,
                        help=f"Silence threshold in dB (default: {SILENCE_THRESH_DB})")
    parser.add_argument("--min-silence", type=float, default=MIN_SILENCE_DURATION,
                        help=f"Minimum silence duration in seconds (default: {MIN_SILENCE_DURATION})")
    parser.add_argument("--padding", type=int, default=PADDING_MS,
                        help=f"Padding around speech in ms (default: {PADDING_MS})")
    parser.add_argument("--no-whisper", action="store_true",
                        help="Skip Whisper alignment (faster but less precise)")
    parser.add_argument("--whisper-model", default=WHISPER_MODEL,
                        help=f"Whisper model size (default: {WHISPER_MODEL})")
    parser.add_argument("--min-segment", type=float, default=MIN_SEGMENT_DURATION,
                        help=f"Minimum segment duration - shorter ones merged (default: {MIN_SEGMENT_DURATION}s)")

    args = parser.parse_args()

    whisper_model = args.whisper_model

    input_path = args.input
    output_path = args.output

    print(f"🎬 Jump Cut Editor")
    print(f"   Input: {input_path}")
    print(f"   Output: {output_path}")
    print()

    # Step 1: Get duration
    duration = get_duration(input_path)
    print(f"📏 Video duration: {duration:.2f}s")

    # Step 2: Detect silences
    silences = detect_silences(input_path, args.silence_thresh, args.min_silence)

    # Step 3: Get speech segments
    padding_s = args.padding / 1000
    speech_segments = get_speech_segments(duration, silences, padding_s)
    print(f"🗣️  Found {len(speech_segments)} speech segments")

    # Step 3b: Merge short segments to prevent fragmentation
    speech_segments = merge_short_segments(speech_segments, args.min_segment)
    print(f"📎 After merging short segments: {len(speech_segments)} segments")

    # Step 4: Snap to word boundaries (optional)
    if not args.no_whisper and len(speech_segments) > 1:
        speech_segments = snap_to_word_boundaries(speech_segments, input_path, whisper_model)

    # Step 5: Concatenate
    concatenate_segments(input_path, speech_segments, output_path)

    # Stats
    original_duration = duration
    new_duration = get_duration(output_path)
    removed = original_duration - new_duration
    print()
    print(f"📊 Stats:")
    print(f"   Original: {original_duration:.2f}s")
    print(f"   New: {new_duration:.2f}s")
    print(f"   Removed: {removed:.2f}s ({100*removed/original_duration:.1f}%)")


if __name__ == "__main__":
    main()
