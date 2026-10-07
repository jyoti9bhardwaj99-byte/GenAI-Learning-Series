import os

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper # TOOL
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

llm = ChatGroq(model="llama-3.3-70b-versatile")
search = GoogleSerperAPIWrapper()
tools = [search.run]



if "memory" not in st.session_state: 
    st.session_state.memory = MemorySaver()
    st.session_state.history = []

agent = create_agent(
    model = llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt="You are a amazing ai agent and can search on google as well. "
)
print(st.session_state.memory)

## Building Web Interface

st.subheader("💭 QuickAnswer - Answer at the speed of Through")
st.markdown("🤖 My Quick AI Agent")

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)





query = st.chat_input("Ask Anything ?")
if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user", "content":query})


    res = agent.invoke(
        {"messages": [{"role":"user", "content":query}]},
        {"configurable": {"thread_id": "1"}},

    )

    answer = res["messages"][-1].content
    st.chat_message("AI").markdown(answer)
    st.session_state.history.append({"role":"AI", "content":answer})