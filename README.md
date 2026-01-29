# AAHA Solutions AI Assistant

An intelligent, RAG-based chatbot designed to answer questions about AAHA Solutions using strictly controlled context from uploaded documents.

## 🚀 Features

- **Retrieval Augmented Generation (RAG)**: Answers questions based *only* on the PDFs uploaded to its Knowledge Base.
- **Strict Fallback**: If a question is not covered by the documents or is personal/irrelevant, the bot politely refuses with a standard message.
- **Admin Panel**: Secure interface (`/admin`) to upload, view, and manage knowledge base files.
- **Dynamic Suggestions**:
    - **Suggested Questions**: Automatically generated from your specific uploaded content.
    - **Related Questions**: Context-aware follow-up suggestions appear after every answer.
- **Visual Cleanup**: Suggestions and buttons are visually removed during processing for a clean chat experience.

## 🛠️ Prerequisites

1.  **Python 3.8+**
2.  **Ollama**: This project uses a local LLM via Ollama.
    - Install Ollama from [ollama.com](https://ollama.com).
    - Pull the model: `ollama pull phi3:mini`

## 📦 Installation

1.  Clone the repository or download the source code.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Running the Application

Run the Streamlit app:
```bash
streamlit run app.py
```
The application will open in your default browser (usually at `http://localhost:8501`).

## 📚 User Guide

### Chat Interface
- Type your question in the input box.
- Click on "Suggested Questions" to get started quickly.
- View "Suggested Questions" (Follow-ups) below answers to dive deeper.

### Admin Panel
1.  Navigate to the **Admin** section via the sidebar (Select "Admin" in the Menu).
2.  **Login**: Use the configured credentials.
3.  **Upload Files**:
    - Upload one or more PDF files.
    - **Replace existing knowledge base**: Check this box if you want to clear old files and strictly use the new ones.
4.  Click **Process Uploads**.
    - The system will index the files and auto-generate new Suggested Questions.

## ⚙️ Configuration
- **LLM Model**: Configured in `hybrid_engine.py` (default: `phi3:mini`).
- **Data Storage**: Uploads are stored in `data/uploads`. Vector index in `data/faiss_index`.

## 📂 Project Structure
- `app.py`: Main application entry point & UI logic.
- `admin.py`: Admin interface logic.
- `hybrid_engine.py`: Core RAG and LLM interaction logic.
- `vector_store.py`: FAISS vector database management.
- `generate_questions.py`: Logic for auto-generating suggestions.
- `prompt_style.py`: Centralized system prompts.
