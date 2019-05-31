#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import time
import re


def version():
    print("0.1")


def function_name(function):
    """Return a printable name for the function"""
    p = re.compile('[ |\.][a-zA-Z0-9_]+? ')
    f = p.findall(str(function))
    f = f[0].strip()
    return f[1:len(f)] + "()"


def stats(fname, fin, loops):
    """Print stats for  function, pass p, l loops"""
    print("FUNCTION " + fname + ". Total runtime = " + str(fin))
    print("for", loops, "loops. Mean loop =", fin/loops, "\n")


def func_compute_time(f, fname, loop):
    """Compute time for each function, pass p, l loops"""
    fname = function_name(f)
    start = time.time()
    for i in range(loop):
        f()
    fin = time.time() - start
    stats(fname, fin, loop)


def compare2(f1, f2, cpass=3, loop=10000):
    """Compare 2 functions f1, f2, cpass passes, loop loops

    Function cannot have parameters
    """
    f1name = function_name(f1)
    f2name = function_name(f2)
    titre = "| Compare " + f1name + " and " + f2name + " |"
    print("\n+" + "-"*(len(titre)-2) + "+")
    print(titre)
    print("+" + "-"*(len(titre)-2) + "+")
    print(str(cpass) + " passes, " + str(loop) + " loops.\n")
    for k in range(cpass):
        print("-- Pass " + str(k+1) + " " + "-"*35)
        func_compute_time(f1, f1name, loop)
        func_compute_time(f2, f2name, loop)


def compare3(f1, f2, f3, cpass=3, loop=10000):
    """Compare 3 functions f1, f2, f3, cpass passes, loop loops

    Function cannot have parameters
    """
    f1name = function_name(f1)
    f2name = function_name(f2)
    f3name = function_name(f3)
    titre = "| Compare " + f1name + ", " + f2name + " and " + f3name + " |"
    print("\n+" + "-"*(len(titre)-2) + "+")
    print(titre)
    print("+" + "-"*(len(titre)-2) + "+")
    print(str(cpass) + " passes, " + str(loop) + " loops.\n")
    for k in range(cpass):
        print("-- Pass " + str(k+1) + " " + "-"*35)
        func_compute_time(f1, f1name, loop)
        func_compute_time(f2, f2name, loop)
        func_compute_time(f3, f3name, loop)
