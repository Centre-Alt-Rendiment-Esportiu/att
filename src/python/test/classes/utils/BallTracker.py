from test.classes.detectors.BallDetector import BallDetector
from test.classes.utils.BallState import PositionState
from test.classes.utils.PolyFitTracker import PolyFitTracker


class BallTracker:
    def __init__(self):
        self.polyfit_tracker = PolyFitTracker()
        self.ball_detector = None

    def first_frame(self, first_frame):
        self.ball_detector = BallDetector(first_frame)

    def track(self, frame):
        found_ball = self.ball_detector.detect(frame)
        if found_ball is None:
            found_ball = self.polyfit_tracker.extrapolate()

        self.polyfit_tracker.add_ball(found_ball)
        self.ball_detector.update_prev(found_ball)

        return found_ball

    def get_bounce(self):
        bounce = self.polyfit_tracker.find_bounce()
        if bounce is not None:
            bounce.position_state = PositionState.IN \
                if self.ball_detector.is_inside_table(bounce.center) \
                else PositionState.OUT
        return bounce

    def clear(self):
        self.polyfit_tracker.clear()