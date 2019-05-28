import re
from enti.api import *
from enti.debugging import debug
class RegexSubstitution(Processor):
    def __init__(self, id, pattern, repl):
        super(RegexSubstitution, self).__init__(id)
        self.pattern = pattern
        self.repl = repl

    def run(self, data, *args, **kwargs):


        output = re.sub(self.pattern, self.repl, data)
        # debug("<<regex sub>>", depth=self.debug_level, data={
        #     "input": data,
        #     "pattern": self.pattern,
        #     "repl": self.repl,
        #     "output": output
        # })
        return output

