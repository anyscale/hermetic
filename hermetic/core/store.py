from abc import ABC, abstractmethod
from hermetic.core.message import Message

class TraceStore(ABC):
    
    @abstractmethod
    def create_trace(self, trace_id: str) -> Trace: 
        pass
    
    def append_to_trace(self, message: Message)

class Store(ABC):
