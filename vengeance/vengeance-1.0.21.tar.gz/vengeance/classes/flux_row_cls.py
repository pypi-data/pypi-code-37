
from collections import OrderedDict
from collections import namedtuple


class flux_row_cls:

    class_names = {'_headers',
                   'is_bound',
                   'values'}

    def __init__(self, headers, values):
        """
        :param headers: OrderedDict of {'header': index}
        :param values:  list of underlying data

        headers is a single dictionary passed byref from the
        flux_cls to all flux_row_cls instances, reducing unneccesary
        memory usage and allowing all mapping updates to be made
        instantaneously

        namedtuples may be more efficient, but too much of a headache to deal
        with their immutability

        self.__dict__ is used to set attributes in __init__ so as to avoid
        premature __setattr__ lookups
        """
        self.__dict__['_headers'] = headers
        self.__dict__['values']   = values
        self.__dict__['is_bound'] = False

    @property
    def names(self):
        return list(self._headers.keys())

    @property
    def view_as_array(self):
        """ for development purposes; used purely to trigger a debugging feature in PyCharm

        PyCharm will recognize returned the (name, value) pairs as an ndarray
        and enable the "...view as array" option in the debugger which displays
        values in a special window
        """
        import numpy
        return numpy.transpose([self.names, self.values])

    def dict(self):
        return OrderedDict(zip(self.names, self.values))

    def namedtuples(self):
        try:
            nt_cls = namedtuple('flux_row_nt', self.names)
            return nt_cls(*self.values)
        except ValueError as e:
            import re

            names = [n for n in self.names
                       if re.search('^[^a-z]|[ ]', n, re.IGNORECASE)]
            raise ValueError("invalid headers for namedtuple: {}".format(names)) from e

    def bind(self):
        """ bind headers / values directly to instance, avoiding need for subsequent __getattr__ lookups
        (only use this if you know the side-effects)
        """
        if self.__dict__['is_bound']:
            return

        self.__dict__.update(zip(self.names, self.values))

        self.__dict__['values']   = '(values bound to __dict__)'
        self.__dict__['is_bound'] = True

    def unbind(self, names=None):
        if not self.__dict__['is_bound']:
            return

        if names is None:
            names = self.__dict__.keys() - self.class_names

        values = self.__dict__['values'] = []
        for k in names:
            v = self.__dict__.pop(k)
            values.append(v)

        self.__dict__['is_bound'] = False

    def __getattr__(self, name):
        """  eg:
             v = row.header
        """
        try:
            i = self._headers.get(name, name)
            return self.values[i]
        except (TypeError, IndexError) as e:
            raise AttributeError(self.__attr_err_msg(name)) from e

    def __getitem__(self, name):
        """ eg:
            v = row['header']

        name is converted to an integer, which is then used to reference self.values

        (if name is already an integer, it's faster to use row.values[i])
        (if name is a slice, it should be called directly on row.values)
        """
        try:
            i = self._headers.get(name, name)
            return self.values[i]
        except (TypeError, IndexError) as e:
            raise AttributeError(self.__attr_err_msg(name)) from e

    def __setattr__(self, name, value):
        """ eg:
            row.header = v
        """
        if name in self.__dict__:               # a property directly on flux_row_cls
            self.__dict__[name] = value
            return

        try:
            i = self._headers.get(name, name)
            self.values[i] = value
        except (TypeError, IndexError) as e:
            raise AttributeError(self.__attr_err_msg(name)) from e

    def __setitem__(self, name, value):
        """ eg:
            row['header'] = v

        name is converted to an integer, which is then used to reference self.values

        (if name is already an integer, it's faster to use row.values[i])
        (if name is a slice, it should be called directly on row.values)
        """
        try:
            i = self._headers.get(name, name)
            self.values[i] = value
        except (TypeError, IndexError) as e:
            raise AttributeError(self.__attr_err_msg(name)) from e

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        super().__setattr__('__dict__', d)

    def __attr_err_msg(self, name):
        if isinstance(name, slice):
            return 'slice should be used on row.values\n(eg, row.values[2:5], not row[2:5])'

        names = '\n\t'.join(self.names)
        return "No flux_row_cls column named '{}'\navailable columns:\n\t{}".format(name, names)

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        i = self.__dict__.get('i')
        if i is not None:
            i = '({:,})  '.format(i)
        else:
            i = ''

        return 'flux_row  {}{}'.format(i, repr(self.values))


class lev_row_cls(flux_row_cls):

    class_names = {'_headers',
                   'is_bound',
                   'values',
                   'address'}

    def __init__(self, headers, values, address):
        super().__init__(headers, values)
        self.__dict__['address'] = address

    def __repr__(self):
        return self.address + ' ' + repr(self.values)
