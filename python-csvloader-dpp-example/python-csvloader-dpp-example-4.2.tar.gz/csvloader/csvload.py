import csv

def load_csv(path):
    with open(path,'rt')as f:
        data = csv.reader(f)
        for row in data:
            print(row)