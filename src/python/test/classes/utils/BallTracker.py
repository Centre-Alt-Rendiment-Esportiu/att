# import the necessary packages

import cv2

from test.classes.detectors.BallDetector import BallDetector


class BallTracker(object):
    def __init__(self, mask_table):
        self.first_frame = True
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=15, varThreshold=2000, detectShadows=False)
        self.mask_table = mask_table

    def track(self, frame):
        background_filter = self.fgbg.apply(frame)

        # add maskTable to frame
        frame_background_sub = cv2.bitwise_and(frame, frame, mask=background_filter)

        # Reduce vision to table
        # frame_background_sub *= self.mask_table

        # Remove salt and pepper noise
        frame_background_sub = cv2.medianBlur(frame_background_sub, 3)

        cv2.imshow("Background-Subtract Mask", frame_background_sub)

        center = BallDetector.detect(frame_background_sub)
        return center
