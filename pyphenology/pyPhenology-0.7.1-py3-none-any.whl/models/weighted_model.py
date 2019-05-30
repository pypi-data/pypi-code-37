import numpy as np
import pandas as pd
from . import utils, validation


class WeightedModel():
    def __init__(self, core_model=None, grid_size=1, parameters={}):
        self.core_model = core_model
        self.grid_size = grid_size
        
    
    def fit(self, observations, predictors, **kwargs):
        # Require lat, long for all observations
        
        pass
    
    def predict(self, to_predict=None, predictors=None, **kwargs):
        pass