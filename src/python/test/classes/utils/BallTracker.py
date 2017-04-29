import cv2

from test.classes.detectors.BackgroundDetector import BackgroundDetector
from test.classes.detectors.BallDetector import BallDetector
from test.classes.detectors.TableDetector import TableDetector
from test.classes.utils.Ball import Ball
from test.classes.utils.BallState import PositionState
from test.classes.utils.Neighborhood import Neighborhood


class BallTracker(object):
    def __init__(self):
        self.background = BackgroundDetector()
        self.table = None

    def first_frame(self, frame):
        self.table = TableDetector(frame)
        self.background.update(frame)

    def track(self, frame, prev1, prev2):
        # Update background subtraction
        self.background.update(frame)

        # CREATE NEIGHBORHOOD FRAME
        # Circle centered in prev1, with radius 2 * norm(prev2-prev1)
            # if prev1 and prev2 exist, otherwise it leaves frame as it is
        frame_neighborhood = Neighborhood.apply_mask(frame, prev1, prev2)

        # SEARCH INSIDE TABLE

        frame_in_table = self.table.apply_mask(frame_neighborhood)

        cv2.imshow("Background-Subtract Mask", frame_in_table)

        center = BallDetector.inside_detect(frame_in_table)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.IN
            return detected_ball

        # If not found inside table,
        # SEARCH OUTSIDE TABLE

        frame_out_table = frame_neighborhood
        background_sub = self.background.detect(frame_out_table)

        cv2.imshow("Background-Subtract Mask", frame_out_table)

        center = BallDetector.outside_detect(background_sub)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.OUT
            return detected_ball

        # If not found anywhere
        return None
