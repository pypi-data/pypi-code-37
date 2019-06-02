import numpy as np
import math

# class Cappy239(object):
# def __init__(self): 
#     print('Instance created...')

def normalize(x):
    return ((x - min(x)) / (max(x) - min(x)) - 0.5) * 2


def powernoise(beta, N, varargin='normalize'):
    N2 = int(N / 2 - 1)
    f = np.arange(2, (N2 + 1) + 1, 1)
    A2 = 1.0 / (f ** (beta / 2.0))

    if varargin == 'normalize':
        p2 = (np.random.uniform(0, 1, N2) - 0.5) * 2 * math.pi
        d2 = A2 * np.exp(1j * p2)
    else:
        p2 = np.random.rand(N2) + 1j * np.random.rand(N2)
        d2 = A2 * p2

    d = np.concatenate(([1], d2, [1.0/((N2 + 2.0) ** beta)], np.flipud(np.conjugate(d2))))
    x = np.real(np.fft.ifft(d))

    if varargin == 'normalize':
        x = normalize(x)

    return x

def logistic_map(rho, a0, n):
    a = np.zeros(n)
    a[0] = a0
    for n in range(0, n-1, 1):
        a[n+1] = rho * a[n] * (1 - a[n])
    return a
