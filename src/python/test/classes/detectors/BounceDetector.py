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

    def has_bounced(self):
        if len(self.pointQueue_x) < self.max_size:
            return False
        p, res, rank, sing, rcond = np.polyfit(np.asarray(self.pointQueue_x), np.asarray(self.pointQueue_y), 2, full=True)
        return res > 5.5

    def clear(self):
        self.pointQueue_x.clear()
        self.pointQueue_y.clear()
        self.prev_error = None
