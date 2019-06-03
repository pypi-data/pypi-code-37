# -*- coding: utf-8 -*-

def every_n_fname(idx, n):
    from time_printer import print_time
    if idx%n is 0:
        print_time()
        print idx
        return True


if __name__ =='__main__':
    x = list(range(100))
    for _, val in enumerate(x):
        every_n_fname(_, 10)