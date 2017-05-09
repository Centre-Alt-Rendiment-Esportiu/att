from test.classes.detectors.BallDetector import BallDetector
from test.classes.detectors.BounceDetector import BounceDetector
from test.classes.detectors.Extrapolator import Extrapolator
from test.classes.utils.BallState import PositionState
from test.classes.utils.Neighborhood import Neighborhood


class BallTracker:
    def __init__(self):
        self.bounce_detector = BounceDetector()
        self.extrapolator = Extrapolator()
        self.ball_detector = None
        self.prev1 = (None, None)
        self.prev2 = (None, None)

    def first_frame(self, first_frame):
        self.ball_detector = BallDetector(first_frame)

    def track(self, frame):
        found_ball = self.ball_detector.detect(frame)
        if found_ball is None:
            prev1_bool = self.prev1[0] is None or (self.prev1[0] is not None and not self.prev1[0].is_extrapolate)
            prev2_bool = self.prev2[0] is None or (self.prev2[0] is not None and not self.prev2[0].is_extrapolate)
            # If previous 2 weren't extrapolates, extrapolate
            if prev1_bool and prev2_bool:
                found_ball = self.extrapolator.extrapolate()

        self.update_detectors(found_ball)

        # Check if prev2 ball has any meaning in terms of distance
        neighborhood = Neighborhood(self.prev1[0], found_ball, factor=3)
        if not neighborhood.is_inside(self.prev2[0]): # or (self.prev1[0] is None and found_ball is None):
            self.prev2 = (None, None)

        found_bounce = self.bounce_detector.find_bounce()
        if found_bounce is not None:
            self.clear()

        ball_to_return, bounce_to_return = self.prev2
        self.prev2 = self.prev1
        self.prev1 = found_ball, found_bounce

        return ball_to_return, bounce_to_return

    def get_bounce(self):
        bounce = self.bounce_detector.find_bounce()
        # if bounce is not None:
        #     bounce.position_state = PositionState.IN \
        #         if self.ball_detector.is_inside_table(bounce.center) \
        #         else PositionState.OUT
        return bounce

    def update_detectors(self, ball):
        self.ball_detector.update_prev(ball)
        # Delete vertical movement
        if self.prev1[0] is not None and ball is not None:
            dx, dy = abs(self.prev1[0].center[0] - ball.center[0]), abs(self.prev1[0].center[1] - ball.center[1])
            if dx < 5 and 2*dx < dy:
                self.clear()
                return  # Vertical movement detected -> Ignore
        self.extrapolator.add_ball(ball)
        self.bounce_detector.add_ball(ball)

    def clear(self):
        self.extrapolator.clear()
        self.bounce_detector.clear()
