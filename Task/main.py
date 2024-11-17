import os
import streamlit as st
from pdf_chatbot import load_document, chunk_data, Create_Embedding_VectorDB, ask_and_get_answer
from LogIn import login_user, register_user, hash_password

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize session state for users and chat history
if "users" not in st.session_state:
    st.session_state.users = {}  # To store registered users {email: {"username": str, "password": hashed_password}}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  


if not st.session_state.authenticated:
    st.title("Welcome to Pdf ChatBot App")
    st.subheader("Please select an option to continue")

    option = st.radio("Choose an option:", ("Register", "Login"))

    if option == "Register":
        st.header("Register")
        with st.form("register_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register_button = st.form_submit_button("Register")

            if register_button:
                if password == confirm_password:
                    message = register_user(username, email, password)
                    st.success(message if "successful" in message else message)
                else:
                    st.error("Passwords do not match!")

    elif option == "Login":
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("Login")

            if login_button:
                success, username = login_user(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.success(f"Welcome back, {username}!")
                else:
                    st.error("Invalid credentials. Please try again.")

# Chatbot Interface
if st.session_state.authenticated:
    st.title("Pdf 📚 ChatBot 🤖🦜")
    st.image("img.png", use_container_width=True)
    
    with st.sidebar:
        upload_file = st.file_uploader("Upload a file", type=['pdf', 'docx'])
        chunk_size = st.number_input("Chunk Size:", min_value=100, max_value=2048, value=256)
        k = st.number_input("K:", min_value=1, max_value=20, value=3)
        add_data = st.button('Add Data')

        if upload_file and add_data:
            with st.spinner("Reading, Chunking, and Embedding file..."):
                bytes_data = upload_file.read()
                file_name = os.path.join('./', upload_file.name)
                with open(file_name, 'wb') as f:
                    f.write(bytes_data)
                
                data = load_document(file_name)
                chunks = chunk_data(data, ChunkSize=chunk_size)
                st.write(f"Chunk size: {chunk_size}, Chunks: {len(chunks)}")

                vector_store = Create_Embedding_VectorDB(chunks)

                st.session_state.vs = vector_store
                st.success("File uploaded, chunked, and embedded!")

   
    # Question input and chatbot response
    question = st.text_input("Ask a Question about the content of your file:")

    if question:
        if 'vs' in st.session_state:
            vector_store = st.session_state.vs
            answer = ask_and_get_answer(vector_store, question, k)
            
            # Store the chat history
            st.session_state.chat_history.append({'sender': 'user', 'message': question})
            st.session_state.chat_history.append({'sender': 'bot', 'message': answer})

            # Display chat history in the main area
            for chat in st.session_state.chat_history:
                if chat['sender'] == 'user':
                    st.markdown(f"**You 👨‍🦰:** {chat['message']}")
                else:
                    st.markdown(f"**Bot 🤖:** {chat['message']}")

    # Log out button
    if st.sidebar.button("Log Out"):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.chat_history = [] 
        st.success("You have been logged out successfully.")
