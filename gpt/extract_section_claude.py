def call_claude(content, title):
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
        print("Calling Claude for extraction...")
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8000,
            temperature=0.2,
            system="You are a helpful assistant that extracts EXACT textual content from research papers. Your task is to identify and extract procedure sections verbatim, not to summarize them.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error with Claude: {e}")
        return f"Error with Claude extraction: {e}"
