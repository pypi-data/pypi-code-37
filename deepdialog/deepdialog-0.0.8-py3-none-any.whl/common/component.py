"""一个基础父类"""


class Component(object):

    def __func__(self, *args, **kwargs):
        return self.forward(args, kwargs)

    def forward(self):
        raise NotImplementedError()
