# -*- coding: utf-8 -*-
"""Utility functions."""
import os
import sys
import subprocess


def tryinput(prompt):
    """Try input() and catch KeyboardInterrupts."""
    try:
        output = input(prompt)
    except KeyboardInterrupt:
        print()
        print("Ctrl+C pressed, exiting")
        sys.exit()
    return output


def kwargs_to_dict(kwargs):
    """Return the kwargs dictionary list as a dictionary instead."""
    out_dict = {}
    for key, value in kwargs.items():
        out_dict[key] = value
    return out_dict


def pull_directory(directory, remote_name, git_url, path):
    """Pull a specific directory from the given respository."""
    saved = os.getcwd()
    remote_branch = remote_name + '/master'
    os.chdir(directory)
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'remote', 'add', remote_name, git_url])
    subprocess.call(['git', 'fetch', remote_name])
    subprocess.call(['git', 'checkout', remote_branch, '--', path])
    os.chdir(saved)
    return directory
