
import ctypes
import numpy

from vosolvers.vo.constrained import VitaOptimumConstrained
from vosolvers.base import Strategy


class Bcs(VitaOptimumConstrained):
    """Binary Constrained Global Optimization Method"""

    def __init__(self, fobj, dim, ng, nh,
                 nfe=100, np=25, f=0.85, cr=0.2,
                 strategy=Strategy.rand3dir, tol=0.001):
        self._f = f
        self._ng = ng
        self._nh = nh
        self._cr = cr
        self._tol = tol
        VitaOptimumConstrained.__init__(self, fobj, dim, nfe, np, strategy)

    def run(self, restarts = 1, verbose=False):
        """Runs the algorithm"""

        xopt = numpy.zeros(self._dim, dtype=ctypes.c_int)
        conv = numpy.zeros(self._nfe, dtype=ctypes.c_double)
        constr = numpy.zeros(self._ng + self._nh, dtype=ctypes.c_double)

        callback_type = ctypes.PYFUNCTYPE(ctypes.c_double,  # return
                                          ctypes.POINTER(ctypes.c_int),
                                          ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int,
                                          ctypes.POINTER(ctypes.c_double),
                                          ctypes.c_int)

        self._lib.vitaOptimum_Bcs.restype = ctypes.c_double
        self._lib.vitaOptimum_Bcs.argtypes = [ctypes.c_bool,
                                              callback_type,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_int,
                                              ctypes.c_double,
                                              ctypes.c_double,
                                              ctypes.c_int,
                                              ctypes.c_double,
                                              self._array_1d_int,
                                              self._array_1d_double,
                                              self._array_1d_double
                                             ]
        best = self._lib.vitaOptimum_Bcs(verbose,
                                         callback_type(self._fobj),
                                         self._dim,
                                         self._ng,
                                         self._nh,
                                         self._nfe,
                                         self._np,
                                         self._f,
                                         self._cr,
                                         self._strategy.value,
                                         self._tol,
                                         xopt,
                                         constr,
                                         conv)
        return best, xopt, constr, conv

    def _info_lib(self):
        self._lib.vitaOptimum_Bcs_info()

    def _validate(self):
        if not isinstance(self._f, float):
            raise TypeError("The differentiation must be a positive floating-point number")
        if self._f <= 0:
            raise ValueError("The differentiation must be > 0")

        if not isinstance(self._cr, float):
            raise TypeError("The crossover number must be a positive floating-point number")
        if self._cr <= 0 or self._cr >= 1:
            raise ValueError("The crossover number must be in [0, 1]")
