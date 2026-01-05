#!/bin/bash
DIR="/Users/lucasnolan/Documents/Work/Client Ascension/AI Development/Agentic Workflows/.tmp/transcripts"
mkdir -p "$DIR"

# Video IDs from Jeremy Haynes channel
videos=(
"rL1FIHwg8PE"
"5sVIMTVkDQ8"
"NKOHsR9nVEM"
"GKGFpHcuvLQ"
"WTrl_dZsLBM"
"7h3jmz6ED9M"
"gBO8-F8hdPA"
"VHM6WLc-quY"
"tZot4E4BnSg"
"LoJ-_DD-ND4"
"eZ2u4giDkvY"
"biOjWH8eJXU"
"SjWRcRug7u4"
"R_YwdxNxcWI"
"K7ESFkNPrrs"
"Z5LG8QtpBTs"
"mYgAZqmtd8g"
"uaBCF8HvEew"
"Rim2s-WFwYg"
"0KKL9NZvSeo"
)

for vid in "${videos[@]}"; do
    if [ ! -f "$DIR/${vid}.en.vtt" ]; then
        echo "Downloading: $vid"
        yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "$DIR/%(id)s" "https://www.youtube.com/watch?v=$vid" 2>/dev/null
        sleep 1
    else
        echo "Already exists: $vid"
    fi
done
