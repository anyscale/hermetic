from abc import ABC, abstractmethod
from hermetic.core.message import Message
from pydantic import BaseModel


class Trace(ABC):
    @abstractmethod
    def append_to_trace(self, message: Message): 
        pass
    

  
class Store(ABC):
    
    def set_environment(self, environment):
        self.env = environment

    @abstractmethod
    def create_trace(self, trace_id: str) -> Trace: 
       pass