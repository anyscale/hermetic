from hermetic.presenters.gradio_presenter import GradioPresenter
from hermetic.agents.openai_chat_agent import OpenAIChatAgent

ta = OpenAIChatAgent(model='gpt-3.5-turbo', greeting='Hello, I am a llama')
gp = GradioPresenter(app_name='Llama Chatbot')

gp.present(ta)