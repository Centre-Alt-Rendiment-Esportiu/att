from collections import deque

lineColors = ((0, 0, 255), (0, 255, 255))

""" Class that represents the ball's position history"""


class BallHistory:
    def __init__(self):
        self.balls = deque(maxlen=16)
        self.direction = 0

    def check_direction_change(self, ball):
        center = ball.center
        if len(self) > 0:
            if (self[0].center[0] - center[0]) < 0 and self.direction != 0:
                self.change_direction()
                return True
            elif (self[0].center[0] - center[0]) > 0 and self.direction != 1:
                self.change_direction()
                return True
        return False

    def change_direction(self):
        self.direction = 1 - self.direction
        self.clear_history()

    def update_history(self, ball):
        if ball is None:
            return
        self.balls.appendleft(ball)

    def clear_history(self):
        self.balls.clear()

    def line_color(self):
        return lineColors[self.direction]

    def __len__(self):
        return len(self.balls)

    def __getitem__(self, item):
        return self.balls[item]
