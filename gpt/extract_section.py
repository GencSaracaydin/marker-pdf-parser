import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import datetime
import re

# Load environment variables
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("[ERROR] OPENAI_API_KEY environment variable not set.")
    print("Please check your .env file or set it in your environment.")
    sys.exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def call_chatgpt(content, title):
    # Improved prompt with more explicit instructions
    prompt = f"""I have a research paper. The filename suggests it might be titled "{title}". I need to extract the Procedure part of the research paper (may come in different names like inside methodology etc.). If that part includes tables, footnotes, or any other non-normal text type I need to extract it as well. 

I am planning to extract it as a markdown file, you can use markdown table style for the needed parts and if there is contextual overflow into close subsections you can include the transition sentence as well. Handle footnotes in line please.

IMPORTANT: Before responding, thoroughly scan the entire document to identify any procedure, methods, methodology, experimental setup, or protocol sections. Look carefully for sections that describe how the research was conducted, even if they're not explicitly labeled as "procedure".

If there is no procedure or similar section after thoroughly scanning the entire document, just respond with: "The paper does not include a procedure or methodology section."

Here's the content of the paper:

{content}"""

    try:
        # Try using gpt-4o-mini first
        print("Attempting to use gpt-4o-mini...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in extracting procedural information from scientific papers. You carefully examine the entire document before responding."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with gpt-4o-mini: {e}")
        
        # Fall back to gpt-3.5-turbo if gpt-4o-mini fails
        print("Falling back to gpt-3.5-turbo...")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant specialized in extracting procedural information from scientific papers. You carefully examine the entire document before responding."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with fallback model: {e}"

def save_output(result, input_file_path):
    # Extract filename without extension and parent directory name
    parent_dir = os.path.basename(os.path.dirname(input_file_path))
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join("/Users/gencsaracaydin/marker-pdf-parser/outputs", parent_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Create timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output file path
    output_file = os.path.join(output_dir, f"{file_name}_procedure_{timestamp}.md")
    
    # Write the result to the file
    with open(output_file, "w") as f:
        f.write(result)
    
    print(f"Output saved to: {output_file}")
    return output_file

def extract_title(file_path):
    # Get the base filename without extension as a fallback title
    base_title = os.path.splitext(os.path.basename(file_path))[0]
    return base_title

if __name__ == "__main__":
    print("Running extract_section.py...")
    
    # Check if a file path was provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python3 extract_section.py <path_to_markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        exit(1)
    
    print(f"Reading file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if content is too short or seems invalid
        if len(content) < 100 or content.strip().startswith("![]"):
            print("[WARNING] File content appears to be very short or invalid.")
            print(f"First 200 characters: {content[:200]}")
            
            # Try reading the file again with different encoding
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
            print(f"Retried reading with different encoding. Content length: {len(content)} characters")
    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")
        exit(1)
    
    # Use filename as title
    title = extract_title(file_path)
    print(f"Using title from filename: {title}")
    
    print(f"File read successfully. Content length: {len(content)} characters")
    
    print("Calling OpenAI API...")
    result = call_chatgpt(content, title)
    
    print("\n[GPT-4 OUTPUT]\n")
    print(result)
    
    # Save the output to a file
    saved_file = save_output(result, file_path)
    print(f"Results have been saved to: {saved_file}")
