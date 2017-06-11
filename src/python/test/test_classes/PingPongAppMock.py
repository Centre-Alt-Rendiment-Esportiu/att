from test.classes.PingPongApp import PingPongApp
from test.test_classes.BallTrackerMock import BallTrackerMock


class PingPongAppMock(PingPongApp):
    def __init__(self, args):
        super(PingPongAppMock, self).__init__(args)
        self.ball_tracker = BallTrackerMock()
