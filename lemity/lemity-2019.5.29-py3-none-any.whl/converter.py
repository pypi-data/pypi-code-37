from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        super().__init__(map)
        self.map = map
        self.regex = args[0]
