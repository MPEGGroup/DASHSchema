#!/bin/bash

# Check if an input file is provided
if [ -z "$1" ]; then
  echo "Usage: ./xml2rtf.sh <input_file.xml>"
  exit 1
fi

INPUT_FILE="$1"
# Create an output filename (e.g., data.xml -> data.rtf)
OUTPUT_FILE="${INPUT_FILE%.*}.rtf"

# Check if 'highlight' is installed
if ! command -v highlight &> /dev/null; then
    echo "Error: 'highlight' is not installed."
    echo "Please run: brew install highlight"
    exit 1
fi

echo "Converting $INPUT_FILE to $OUTPUT_FILE..."

# 1. xmllint --format: Indents and pretty-prints the XML
# 2. highlight: Converts to RTF with B&W styling
#    --syntax=xml: Tells the tool it is processing XML
#    --out-format=rtf: Sets output to Rich Text
#    --style=bw: Uses the built-in Black & White theme (Bold/Italic only)
#    --font="Courier New": Sets a monospaced font
#    --font-size=24: Sets font size (approx 12pt in RTF context)

xmllint --format "$INPUT_FILE" | \
highlight --syntax=xml \
          --out-format=rtf \
          --style=print \
          --font="Courier New" \
          --font-size=9 \
          > "$OUTPUT_FILE"

echo "Done! Saved to $OUTPUT_FILE"
