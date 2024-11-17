import streamlit as st
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):
    if email in st.session_state.users:
        return "Email already registered."
    st.session_state.users[email] = {"username": username, "password": hash_password(password)}
    return "Registration successful."


def login_user(email, password):
    if email in st.session_state.users:
        user = st.session_state.users[email]
        if user["password"] == hash_password(password):
            return True, user["username"]
    return False, None
