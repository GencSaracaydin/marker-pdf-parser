def call_chatgpt(content, title):
    # Modified prompt with explicit instructions to extract verbatim text
    prompt = f"""I have a research paper titled "{title}". I need to extract the EXACT TEXT of the Procedure/Methods part of the research paper (may come in different names like inside methodology, methods, experimental procedures, etc.).

IMPORTANT INSTRUCTIONS:
1. Extract the EXACT ORIGINAL TEXT verbatim, not a summary or overview
2. Include ALL procedural details exactly as written in the paper
3. If procedures are scattered across multiple sections (e.g., in Results and Methods), extract ALL of those sections completely
4. Include any tables, figures, footnotes related to procedures
5. Use markdown formatting to preserve the structure
6. DO NOT summarize or paraphrase - I need the exact text from the paper
7. If a procedure is mentioned across various sections, extract all those sections completely

Only if there is absolutely no procedural information in the paper, respond with: "The paper titled '{title}' does not include any procedure or methodology information."

Here's the content of the paper:

{content}"""

    try:
        # Try using gpt-4o-mini first
        print("Attempting to use gpt-4o-mini...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts EXACT textual content from research papers. Your task is to identify and extract procedure sections verbatim, not to summarize them."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=10000  # Increased to 10k tokens as requested
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
                    {"role": "system", "content": "You are a helpful assistant that extracts EXACT textual content from research papers. Your task is to identify and extract procedure sections verbatim, not to summarize them."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=10000  # Increased to 10k tokens as requested
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with fallback model: {e}"
