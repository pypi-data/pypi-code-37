import pandas

def load_csv():
    result = pandas.read_csv('csvloaderData/data.csv')
    print(result)