import cv2
import numpy as np

min_color = (131, 0, 255)
max_color = (255, 255, 255)
ARC_EPSILON = 0.1


class TableDetector:
    @staticmethod
    def create_outer_mask(frame, height, width):
        maskTable = np.zeros((height, width), np.uint8)
        # 0 is table, 1 is background
        tableContours = TableDetector.detect_outer(frame)
        cv2.fillConvexPoly(maskTable, tableContours, 1)
        maskTable = np.dstack(3 * (maskTable,))
        return maskTable

    @staticmethod
    def create_inner_mask(frame, height, width):
        maskTable = np.zeros((height, width), np.uint8)
        # 0 is table, 1 is background
        tableContours = TableDetector.detect_inner(frame)
        cv2.fillConvexPoly(maskTable, tableContours, 1)
        maskTable = np.dstack(3 * (maskTable,))
        return maskTable

    @staticmethod
    def detect_outer(frame):
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame_hsv, min_color, max_color)
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=5)
        mask = cv2.erode(mask, None, iterations=5)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts) > 0:
            sort = sorted(cnts, key=cv2.contourArea, reverse=True)
            cmax = sort[0]
            epsilon = ARC_EPSILON * cv2.arcLength(cmax, True)
            approx = cv2.approxPolyDP(cmax, epsilon, True)
        return approx

    @staticmethod
    def detect_inner(frame):
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