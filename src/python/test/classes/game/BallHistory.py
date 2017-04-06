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

    def check_direction_change(self, center):
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

    def has_bounced(self, center):
        self.bounceQueue.add_point(center)
        bounce_point = self.bounceQueue.detect()
        if bounce_point:
            self.balls.appendleft(Ball(bounce_point, colorIndx=1))
            self.bounceQueue.clear()
            return bounce_point
        return None

    def update_history(self, center):
        self.balls.appendleft(Ball(center, colorIndx=0))

    def clear_history(self):
        self.balls.clear()
        self.bounceQueue.clear()

    def line_color(self):
        return lineColors[self.direction]

    def __len__(self):
        return len(self.balls)

    def __getitem__(self, item):
        return self.balls[item]
