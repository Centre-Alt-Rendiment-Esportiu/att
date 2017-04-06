from collections import deque

import numpy as np

"""Represents that queue that stores all info necessary for bounce detection """


class BounceDetector(object):
    def __init__(self, size):
        self.pointQueue_x = deque(maxlen=size)
        self.pointQueue_y = deque(maxlen=size)
        self.max_size = size
        self.prev_error = None

    def add_point(self, elem):
        self.pointQueue_x.append(elem[0])
        self.pointQueue_y.append(elem[1])

    def detect(self):
        if len(self.pointQueue_x) < self.max_size:
            return None
        p, res, rank, sing, rcond = np.polyfit(np.asarray(self.pointQueue_x), np.asarray(self.pointQueue_y), 2, full=True)
        if res < 7:
            return None
        center_x = int(np.rint(self.pointQueue_x[-1] + self.pointQueue_x[-2])/2)
        center_y = int(np.rint(np.polyval(p, center_x)))
        return tuple([center_x, center_y])

    def clear(self):
        self.prev_error = None

        if not self.pointQueue_x:
            return

        last_x = self.pointQueue_x.pop()
        self.pointQueue_x.clear()
        self.pointQueue_x.append(last_x)

        last_y = self.pointQueue_x.pop()
        self.pointQueue_y.clear()
        self.pointQueue_y.append(last_y)
