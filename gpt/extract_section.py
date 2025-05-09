import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import datetime

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

def call_chatgpt(prompt_text):
    try:
        # Try using gpt-4o-mini first
        print("Attempting to use gpt-4o-mini...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that processes research papers."},
                {"role": "user", "content": prompt_text}
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
                    {"role": "system", "content": "You are a helpful assistant that processes research papers."},
                    {"role": "user", "content": prompt_text}
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
    with open(file_path, "r") as f:
        content = f.read()
    
    print(f"File read successfully. Content length: {len(content)} characters")
    prompt = f"Here's the content of a research paper:\n\n{content}\n\nExtract the PROCEDURE section."
    
    print("Calling OpenAI API...")
    result = call_chatgpt(prompt)
    
    print("\n[GPT-4 OUTPUT]\n")
    print(result)
    
    # Save the output to a file
    saved_file = save_output(result, file_path)
    print(f"Results have been saved to: {saved_file}")
