from pydantic import BaseModel
from typing import Union
from abc import ABC, abstractmethod

from enum import Enum

class InputMarker(Enum):
    """
    Represents an out-of-band input type, 
    eg. start a conversation  

    """
    START = '-- START --'
    CANCEL = '-- CANCEL --'
    END = '-- END --'

class Input(BaseModel):
    input: Union[InputMarker, str]


class Agent(ABC):
    @abstractmethod
    def process_input(self, input: Input) -> str:
        pass

    def process_all(self, input: str) -> str:
        return ''.join(self.process_input(Input(input=input)))

    def __init__(self, environment, primary: bool = False, id: str = None):
        self.env = environment
        self.id = id
        if primary:
            self.env.set_primary_agent(self.id)

    def greet(self):
        return None
        


