"""
Gracefully handle term signals.

Term signals handled by default are: SIGTERM, SIGINT, SIGHUP
"""

import signal
import logging
from functools import partial

TERM_SIGNALS = ["SIGINT", "SIGHUP", "SIGTERM"]

TERM_SIGNAL_RECEIVED = []

log = logging.getLogger(__name__)

class TermSignalException(KeyboardInterrupt):
    """
    Raised when a term signal is received.

    Attributes:
        signame: Name of the signal, e.g. SIGINT
        signum: Number of the signal, e.g. 2 for SIGINT
        frame: Stack frame
    """

    def __init__(self, signame, signum, frame):
        super().__init__("Received %s(%d)" % (signame, signum))

        self.signame = signame
        self.signum = signum
        self.frame = frame

def _handle_term_signal(signame, raise_exc, raise_once, signum, frame):
    """
    Handle the given term signal.
    """

    log.info("Received %s(%d)", signame, signum)

    TERM_SIGNAL_RECEIVED.append((signame, signum))

    if raise_exc:
        if raise_once and len(TERM_SIGNAL_RECEIVED) > 1:
            return

        raise TermSignalException(signame, signum, frame)

def have_received_term_signal():
    """
    Return the list of term signals received.
    """

    return TERM_SIGNAL_RECEIVED

def register_term_signal_handlers(raise_exc, raise_once=True):
    """
    Register term signal handlers.

    Args:
        raise_exc: If True,
            then the registered term signal handlers
            will raise TermSignalException
            when a term signal is received.
        raise_once: If raise_exc is True and raise_once is True,
            then the registered term signal handlers
            will raise TermSignalException
            only the first time a term signal is received.
    """

    for signame in TERM_SIGNALS:
        signum = getattr(signal, signame)
        handler = partial(_handle_term_signal, signame, raise_exc, raise_once)
        signal.signal(signum, handler)
