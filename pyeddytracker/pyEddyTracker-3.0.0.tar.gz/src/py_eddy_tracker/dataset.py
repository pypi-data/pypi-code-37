from netCDF4 import Dataset as nc_Dataset


class EddyDataset(object):
    __slots__ = (
        '_original_filename',
        '_global_attrs',
        '_dimensions',
        '_dtype',
    )

    def __init__(self):
        self._original_filename = None
        self._global_attrs = None
        self._dimensions = None
        self._dtype = None

    def __getattr__(self, attr):
        if attr in self.dtype.keys():
            with nc_Dataset(self._original_filename, 'r') as h_ori:
                return h_ori.variables[attr][:]
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self), attr))

    def view(self):
        pass

    def _extract(self, mask):
        instance = self.__class__()
        return instance

    @classmethod
    def load(cls, filename):
        eddy_dataset = cls()
        eddy_dataset._original_filename = filename
        return eddy_dataset

    def get_global_attrs(self):
        self._global_attrs = dict()
        if self._original_filename is None:
            pass
        with nc_Dataset(self._original_filename, 'r') as h_ori:
            for attr in h_ori.ncattrs():
                self._global_attrs[attr] = getattr(h_ori, attr)

    def get_dimensions(self):
        self._dimensions = dict()
        if self._original_filename is None:
            pass
        else:
            with nc_Dataset(self._original_filename, 'r') as h_ori:
                for key, value in h_ori.dimensions.items():
                    self._dimensions[key] = len(value)

    def get_dtype(self):
        self._dtype = dict()
        if self._original_filename is None:
            pass
        else:
            with nc_Dataset(self._original_filename, 'r') as h_ori:
                for key, value in h_ori.variables.items():
                    self._dtype[key] = dict(
                        dimensions=value.dimensions,
                        dtype=value.dtype,
                        # fill_value=value.dtype,
                        attrs={attr: getattr(value, attr) for attr in value.ncattrs()}
                    )

    @property
    def dtype(self):
        if self._dtype is None:
            self.get_dtype()
        return self._dtype

    @property
    def dimensions(self):
        if self._dimensions is None:
            self.get_dimensions()
        return self._dimensions

    @property
    def global_attr(self):
        if self._global_attrs is None:
            self.get_global_attrs()
        return self._global_attrs

    def write(self, filename):
        with nc_Dataset(filename, 'w') as h_out:
            for key, value in self.dimensions.items():
                h_out.createDimension(key, value)
            for key, value in self.dtype.items():
                # print value
                h_out.createVariable(
                    varname=key,
                    datatype=value['dtype'],
                    dimensions=value['dimensions'],
                    zlib=True,
                    # fill_value=None,
                )
            for key, value in self.global_attr.items():
                h_out.setncattr(key, value)
