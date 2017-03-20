# import the necessary packages

import cv2

from test.classes.detectors.BallDetector import BallDetector
from test.classes.detectors.TableDetector import TableDetector


class BallTracker(object):
    def __init__(self, height, width):
        self.first_frame = True
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=15, varThreshold=4000, detectShadows=False)
        self.maskTable = None
        self.frameHeight = height
        self.frameWidth = width

    def track(self, frame):
        # first frame detect table
        if self.first_frame:
            self.maskTable = TableDetector.create_table_mask(frame, self.frameHeight, self.frameWidth)
            self.first_frame = False

        background_filter = self.fgbg.apply(frame)
        # background_filter[background_filter > 0] = 255

        # add maskTable to frame
        frame_background_sub = cv2.bitwise_and(frame, frame, mask=background_filter)

        # Reduce vision to table
        # frame_background_sub *= self.maskTable

        # Remove salt and pepper noise
        frame_background_sub = cv2.medianBlur(frame_background_sub, 3)

        # cv2.imshow("Background-Subtract Mask", frame_background_sub)

        center = BallDetector.detect(frame_background_sub)
        return center
