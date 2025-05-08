#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./parse.sh <PDF_FOLDER>"
  exit 1
fi

PDF_FOLDER=$1
OUTPUT_DIR="protocol_outputs"

source venv/bin/activate

cd "$PDF_FOLDER"
find . -name ".DS_Store" -delete
cd ..

ulimit -n 4096
marker "./$PDF_FOLDER" --workers 5 --output_dir ./$OUTPUT_DIR --output_format markdown

echo "[✔] Parsing complete. Outputs saved in $OUTPUT_DIR/"

