import gradio as gr
from hermetic.core.agent import Agent, InputMarker, Input
from hermetic.core.presenter import Presenter
from threading import Thread
from queue import SimpleQueue
from langchain.callbacks.base import BaseCallbackHandler
import uuid

CSS ="""
.contain { display: flex; flex-direction: column; }x
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; }
"""

class GradioPresenter(Presenter): 
    def __init__(self, 
                app_name: str = 'Hermetic',
                news: str = ''):
        self.app_name = app_name
        self.news = news
        
    def present(self, agent):
        self.agent = agent
        with gr.Blocks(title=self.app_name, css=CSS) as app:
            greeting = self.agent.greet()
            conv_start = []
            if greeting:
                conv_start=[[None,greeting]]

            chatbot = gr.Chatbot(value=conv_start,elem_id="chatbot")
            msg = gr.Textbox(show_label=False) 
            # Note: the state is deep copied at this point
            agent = gr.State(self.agent)


            def user(user_message,history):
                return "", history + [[user_message,None]]
            
            def bot(history,agent):
                history[-1][1] = ''
                for word in agent.process_input(history[-1][0]):
                    history[-1][1] += word
                    yield history, agent
                 
            msg.submit(fn=user, 
                    inputs=[msg, chatbot], 
                    outputs=[msg, chatbot], queue=False).then(
                    fn=bot, 
                    inputs=[chatbot, agent],
                    outputs=[chatbot, agent])

        app.queue(concurrency_count=8)
        app.launch()



    

        


    
        