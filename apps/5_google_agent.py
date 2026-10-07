

from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

llm = ChatGroq(model="llama-3.3-70b-versatile")
search = GoogleSerperAPIWrapper()
memory = MemorySaver()

agent = create_agent(
    model = llm,
    tools = [search.run],
    checkpointer=memory,
    system_prompt="You are a agent and you can search any question on google"
    
)

while True:
    query = input("user: ")
    if query.lower() == "quit":
        print("Good Bye👋")
        break


    res = agent.invoke(
        {"messages":[{"role":"user", "content": query}]},
        {"configurable": {"thread_id":"1"}}
    )

    print("AI:", res["messages"][-1].content)


