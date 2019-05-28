import json
import random
from enti.pipelines.report import *


def get_headline(sent):
    return sent_tokenize(sent)[0]

class Report:
    def __init__(self, text):
        self.text = text
        self.data = report_pipeline.run(text)

    @staticmethod
    def load_reports_from_json(filepath, sample_size: int = None):
        with open(filepath) as f:
            data = json.load(f)
        reports = []
        for rows in data.values():
            for e in rows:
                r = e["text"]
                reports.append(r)
        if sample_size is not None:
            if sample_size == 1:
                reports = [random.choice(reports)]
            elif sample_size == len(reports):
                pass
            else:
                reports = random.sample(reports, sample_size)
        #reports = [Report(r) for r in reports]
        data = [report_pipeline.run(r) for r in reports]
        return data



if __name__ == "__main__":
    random.seed(43)
    from pprint import pprint
    import shutil
    input_fp = "/projects/priism/priism/satp-20180801_20190508.json"
    reports = Report.load_reports_from_json(input_fp, 10)
    pprint(reports, compact=True, width=shutil.get_terminal_size((150,20))[0])
