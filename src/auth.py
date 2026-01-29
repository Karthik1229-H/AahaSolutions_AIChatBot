import streamlit as st

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def admin_login():
    if "admin_logged" not in st.session_state:
        st.session_state.admin_logged = False

    if not st.session_state.admin_logged:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == ADMIN_USER and pwd == ADMIN_PASS:
                st.session_state.admin_logged = True
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")
        return False

    return True
