from test.classes.BallTracker import BallTracker
from test.test_classes.BounceCalculatorMock import BounceCalculatorMock


class BallTrackerMock(BallTracker):
    def __init__(self):
        super(BallTrackerMock, self).__init__()
        self.bounce_calculator = BounceCalculatorMock()
