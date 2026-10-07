
from pydantic import BaseModel,Field

class BlogState(BaseModel):
    ### User Input
    topic:str = "" 
    audience:str = "general reader"

    ## Researcher Output
    research:str = ""
    research_feedback:str = ""

    ## Writer Output
    draft:str = ""
    draft_feedback:str = ""

    ## Editor Output
    final_blog:str = ""
    
    ## Metadata
    revision_count: int = 0