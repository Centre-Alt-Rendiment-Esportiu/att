from collections import deque

from test.classes.detectors.BallInsideSearch import BallInsideSearch
from test.classes.detectors.BallOutsideSearch import BallOutsideSearch
from test.classes.utils.Ball import Ball
from test.classes.utils.BallState import PositionState
from test.classes.utils.Neighborhood import Neighborhood


class BallDetector:
    def __init__(self, first_frame):
        self.inside = BallInsideSearch(first_frame)
        self.outside = BallOutsideSearch(first_frame)
        self.prevs = deque(maxlen=2)
        self.prevs.append(Ball())
        self.prevs.append(Ball())

    def detect(self, frame):
        # Update detectors
        self.update_detectors(frame)

        # CREATE NEIGHBORHOOD FRAME
        # Circle centered in prev1, with radius 2 * norm(prev2-prev1)
        # if prev1 and prev2 exist, otherwise it leaves frame as it is
        neighborhood = Neighborhood(self.prevs[-1], self.prevs[-2], factor=2)
        frame_neighborhood = neighborhood.apply(frame)

        # SEARCH INSIDE TABLE
        in_center = self.inside.search(frame_neighborhood)
        if in_center:
            in_detected_ball = Ball(in_center)
            in_detected_ball.position_state = PositionState.IN
            self.prevs.append(in_detected_ball)
            return in_detected_ball

        # If not found inside table,
        # SEARCH OUTSIDE TABLE

        out_center = self.outside.search(frame_neighborhood)
        if out_center:
            out_detected_ball = Ball(out_center)
            out_detected_ball.position_state = PositionState.OUT
            self.prevs.append(out_detected_ball)
            return out_detected_ball

        # Not found anywhere: return None
        not_found = Ball()
        self.prevs.append(not_found)
        return not_found

    def update_detectors(self, frame):
        self.inside.update(frame)
        self.outside.update(frame)
