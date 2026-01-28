#!/usr/bin/env python3
"""
Parse VTT subtitle files and extract clean transcript text.
"""

import os
import re
import sys
from pathlib import Path


def parse_vtt(vtt_path: str) -> str:
    """Parse a VTT file and return clean transcript text."""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove VTT header
    lines = content.split('\n')
    
    # Skip header lines (WEBVTT, Kind:, Language:, etc.)
    text_lines = []
    skip_next = False
    seen_text = set()  # Deduplicate repeated lines
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines, timestamps, and header
        if not line:
            continue
        if line.startswith('WEBVTT'):
            continue
        if line.startswith('Kind:') or line.startswith('Language:'):
            continue
        if re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3}', line):
            continue
        if re.match(r'^\d+$', line):
            continue
        if '-->' in line:
            continue
        
        # Remove VTT formatting tags
        line = re.sub(r'<[^>]+>', '', line)
        line = re.sub(r'\[.*?\]', '', line)  # Remove [Music] etc.
        
        # Clean up whitespace
        line = ' '.join(line.split())
        
        if line and line not in seen_text:
            # YouTube auto-captions often repeat, keep unique sentences
            seen_text.add(line)
            text_lines.append(line)
    
    # Join into paragraphs (group every ~10 sentences)
    paragraphs = []
    current = []
    
    for line in text_lines:
        current.append(line)
        # New paragraph after sentence-ending punctuation
        if len(current) >= 10 or (line.endswith(('.', '!', '?')) and len(current) >= 5):
            paragraphs.append(' '.join(current))
            current = []
    
    if current:
        paragraphs.append(' '.join(current))
    
    return '\n\n'.join(paragraphs)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse VTT subtitle files and extract clean transcript text")
    parser.add_argument("vtt_file", nargs="?", help="VTT file to parse")
    parser.add_argument("--output", "-o", help="Output file path (prints to stdout if not specified)")
    args = parser.parse_args()
    
    if not args.vtt_file:
        parser.print_help()
        sys.exit(1)
    
    vtt_path = args.vtt_file
    output_path = args.output
    
    if not os.path.exists(vtt_path):
        print(f"Error: File not found: {vtt_path}")
        sys.exit(1)
    
    transcript = parse_vtt(vtt_path)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"Transcript saved to {output_path}")
    else:
        print(transcript)


if __name__ == "__main__":
    main()
