from .searcher import Searcher
from typing import Dict

class GridSearcher(Searcher):
    params: Dict
    param_indices: Dict
    started: bool

    def __init__(self, params: Dict):
        self.params = params        
        self.param_indices = {}
        self.started = False

        for param in params:
            self.param_indices[param] = 0
        
    def __iter__(self) -> Searcher:
        return self

    def __next__(self) -> Dict:
        if not self.started:
            self.started = True
            return self.current_params()
        elif self.param_step():
            return self.current_params()
        else:
            raise StopIteration                    

    def param_step(self) -> bool:
        updated = False
        for param in self.param_indices:
            if self.untried_values_for(param):
                self.param_indices[param] += 1
                updated = True
                break
        
        return updated
            
    def current_params(self) -> Dict:
        current_params = {}
        for param, index in self.param_indices.items():
            current_params[param] = self.params[param][index]
        
        return current_params

    def untried_values_for(self, param: str):
        return self.param_indices[param] < len(self.params[param]) - 1