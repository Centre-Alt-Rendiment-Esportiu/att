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
        self.prevs.append(None)
        self.prevs.append(None)

    def detect(self, frame):
        # Update detectors
        self.update_detectors(frame)

        # CREATE NEIGHBORHOOD FRAME
        # Circle centered in prev1, with radius 2 * norm(prev2-prev1)
        # if prev1 and prev2 exist, otherwise it leaves frame as it is
        neighborhood = Neighborhood(self.prevs[-1], self.prevs[-2], factor=2)
        frame_neighborhood = neighborhood.apply(frame)

        # SEARCH INSIDE TABLE
        center = self.inside.search(frame_neighborhood)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.IN
            self.prevs.append(detected_ball)
            return detected_ball

        # If not found inside table,
        # SEARCH OUTSIDE TABLE

        center = self.outside.search(frame_neighborhood)
        if center:
            detected_ball = Ball(center)
            detected_ball.position_state = PositionState.OUT
            self.prevs.append(detected_ball)
            return detected_ball

        # Not found anywhere: return None
        self.prevs.append(None)
        return None

    def update_detectors(self, frame):
        self.inside.update(frame)
        self.outside.update(frame)
