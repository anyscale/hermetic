from hermetic.core.store import Store, Trace
from hermetic.core.message import Message
import os
import uuid

class FileTrace(Trace):
    def __init__(self, trace_id: str, session_id: str):
        self.trace_id = trace_id
        self.session_id = session_id
        self.trace_file = f'{session_id}/{trace_id}.txt'
        self.create_trace_file()
    
    def create_trace_file(self):
        if not os.path.exists(self.trace_file):
            with open(self.trace_file, 'w') as f:
                f.write('')
    
    def append_to_trace(self, message: Message):
        with open(self.trace_file, 'a') as f:
            f.write(f'{message}\n')

class FileStore(Store):
    """
    A store that saves traces to the local filesystem
    """
    def __init__(self, root_dir: str, session_id: str = str(uuid.uuid4())):
        self.root_dir = root_dir
        self.session_id = session_id
        self.session_dir = f'{root_dir}/{session_id}'
        self.create_session_dir()
        #if the root dir doesn't exist create it. 

    def create_session_dir(self):
        if not os.path.exists(self.session_dir):
            os.makedirs(self.session_dir)

    def create_trace(self, trace_id: str) -> Trace:
        return FileTrace(trace_id, self.session_dir)