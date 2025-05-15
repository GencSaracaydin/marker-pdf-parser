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
  echo "[1/3] Parsing single PDF to markdown..."
  TEMP_DIR="temp_pdf_dir_$(date +%s)"  # Add timestamp to avoid conflicts
  mkdir -p $TEMP_DIR
  
  # Copy the PDF to the temporary directory
  cp "$INPUT_PATH" "$TEMP_DIR/"
  PDF_FILENAME=$(basename "$INPUT_PATH")
  
  # Parse the PDF
  ulimit -n 4096
  marker "$TEMP_DIR" --workers 5 --output_dir ./$OUTPUT_DIR --output_format markdown
  
  echo "[✔] Parsing complete. Outputs saved in $OUTPUT_DIR/"
  
  echo "[2/3] Extracting procedures using LLMs..."
  mkdir -p outputs
  
  # Find the markdown file corresponding to our input PDF
  PDF_BASENAME=$(basename "$PDF_FILENAME" .pdf)
  echo "Looking for markdown files matching: $PDF_BASENAME"
  MARKDOWN_FILES=$(find ./$OUTPUT_DIR -name "$PDF_BASENAME*.md")
  
  if [ -z "$MARKDOWN_FILES" ]; then
    echo "[ERROR] No markdown files found for $PDF_BASENAME"
    exit 1
  fi
  
  for MARKDOWN_FILE in $MARKDOWN_FILES; do
    echo "Processing with GPT: $MARKDOWN_FILE"
    # Run the GPT extraction script on the markdown file
    python3 gpt/extract_section.py "$MARKDOWN_FILE"
    
    echo "Processing with Claude: $MARKDOWN_FILE"
    # Run the Claude extraction script on the markdown file
    python3 gpt/extract_section_claude.py "$MARKDOWN_FILE"
  done
  
  # Clean up
  rm -rf "$TEMP_DIR"
else
  # It's a directory
  echo "[1/3] Parsing all PDFs in directory to markdown..."
  
  # Parse the PDFs
  ulimit -n 4096
  marker "$INPUT_PATH" --workers 5 --output_dir ./$OUTPUT_DIR --output_format markdown
  
  echo "[✔] Parsing complete. Outputs saved in $OUTPUT_DIR/"
  
  echo "[2/3] Extracting procedures using LLMs..."
  mkdir -p outputs
  
  # Find all markdown files in the output directory
  find ./$OUTPUT_DIR -name "*.md" | while read markdown_file; do
    echo "Processing with GPT: $markdown_file"
    # Run the GPT extraction script on each markdown file
    python3 gpt/extract_section.py "$markdown_file"
    
    echo "Processing with Claude: $markdown_file"
    # Run the Claude extraction script on each markdown file
    python3 gpt/extract_section_claude.py "$markdown_file"
  done
fi

echo "[3/3] LLM extractions complete..."
echo "All extractions complete. GPT and Claude outputs saved in outputs/ directory"
echo "[✔] Process complete. Check the outputs directory for results."
