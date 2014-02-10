import multiprocessing as mp
import os
import logging


log = logging.getLogger(__name__)


class DeadActorException(Exception):
    pass


def die(msg="Giving up!"):
    raise RuntimeError(msg)


class Actor(object):
    inbox_size = 4
    SEND_TIMEOUT = 3600 * 4

    def __init__(self, inbox_size=None):
        self.inbox_size = inbox_size or self.inbox_size
        self._q = mp.Queue(maxsize=self.inbox_size)
        self._lock = mp.RLock()
        self._p = None

    def send(self, args):
        log.debug("sending to %r", self)
        self._q.put(args, timeout=self.SEND_TIMEOUT)

    def recv(self, nowait=False):
        log.debug("recv %r", self)
        self._lock.acquire(False) or die(
            "Failed to acquire lock in recv.")
        try:
            if nowait and self._q.empty():
                log.debug("%r empty queue", self)
                return None
            msg = self._q.get()
            log.debug("%r got %r", self, msg)
            return msg
        finally:
            self._lock.release()

    def start(self):
        assert self._p is None
        self._p = mp.Process(target=self._start)
        self._p.daemon = True
        self._p.start()

    def sub_init(self):
        """Initialize stuff in subprocess, called after fork."""
        pass

    def _start(self):
        self.sub_init()
        self._lock.acquire(False) or die(
            "failed to acquire lock in _start")
        log.debug("start %r", self)
        self.process()

    def process(self):
        raise NotImplementedError()

    def check_alive(self):
        if not self._p.is_alive():
            raise DeadActorException("{}:{} is dead".format(self, self._p))

    def __repr__(self):
        return "<%s object at %x pid:%d>" % (type(self).__name__, id(self), os.getpid())


class LActor(Actor):
    """a simple looping actor"""

    STOP = "stop"

    def process(self):
        while self.tick() is not self.STOP:
            pass

    def tick(self):
        raise NotImplementedError()


class CPActor(Actor):
    """An Actor for the Current Process. Doesn't spawn a child."""
    def start(self):
        raise AssertionError("This actor doesn't spawn a process!")

    def process(self):
        pass

    def check_alive(self):
        raise AssertionError("current process actor has no subprocess to check")
