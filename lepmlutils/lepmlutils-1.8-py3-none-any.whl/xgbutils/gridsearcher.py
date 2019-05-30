from .searcher import Searcher
from typing import Dict
import itertools

class GridSearcher(Searcher):
    params: Dict
    param_indices: Dict
    started: bool

    def __init__(self, params: Dict):
        self.params = params        
        self.perms = itertools.product(*params.values())
        
    def __iter__(self) -> Searcher:
        return self

    def __next__(self) -> Dict:
        current_params = {}
        values = next(self.perms)
        for index, key in enumerate(self.params.keys()):
            current_params[key] = values[index] 

        return current_params                  