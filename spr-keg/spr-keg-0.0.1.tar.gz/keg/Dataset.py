class Dataset:
    def __init__(self, id, env):
        self.id = id
        self.env = env

    def load(self):
        return None

    def say_hello(self, name = "dataset"):
        return "hello " + name + "!"
