import cv2
import numpy as np

ARC_EPSILON = 0.1


class TableDetector:
    def __init__(self, white_mask):
        height, width = white_mask.shape[:2]
        self.in_table, self.out_table = None, None
        self.detect(white_mask)

        # 1 is table, 0 is background
        in_table_mask = np.zeros((height, width), np.uint8)
        cv2.fillConvexPoly(in_table_mask, self.in_table, 1)
        self.in_table_mask = np.dstack(3 * (in_table_mask,))

        out_table_mask = np.zeros((height, width), np.uint8)
        cv2.fillConvexPoly(out_table_mask, self.out_table, 1)
        self.out_table_mask = np.dstack(3 * (1 - out_table_mask,))

    def apply_inside(self, frame):
        return frame * self.in_table_mask

    def apply_outside(self, frame):
        return frame * self.out_table_mask

    def is_inside(self, point):
        return cv2.pointPolygonTest(self.in_table, point, False) >= 0

    def detect(self, white_mask):
        open_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))
        close_mask = cv2.morphologyEx(open_mask, cv2.MORPH_CLOSE, np.ones((20, 20), np.uint8))

        cnts = cv2.findContours(close_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) >= 2:
            sort = sorted(cnts, key=cv2.contourArea, reverse=True)

            cmax = sort[0]
            epsilon = ARC_EPSILON * cv2.arcLength(cmax, True)
            self.out_table = cv2.approxPolyDP(cmax, epsilon, True)

            cmax2 = sort[1]
            epsilon = ARC_EPSILON * cv2.arcLength(cmax2, True)
            self.in_table = cv2.approxPolyDP(cmax2, epsilon, True)
        else:
            raise Exception
