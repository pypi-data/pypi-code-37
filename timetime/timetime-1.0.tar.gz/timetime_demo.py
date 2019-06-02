#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from timetime import TimeTime

# Voici les fonctions qu'on veut comparer:
base = "A"


def base_egal_a():
    "Les fonctions à comparer ne doivent pas avoir d'argument"
    if base == "A":
        b = base


def base_in_a():
    if base in "A":
        b = base


def for_i_in_range():
    for i in range(1000):
        b = base


def while_i():
    i = 0
    while i < 1000:
        b = base
        i += 1


# On créé les objet TimeTime:
f1 = TimeTime(base_egal_a)
f2 = TimeTime(base_in_a)

f3 = TimeTime(for_i_in_range)
f4 = TimeTime(while_i)


def demo():
    print("A l'aide de 2 fonctions (base_egal_a et base_in_a), on vérifie ")
    print("si index == \"A\" est plus ou moins rapide que index in \"A\".\n")
    print("Voici les 2 fonctions :")
    print("""
base = "A"

def base_egal_a():
    "Les fonctions à comparer ne doivent pas avoir d'argument"
    if base == "A":
        b = base

def base_in_a():
    if base in "A":
        b = base
""")

    print("On crée donc 2 objet Timetime: f1 = TimeTime(base_egal_a) et ")
    print("f2 = TimeTime(base_in_a). On peut alors faire :\n")
    print("print(f1) puis print(f2) :")
    print(f1)
    print(f2)

    print("\nou print(f1 == f2) :")
    print(f1 == f2)
    print("\nou encore print(f1 < f2) :")
    print(f1 < f2)
    print("\nou enfin print(f1 > f2) :")
    print(f1 > f2)
    print("\nC'est assez semblable, ici.")

    print("""

Essayons maintenant les fonctions:
def for_i_in_range():
    for i in range(1000):
        b = base

def while_i():
    i = 0
    while i < 1000:
        b = base
        i += 1

avec f3 = TimeTime(for_i_in_range) et f4 = TimeTime(while_i)
""")

    print("print(f3)")
    print(f3)
    print("et maintenant: print(f4)")
    print(f4)
    print("ou les commandes de comparaison: print(f3 == f4),")
    print("print(f3 < f4) et ou print(f3 > f4)")
    print(f3 == f4)
    print(f3 < f4)
    print(f3 > f4)

    print("\n\nAttention, si les fonctions renvoie une impression à l'écran,")
    print("cela peut nuire (éventuellement fortement) à la lisibilité. Pour")
    print("contourner ce type de problème, voyez l'exemple du README.md")
    print("sur https://framagit.org/zenjo/timetime/blob/master/README.md")


if __name__ == "__main__":
    demo()
    # code_demo()
