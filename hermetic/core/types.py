from pydantic import BaseModel
from typing import Union, ABC
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

class Presenter(ABC):
    @abstractmethod
    def present(self, agent: Agent):
        pass
        


