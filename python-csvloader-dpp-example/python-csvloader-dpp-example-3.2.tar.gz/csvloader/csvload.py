import csv, pandas

def load_csv():
    with open('csvloaderData/data.csv','rt')as f:
        data = csv.reader(f)
        for row in data:
            print(row)

def load_pandas():
    result = pandas.read_csv('csvloaderData/data.csv')
    print(result)