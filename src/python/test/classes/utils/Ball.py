from test.classes.utils.BallState import PositionState

ballColors = ((0, 255, 0), (255, 0, 0), (51, 102, 0))


class Ball:
    def __init__(self, center=None):
        self.center = center
        self.is_bounce = False
        self.is_extrapolate = False
        self.position_state = PositionState.UNKNOWN

    def get_color(self):
        if self.is_bounce:
            return ballColors[1]
        if self.is_extrapolate:
            return ballColors[2]
        else:
            return ballColors[0]

    def get_size(self):
        if self.is_bounce:
            return 10
        if self.is_extrapolate:
            return 7
        else:
            return 5

    def is_none(self):
        return self.center is None

    def __eq__(self, other):
        return self.center == other.center
