from .error import error_ee


def ls_ee(X, Wp, Wn, lam, P, ff, G, alpha0=1, rho=0.8, c=1e-1):
    """Backtracking line search for EE

    Reference: procedure 3.1, p. 41ff in:
        Nocedal and Wright: "Numerical Optimization", Springer, 1999.
    """

    alpha = alpha0
    tmp = c * G.view(-1).dot(P.view(-1))
    e, ker = error_ee(X + alpha * P, Wp, Wn, lam)
    while e > ff + alpha * tmp:
        alpha = rho * alpha
        e, ker = error_ee(X + alpha * P, Wp, Wn, lam)

    Xnew = X + alpha * P

    return Xnew, e, ker, alpha
