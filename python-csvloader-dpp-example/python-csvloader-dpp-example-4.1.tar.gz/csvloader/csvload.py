import pandas

def load_csv(path):
    result = pandas.read_csv(path)
    print(result)