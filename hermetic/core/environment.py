from hermetic.core.store import Store
from hermetic.core.presenter import Presenter
from hermetic.core.agent import Agent
from hermetic.core.tool import Tool, ToolResult
from hermetic.core.prompt_mgr import PromptMgr
from typing import Any, List, Dict
import uuid 

class Environment():
    store: Store
    prompt_mgr: PromptMgr
    agents: Dict[str, Agent]
    tools: Dict[str, Tool]

    primary_agent: str 
    # right now we supoprt one presenter 
    # per environment but that's not a hard limit. 
    # we could have multiple. 
    presenter: Presenter



    def create_session_id(self):
        return str(uuid.uuid4())

    def add_agent(self, id: str, agent: Agent):
        self.agents[id] = agent

    def add_tool(self, id: str, tool: Tool):
        self.tools[id] = tool


    def set_primary_agent(self, id: str):
        self.primary_agent = id

    def __init__(self, store: Store, presenter: Presenter, prompt_mgr: PromptMgr):
        self.store = store
        self.store.set_environment(self)    
        self.presenter = presenter
        self.presenter.set_environment(self)
        self.agents = {}
        self.tools = {}
        self.primary_agent = None
        self.prompt_mgr = prompt_mgr 



    def start(self):
        agent = self.agents[self.primary_agent]
        self.presenter.present(agent)

    
