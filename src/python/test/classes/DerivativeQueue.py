from collections import deque
import numpy as np

THRESHOLD = 0.5


class DerivativeQueue(object):
    def __init__(self, size):
        self.pointQueue = deque(maxlen=size)
        self.dxValue = None

    def add_point(self, elem):
        self.pointQueue.append(np.asarray(elem))

    def has_bounced(self):
        tmpValue = (self.pointQueue[-1][1] - self.pointQueue[0][1]) / \
                   (self.pointQueue[-1][0] - self.pointQueue[0][0] + 1)
        bounced = np.abs(tmpValue - self.dxValue) > THRESHOLD if self.dxValue is not None else False
        self.dxValue = tmpValue
        return bounced

    def clear(self):
        self.pointQueue.clear()
        self.dxValue = None
