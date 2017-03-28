# import the necessary packages

import cv2

from test.classes.detectors.BallDetector import BallDetector


class BallTracker(object):
    def __init__(self, mask_table):
        self.first_frame = True
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=16, detectShadows=False)
        self.mask_table = mask_table

    def track(self, frame):
        # Update background subtractor
        background_filter = self.fgbg.apply(frame)

        # Search for ball inside table
        frame_table = frame * self.mask_table
        center = BallDetector.detect(frame_table)
        if center:
            return center

        # If not found, search outside table

        # Remove salt and pepper noise
        median_frame = cv2.medianBlur(background_filter, 3)

        # Apply background substracted frame
        frame_background_sub = cv2.bitwise_and(frame, frame, mask=median_frame)

        # Reduce vision to table
        cv2.imshow("Background-Subtract Mask", frame_background_sub)

        center = BallDetector.detect(frame_background_sub)
        return center
