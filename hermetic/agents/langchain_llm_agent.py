from hermetic.core.types import Agent

from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from queue import SimpleQueue
from threading import Thread
import sys


from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

class MyCBH(BaseCallbackHandler):
    def __init__(self, q):
        self.q = q

    def on_llm_new_token(
        self,
        token,
        *,
        run_id,
        parent_run_id = None,
        **kwargs,
    ) -> None:
        self.q.put(token)
    
    def on_llm_end(self, response, *, run_id, parent_run_id, **kwargs):
        self.q.put(END)
    
class LangChainChatAgent(): 
    def __init__(self, personality: str = None, start_string: str = None):
        self.message_history = []
        self.q = SimpleQueue()
        
        if personality: 
            self.message_history.append(SystemMessage(content=personality))
        
        if start_string: 
            self.message_history.append(AIMessage(content=start_string))

    def set_llm(self, llm):
        self.llm = llm
    
    def get_queue(self):
        return self.q
    
    def respond(self, input: str):
        self.message_history.append(HumanMessage(content=input))
        thread =  Thread(target = self.llm.predict_messages, kwargs = {'messages': self.message_history})
        thread.start() 
        words = ''
        while True: 
            token = self.q.get()
            if token == END:
               break
            words += token 
            yield token

        self.message_history.append(AIMessage(content=words))
    
