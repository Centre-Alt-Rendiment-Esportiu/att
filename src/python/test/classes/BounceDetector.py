from collections import deque

from test.classes.DerivativeQueue import DerivativeQueue
import numpy as np

"""Represents that queue that stores all info necessary for bounce detection """


class BounceDetector(object):
    def __init__(self, size):
        self.pointQueue = DerivativeQueue(size)
        self.firstDxQueue = DerivativeQueue(size)
        self.secondDxQueue = DerivativeQueue(2)

    def add_point(self, elem):
        self.pointQueue.add_point(elem)
        self.firstDxQueue.add_point(self.pointQueue[-1] - self.pointQueue[0])

    def has_bounced(self):
        currDx2 = self.firstDxQueue[-1] - self.firstDxQueue[0]
        if not self.secondDxQueue:
            self.secondDxQueue.add_point(currDx2)
            return False
        currDifference = currDx2 - self.secondDxQueue[-1]
        prevDifference = self.secondDxQueue[-1] - self.secondDxQueue[0]
        bounced = np.sign(currDifference) < 0 < np.sign(prevDifference)
        self.secondDxQueue.add_point(currDx2)
        return bounced

    def clear(self):
        self.pointQueue.clear()
        self.firstDxQueue.clear()
        self.secondDxQueue.clear()
