from test.classes.BounceDetector import BounceDetector

bounce_frames = {22, 48, 65, 72, 88, 102, 117, 131, 291, 441, 462, 491, 508, 648, 675, 812, 836, 865, 901, 1107, 1136,
                 1343, 1376, 1414, 1493, 1515, 1616, 1644, 1670, 1707, 1718, 1730, 1849, 1872, 1898, 2409, 2440, 2585,
                 2606, 2646, 2666, 2671, 2688, 2953, 2975, 3004, 3034, 3230, 3259, 3286, 3330, 3338, 3530, 3540, 3652,
                 3681, 3828, 3852, 3964, 3993, 4019, 4142, 4164, 4187, 4425, 4450, 4494, 4548, 4572, 4700, 4722, 4763,
                 4810, 4863, 4906}

class BounceDetectorTest(BounceDetector):
    def __init__(self, size):
        self.curr_frame = 0
        self.bounce_points = []
        super(BounceDetectorTest, self).__init__(size=size)

    def has_bounced(self):
        bounced = super(BounceDetectorTest, self).has_bounced()
        if bounced:
            self.bounce_points.append(self.curr_frame)
        return bounced

    def set_frame(self, frame):
        self.curr_frame = frame

    def end_test(self):
        self.bounce_points = set(self.bounce_points)
