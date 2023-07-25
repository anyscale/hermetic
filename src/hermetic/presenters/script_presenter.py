
from hermetic.core.presenter import Presenter

class ScriptPresenter(Presenter):
    def present(self, agent):
        print(agent.greet())
        while True:
            print('> ', end='')
            inp = input()
            for word in agent.process_input(inp):
                print(word, end='')
            print()