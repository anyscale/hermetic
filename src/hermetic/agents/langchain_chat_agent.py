from typing import Any, Dict, List, Optional
from uuid import UUID
from langchain.schema.messages import BaseMessage
import openai
from hermetic.core.agent import Agent, InputMarker
from abc import abstractmethod
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks import LangChainTracer
from queue import Queue
from threading import Thread
import sys

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

class LangchainChatAgent(Agent):

    class StreamingCBH(BaseCallbackHandler):
        def __init__(self, q):
            self.q = q
            print('Queue created')
                

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
            self.q.put(InputMarker.END)

    def set_llm(self, llm):
        self.llm = llm


    def __init__(self, environment, id: str = None):
        super().__init__(environment, id)
        self.message_history = []

    def greet(self):
        return None

    def process_input(self, input):
        self.update_message_history(input)
        myq = Queue()
        thread =  Thread(target = self.llm.predict_messages, kwargs = 
                        {'messages': self.message_history, 'callbacks': [self.StreamingCBH(myq)]})
        thread.start() 
        words = ''
        while True: 
            token = myq.get()
            if token == InputMarker.END:
               break
            words += token 
            yield token

        self.message_history.append(AIMessage(content=words))

    def update_message_history(self, inp):
        """
        Subclasses of OpenAIChatAgent may want to override this
        method to do things like add metadata to the message history
        """
        self.message_history.append(HumanMessage(content=inp))

        