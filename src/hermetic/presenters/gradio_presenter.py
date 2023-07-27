import gradio as gr
from hermetic.core.agent import Agent, InputMarker, Input
from hermetic.core.presenter import Presenter
from threading import Thread
from multiprocessing import Queue
from langchain.callbacks.base import BaseCallbackHandler
from hermetic.core.environment import Environment
import uuid

CSS ="""
.contain { display: flex; flex-direction: column; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; overflow: auto;}
#chatbot .wrap {max-height: 700px; overflow: auto;}} 
"""

class GradioPresenter(Presenter): 
    def __init__(self, 
                env: Environment, 
                app_name: str = 'Hermetic',
                news: str = '',
                favicon_path: str = None,
):

        self.app_name = app_name
        self.news = news
        self.favicon_path = favicon_path
        self.env = env
        
    def present(self):
        self.agent = self.env.agents[self.env.primary_agent]
        with gr.Blocks(title=self.app_name, css=CSS) as app:
            greeting = self.agent.greet()
            conv_start = []
            if greeting:
                conv_start=[[None,greeting]]

            chatbot = gr.Chatbot(value=conv_start,elem_id="chatbot")
            msg = gr.Textbox(show_label=False) 
            # Note: the state is deep copied at this point
            #agent_state = gr.State(self.agent)


            def user(user_message,history):
                return "", history + [[user_message,None]]
            
            def bot(history):
                history[-1][1] = ''
                for word in self.agent.process_input(history[-1][0]):
                    history[-1][1] += word
                    yield history# , agent
                 
            msg.submit(fn=user, 
                    inputs=[msg, chatbot], 
                    outputs=[msg, chatbot], queue=False).then(
                    fn=bot, 
                    inputs=[chatbot],
                    outputs=[chatbot])

        app.queue(concurrency_count=8)
        if self.favicon_path:
            app.launch(favicon_path=self.favicon_path)
        else:
            app.launch()



    

        


    
        