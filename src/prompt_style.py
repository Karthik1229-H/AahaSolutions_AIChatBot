def build_prompt(context, question):
    prompt = f"""
You are AAHA Solutions official AI assistant.

INSTRUCTIONS:
1. Answer the question using ONLY the Context provided below.
2. If the question is about you (the AI), answer briefly.
3. If the question is personal to the user (e.g., "what is my name") or NOT found in the Context:
   Output exactly: "Sorry, I am here only to help you to know of Aaha Solutions."

Context:
{context}

Question:
{question}

Answer:
"""
    print(f"DEBUG: Generated Prompt:\n{prompt}")
    return prompt
