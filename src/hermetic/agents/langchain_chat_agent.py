from typing import Any, Dict, List, Optional, Union
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
import uuid

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

    class MessageHistory:
        def __int__(
                self,
                agent: "LangchainChatAgent",
                messages: Optional[List[Union[AIMessage, HumanMessage, SystemMessage]]] = []):
            self._agent = agent
            self._messages: List[Union[AIMessage, HumanMessage, SystemMessage]] = []
            for msg in messages:
                self.append(msg)  # So that the `on_message_history_append` callback is called.

        @property
        def messages(self):
            return self._messages

        def append(self, msg: Union[AIMessage, HumanMessage, SystemMessage]) -> None:
            self._messages.append(msg)
            self._agent.on_message_history_append(msg)

    def __init__(self, environment, id: str = None):
        super().__init__(environment, id)
        self.session_tag = f'session_{uuid.uuid4()}'
        self._message_history = LangchainChatAgent.MessageHistory(agent=self)
        self._llm = None

    @property
    def message_history(self):
        return self._message_history

    @message_history.setter
    def message_history(self, messages: List[Union[AIMessage, HumanMessage, SystemMessage]]):
        self._message_history = LangchainChatAgent.MessageHistory(agent=self, messages=messages)

    @property
    def llm(self):
        """Return the LLM to be used for a prediction upon calling process_input.

        Subclasses can override to choose a suitable LLM, for example based on the message_history."""
        return self._llm

    @llm.setter
    def llm(self, llm):
        """If you don't override the `llm` property, make sure to assign an LLM to it before calling `process_input`."""
        self._llm = llm

    def greet(self):
        return None

    def process_input(self, input):
        self.update_message_history(input)
        myq = Queue()
        thread =  Thread(target = self.llm.predict_messages, kwargs =
                        {
                            'messages': self.message_history.messages,
                            'tags': [self.session_tag],
                            'callbacks': [self.StreamingCBH(myq)].extend(self.create_predict_messages_callbacks())
                        })
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

    def on_message_history_append(self, msg: Union[AIMessage, HumanMessage, SystemMessage]):
        """Subclasses can override to update their state whenever a new message is appended to the `message_history`.

        :param msg: The message that was appended to the message_history. Should be the same instance as message[-1].
        """
        pass

    def create_predict_messages_callbacks(self) -> List:
        """Subclasses can override to create callbacks for the LLM's predict_messages method."""
        return []
