#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./parse.sh <PDF_FILE_OR_FOLDER>"
  exit 1
fi

INPUT_PATH=$1
OUTPUT_DIR="protocol_outputs"

# Activate the virtual environment
source venv/bin/activate

# Check if input is a file or directory
if [ -f "$INPUT_PATH" ]; then
  # It's a file - create a temporary directory
  echo "[1/2] Parsing single PDF to markdown..."
  TEMP_DIR="temp_pdf_dir"
  mkdir -p $TEMP_DIR
  
  # Copy the PDF to the temporary directory
  cp "$INPUT_PATH" "$TEMP_DIR/"
  
  # Parse the PDF
  ulimit -n 4096
  marker "$TEMP_DIR" --workers 5 --output_dir ./$OUTPUT_DIR --output_format markdown
  
  # Clean up
  rm -rf "$TEMP_DIR"
else
  # It's a directory
  echo "[1/2] Parsing all PDFs in directory to markdown..."
  
  # Parse the PDFs
  ulimit -n 4096
  marker "$INPUT_PATH" --workers 5 --output_dir ./$OUTPUT_DIR --output_format markdown
fi

echo "[✔] Parsing complete. Outputs saved in $OUTPUT_DIR/"

echo "[2/2] Extracting procedures using GPT..."
mkdir -p outputs

# Find all markdown files in the output directory
find ./$OUTPUT_DIR -name "*.md" | while read markdown_file; do
  echo "Processing $markdown_file"
  
  # Run the protocol extraction script on each markdown file
  python3 gpt/extract_section.py "$markdown_file"
done

echo "[✔] Extraction complete. Outputs saved in outputs/"
