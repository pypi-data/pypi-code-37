from dero.latex.models.item import MultiOptionSimpleItem


class NewEnvironment(MultiOptionSimpleItem):
    name = 'newenvironment'

    def __init__(self, env_name: str, begin_env: str, end_env: str):
        self.env_name = env_name
        self.begin = begin_env
        self.end = end_env
        super().__init__(self.name, env_name, begin_env, end_env)
