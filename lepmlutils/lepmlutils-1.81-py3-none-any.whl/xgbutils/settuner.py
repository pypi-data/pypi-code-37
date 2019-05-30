import xgboost as xgb
from typing import Dict, List
from .gridsearcher import GridSearcher
from .searcher import Searcher
from .recorder import Recorder

class SetTuner(Recorder):
    param_searcher: Searcher
    set_params: Dict

    def __init__(self):
        super().__init__()
        pass
    
    def tune(
        self, 
        search_params: Dict,
        set_params: Dict, 
        train_features, 
        train_targets,
        test_features,
        test_targets,
        sort_records: bool = True
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

        if (sort_records):
            return self.tune_and_sort()

        return self.tune_classifier()

    def tune_classifier(self) -> List[Dict]:
        for candidates in self.param_searcher:
            args: Dict = {**self.set_params, **candidates}
            # Note: candidates override set_params here.

            classifier = xgb.XGBClassifier(**args)
            classifier.fit(self.train_features, self.train_targets)
            train_score: float = classifier.score(self.train_features, self.train_targets)
            test_score: float = classifier.score(self.test_features, self.test_targets)
            self.save_score(args, train_score, test_score)
        return self.records
    
    def tune_and_sort(self) -> List[Dict]:
        self.tune_classifier()
        self.sort_records()
        return self.records
        
    def save_score(self, params_used: Dict, train_score: float, test_score: float):
        self.records.append({
            "test_score": test_score,
            "train_score": train_score,
            "params": params_used
        })