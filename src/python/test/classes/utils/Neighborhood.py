import cv2
import numpy as np


class Neighborhood:
    def __init__(self, b1, b2):
        if b1 is None or b2 is None:
            self.center = None
            self.radius = -1
        else:
            c1, c2 = np.array(b1.center), np.array(b2.center)
            self.center = b1.center
            self.radius = int(np.linalg.norm(c2-c1))

    def is_inside(self, b):
        if self.center is None:
            return True
        if b is None:
            return True
        c2 = np.array(b.center)
        return int(np.linalg.norm(c2 - self.center)) <= self.radius

    def apply_to_frame(self, frame):
        if self.center is None:
            return frame
        height, width = frame.shape[:2]
        neighbor_mask = np.zeros((height, width), np.uint8)
        neighbor_mask = cv2.circle(neighbor_mask, self.center, self.radius * 2, 1, -1)
        neighbor_mask = np.dstack(3 * (neighbor_mask,))
        return frame * neighbor_mask
