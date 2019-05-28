from Fortuna import quick_test
from fortuna_extras.range_tests import range_tests
from fortuna_extras.monty_tests import monty_tests
from fortuna_extras.flex_cat_tests import flex_cat_tests


if __name__ == "__main__":

    print("\nFortuna Test Suite: RNG Storm Engine")
    range_tests()
    print(f"\n{'=' * 73}")
    quick_test()
    print(f"\n{'=' * 73}")
    monty_tests()
    print(f"\n{'=' * 73}")
    flex_cat_tests()
