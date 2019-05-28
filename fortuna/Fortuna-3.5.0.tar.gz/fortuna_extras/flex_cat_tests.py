from Fortuna import *
from time import time


def flex_cat_tests():
    print("\nFlexCat Test Suite\n")

    some_matrix = {
        "A": (lambda: 1, lambda: 2, lambda: 3),
        "B": (10, 20, 30),
        "C": (100, 200, 300),
    }
    cycles = 1000

    str_zero_cool_dispatch = (
        "front_linear", "middle_linear", "back_linear", "quantum_linear",
        "front_gauss", "middle_gauss", "back_gauss", "quantum_gauss",
        "front_poisson", "middle_poisson", "back_poisson", "quantum_poisson",
        "quantum_monty", "flat_uniform",
    )
    start_fcc = time()
    for v_bias in str_zero_cool_dispatch:
        for k_bias in str_zero_cool_dispatch:
            f_cat = FlexCat(some_matrix, key_bias=k_bias, val_bias=v_bias)
            distribution_timer(f_cat, num_cycles=cycles)
    stop_fcc = time()

    zero_cool_dispatch = (
        front_linear, middle_linear, back_linear, quantum_linear,
        front_gauss, middle_gauss, back_gauss, quantum_gauss,
        front_poisson, middle_poisson, back_poisson, quantum_poisson,
        quantum_monty, random_index,
    )
    start_fcf = time()
    for v_bias in zero_cool_dispatch:
        for k_bias in zero_cool_dispatch:
            distribution_timer(flex_cat, some_matrix, key_bias=k_bias, val_bias=v_bias, num_cycles=cycles)
    stop_fcf = time()

    print(f"FlexCat Class: {round(stop_fcc - start_fcc, 3)} sec")
    print(f"flex_cat Function: {round(stop_fcf - start_fcf, 3)} sec")


if __name__ == "__main__":
    flex_cat_tests()
