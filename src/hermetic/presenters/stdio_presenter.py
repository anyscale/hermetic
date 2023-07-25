import sys
from hermetic.core.agent import Agent


class StdioPresenter:

    def present(self, agent: Agent): 
        sys.stdout.write(agent.greet()) 
        while True: 
            sys.stdout.write('> ')
            inp = input()
            for word in agent.process_input(inp):
                sys.stdout.write(word)
                sys.stdout.flush()
            sys.stdout.write('\n')