import os

path = "data/" if "MAP_DATA_PATH" not in os.environ else os.environ["MAP_DATA_PATH"]

print(path)
