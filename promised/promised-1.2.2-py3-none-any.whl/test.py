class Member(dict):
    """
    A map of cached properties per input key which will cache a property for that key when first accessed.

    What is a Member? It is a mapping instance with similar usage to the @promise decorator which will call:
        self._getter(key, *self._args, **self._kwargs)
    and set the mapped value of key to the return from that call if key is not already mapped, and will always return
    the mapped value of that key.

    Why? This is very similar to the need memoization fulfills, but I wanted to treat these cached values as if they
    were any other attribute in a mapping property and planned to use a small set of possible inputs to access them
    multiple times.

    As they could potentially change after being initially set just like @promise properties, it could have been wiser
    to set the values as a promise within the input objects - but, as the attribute was purely for functions within
    the calling instance, this was a useful tool.

    What is self._getter? self._getter is the first argument in __init__ - it should take key as an argument, and return
    the calculated value for that key. Additionally, the optional *args and **kwargs from __init__ are provided as
    arguments to self._getter. (if provided)

    This gives rise to some interesting patterns for similar attributes as well, for example:

        def _children_of_parent_with_attribute_value(self, parent, child_attribute_value):
            return self.parent_children_map[parent] & self.attribute_value_to_set_of_objects_map[child_attribute_value]

        @promise
        def homeless_children(self):
            self._homeless_children = Member(self._children_of_parent_with_attribute_value, "homeless")

        @promise
        def adult_children(self):
            self._adult_children = Member(self._children_of_parent_with_attribute_value, "The White House")

    Getting all homeless children of an object would then be a readily available attribute as
    self.homeless_children[object], and any inner workings for finding and caching those matches is handled by the
    promise and Member decorators. Meanwhile, no calculations for unnecessary properties or members are done.
    """
    def __init__(self, getter, *args, **kwargs):
        super().__init__()
        self._args = args
        self._kwargs = kwargs
        self._getter = getter

    def __missing__(self, key):
        value = self._getter(key, *self._args, **self._kwargs)
        self.update({key: value})
        return value


class Test(object):
    def test_getter(self, value):
        return str(value)

    @property
    def membering(self):
        try:
            return self._membering
        except AttributeError:
            self._membering = Member(self.test_getter)
            return self._membering


def main():
    test = Test()
    print(test.membering)
    one = test.membering[1]
    print(one)
    print(test.membering)


if __name__ == "__main__":
    main()
