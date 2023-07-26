import openai
from hermetic.core.agent import Agent
from abc import abstractmethod

class OpenAIChatAgent(Agent):

    def __init__(self, model: str, environment, id: str = None):
        super().__init__(environment, id=id)
        self.message_history = []
        self.model = model 

    def greet(self):
        return None

    def process_input(self, input: str):
        self.update_message_history(input)

        response = openai.ChatCompletion.create(
           model = self.model,
           messages = self.message_history,
           stream = True
        )
        words = ''
        for tok in response: 
            delta = tok.choices[0].delta
            if not delta: # End token 
                self.message_history.append({
                    'role': 'assistant',
                    'content': words
                })
                break
            elif 'content' in delta:
                words += delta['content']
                yield delta['content'] 
            else: 
                continue

    def update_message_history(self, inp):
        """
        Subclasses of OpenAIChatAgent may want to override this
        method to do things like add metadata to the message history
        """
        self.message_history.append({
            'role': 'user',
            'content': inp
        })

        