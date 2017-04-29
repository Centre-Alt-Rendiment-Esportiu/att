import numpy as np
import cv2


class Neighborhood:
    @staticmethod
    def apply_mask(frame, p1, p2):
        if p1 is None or p2 is None:
            return frame
        height, width = frame.shape[:2]
        neighbor_mask = np.zeros((height, width), np.uint8)
        c1 = np.array([p1.center[0], p1.center[1]])
        c2 = np.array([p2.center[0], p2.center[1]])
        neighbor_mask = cv2.circle(neighbor_mask, p1.center, int(np.linalg.norm(c2-c1)) * 2, 1, -1)
        neighbor_mask = np.dstack(3 * (neighbor_mask,))
        return frame * neighbor_mask
