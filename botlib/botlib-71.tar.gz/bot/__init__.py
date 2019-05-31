""" bot package. """

__version__ = 71

import logging
import os
import sys
import stat
import threading

import bot
import obj

class Cfg(obj.Cfg):

    pass

class Event(obj.event.Event):

    def show(self):
        if not self._result:
            return
        for txt in self._result:
            bot.run.kernel.say(self.orig, self.channel, txt)
        b = bot.run.kernel.get_bot(self.orig)
        if b and "_prompted" in dir(b):
            b._prompted.set()


class Bot(obj.handler.Handler):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._prompted = threading.Event()
        self.cfg = Cfg()
        self.cfg.update(kwargs)
        self.channels = []
        self.state = obj.Object()
        self.verbose = True

    def announce(self, txt):
        for channel in self.channels:
             self.say(channel, txt)

    def cmd(self, txt, options="", origin=""):
        self.start()
        e = Event()
        e.txt = txt
        e.orig = repr(self)
        e.options = options
        e.origin = origin or "root@shell"
        self.dispatch(e)
        self.ready()
        return e

    def dispatch(self, event):
        e = Event()
        e.update(event)
        return super().dispatch(e)

    def fileno(self):
        import sys
        return sys.stdin

    def join(self):
        pass

    def raw(self, txt):
        print(txt)

    def resume(self):
        pass

    def say(self, botid, channel, txt):
        if self.verbose:
            self.raw(txt)

    def start(self):
        super().start()
        bot.run.kernel.add(self)

class Console(obj.shell.Console):

    def get_event(self):
        """ return an event from a typed string. """
        e = Event()
        self._prompted.wait()
        e.txt = input("> ")
        self._prompted.clear()
        e.orig = repr(self)
        e.origin = "root@shell"
        return e

class Fleet(obj.Object):

    def __init__(self):
        super().__init__()
        self.bots = []

    def __iter__(self):
        return iter(self.bots)

    def add(self, bot):
        logging.warn("add %s" % obj.get_name(bot))
        self.bots.append(bot)
        return self

    def announce(self, txt):
        for bot in self.bots:
            bot.announce(str(txt))

    def by_type(self, btype):
        res = None
        for bot in self.bots:
            if str(btype).lower() in str(type(bot)).lower():
                res = bot
        return res

    def get_bot(self, bid):
        res = None
        for bot in self.bots:
            if str(bid) in repr(bot):
                res = bot
                break
        return res

    def get_firstbot(self):
        return self.bots[0]

    def match(self, m):
        res = None
        for bot in self.bots:
            if m.lower() in repr(bot):
                res = bot
                break
        return res

    def remove(self, bot):
        self.bots.remove(bot)

    def save(self):
        for bot in self.bots:
            bot.save()

    def say(self, botid, channel, txt):
        bot = self.get_bot(botid)
        if bot:
            bot.say(botid, channel, txt)

    def stop(self):
        for bot in self.bots:
            bot.stop()

    def wait(self):
        for bot in self.bots:
            bot.wait()

class Kernel(Fleet, obj.handler.Handler, obj.Store):

    def __init__(self):
        super().__init__()
        self.cfg = Cfg()

    def initialize(self, mods):
        """ initialize modules. """
        res = []
        thrs = []
        exclude = obj.cfg.exclude.split(",")
        for m in mods:
            if not m or m in exclude:
                continue
            logging.warn("init %s" % m)
            try:
                thrs = self.walk(m, True)
                for thr in thrs:
                    thr.join()
            except Exception as ex:
                logging.error(obj.get_exception())

    def start(self):
        """ start the kernel. """
        self.cfg.update(obj.cfg)
        if self.cfg.args:
            self.cfg.verbose = False
        super().start()

    def tail(self):
        """ wait for kernel to finish. """
        if self.cfg.args:
            self.cfg.verbose = False
            e = obj.cmd(" ".join(self.cfg.args))
            for txt in e._result:
                print(txt)
            return e
        if self.cfg.shell:
            c = Console()
            c.start()
            c.verbose = (not self.cfg.verbose) or True
            self.add(c)
            super().wait()

def start(name="botlib", modules=[], version=bot.__version__, wd=obj.hd(".botlib"), shell=False):
    obj.shell.termsave()
    try:
        obj.shell.parse_cli(name, version=version, wd=wd)
        obj.cfg.shell = (not obj.cfg.shell) or shell
        if modules:
            obj.cfg.modules += "," + ",".join(modules) 
        k = bot.run.kernel
        k.initialize(obj.cfg.modules.split(","))
        k.start()
        k.tail()
    except KeyboardInterrupt:
        print("")
    except Exception as ex:
        logging.error(obj.get_exception())
    obj.shell.reset()
    os._exit(0)

import bot.cmds
import bot.entry
import bot.irc
import bot.users
import bot.run
