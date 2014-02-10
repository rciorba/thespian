import time

import pytest

from thespian.actor import LActor, DeadActorException


class A(LActor):
    def __init__(self, other):
        super(A, self).__init__()
        self._o = other
        self.count = 10

    def tick(self):
        self.recv()
        self._o.send("pong")
        self.count -= 1
        if self.count == 0:
            return self.STOP


class B(LActor):
    def __init__(self, other):
        super(B, self).__init__()
        self._o = other
        self.count = 10

    def tick(self):
        self._o.send("ping")
        self.recv()
        self.count -= 1
        if self.count == 0:
            return self.STOP

class DeadActor(LActor):
    def __init__(self, other):
        super(DeadActor, self).__init__()
        self._o = other
        self.count = 3

    def tick(self):
        self._o.send("ping")
        self.recv()
        self.count -= 1
        if self.count == 0:
            raise RuntimeError("Fatal exception: FOO is BARed")

def test_actor():
    a = A(None)
    b = B(a)
    a._o = b
    b.start()
    a.start()
    b._p.join()
    a._p.join()
    # if this dind't deadlock, we're happy campers
    # TODO: enhance the assertions

def test_dead_actor():
    a = A(None)
    dead = DeadActor(a)
    a._o = dead
    dead.start()
    a.start()
    a.check_alive()
    with pytest.raises(DeadActorException):
        for _ in xrange(20):
            # this happens asyncronosly; wait for up to 2 seconds
            dead.check_alive()
            time.sleep(.1)
