from typing import Any, Dict, List, Optional, Union, Callable, Tuple
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

    def __init__(self, environment, id: str = None):
        super().__init__(environment, id)
        self.session_tag = f'session_{uuid.uuid4()}'
        self._message_history = []
        self._llm = None

    @property
    def message_history(self):
        """Returns an immutable view of the message history. Use `update_message_history` to append messages."""
        return tuple(self._message_history)

    @message_history.setter
    def message_history(self, messages: List[Union[AIMessage, HumanMessage, SystemMessage]]):
        """Resets the message history to the messages passed, calling `update_message_history` for each of them."""
        self._message_history = []
        for msg in messages:
            self.update_message_history(msg)

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

    def create_human_message_for_input(self, input):
        """When a human input is passed in to process_input, it turns it to a langchain HumanMessag with this method.

        Subclasses can override to add any custom logic to preprocess the input; e.g., recognizing commands."""
        return HumanMessage(content=input)

    def process_input(self, input):
        self.update_message_history(self.create_human_message_for_inpu(input))
        myq = Queue()
        thread = Thread(target = self.llm.predict_messages, kwargs =
                        {
                            'messages': self.message_history,
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

        self.update_message_history(AIMessage(content=words))

    def update_message_history(self, msg: Union[AIMessage, HumanMessage, SystemMessage]):
        """The only correct way to update the message history, allowing subclasses to override and include custom logic.

        The message history should not be accessed directly, but only through the property or this method. Otherwise,
        any custom logic that the subclasses assume will be applied to each newly added message may not be applied.
        """
        self._message_history.append(msg)

    def create_predict_messages_callbacks(self) -> List:
        """Subclasses can override to create callbacks for the LLM's predict_messages method."""
        return []
