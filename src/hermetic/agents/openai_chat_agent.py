import openai
from hermetic.core.agent import Agent
from abc import abstractmethod

class OpenAIChatAgent(Agent):

    def __init__(self, model: str, environment, id: str = None):
        super().__init__(environment, id=id)
        self.message_history = []
        self.model = model 
        self.functions = None

    def greet(self):
        return None
    
    def process_fn_call(self, orig_question: str, function_name: str, function_arguments: str):
        pass

    def process_input(self, input: str):
        self.update_message_history(input)
        if self.functions is None:
            response = openai.ChatCompletion.create(
            model = self.model,
            messages = self.message_history,
            stream = True
            )
        else: 
            print("Using functions!" + str(self.functions))
            response = openai.ChatCompletion.create(
            model = self.model,
            messages = self.message_history,
            stream = True,
            functions = self.functions
            )
        words = ''
        function_name = ''
        function_arguments = ''
        response_mode = '' # words or fn
        for tok in response: 
            #print('Token received: ' + str(tok))
            delta = tok.choices[0].delta
            if not response_mode: 
                # This code should only trigger the first 
                # time through the loop.
                if 'function_call' in delta:
                    # We are in function mode
                    response_mode = 'fn'
                    function_name = delta['function_call']['name']
                else: 
                    response_mode = 'words'
                print('Response mode: ' + response_mode)

            # We process things differently depending on whether it is a function or a 
            # text
            if response_mode == 'words':
                if not delta: # End token
                    self.message_history.append({
                            'role': 'assistant',
                            'content': words
                        })

                    break
                elif 'content' in delta:
                    if delta['content']: 
                        words += delta['content']
                        yield delta['content'] 
                else: 
                    continue
            elif response_mode == 'fn':
                if not delta: # End token
                    function_call = function_name + '(' + function_arguments + ')'
                    print(f"Function call is {function_call}")
                    result = self.process_fn_call(input, function_name, function_arguments)
                    self.message_history.append({
                            'role': 'assistant',
                            'content': result
                    })
                    yield result
                    break
                elif 'function_call' in delta:
                    #print(f"Function call --{delta['function_call']['arguments']}")
                    function_arguments += delta['function_call']['arguments']
                    yield '' # delta['function_call']['arguments'] # we shouldn't yield anything if it's a fn
                else: 
                    continue
            else:
                raise Exception("Invalid response mode: " + response_mode)
            

    def update_message_history(self, inp):
        """
        Subclasses of OpenAIChatAgent may want to override this
        method to do things like add metadata to the message history
        """
        self.message_history.append({
            'role': 'user',
            'content': inp
        })

        