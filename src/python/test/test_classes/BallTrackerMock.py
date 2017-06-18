from test.classes.BallTracker import BallTracker
from test.test_classes.BounceCalculatorMock import BounceCalculatorMock
from test.test_classes.TestWriter import TestWriter


frames = [(321, 530), (552, 1137), (1190, 2194), (2244, 2766), (2834, 2940), (3497, 3655), (3745, 3816),
          (3888, 4005), (4249, 4511), (4585, 4664), (4751, 4902), (5011, 5134), (5361, 5581), (5694, 5981),
          (6171, 6353), (6561, 6809), (6982, 7248), (7424, 7709), (7952, 8099), (8235, 8362), (8503, 8577),
          (8793, 8978), (9206, 9344), (9617, 9761), (9970, 10192), (10461, 10606), (10620, 10687), (10754, 11042),
          (11056, 11103), (11176, 11304), (11525, 11677), (12076, 12134), (12249, 12715), (12856, 13017),
          (13285, 13411), (13588, 13759), (14117, 14258), (14314, 14383), (14588, 14587), (14979, 15345),
          (15602, 15751), (15809, 15819), (15822, 15833), (16060, 16065), (16124, 16220), (16247, 16285)]

m = lambda x1, x2: list(range(x1, x2+1))
s = lambda t: [item for sublist in t for item in sublist]

real_frames = s(map(lambda x: m(x[0], x[1]), frames))


class BallTrackerMock(BallTracker):
    def __init__(self):
        self.curr_frame = 1
        self.found_frames = []
        super(BallTrackerMock, self).__init__()
        self.bounce_calculator = BounceCalculatorMock()

    def track(self, frame):
        self.curr_frame += 1
        found_ball = super(BallTrackerMock, self).track(frame)
        if not found_ball.is_none():
            self.found_frames.append(self.curr_frame)
        return found_ball

    def end_test(self):
        self.bounce_calculator.end_test()
        print('\n----- TRACKER RANKINGS: -----')
        TestWriter(real_frames, self.found_frames, tol1=0, tol2=0).test()
