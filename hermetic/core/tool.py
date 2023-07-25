
from abc import ABC, abstractmethod
from typing import Union, List
from pydantic import BaseModel

class ToolResult(BaseModel):
    """
    Represents the result of a tool run
    """
    id: str # unique identifier for the resolut. 
    content: str
    metadata: dict = {} # for things like confidences etc

class Tool(ABC):

    def __init__(self, env):
        self.env = env

    @abstractmethod
    def run(self, input: str, **kwargs) -> Union[str, List[ToolResult]]:
        pass

