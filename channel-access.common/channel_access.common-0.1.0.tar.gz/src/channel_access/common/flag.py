import enum



class Flag(enum.Enum):
    """ A simple flag class with support for binary operations.

    In order to function correctly all possible bit combinations
    must exist as members.
    """
    def __contains__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return other._value_ & self._value_ == other._value_

    def __bool__(self):
        return bool(self._value_)

    def __or__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value_ | other._value_)

    def __and__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value_ & other._value_)

    def __xor__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value_ ^ other._value_)


def is_power_two(value):
    return value == 2**(value.bit_length() - 1)

def create_flag(name, members):
    # Create all possible members and use them with an enum which supports
    # the binary operators
    max_value = 0
    for n, v in members:
        max_value |= v

    names = { v: n for n, v in members }

    new_members = []
    for value in range(max_value + 1):
        if value in names:
            new_members.append((names[value], value))
        else:
            member_parts = []
            for n, v in members:
                if is_power_two(v) and value & v:
                    member_parts.append(n)
            new_members.append(('-'.join(member_parts), value))

    return Flag(name, new_members)
