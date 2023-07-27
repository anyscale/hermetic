

# Hermetic

Hermetic is a library that makes it easy to develop, test, evaluate and deploy LLM Applications. 


# Quick start guide

These particular instructions are focused on Anyscale Endpoints, but they should generalize.  


## Prerequisites

Before you get started, you’ll need an Anyscale Endpoints key. You can get that from [https://console.endpoints.anyscale.com/credentials](https://console.endpoints.anyscale.com/credentials) (after you’ve entered your credit card). 

**Make sure you save this – it is only given once. **

You also need a clean python environment. 


### Install Hermetic, Langchain, Gradio, OpenAI libraries

To install these libraries, just install hermetic and hermetic will install the rest. Update pip first, since it seems to reduce installation time. 


```
% python -m pip install --upgrade pip
% pip install git+https://github.com/anyscale/hermetic.git
```



### Create a .env file and put some environment variables in it

We need quite a few environment variables to get this demo working, so the easiest way is to put them in a .env file.

Add the following lines there: 


```
export OPENAI_API_BASE=https://console.endpoints.anyscale.com/m/v1
export OPENAI_API_KEY=secret_<your secret> 
```


**NOTE: **It may seem weird that we are defining OPENAI_API_* variables when we want to connect to Anyscale. But this is because Anyscale offers an OpenAI compatible api. Note that you did not need to install any libraries to use Anyscale Endpoints specifically, it reuses the OpenAI python SDK. 

And now to load them 


```
% source .env
```



### Create a system prompt

Now  create a simple file 

resources/prompts/system_prompt.txt

That contains:


```
You are helpful assistant who is also a pirate and speaks like a pirate. You litter your conversation with references to pirates. You also enjoy the humor of Monty Python and include many references to Monty Python sketches in your answers.  
```



### Create a Langchain-based agent that uses Anyscale Endpoints

Create a file called pirate.py that contains the following: 


```python
from hermetic.agents.langchain_chat_agent import LangchainChatAgent
from hermetic.agents.openai_chat_agent import OpenAIChatAgent
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage 
from hermetic.core.prompt_mgr import PromptMgr
from hermetic.core.environment import Environment
from hermetic.presenters.gradio_presenter import GradioPresenter

NAME = 'pirate'
MODEL = 'meta-llama/Llama-2-13b-chat-hf'
#MODEL = 'gpt-3.5-turbo'
class Pirate(OpenAIChatAgent):

    def __init__(self, env):
        # Call the super class constructor
        super().__init__(environment = env, id=NAME, model=MODEL)
        env.add_agent(NAME, self)
        self.pm = self.env.prompt_mgr


        # bind to the system message
        sys_msg = self.pm.bind('system_msg')
        self.llm = ChatOpenAI(temperature=0, model_name=MODEL, streaming=True)

        # Let's add our system message to the message history
        #self.message_history = [SystemMessage(content=sys_msg.render())]
        self.message_history = [{
            'role': 'system',
            'content': sys_msg.render()
        }]

    # Our superclass takes care of the details, all we need to do
    # is to update the message history
    def update_message_history(self, inp): 
        # If we wanted we could add additional details here. 
        #self.message_history.append(HumanMessage(content=inp))
        self.message_history.append({
            'role': 'user',
            'content': inp
        })

# Now let's set up the enviroment and presenter
env = Environment(store = None, prompt_mgr = PromptMgr(hot_reload=True))

# Let's add our agent to the environment
pirate = Pirate(env)
env.set_primary_agent(NAME)

# Now present graphically. 

presenter = GradioPresenter(app_name='Pirate', 
                            env=env)

# This starts the UI. 
presenter.present()
```


Now connect to localhost:7860 in your browser and you should be able to talk to a pirate! 
