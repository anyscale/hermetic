
from pydantic import BaseModel

class Prompt():
    # Note: In Hermetic we use Prompt for templates as well. 
    # If it is in hot_reload mode, it will reload the template
    # every time it is called.
    def __init__(self, file_path: str, hot_reload: bool = True):
        self.file_path = file_path
        self.cached = None
        self.hot_reload = hot_reload

    def render(self, **kwargs) -> str:
        if (self.cached is None) or (self.hot_reload):
            with open(self.file_path, 'r') as f:
                self.cached = f.read()
        print (f'kwargs is {kwargs}')
        return self.cached.format(**kwargs)


class PromptMgr():
    def __init__(self, hot_reload: bool = True, src_dir: str = 'resources/prompts'):
        """ Creates a prompt manager. 

        Args:
            hot_reload: If true, reloads the prompt every time it is called.
            src_dir: The directory where the prompts are stored.

        """
        self.hot_reload = hot_reload
        self.src_dir = src_dir

    def bind(self, prompt_id: str) -> Prompt:
        return Prompt(f'{self.src_dir}/{prompt_id}.txt', hot_reload=self.hot_reload)

