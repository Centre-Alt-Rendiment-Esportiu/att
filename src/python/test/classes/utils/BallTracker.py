from test.classes.detectors.BallDetector import BallDetector
from test.classes.detectors.BounceDetector import BounceDetector
from test.classes.detectors.Extrapolator import Extrapolator
from test.classes.utils.BallHistory import BallHistory


class BallTracker:
    def __init__(self):
        self.ball_history = BallHistory()
        self.ball_detector = None

    def first_frame(self, first_frame):
        self.ball_detector = BallDetector(first_frame)

    def track(self, frame):
        found_ball = self.ball_detector.detect(frame)

        if found_ball.is_none():
            found_ball = Extrapolator.extrapolate(self.ball_history)

        # TODO Remove vertical movement
        self.ball_history.update_history(found_ball)

        return found_ball

    def get_bounce(self):
        bounce = BounceDetector.find_bounce(self.ball_history)
        if not bounce.is_none():
            # Bounces are detected after happening
            after_bounce_ball = self.ball_history[-1]
            self.ball_history.clear_history()
            self.ball_history.update_history(after_bounce_ball)
        # We don't care about outside bounces
        if not self.ball_detector.is_inside_table(bounce):
            return Ball()

        # TODO see if ball's inside or outside table - undo fisheye effect
        # bounce.position_state = PositionState.IN \
        #     if self.ball_detector.is_inside_table(bounce.center) \
        #     else PositionState.OUT
        return bounce

    def clear(self):
        self.ball_history.clear_history()
        self.ball_detector.clear()
