from collections import defaultdict
import csv


def load_csv(filepath, headers=True):
    """Load CSV in simple schema, with one row of column headers"""
    with open(filepath) as f:
        reader = csv.reader(f)
        if headers:
            next(reader)

        dct = defaultdict(list)
        for line in reader:
            if len(line) == 3:
                dct[line[0]].append({
                    "value": line[1],
                    "type": "exact",
                    "weight": float(line[2])
                })
            else:
                dct[line[0]].append({
                    "value": line[1],
                    "type": "exact",
                })

    for v in dct.values():
        if len(v) > 1:
            for elem in v:
                assert 'weight' in elem
                elem['type'] = 'disaggregation'

    return dct
