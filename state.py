from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
import operator
from langchain_core.messages import BaseMessage

class AgentState(BaseModel):
    messages: Annotated[List[BaseMessage], operator.add] = Field(default_factory=list)
    question: str = ""
    classification: Optional[str] = None
    response: Optional[str] = None