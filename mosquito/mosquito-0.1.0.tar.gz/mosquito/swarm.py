# Standard library modules.
from queue import Empty
from threading import Lock
from itertools import count
from functools import wraps
from collections import Counter
from contextlib import contextmanager

# Third party modules.
import requests

# Local modules
from mosquito.utils import (
    logger, args_to_kwargs, evaluate, MosquitoError, DelayQueue, SingletonContextABC)


# Globals and constants variables.


class Session(requests.Session):
    """
    Monitorable session object
    """
    __id_counter = count()

    def __init__(self, **kwargs):
        """
        :param kwargs: attributes to be set (see :meth:`update`)
        """
        super().__init__()

        self._id = next(self.__id_counter)
        self._observer = SessionObserver()
        self._observers = [self.observer]

        self.update(kwargs)

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    @property
    def id(self):
        return self._id

    @property
    def observer(self):
        return self._observer

    @args_to_kwargs(ftype='method')
    def update(self, **kwargs):
        """
        Patch attributes of a session. Dict like attributes will be updated. Other attributes are
        casted if possible and then set.

        :param kwargs: attributes to be updated
        """
        for name, value in kwargs.items():
            if name not in self.__attrs__:
                raise AttributeError(
                    f'\'{self.__class__.__name__}\' object has no attribute \'{name}\''
                )

            attr_t = type(getattr(self, name, None))

            # update dict like attributes (dict, cookie jar, ...)
            if hasattr(attr_t, 'update'):
                getattr(self, name).update(value)
                continue

            # set (casted) value
            try:
                setattr(self, name, attr_t(value))

            except TypeError:
                setattr(self, name, value)

    def register_observer(self, observer):
        """
        Attach observer to session.

        :param observer: a session observer instance
        :type observer: SessionObserver
        """
        self._observers.append(observer)

    @wraps(requests.Session.request)
    def request(self, method, url, *args, **kwargs):
        logger.debug(f'{self}: {method} {url}')
        response = super().request(method, url, *args, **kwargs)

        for observer in self._observers:
            observer.update(self, response)

        return response


class SessionObserver:
    """An observer for sessions that collects request statistics."""
    def __init__(self):
        self._lock = Lock()

        self.count = None
        self.duration = None
        self.sessions = None
        self.status_codes = None

        self.reset()

    def __str__(self):
        mean_duration = self.duration / (self.count or 1)
        return \
            f'{self.__class__.__name__}(' \
            f'count={self.count}, ' \
            f'mean_duration={mean_duration:.5f}s, ' \
            f'sessions={self.sessions}, ' \
            f'status_codes={self.status_codes}' \
            f')'

    def reset(self):
        """Reset session observer."""
        with self._lock:
            self.count = 0
            self.duration = 0
            self.sessions = Counter()
            self.status_codes = Counter()

    def update(self, session, response):
        """
        Update session statistics.

        :param session: session object
        :type session: Session
        :param response: response object
        :type response: requests.Response
        """
        with self._lock:
            self.count += 1
            self.duration += response.elapsed.total_seconds()
            self.sessions.update([session.id])
            self.status_codes.update([response.status_code])


class IdentityFactory:
    """Generate session identities from given attributes."""
    def __init__(self, attributes, require=None):
        """
        :param attributes: attributes to generate identities from, usually a dictionary where keys
                           are attribute names and values that evaluate to iterables with actual
                           attribute values
        :param require: container with keys of mandatory attributes
        """
        self._attributes = attributes
        self._require = require

    def __iter__(self):
        # evaluate all attributes
        attributes_dict = {attr: evaluate(value) for attr, value in self._attributes.items()} or {}

        # validate attributes
        for attribute in attributes_dict.keys():
            if attribute not in Session.__attrs__:
                raise AttributeError(f'unknown attribute "{attribute}"')

        # validate requirements
        for attribute in evaluate(self._require) or ():
            if attribute not in Session.__attrs__:
                raise AttributeError(f'unknown attribute "{attribute}"')

            if attribute not in self._attributes:
                raise MosquitoError(f'requirement "{attribute}" is not fulfilled')

        # generate identities
        if attributes_dict:
            keys, values = zip(*attributes_dict.items())

            for i, vals in enumerate(zip(*values)):
                yield dict(zip(keys, vals))

        else:
            yield {}


class SessionFactory(IdentityFactory):
    """Generate request sessions from given attributes."""
    def __iter__(self):
        for attributes in super().__iter__():
            yield Session(**attributes)


class Swarm(SingletonContextABC):
    """
    A swarm is a collection of request sessions that manages initialisation, teardown and access to
    those. Note that there exists only one swarm at a time and manipulation of the swarm object only
    has effects if no swarm context is active.
    """
    __attrs__ = ['on_init', 'delay', 'require', *Session.__attrs__]
    observer = SessionObserver()

    def __init__(self, delay=0., on_init=None, require=None, **session_attributes):
        """
        :param delay: delay for each session that determines max request frequency
        :type delay: float
        :param on_init: call back function to initialize sessions
        :param require: a list of attributes that have to be provided to each session
        :param session_attributes: session attributes
        """
        self._delay = delay
        self._on_init = on_init
        self._session_factory = SessionFactory(session_attributes, require)
        self._lock = Lock()
        self._sessions = None
        self._size = 0

    def __len__(self):
        """Counts items in session queue."""
        with self._lock:
            return self._size

    @contextmanager
    def session(self, timeout=None):
        """
        A context that provides the next available session object. If time passed since the last
        time using that session is less than :attr:`delay` this method blocks.

        :param timeout: max time to wait for session
        :return: session
        :rtype: Session
        """
        if self._sessions is None:
            raise MosquitoError('sessions are available in open swarm context only')

        session = self._sessions.get(timeout)

        try:
            yield session

        finally:
            self._sessions.put(session)

    def __on_open__(self):
        """Initialize sessions."""
        self._sessions = DelayQueue(delay=evaluate(self._delay))

        for session in self._session_factory:
            session.register_observer(self.observer)

            if self._on_init:
                self._on_init(session)

            self._size += 1
            self._sessions.put(session)

        logger.debug(f'opened swarm with {len(self)} sessions')

    def __on_close__(self):
        """Close all sessions."""
        try:
            while True:
                session = self._sessions.get_nowait()
                session.close()

        except Empty:
            pass

        self._size = 0
        self._sessions = None
        logger.debug(f'closed swarm successfully')
