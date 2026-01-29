import streamlit as st
import os
from .vector_store import build_index
from .generate_questions import generate_questions

UPLOAD_DIR = "data/uploads"

def admin_panel():
    st.subheader("📂 Manage Company Files")

    replace_existing = st.checkbox("Replace existing knowledge base", value=True)
    
    files = st.file_uploader(
        "Upload PDFs", type="pdf", accept_multiple_files=True
    )

    if files:
        if st.button("Process Uploads"):
            if replace_existing:
                # Clear existing files
                for f in os.listdir(UPLOAD_DIR):
                    os.remove(os.path.join(UPLOAD_DIR, f))
                st.info("Cleared existing knowledge base.")

            for f in files:
                with open(os.path.join(UPLOAD_DIR, f.name), "wb") as out:
                    out.write(f.read())
            
            with st.spinner("Building Index..."):
                build_index()
            
            # Use a separate spinner or just status
            with st.spinner("Generating Suggested Questions..."):
                generate_questions()
            
            st.success("Files uploaded, indexed, and questions updated!")

    st.divider()
    st.subheader("Existing Files")

    for file in os.listdir(UPLOAD_DIR):
        col1, col2 = st.columns([4, 1])
        col1.write(file)
        if col2.button("❌ Delete", key=file):
            os.remove(os.path.join(UPLOAD_DIR, file))
            build_index()
            st.warning(f"{file} deleted")
            st.rerun()
