import cv2
import numpy as np


class Neighborhood:
    @staticmethod
    def apply(frame, p1, p2):
        if p1 is None or p2 is None:
            return frame
        height, width = frame.shape[:2]
        neighbor_mask = np.zeros((height, width), np.uint8)
        c1 = np.array(p1)
        c2 = np.array(p2)
        neighbor_mask = cv2.circle(neighbor_mask, p1, int(np.linalg.norm(c2-c1)) * 2, 1, -1)
        neighbor_mask = np.dstack(3 * (neighbor_mask,))
        return frame * neighbor_mask
