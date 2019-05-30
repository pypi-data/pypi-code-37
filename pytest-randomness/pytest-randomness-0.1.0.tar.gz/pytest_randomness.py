import random


class RandomnessPlugin(object):
    try:
        from factory import random as factory_random
        have_factory_boy = True
    except ImportError:
        have_factory_boy = False

    try:
        from faker.generator import random as faker_random
        have_faker = True
    except ImportError:
        have_faker = False

    def __init__(self, config):
        self.tests = config.cache.get('randomness', {})

    def pytest_runtest_call(self, item):
        nodeid = item.nodeid
        if item.config.getoption('randomness_reset_seed') and nodeid in self.tests:
            self.set_seeds(self.tests[nodeid])
        else:
            self.tests[nodeid] = self.get_seeds()

    def pytest_sessionfinish(self, session):
        session.config.cache.set('randomness', self.tests)

    def get_seeds(self):
        seeds = {
            'python': random.getstate(),
        }
        if self.have_factory_boy:
            seeds['factory_boy'] = self.factory_random.get_random_state()
        if self.have_faker:
            seeds['faker'] = self.faker_random.getstate()
        return seeds

    def set_seeds(self, seeds):
        def seed_to_state(seed):
            return seed[0], tuple(seed[1]), seed[2]

        if 'python' in seeds:
            random.setstate(seed_to_state(seeds['python']))
        if self.have_factory_boy and 'factory_boy' in seeds:
            self.factory_random.set_random_state(seed_to_state(seeds['factory_boy']))
        if self.have_faker and 'faker' in seeds:
            self.faker_random.setstate(seed_to_state(seeds['faker']))
        return seeds


def pytest_configure(config):
    config.pluginmanager.register(RandomnessPlugin(config), 'randomnessplugin')


def pytest_addoption(parser):
    group = parser.getgroup('random', 'Random seed management')

    group.addoption(
        '--randomness-reset-seed', action='store_true',
        dest='randomness_reset_seed', default=False,
        help="""Do pytest-randomness to reset random.seed() at the
                start of every individual test."""
    )
