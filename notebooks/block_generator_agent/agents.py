import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

### Get LLM
def get_llm(model_name:str = "llama-3.3-70b-versatile", temperature: float = 0.5):
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model=model_name, temperature=temperature, api_key=api_key)
    return llm



### Research Agent
Researcher_Prompt = ChatPromptTemplate.from_messages([
    {"role":"system", "content":"""
       "You are a Research Agent. Give a blog topic and target audience, produce a clear,"
       "structured research outline. Include:\n"
       "1.  5-7 key points the blog should cover\n"
       "2.  Important facts, stats, or example for each points\n"
       "3. Suggestes angle or hook\n"
       "Be concise. Use bullet points. Do NOT write the full bolg yet." 
    """},
    {"role":"user","content":"Topic: {topic}, Audience: {audience}, {revision_hints}, write the research outline now."}
]) 


def researcher_agent(llm:ChatGroq, topic:str, audience:str, feedback:str = "") ->str:
    revision_hints = f"The human provided this feedback on your previous research please address it:{feedback},"
    if not feedback:
        revision_hints = "This is your first attempt."

    chain = Researcher_Prompt |  llm

    result = chain.invoke({
        "topic":topic,
        "audience":audience,
        "revision_hints":revision_hints

    })

    return result.content


Writer_Prompt = ChatPromptTemplate.from_messages([
    {"role":"system", "content":"""
       "You are a Blog Writer Agent. Using the research notes provided, write a complete,"
       "engaging blog post.\n"
       "Rules:\n"
       "- Length: 500-800 words\n"
       "- Structure: catchy title, intro hook, 3-5 sections with H2 headings, conclusion\n"
       "-Tone: clear, frienndly, suited to the target audience\n"
       "Use markdown formatting\n"
       "Do NOT add a 'word count' line at the end."

    """},
    {"role":"user","content": """
        Topic:{topic},
        Audience:{audience},
        Research Notes:{research},
        
        {revision_hints}

        Write the full the blog post now.
    """}
])    


def writer_agent(llm:ChatGroq, topic:str, audience:str, research:str="", feedback:str = "") ->str:
    revision_hints = f"The human provided this feedback on your previous draft and asked for these changes :{feedback}. Please apply these changes during writtimg the blog"
    if not feedback:
        revision_hints = "This is your first attempt."

    chain = Writer_Prompt |  llm
    print(revision_hints)

    result = chain.invoke({
        "topic":topic,
        "audience":audience,
        "research":research,
        "revision_hints":revision_hints

    })

    return result.content


### Editor Agnet

Editor_Prompt = ChatPromptTemplate.from_messages([
    {"role":"system", "content":"""
       "You are a Editor Agent. the final quality gate before publishing.\n"
       "Take the draft and produce the FINAL polished version. Specifically:\n"
       "- Fix grammar, apelling, and awkward phrasing\n"
       "- Tighten wordy sentences\n"
       "- Improve flow and transitions between sections\n"
       "- Make the title and intro more compelling if needed\n"
       "- Keep the same structure and markdown formatting\n"
       "- Blog wording should look like human , not a AI, and don't use any special chars and complex / fancy words\n"
       "Output only the final polishes blog post - no commentary."

    """},
    {"role":"user","content": """
        Topic:{topic},
        Draft:{draft}

        Return the published block post.
    """}
])    


def editor_agent(llm:ChatGroq, topic:str, draft:str="", feedback:str = "") ->str:
    chain = Editor_Prompt |  llm

    result = chain.invoke({
        "topic":topic,
        "draft":draft
        
    })

    return result.content