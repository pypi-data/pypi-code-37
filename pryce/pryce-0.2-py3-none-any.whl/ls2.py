import numpy as np
from smolyak.applications.polynomials.polynomial_approximation import PolynomialSpace as PS
from smolyak.applications.polynomials.polynomial_approximation import PolynomialApproximation as PA


def ls2(model, k, M, **kwargs):
    '''
    Compute American option prices using the Longstaff--Schwartz algorithm

    :param model: Market model
    :type model: Function that generates random market trajectories
    :param k: Polynomial degree
    :param M: Number of random market trajectories to be used in optimization
    '''
    poly_space = PS(n = model.d_eff, k = k)
    securities, times = model(M)
    N = model.N
    poly_continuation = lambda x: -np.inf*np.ones(M)
    coeff_payoff = 1
    coeff_poly = np.zeros(poly_space.dimension)
    coeffs = [coeff_poly]
    C = np.zeros(M)
    C = model.payoff(securities[-1])
    for i in range(N-2, -1, -1):
        print(f'{10+(N-2-i)/(N-2)*60:.0f}%',end='\r')
        C*=np.exp(-model.r*(times[i+1]-times[i]))
        x = securities[i, ...]
        payoffs = model.payoff(x)
        xx = x[payoffs>0]
        yy = C[payoffs>0]
        coeff_poly, *_ = poly_space.weighted_least_squares(
            X=xx,
            Y=yy,
            #basis_extension=lambda x: model.payoff(x).reshape(-1, 1)
        )
        poly_continuation = PA(poly_space, coeff_poly)
        expect = poly_continuation(x)
        would_exercise = (payoffs > expect) & (payoffs>0)
        C[would_exercise] = payoffs[would_exercise]
        coeffs.append(coeff_poly)
    v_train = np.mean(C)
    securities, times = model(M)
    stopped = np.zeros(M, dtype = bool)
    gain = np.nan*np.zeros(M)
    for i in range(N):
        print(f'{80+20*i/(N-1):.0f}%',end='\r')
        payoffs = model.payoff(securities[i])
        coeff_poly  = coeffs[~i]
        continuation_value = PA(poly_space, coeff_poly)(securities[i, ...])
        stop = (payoffs > continuation_value) & (payoffs>0)
        gain[~stopped & stop] = np.exp(-model.r*times[i])*payoffs[~stopped & stop]
        stopped |= stop
    gain[~stopped] = np.exp(-model.r*times[-1])*payoffs[~stopped]
    return np.mean(gain), np.std(gain)/np.sqrt(M), v_train, np.exp(-model.r*model.T)*np.mean(payoffs)
