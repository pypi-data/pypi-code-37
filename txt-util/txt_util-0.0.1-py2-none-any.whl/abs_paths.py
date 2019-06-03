# -*- coding: utf-8 -*-
'''/**
     * created by M. Im 2017-08-03
     */'''


def get_paths(directory):
    import os
    try:
        os.path.exists(directory)
        return list(sorted([os.path.join(directory,f) for f in os.listdir(directory)]))
    except:
        print('Path doesn\'t exists or it is not a directory! ')


def get_file_paths(directory):
    import os
    from os.path import isfile

    try:
        os.path.exists(directory)
        files = [os.path.join(directory,f) for f in os.listdir(directory) ]
        return list(sorted([f for f in files if isfile(f)]))
    except:
        print('Path doesn\'t exists or it is not a directory! ')

def get_file_paths_idx(directory):
    import os
    from os.path import isfile

    try:
        os.path.exists(directory)
        files = [os.path.join(directory,f) for f in os.listdir(directory) ]
        files = list(sorted([f for f in files if isfile(f)]))
        return [(i, f) for i, f in enumerate(files)]
    except:
        print('Path doesn\'t exists or it is not a directory! ')

def get_special_file_paths(directory, extension):
    import os
    from os.path import isfile

    try:
        os.path.exists(directory)
        return list(sorted([os.path.join(directory,f) for f in os.listdir(directory) if bool(f.count(extension))]))
    except:
        print('Path doesn\'t exists or it is not a directory! ')