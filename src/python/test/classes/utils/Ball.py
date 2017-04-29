from test.classes.utils.BallState import PositionState

ballColors = ((0, 255, 0), (255, 0, 0))


class Ball:
    def __init__(self, center):
        self.center = center
        self.is_bounce = False
        self.position_state = PositionState.UNKNOWN

    def get_color(self):
        return ballColors[1 if self.is_bounce else 0]

    def get_size(self):
        return 10 if self.is_bounce else 5
