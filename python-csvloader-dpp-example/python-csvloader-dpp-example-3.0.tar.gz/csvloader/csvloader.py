import csv, pandas

with open('csvloaderData/data.csv','rt')as f:
  data = csv.reader(f)
  for row in data:
        print(row)

result = pandas.read_csv('csvloaderData/data.csv')
print(result)