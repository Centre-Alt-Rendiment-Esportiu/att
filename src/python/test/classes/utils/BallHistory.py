from collections import deque

from test.classes.detectors.BounceDetector import BounceDetector
from test.classes.utils.Ball import Ball

lineColors = ((0, 0, 255), (0, 255, 255))

""" Class that represents the ball's position history"""


class BallHistory:
    def __init__(self, tailsize):
        self.balls = deque(maxlen=tailsize)
        self.bounceQueue = BounceDetector(size=7)
        self.direction = 0

    def add_ball(self, center):
        if len(self) > 0:
            if (self[0].center[0] - center[0]) < 0 and self.direction != 0:
                self.direction = 0
                self.clear_history()
            elif (self[0].center[0] - center[0]) > 0 and self.direction != 1:
                self.direction = 1
                self.clear_history()
        self.bounceQueue.add_point(center)
        bounce_point = self.bounceQueue.bounce_point()
        if bounce_point:
            self.balls.appendleft(Ball(bounce_point, colorIndx=1))
            self.bounceQueue.clear()
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
