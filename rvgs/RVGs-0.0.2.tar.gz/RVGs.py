import scipy.stats as scipy
from numpy.random import RandomState


class RNG(RandomState):
    def __init__(self, seed):
        RandomState.__init__(self, seed)

    def sample(self):
        return self.random_sample()


class RVG:
    def __init__(self):
        pass

    def sample(self, rng, arg=None):
        """
        :param rng: an instant of RNG class
        :param arg: optional arguments
        :returns one realization from the defined probability distribution """

        # abstract method to be overridden in derived classes to process an event
        raise NotImplementedError("This is an abstract method and needs to be implemented in derived classes.")


class Constant (RVG):
    def __init__(self, value):
        RVG.__init__(self)
        self.value = value

    def sample(self, rng, arg=None):
        return self.value


class Exponential(RVG):
    def __init__(self, scale, loc=0):
        """
        E[X] = scale + loc
        Var[X] = scale**2
        """
        RVG.__init__(self)
        self.scale = scale
        self.loc = loc

    def sample(self, rng, arg=None):
        return scipy.expon.rvs(loc=self.loc, scale=self.scale, random_state=rng)


class Bernoulli(RVG):
    def __init__(self, p):
        """
        E[X] = p
        Var[X] = p(1-p)
        """
        RVG.__init__(self)
        self.p = p

    def sample(self, rng, arg=None):
        sample = 0
        if rng.random_sample() <= self.p:
            sample = 1
        return sample


class Beta(RVG):
    def __init__(self, a, b, loc=0, scale=1):
        """
        E[X] = a/(a + b)*scale + loc
        Var[X] = (scale**2) ab/[(a + b)**2(a + b + 1)]
        min[X] = loc
        max[x] = min[X] + scale
        """
        RVG.__init__(self)
        self.a = a
        self.b = b
        self.scale = scale
        self.loc = loc

    def sample(self, rng, arg=None):
        return scipy.beta.rvs(self.a, self.b, self.loc, self.scale, random_state=rng)
