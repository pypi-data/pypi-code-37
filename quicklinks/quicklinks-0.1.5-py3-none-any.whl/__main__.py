import webbrowser
import sys
import os
import argparse
from pathlib import Path


default_file_name = os.path.join(str(Path.home()), '.quicklinks')

def opener():
    with open(default_file_name) as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            try:
                shortcut, domain = line.split(':', 1)
                if shortcut == sys.argv[1]:
                    webbrowser.open(domain, new=0, autoraise=True)
                    return
            except ValueError:
                raise ValueError('u dom')

#
parser = argparse.ArgumentParser(description='will open a website for you')
parser.add_argument('--add', metavar='N', type=str, nargs='+',
                    help='an integer for the accumulator')

if __name__ == '__main__':
    opener()