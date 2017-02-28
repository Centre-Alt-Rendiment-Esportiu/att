from test.classes.DerivativeQueue import DerivativeQueue
import numpy as np


class BounceQueue(DerivativeQueue):
    def __init__(self, size):
        super(BounceQueue, self).__init__(size)
        self.secondDerivQ = DerivativeQueue(size)
        self.sign = None

    def add_point(self, elem):
        super(BounceQueue, self).add_point(elem)
        self.secondDerivQ.add_point(self[-1] - self[0])

    def has_bounced(self):
        currDerivative = self.secondDerivQ[-1] - self.secondDerivQ[0]
        if self.secondDerivQ.prevDerivative is None:
            self.secondDerivQ.prevDerivative = currDerivative
            return False
        derivSign = np.sign(currDerivative - self.secondDerivQ.prevDerivative)
        if self.sign is None:
            self.sign = derivSign
            return False
        bounced = derivSign * self.sign < 0
        self.sign = derivSign
        self.secondDerivQ.prevDerivative = currDerivative
        return bounced

    def clear(self):
        super(BounceQueue, self).clear()
        self.secondDerivQ.clear()
        self.sign = None
