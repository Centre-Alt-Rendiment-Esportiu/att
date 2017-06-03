import cv2
import numpy as np

sensitivity = 15
lower_white = np.array([0, 0, 255 - sensitivity])
upper_white = np.array([255, sensitivity, 255])
ARC_EPSILON = 0.1


class TableDetector:
    def __init__(self, first_frame):
        height, width = first_frame.shape[:2]
        self.in_table, self.out_table = None, None
        self.detect(first_frame)

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

    def detect(self, frame):
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_hsv, lower_white, upper_white)
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((4, 4), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((20, 20), np.uint8))

        cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) >= 2:
            sort = sorted(cnts, key=cv2.contourArea)

            cmin = sort[0]
            epsilon = ARC_EPSILON * cv2.arcLength(cmin, True)
            self.in_table = cv2.approxPolyDP(cmin, epsilon, True)

            cmax = sort[-1]
            epsilon = ARC_EPSILON * cv2.arcLength(cmax, True)
            self.out_table = cv2.approxPolyDP(cmax, epsilon, True)
        else:
            raise Exception
