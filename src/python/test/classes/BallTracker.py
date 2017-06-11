from test.classes.ball_detector.BallDetector import BallDetector
from test.classes.ball_detector.BounceCalculator import BounceCalculator
from test.classes.ball_detector.Extrapolator import Extrapolator
from test.classes.utils.Ball import Ball
from test.classes.utils.BallHistory import BallHistory


VERTICAL_THRESHOLD = 10


class BallTracker:
    def __init__(self):
        self.track_history = BallHistory()
        self.ball_detector = None
        self.bounce_calculator = BounceCalculator()
        self.extrapolator = Extrapolator()

    def first_frame(self, first_frame):
        self.ball_detector = BallDetector(first_frame)

    def track(self, frame):
        found_ball = self.ball_detector.detect(frame)

        if found_ball.is_none():
            found_ball = self.extrapolator.extrapolate(self.track_history)

        # Remove vertical movement logic

        # If we have no one to compare to, cannot detect vertical movement
        if len(self.track_history) == 0 or self.track_history[-1].is_none() or found_ball.is_none():
            self.track_history.update_history(found_ball)
        else:
            # If we have someone to compare to, look if x coordinates have changed enough
            if abs(self.track_history[-1].center[0] - found_ball.center[0]) < VERTICAL_THRESHOLD:
                self.track_history.update_history(Ball())
            else:
                self.track_history.update_history(found_ball)

        return found_ball

    def get_bounce(self):
        bounce = self.bounce_calculator.find_bounce(self.track_history)
        if not bounce.is_none():
            # Bounces are detected after happening
            after_bounce_ball = self.track_history[-1]
            self.track_history.clear_history()
            self.track_history.update_history(after_bounce_ball)
        # We don't care about outside bounces
        if not self.ball_detector.is_inside_table(bounce):
            return Ball()

        return bounce

    def clear(self):
        self.track_history.clear_history()
        self.ball_detector.clear()
