def test1(self):
    self.context.page['content'] += ' View1'


def test2(self):
    self.context.page['content'] += ' View2'


def test3(self, options):
    self.context.page['content'] += \
        f" View3(a:{options['a']}, b:{options['b']})"


def test4(self, options):
    self.context.page['content'] += \
        f" View4({options})"
