import csv

def load_csv():
    with open('csvloaderData/data.csv','rt')as f:
        data = csv.reader(f)
        for row in data:
            print(row)
