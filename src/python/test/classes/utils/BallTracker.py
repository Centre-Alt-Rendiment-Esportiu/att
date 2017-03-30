# import the necessary packages

import cv2

from test.classes.detectors.BackgroundDetector import BackgroundDetector
from test.classes.detectors.BallDetector import BallDetector


class BallTracker(object):
    def __init__(self, mask_table):
        self.background = BackgroundDetector()
        self.mask_table = mask_table
        self.is_filled = False

    def track(self, frame):
        # Update background subtraction
        self.background.update(frame)

        # Search for ball inside table
        frame_table = frame * self.mask_table
        center = BallDetector.simple_detect(frame_table)
        if center:
            return center

        # If not found, search outside table
        frame_background_sub = self.background.detect(frame)

        cv2.imshow("Background-Subtract Mask", frame_background_sub)

        center = BallDetector.complex_detect(frame_background_sub)
        return center
