from test.classes.utils.BallState import PositionState

ballColors = ((0, 255, 0), (255, 0, 0))


class Ball:
    def __init__(self, center, is_bounce):
        self.center = center
        self.is_bounce = is_bounce
        self.position_state = PositionState.UNKNOWN

    def get_color(self):
        return ballColors[1 if self.is_bounce else 0]

    def get_size(self):
        return 10 if self.is_bounce else 5

    def set_position_state(self, pos_state):
        self.position_state = pos_state
