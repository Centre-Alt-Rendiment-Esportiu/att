import cv2
from test.classes.detectors.TableDetector import TableDetector
from test.classes.detectors.BackgroundDetector import BackgroundDetector
from test.classes.detectors.BallDetector import BallDetector
from test.classes.utils.Ball import Ball
from test.classes.utils.BallState import PositionState


class BallTracker(object):
    def __init__(self):
        self.background = BackgroundDetector()
        self.mask_inner_table = None
        self.mask_outer_table = None

    def first_frame(self, frame):
        height, width = frame.shape[:2]
        self.mask_inner_table = TableDetector.create_inner_mask(frame, height, width)
        self.mask_outer_table = TableDetector.create_outer_mask(frame, height, width)
        self.background.update(frame)

    def track(self, frame):
        # Update background subtraction
        self.background.update(frame)

        # SEARCH INSIDE TABLE

        frame_in_table = frame * self.mask_inner_table
        center = BallDetector.inside_detect(frame_in_table)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.IN
            return detected_ball

        # If not found
        # SEARCH OUTSIDE TABLE

        frame_out_table = frame - frame * self.mask_inner_table
        background_sub = self.background.detect(frame_out_table)

        cv2.imshow("Background-Subtract Mask", background_sub)

        center = BallDetector.outside_detect(background_sub)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.OUT
            return detected_ball
        return None
