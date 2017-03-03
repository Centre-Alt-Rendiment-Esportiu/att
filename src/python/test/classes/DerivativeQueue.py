from collections import deque
import numpy as np

""" Represents the queue that stores accumulated derivatives history """


class DerivativeQueue(object):
    def __init__(self, size):
        self.pointQueue = deque(maxlen=size)

    def add_point(self, elem):
        self.pointQueue.append(elem)

    def clear(self):
        self.pointQueue.clear()

    def __getitem__(self, item):
        return self.pointQueue[item]

    def __len__(self):
        return len(self.pointQueue)
