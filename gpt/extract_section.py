import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Define your project root
project_root = "/Users/gencsaracaydin/marker-pdf-parser"
env_path = os.path.join(project_root, '.env')

# Check if .env file exists (just for verification)
if os.path.exists(env_path):
    print(f".env file found at: {env_path}")
else:
    print(f"[ERROR] .env file not found at: {env_path}")
    print("This is unusual since you confirmed it exists with nano.")
    print("Check if the path is correct.")
    sys.exit(1)

# Load environment variables
print("Loading environment variables...")
load_dotenv(env_path)

# Get API key from environment variable (and print a masked version for verification)
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    # Mask the API key for security when printing
    masked_key = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "****"
    print(f"API key loaded successfully: {masked_key}")
else:
    print("[ERROR] OPENAI_API_KEY environment variable not set in .env file.")
    print("Your .env file should contain a line like: OPENAI_API_KEY=sk-your-key-here")
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

if __name__ == "__main__":
    print("Running extract_section.py...")
    file_path = "/Users/gencsaracaydin/Documents/protocol_outputs1/CAM4-14-e70726/CAM4-14-e70726.md"
    
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
