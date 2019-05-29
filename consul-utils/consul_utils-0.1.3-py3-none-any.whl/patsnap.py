from .filters import PairedFilter


class PatsnapDiffFilter(PairedFilter):

    def filter_pair(self, key1, value1, key2, value2, index, **kwargs) -> bool:
        self.filter_env(key=key1, value=value1, index=index, group='1')
        self.filter_env(key=key2, value=value2, index=index, group='2')
        if self.check_skip(key1=key1, key2=key2):
            return False
        return value1 != value2

    def filter_env(self, key, value, index, group):
        keycol = key.split('/')
        env = keycol[3]
        if keycol[5] == 'environment' and len(keycol) >= 7:
            if self.check_env(env, 'prod'):
                if 'patsnap.release' in value:
                    self.add_result(key=key, value=value, index=index, group=group, flag='danger')
            elif self.check_env(env, 'release') or self.check_env(env, 'ci') or self.check_env(env, 'qa'):
                if 'patsnap.private' in value:
                    self.add_result(key=key, value=value, index=index, group=group, flag='danger')

    def check_skip(self, key1, key2):
        keycol1 = key1.split('/')
        keycol2 = key2.split('/')
        if keycol1[5] == 'history_conf' and keycol2[5] == 'history_conf':
            return True
        return False

    def check_env(self, env, check):
        return env.lower().startswith(check)

    def add_result(self, key, value, index, group, flag=None, template=None):
        if not self.results:
            self.results = []
        self.results.append({'key': key, 'value': value, 'index': index, 'group': group, 'flag': flag, 'template': template})

