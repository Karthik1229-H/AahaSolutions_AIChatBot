import json
import os
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader

UPLOAD_DIR = "data/uploads"
OUTPUT_FILE = "suggested_questions.json"

llm = ChatOllama(
    model="phi3:mini",
    temperature=0.2, # Slight creativity for questions
    num_ctx=2048
)

def generate_questions():
    """
    Reads PDFs from uploads, summarizes content, and asks LLM to generate 4 questions.
    """
    print("Generating suggested questions from uploads...")
    
    # 1. Read Content
    context = ""
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".pdf")]
    
    if not files:
        print("No files found to generate questions from.")
        return

    # Limit to first few pages of first few files to fit context window
    # Simple strategy: Read first page of first 3 files
    for f in files[:3]:
        try:
            loader = PyPDFLoader(os.path.join(UPLOAD_DIR, f))
            pages = loader.load()
            if pages:
                context += pages[0].page_content + "\n\n"
        except Exception as e:
            print(f"Error reading {f}: {e}")

    if not context.strip():
        print("No text extracted.")
        return

    # 2. Prompt LLM
    prompt = f"""
    Analyze the following text and generate 4 short, relevant questions that a user might ask a chatbot about this content.
    Return ONLY a JSON list of strings, like ["Question 1", "Question 2", "Question 3", "Question 4"].
    
    IMPORTANT: The questions must be derivable ONLY from the provided text. Do not use outside knowledge.

    Text:
    {context[:3000]} # Limit context
    """

    try:
        response = llm.invoke(prompt).content
        # Basic cleanup to find JSON list in response
        # Phi3 might output text around it, so let's try to extract list
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end != -1:
            json_str = response[start:end]
            questions = json.loads(json_str)
            
            # 3. Save to JSON
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(questions[:4], f, indent=4)
            print(f"Generated questions: {questions[:4]}")
        else:
            print("Could not parse JSON from LLM response.")
            print(response)

    except Exception as e:
        print(f"Error generating questions: {e}")

if __name__ == "__main__":
    generate_questions()
