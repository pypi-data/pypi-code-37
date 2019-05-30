from typing import Dict, List
from pandas import DataFrame
from .recorder import Recorder
from .partition import Partition
from .settuner import SetTuner

class Tuner(Recorder):

    tuner: SetTuner

    def __init__(self):
        self.tuner = SetTuner()
        super().__init__()
    
    def tune(
        self, 
        search_params: Dict,
        set_params: Dict, 
        dataset: DataFrame ,
        features: List[str],
        targets: List[str],
        folds: int,
    ) -> List[Dict]:
        partitions = Partition(dataset, folds)

        for split in partitions:
            fold_records = self.tuner.tune(
                search_params,
                set_params,
                split["train"][features],
                split["train"][targets].values.ravel(),
                split["test"][features],
                split["test"][targets],
                False,
            )

            if (not self.records):
                self.records = fold_records
            else:
                self.aggeregate(fold_records)

        
        self.average_scores(folds)
        self.sort_records()
        return self.records 