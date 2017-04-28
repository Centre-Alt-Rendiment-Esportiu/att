from collections import deque

from test.classes.detectors.BounceDetector import BounceDetector
from test.classes.utils.Ball import Ball

lineColors = ((0, 0, 255), (0, 255, 255))

""" Class that represents the ball's position history"""


class BallHistory:
    def __init__(self, tailsize):
        self.balls = deque(maxlen=tailsize)
        self.bounceQueue = BounceDetector(size=8)
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

    def has_bounced(self, ball):
        self.bounceQueue.add_point(ball.center)
        bounce_point = self.bounceQueue.detect()
        if bounce_point:
            bounce = Ball(bounce_point)
            bounce.is_bounce = True
            self.balls.appendleft(bounce)
            self.bounceQueue.clear()
            return bounce_point
        return None

    def update_history(self, ball):
        ball.is_bounce = False
        self.balls.appendleft(ball)

    def clear_history(self):
        self.balls.clear()
        self.bounceQueue.clear()

    def line_color(self):
        return lineColors[self.direction]

    def __len__(self):
        return len(self.balls)

    def __getitem__(self, item):
        return self.balls[item]
