import cv2
import numpy as np


class Neighborhood:
    def __init__(self, b1, b2, factor):
        if b1 is None or b2 is None:
            self.center = None
            self.radius = -1
            self.factor = -1
        else:
            c1, c2 = np.array(b1.center), np.array(b2.center)
            self.center = tuple([int(b1.center[0]), int(b1.center[1])])
            self.radius = int(np.linalg.norm(c2 - c1))
            self.factor = int(factor)

    def is_inside(self, b):
        if self.center is None:
            return True
        if b is None:
            return True  # Indifferent really
        c2 = np.array(b.center)
        return int(np.linalg.norm(c2 - self.center)) <= self.radius * self.factor

    def apply(self, frame):
        if self.center is None:
            return frame
        height, width = frame.shape[:2]
        neighbor_mask = np.zeros((height, width), np.uint8)
        neighbor_mask = cv2.circle(neighbor_mask, self.center, self.radius * self.factor, 1, -1)
        neighbor_mask = np.dstack(3 * (neighbor_mask,))
        return frame * neighbor_mask
