from .error import sqdist


def gradient_ee(X, Lp, Wn, lam):
    ker = (-sqdist(X)).exp()
    WWn = lam * Wn * ker
    DDn = WWn.sum(dim=1).diagflat()
    return (4 * (Lp + WWn - DDn)) @ X
