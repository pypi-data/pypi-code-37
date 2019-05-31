""" place to stash runtime objects. """

import sys
import bot

kernel = bot.Kernel()
users = bot.users.Users()

def cmd(txt):
    e = kernel.cmd(txt)
    e.wait()
    return e

