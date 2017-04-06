import cv2
from test.classes.detectors.TableDetector import TableDetector
from test.classes.detectors.BackgroundDetector import BackgroundDetector
from test.classes.detectors.BallDetector import BallDetector


class BallTracker(object):
    def __init__(self):
        self.background = BackgroundDetector()
        self.mask_table = None

    def first_frame(self, frame):
        height, width = frame.shape[:2]
        self.mask_table = TableDetector.create_table_mask(frame, height, width)
        self.background.update(frame)

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
