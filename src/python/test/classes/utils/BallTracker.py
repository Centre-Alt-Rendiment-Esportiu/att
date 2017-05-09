from test.classes.detectors.BallDetector import BallDetector
from test.classes.detectors.BounceDetector import BounceDetector
from test.classes.detectors.Extrapolator import Extrapolator


class BallTracker:
    def __init__(self):
        self.bounce_detector = BounceDetector()
        self.extrapolator = Extrapolator()
        self.ball_detector = None

    def first_frame(self, first_frame):
        self.ball_detector = BallDetector(first_frame)

    def track(self, frame):
        found_ball = self.ball_detector.detect(frame)

        # TODO Limit extrapolations
        if found_ball is None:
            found_ball = self.extrapolator.extrapolate()

        self.update_detectors(found_ball)

        return found_ball

    def get_bounce(self):
        bounce = self.bounce_detector.find_bounce()
        # TODO see if ball's inside or outside table - undo fisheye effect
        # if bounce is not None:
        #     bounce.position_state = PositionState.IN \
        #         if self.ball_detector.is_inside_table(bounce.center) \
        #         else PositionState.OUT
        return bounce

    def update_detectors(self, ball):
        # TODO Delete vertical movement
        self.extrapolator.add_ball(ball)
        self.bounce_detector.add_ball(ball)

    def clear(self):
        self.extrapolator.clear()
        self.bounce_detector.clear()
