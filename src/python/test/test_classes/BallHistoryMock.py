from test.classes.game.BallHistory import BallHistory
from test.test_classes.BounceDetectorTest import BounceDetectorTest


class BallHistoryMock(BallHistory):
    def __init__(self, tailsize):
        super(BallHistoryMock, self).__init__(tailsize=tailsize)
        self.bounceQueue = BounceDetectorTest(size=tailsize)

    def add_ball(self, center, frame):
        self.bounceQueue.curr_frame = frame
        super(BallHistoryMock, self).add_ball(center)

    def end_test(self):
        self.bounceQueue.end_test()
