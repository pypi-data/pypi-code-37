#
# qaffeine - prevent inactivity on your computer by simulating key events
#
# Clem Lorteau - 2019-05-31

import sys
import os
import argparse
from threading import Event
from src.UI import UI
from src.KeyPressesSender import KeyPressesSender
from src.__init__ import __version__

def gui():
    UI().start()
    
def cli():
    ap = argparse.ArgumentParser('Prevent computer inactivity by simulating key presses')
    ap.add_argument('-n','--nogui', action='store_true', help='Don\'t start a GUI, only a operate in text mode')
    ap.add_argument('-d', '--delay', type=int, default = 5, help='Delay between key presses in seconds [default: 5] - only valid with --nogui')
    ap.add_argument('-k', '--key', type=str, default='altright', help='Key to press [default: altright]; see keys.txt for a list of valid values - only valid with --nogui')
    ap.add_argument('-v', '--version', action='store_true', help='Show version number and exit')
    args = ap.parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    if args.nogui:
        stopFlag = Event()
        thread = KeyPressesSender(stopFlag, args.key, args.delay)

        thread.start()
        input('Preventing inactivity; press <Enter> to stop...')
        stopFlag.set()

        sys.exit(0)
    
    else:
        gui()

if __name__ == '__main__':
    cli()

        
    
