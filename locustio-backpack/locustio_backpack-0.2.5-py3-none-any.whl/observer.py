
### WIP - This module is imported in __init__ but do not use it yet
### Currently Proof of Concept

from abc import ABC, abstractmethod

class Watcher(object):
    def __init__(self, events):
        self.subscribers = {event: dict()
                            for event in events}

    def get_subscribers(self, event):
        return self.subscribers[event]

    def register(self, event, asker, callback=None):
        if callback is None:
            callback = getattr(asker, 'update')
        self.get_subscribers(event)[asker] = callback

    def unregister(self, event, asker):
        del self.get_subscribers(event)[asker]

    def dispatch(self, event, mod):
        for _, callback in self.get_subscribers(event).items():
            callback(mod)




