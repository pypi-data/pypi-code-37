import torch
import numpy as np
import math


def error_ee(X, Wp, Wn, lam):
    ker, sqd = ker_ee(X)
    error = Wp.view(-1).dot(sqd.view(-1)) + lam * Wn.view(-1).dot(ker.view(-1))
    return error, ker


def error_ee_from_ker(ker, sqd, Wp, Wn, lam):
    return Wp.view(-1).dot(sqd.view(-1)) + lam * Wn.view(-1).dot(ker.view(-1))


def ker_ee(X):
    sqd = sqdist(X)
    ker = torch.exp(-sqd)
    return ker, sqd


def sqdist(X):
    x = (X ** 2).sum(dim=1, keepdim=True)
    sqd = x - 2 * X @ X.t() + x.t()
    ind = torch.arange(X.shape[0]).tolist()
    sqd[ind, ind] = torch.zeros(
        X.shape[0], device=X.device, dtype=torch.float32)
    return sqd


def error_ee_cpu(X, Wp, Wn, lam):
    mem = 4
    N = X.shape[0]
    # This will fit in mem GB RAM
    B = math.floor((mem * 1024 ** 3) / (2 * N * 8))
    error = 0
    i1 = 0
    i2 = min(N, B)
    X2 = X ** 2
    x2 = X2.sum(axis=1, keepdims=True)

    while i1 < N:
        sqd = X2[i1: i2, :].sum(axis=1, keepdims=True) - \
            2 * X[i1: i2, :] @ X.T + x2.T
        ker = np.exp(-sqd)
        error += Wp[i1: i2, :].reshape(-1).dot(sqd.reshape(-1)) + \
            lam * Wn[i1: i2, :].reshape(-1).dot(ker.reshape(-1))
        i1 = i1 + B
        i2 = min(N, i1 + B)
    return error


def error_ee_cuda(X, Wp, Wn, lam):
    device = X.device
    mem = 2
    N = X.shape[0]
    # This will fit in mem GB RAM
    B = math.floor((mem * 1024 ** 3) / (2 * N * 8))
    error = 0
    i1 = 0
    i2 = min(N, B)
    X2 = X ** 2
    x2 = X2.sum(dim=1, keepdim=True)

    while i1 < N:
        sqd = X2[i1: i2, :].sum(dim=1, keepdim=True) - \
            2 * X[i1: i2, :] @ X.t() + x2.t()
        ker = (-sqd).exp()
        error += Wp[i1: i2, :].to(device).view(-1).dot(sqd.view(-1)) + \
            lam * Wn[i1: i2, :].to(device).view(-1).dot(ker.view(-1))
        i1 = i1 + B
        i2 = min(N, i1 + B)
    return error
