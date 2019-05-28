from Fortuna import *
from time import time


def monty_tests():
    some_array = tuple(i for i in range(11))
    print("\nQuantum Monty Methods:\n")
    start_qm = time()
    monty = QuantumMonty(some_array)
    distribution_timer(monty.flat_uniform)
    distribution_timer(monty.front_linear)
    distribution_timer(monty.middle_linear)
    distribution_timer(monty.back_linear)
    distribution_timer(monty.quantum_linear)
    distribution_timer(monty.front_gauss)
    distribution_timer(monty.middle_gauss)
    distribution_timer(monty.back_gauss)
    distribution_timer(monty.quantum_gauss)
    distribution_timer(monty.front_poisson)
    distribution_timer(monty.middle_poisson)
    distribution_timer(monty.back_poisson)
    distribution_timer(monty.quantum_poisson)
    distribution_timer(monty.quantum_monty)
    stop_qm = time()
    print("\nLazy Cat: Functional, More General Form of QuantumMonty:\n")
    start_lc = time()
    distribution_timer(lazy_cat, some_array, -5, zero_cool=random_index)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=front_linear)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=middle_linear)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=back_linear)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=quantum_linear)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=front_gauss)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=middle_gauss)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=back_gauss)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=quantum_gauss)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=front_poisson)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=middle_poisson)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=back_poisson)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=quantum_poisson)
    distribution_timer(lazy_cat, some_array, -5, zero_cool=quantum_monty)
    stop_lc = time()

    qm, lc = round(stop_qm - start_qm, 3), round(stop_lc - start_lc, 3)
    print(f"QuantumMonty Class: {qm} sec")
    print(f"LazyCat Function: {lc} sec")


if __name__ == "__main__":
    monty_tests()
