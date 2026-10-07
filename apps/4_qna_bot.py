import os

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
import streamlit as st

llm = ChatGroq(model="llama-3.1-8b-instant")

st.title("🫡 AskBuddy - AI QnA Bot")
st.markdown("My Ai QnA ChatBot with Langchain and Groq")

# Memory Storage
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old chat
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)




query = st.chat_input("Ask Anything!")
if query:
    st.session_state.messages.append({"role":"user", "content": query})
    st.chat_message("user").markdown(query)
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role":"ai", "content": res.content})
