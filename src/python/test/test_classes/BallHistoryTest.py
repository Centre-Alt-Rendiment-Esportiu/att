from test.classes.BallHistory import BallHistory
from test.test_classes.BounceDetectorTest import BounceDetectorTest


class BallHistoryTest(BallHistory):
    def __init__(self, tailsize):
        super(BallHistoryTest, self).__init__(tailsize=tailsize)
        self.bounceQueue = BounceDetectorTest(size=tailsize)

    def add_ball(self, center, frame):
        self.bounceQueue.curr_frame = frame
        super(BallHistoryTest, self).add_ball(center)

    def end_test(self):
        self.bounceQueue.end_test()
