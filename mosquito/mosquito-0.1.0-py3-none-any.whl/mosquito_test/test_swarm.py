# Standard library modules.
from time import time
from math import isclose
from itertools import repeat
from unittest import TestCase
from collections import Counter

# Third party modules.
import requests

# Local modules
from mosquito import MosquitoError
from mosquito.swarm import Session, SessionObserver, IdentityFactory, SessionFactory, Swarm
from mosquito_test.utils import httpbin, time_critical

# Globals and constants variables.


class TestSession(TestCase):
    def test_id(self):
        sessions = [Session() for _ in range(5)]

        for i, session in enumerate(sessions):
            self.assertEqual(i, session.id - sessions[0].id)

    def test_update(self):
        # 1. update attributes via kwargs
        # 2. update attributes via args
        # 3. update attributes via both, demonstrating that kwargs dominate
        # 4. update attributes via args using mapping
        args_l = [
            (),
            (dict(headers=dict(foo=42), max_redirects=42.0, auth=('foo', 'bar')),),
            (dict(headers=dict(foo=13), max_redirects=37.0, auth=('bar', 'foo')),),
            ((('headers', dict(foo=42)), ('max_redirects', 42.0), ('auth', ('foo', 'bar')),), )
        ]
        kwargs_l = [
            dict(headers=dict(foo=42), max_redirects=42.0, auth=('foo', 'bar')),
            {},
            dict(headers=dict(foo=42), max_redirects=42.0, auth=('foo', 'bar')),
            {}
        ]

        for args, kwargs in zip(args_l, kwargs_l):
            s = Session()
            s.update(*args, **kwargs)

            self.assertIn('foo', s.headers)
            self.assertIn('user-agent', s.headers)
            self.assertEqual(42, s.headers.get('foo'))

            self.assertIs(int, type(s.max_redirects))
            self.assertEqual(42, s.max_redirects)

            self.assertEqual(('foo', 'bar'), s.auth)

            with self.assertRaises(AttributeError):
                s.update(foo=42)

        s = Session()
        # invalid type of positional argument
        with self.assertRaises(TypeError):
            s.update((None,))

    def test_request(self):
        with Session() as session:
            observer = SessionObserver()
            session.register_observer(observer)

            _ = session.get(httpbin('/get'))

            self.assertEqual(1, observer.count)
            self.assertEqual(1, session.observer.count)


class TestSessionObserver(TestCase):
    @staticmethod
    def generate_response(status_code=200):
        response = requests.Response()

        response.status_code = status_code

        return response

    def test_update_reset(self):
        sessions = [Session() for _ in range(3)]
        sm = SessionObserver()

        for i in range(10):
            sm.update(sessions[i % 3], self.generate_response((i % 2 * 100 + 200)))

        self.assertEqual(10, sm.count)
        self.assertEqual(0., sm.duration)
        self.assertEqual([3, 3, 4], sorted(sm.sessions.values()))
        self.assertEqual(Counter({200: 5, 300: 5}), sm.status_codes)

        sm.reset()

        self.assertEqual(0, sm.count)
        self.assertEqual(0., sm.duration)
        self.assertEqual(Counter(), sm.sessions)
        self.assertEqual(Counter(), sm.status_codes)


class TestIdentityFactory(TestCase):
    def test_identities(self):
        val = lambda: [42]

        if_1 = IdentityFactory({})
        if_2 = IdentityFactory({attr: vals for attr, vals in zip(Session.__attrs__, repeat(val))})
        if_3 = IdentityFactory({attr: vals for attr, vals in zip(Session.__attrs__, repeat(val))},
                               require=Session.__attrs__)
        if_4 = IdentityFactory(dict(foo=42))
        if_5 = IdentityFactory({}, require=['fnord'])
        if_6 = IdentityFactory({}, require=['headers'])

        self.assertEqual([{}], list(if_1))

        for im in (if_2, if_3):
            self.assertEqual(set(Session.__attrs__), set(list(im)[0].keys()))
            self.assertEqual({42}, set(list(im)[0].values()))

        with self.assertRaises(AttributeError):
            _ = list(if_4)

        with self.assertRaises(AttributeError):
            _ = list(if_5)

        with self.assertRaises(MosquitoError):
            _ = list(if_6)


class TestSessionFactory(TestCase):
    def setUp(self):
        self.factory_class = SessionFactory

    def test_sessions(self):
        attributes = dict(params=(dict(foo=i) for i in range(3)))
        sessions = tuple(SessionFactory(attributes))

        self.assertEqual(3, len(sessions))
        for i, session in enumerate(sessions):
            self.assertEqual(dict(foo=i), session.params)
            self.assertIsInstance(session, Session)


class TestSwarm(TestCase):
    def setUp(self):
        Swarm.detach()

    @time_critical
    def test_session_context(self):
        delay = .001
        iters = 32

        with Swarm(delay=delay, headers=[{}] * 4) as swarm:
            t_start = time()

            for i in range(iters):
                with swarm.session():
                    pass

            t_total = time() - t_start

            mean_duration = (t_total / iters) * len(swarm)

            # The above formula is correct only if iters is a multiple of swarm size or infinite
            self.assertEqual(0, iters % len(swarm))

            # ensure delay is hard lower limit
            self.assertLess(delay, mean_duration)

            # tolerance of 25%
            self.assertTrue(isclose(delay, mean_duration, rel_tol=25e-2))

    def test_on_init(self):
        sids = set()

        def init_callback(session):
            sids.add(session.id)

        with Swarm(on_init=init_callback, headers=[{}] * 3):
            pass

        self.assertEqual(3, len(sids))

    def test_open_close(self):
        swarm = Swarm(headers=[{}] * 3)

        self.assertEqual(0, len(swarm))
        with self.assertRaises(MosquitoError):
            with swarm.session():
                pass

        swarm.open()
        with swarm.session():
            pass

        self.assertEqual(3, len(swarm))

        swarm.close()

        self.assertEqual(0, len(swarm))
        with self.assertRaises(MosquitoError):
            with swarm.session():
                pass

        with swarm:
            self.assertEqual(3, len(swarm))
            with swarm.session():
                pass

        self.assertEqual(0, len(swarm))

        with Swarm() as swarm:
            self.assertEqual(1, len(swarm))
