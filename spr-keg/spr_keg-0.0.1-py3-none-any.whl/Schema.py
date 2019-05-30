class Schema:
    def __init__(self, id):
        self.id = id

    def load_schema(self):
        return None
    
    def say_hello(self, name = "schema"):
        return "hello " + name + "!"
