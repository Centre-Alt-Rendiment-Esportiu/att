import cv2
import numpy as np

min_color = (131, 0, 255)
max_color = (255, 255, 255)
ARC_EPSILON = 0.1


class TableDetector:
    def __init__(self, first_frame):
        height, width = first_frame.shape[:2]
        table_mask = np.zeros((height, width), np.uint8)
        # 1 is table, 0 is background
        self.table_contours = TableDetector.detect(first_frame)
        cv2.fillConvexPoly(table_mask, self.table_contours, 1)
        self.table_mask = np.dstack(3 * (table_mask,))

    def apply(self, frame):
        return frame * self.table_mask

    def is_inside(self, point):
        return cv2.pointPolygonTest(self.table_contours, point, False) >= 0

    @staticmethod
    def detect(frame):
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_hsv, min_color, max_color)
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=5)
        mask = cv2.erode(mask, None, iterations=5)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            sort = sorted(cnts, key=cv2.contourArea, reverse=True)
            cmax = sort[1]
            epsilon = ARC_EPSILON * cv2.arcLength(cmax, True)
            approx = cv2.approxPolyDP(cmax, epsilon, True)
        return approx