import cv2
import numpy as np

from test.classes.detectors.TableDetector import TableDetector

"""Class that represents the inside table search algorithm"""

sensitivity = 15
lower_white = np.array([0, 0, 255 - sensitivity])
upper_white = np.array([255, sensitivity, 255])


class BallInsideSearch:
    def __init__(self, first_frame):
        self.table = TableDetector(first_frame)

    def search(self, frame):
        # Restrict frame to table
        frame_in_table = self.table.apply(frame)
        # Create ball mask to apply
        hsv = cv2.cvtColor(frame_in_table, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        # Find white contour with greatest area
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        # Only proceed if at least one contour was found
        if len(cnts) > 0:
            cmax = max(cnts, key=cv2.contourArea)
            M = cv2.moments(cmax)
            if M["m00"] > 0:
                center = tuple([M["m10"] / M["m00"], M["m01"] / M["m00"]])
        return center

    def update(self, frame):
        pass
