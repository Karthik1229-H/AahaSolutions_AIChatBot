from langchain_ollama import ChatOllama
from .vector_store import search_docs
from .prompt_style import build_prompt

llm = ChatOllama(
    model="phi3:mini",
    temperature=0,
    num_ctx=4096
)

def ask_company(question):
    docs = search_docs(question)
    context = "\n\n".join(d.page_content[:800] for d in docs)
    prompt = build_prompt(context, question)
    return llm.invoke(prompt).content, context

def generate_followups(answer, context):
    print(f"DEBUG: Context length for followups: {len(context)}")
    print(f"DEBUG: Context snippet: {context[:200]}...")
    
    prompt = f"""
You are a helpful assistant. Use the following context to generate 3 relevant follow-up questions.
The questions must be answerable using ONLY the information in the context.
OUTPUT FORMAT:
- Return ONLY the questions.
- Do NOT include the answer or explanation.
- Do NOT include numbering or bullets.
- Each question should be short (under 15 words).

Context:
{context}

Answer:
{answer}

Generate 3 questions now:
"""
    res = llm.invoke(prompt).content
    print(f"DEBUG: Raw LLM Response for followups: {res}")
    return [q.strip("-• ") for q in res.split("\n") if q.strip()][:3]
