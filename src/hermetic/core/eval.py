from pydantic import BaseModel
from typing import List, Dict
from hermetic.core.environment import Environment
import ray

class EvalItem(BaseModel):
    prompt: str
    ideal: str

class EvalResult(BaseModel):
    agent: str
    output: str

class EvalResultSet(BaseModel):
    item: EvalItem
    results: Dict[str, EvalResult]

class EvalInput(BaseModel):
    items: List[EvalItem]
        
class EvalOutput(BaseModel):
    results: List[EvalResultSet]