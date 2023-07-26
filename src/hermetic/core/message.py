
from pydantic import BaseModel
from enum import Enum
from typing import List, Union

class AnnotationType(Enum):
    SCORE = "score"
    VOTE = "vote"
    COMMENT = "comment"

class Annotation(BaseModel):
    type: AnnotationType
    content: Union[str,int]

class Role(Enum):
    """
    Represents the role of a message
    """
    USER = "user"
    SYSTEM = "system"
    AI = "ai"
    INTERNAL = "internal"

class Message(BaseModel):
    """
    Represents a message from the user or the system
    """
    role: Role
    content: str
    metadata: dict = {} # for things like tokens
    annotations: List[Annotation] = []  
