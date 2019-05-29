import xgboost as xgb
from typing import Dict, List, Type
from .gridsearcher import GridSearcher
from .searcher import Searcher

class Tuner():
    param_searcher: Searcher
    set_params: Dict
    records: List[Dict]

    def __init__(self):
        self.records = []
        pass
    
    def tune(
        self, 
        search_params: Dict,
        set_params: Dict, 
        train_features, 
        train_targets,
        test_features,
        test_targets
    ) -> List[Dict]:
        if (len(search_params) == 0):
            raise ValueError("No search parameters provided")

        self.param_searcher = GridSearcher(search_params)
        self.set_params = set_params
        self.train_features = train_features 
        self.train_targets = train_targets
        self.test_features = test_features
        self.test_targets = test_targets
        self.records = []
        return self.tune_classifier()

    def tune_classifier(self)-> List[Dict]:
        for candidates in self.param_searcher:
            args: Dict = {**self.set_params, **candidates}
            # Note: candidates override set_params here.

            classifier = xgb.XGBClassifier(**args)
            classifier.fit(self.train_features, self.train_targets)
            score: float = classifier.score(self.test_features, self.test_targets)
            self.save_score(args, score)
        self.sort_records()
        return self.records

    def save_score(self, params_used: Dict, score: float):
        self.records.append({
            "score": score,
            "params": params_used
        })
    
    def sort_records(self):
        self.records = sorted(self.records, key = lambda i: i["score"], reverse=True)
    
    def best_n_params(self, records_wanted: int) -> List[Dict]:
        self.confirm_records()
        return self.records[:records_wanted]

    def best_params(self) -> Dict:
        self.confirm_records()
        return self.records[0]
    
    def confirm_records(self):
        if (len(self.records) == 0):
            raise RuntimeError("Attempt to access tuning results before tuning has occurred")