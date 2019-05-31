#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8


def demo():
    import timetime

    base = "A"

    # On va comparer l'efficience de ces 2 fonctions
    def base_egal_a():
        "Les fonctions à comparer ne doivent pas avoir d'argument"
        if base == "A":
            b = base

    def base_in_a():
        if base in "A":
            b = base

    timetime.compare2(base_egal_a, base_in_a)
    # compare2(f1, f2, cpass=3 (default), loop=10000 (default))

    # On va comparer l'efficience de ces 3 fonctions
    def for_in_ennumerate():
        a = 0
        for i, j in enumerate(range(10000)):
            a = i

    def for_in_range():
        a = 0
        for i in range(10000):
            a = i

    def while_i():
        i = 0
        a = 0
        while i < 10000:
            a = i
            i += 1

    timetime.compare3(for_in_ennumerate, for_in_range, while_i, 2, 1000)
    # compare3(f1, f2, f3, nb_passes, nb_loops)


def code_demo():
    print("""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import timetime

base = "A"

# On va comparer l'efficience de ces 2 fonctions
def base_egal_a():
    "Les fonctions à comparer ne doivent pas avoir d'argument"
    if base == "A":
        B = base

def base_in_a():
    if base in "A":
        B = base

timetime.compare2(base_egal_a, base_in_a)
# compare2(f1, f2, cpass=3 (default), loop=10000 (default))

# On va comparer l'efficience de ces 3 fonctions
def for_in_ennumerate():
    a=0
    for i, j in enumerate(range(10000)):
        a=i

def for_in_range():
    a = 0
    for i in range(10000):
        a = i

def while_i():
    i=0
    a = 0
    while i < 10000:
        a = i
        i+=1

timetime.compare3(for_in_ennumerate, for_in_range, while_i, 2, 1000)
# compare3(f1, f2, f3, nb_passes, nb_loops)
    """)


if __name__ == "__main__":
    demo()
    # code_demo()
