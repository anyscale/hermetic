from hermetic.core.store import Store
from hermetic.core.presenter import Presenter
from hermetic.core.agent import Agent
from hermetic.core.tool import Tool, ToolResult
from hermetic.core.prompt_mgr import PromptMgr
from typing import Any, List, Dict
import uuid
import os

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

    def primary(self) -> Agent:
        return self.agents[self.primary_agent]

    def set_primary_agent(self, id: str):
        self.primary_agent = id

    def __init__(self, prompt_mgr: PromptMgr,store: Store = None):
        self.store = store
        if self.store:
            self.store.set_environment(self)    
        self.agents = {}
        self.tools = {}
        self.primary_agent = None
        self.prompt_mgr = prompt_mgr 

    def start(self):
        agent = self.agents[self.primary_agent]
        self.presenter.present(agent)

def load_environments(root_dir: str = 'resources/environments'):
    dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) and not d.startswith('.')]
    retval = {}
    for d in dirs:
        retval[d] = Environment(PromptMgr(src_dir=root_dir + '/' + d + '/prompts'))
    return retval 

        
    
