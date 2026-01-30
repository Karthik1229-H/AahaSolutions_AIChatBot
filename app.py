import streamlit as st
import time
from src.hybrid_engine import ask_company, generate_followups
from src.admin import admin_panel
from src.auth import admin_login
from src.mailer import send_email
from src.whatsapp import whatsapp_link


st.set_page_config(page_title="AAHA AI Assistant", page_icon="🤖")
st.write("✅ App started successfully")

# ---------------- CSS ----------------
st.markdown("""
<style>
.chat-box { background:#f5f5f5; padding:15px; border-radius:10px; }
.user-msg {
    background:#dcf8c6; padding:10px; border-radius:12px;
    margin:5px 0; text-align:right;
}
.bot-msg {
    background:#ffffff; padding:10px; border-radius:12px;
    margin:5px 0; border:1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hello! This is AAHA AI Assistant. I am here to help you know of AAHA Solutions."}
    ]
if "followups" not in st.session_state:
    st.session_state.followups = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False

def chat_callback(q):
    """Callback to append user message and trigger processing"""
    if q == "Other":
        st.session_state.show_form = True
    else:
        st.session_state.messages.append({"role": "user", "text": q})
        # We clear followups immediately so they disappear while thinking
        st.session_state.followups = []

def cancel_form_callback():
    st.session_state.show_form = False

menu = st.sidebar.selectbox("Menu", ["Chat", "Admin"])
# WhatsApp link removed from sidebar as per request for moving it to main chat
# st.sidebar.link_button("💬 Chat on WhatsApp", whatsapp_link())

# ================= CHAT =================
if menu == "Chat":
    # --- FORM VIEW ---
    if st.session_state.show_form:
        st.markdown("## 📝 Submit your requirement")
        with st.form("requirement_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            requirement = st.text_area("Requirement")
            
            c1, c2 = st.columns([1, 1])
            submitted = c1.form_submit_button("Submit")
            cancelled = c2.form_submit_button("Cancel", on_click=cancel_form_callback)

            if submitted:
                if name and email and requirement:
                    try:
                        send_email(name, email, phone, requirement)
                        st.success("✅ Requirement submitted successfully!")
                        time.sleep(2)
                        st.session_state.show_form = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to send email: {e}")
                else:
                    st.error("Please fill in Name, Email, and Requirement.")
            
            if cancelled:
                st.session_state.show_form = False
                st.rerun()

    # --- CHAT VIEW ---
    else:
        c_title, c_wa = st.columns([3, 1])
        c_title.markdown("## 🤖 AAHA Solutions AI Assistant")
        c_wa.link_button(" WhatsApp", whatsapp_link())

        # --- 1. DISPLAY CHAT HISTORY ---
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-msg">{msg["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-msg">{msg["text"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- 2. SUGGESTED QUESTIONS (Only if no USER messages yet) ---
        has_user_messages = any(m["role"] == "user" for m in st.session_state.messages)
        
        # Use a placeholder to ensure we can clear this section cleanly
        suggestions_placeholder = st.empty()
        
        if not has_user_messages:
            with suggestions_placeholder.container():
                st.markdown("### ✨ Suggested Questions")
                # Load dynamic questions if available
                import json
                import os
                
                questions = []
                if os.path.exists("suggested_questions.json"):
                    try:
                        with open("suggested_questions.json", "r", encoding="utf-8") as f:
                            questions = json.load(f)
                    except:
                        pass
                
                # Fallback if no file or loading failed
                if not questions:
                    questions = [
                        "What is AAHA Solutions?",
                        "Do you offer AI services?",
                        "Does AAHA Solutions offer internships?",
                        "Where is the India office located?"
                    ]
                
                # Use columns for a better layout
                cols = st.columns(2)
                for i, q in enumerate(questions):
                    # Ensure we don't crash if we have fewer than 4 or odd number
                    if cols[i % 2].button(q, use_container_width=True, on_click=chat_callback, args=(q,)):
                        pass 
                
                # Other option
                if st.button("Other", use_container_width=True, on_click=chat_callback, args=("Other",)):
                    pass
        else:
            suggestions_placeholder.empty()

        # --- 3. PROCESSING LOGIC ---
        # Check if the last message is from USER. If so, generate BOT response.
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            user_text = st.session_state.messages[-1]["text"]
            
            # 1. Check Cache for Instant Answer -> DISABLED to ensure fresh answers from new uploads
            # if user_text in FAQ_CACHE: ... (removed)
            
            # 2. Always use LLM/RAG
            with st.spinner("Thinking..."):
                answer, context = ask_company(user_text)
                # For custom questions, we WANT dynamic follow-ups
                new_followups = generate_followups(answer, context)
                
                if "Other" not in new_followups:
                    new_followups.append("Other")
            
            st.session_state.messages.append({"role": "bot", "text": answer})
            st.session_state.followups = new_followups
            st.rerun()

        # --- 4. FOLLOW-UP QUESTIONS (Only if we are NOT processing AND we have user history) ---
        # We check that the last message is NOT user (i.e., we are idle) AND interaction has started
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "bot" and has_user_messages:
            current_followups = st.session_state.followups
            
            # Ensure "Other" is available in Related Questions logic
            # We append it fresh every time we render this block
            display_options = current_followups + [] if current_followups else ["Other"]

            if display_options:
                st.markdown("### ✨ Suggested Questions")
                # Using columns for followups too
                fcols = st.columns(len(display_options))
                for i, fq in enumerate(display_options):
                    # Ensure unique keys for buttons
                    # Use length of messages + index for unique key
                    if fcols[i].button(fq, key=f"fq_{len(st.session_state.messages)}_{i}", use_container_width=True, on_click=chat_callback, args=(fq,)):
                        pass

        # --- 5. CHAT INPUT ---
        if user_input := st.chat_input("Type a message..."):
            chat_callback(user_input)
            st.rerun()

# ================= ADMIN =================
else:
    if admin_login():
        admin_panel()

