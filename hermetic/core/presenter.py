from abc import ABC, abstractmethod
from hermetic.core.agent import Agent

class Presenter(ABC):

    def set_environment(self, environment):
        self.env = environment

    @abstractmethod
    def present(self, agent: Agent):
        pass