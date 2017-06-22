from test.classes.ball_detector.BounceCalculator import BounceCalculator
from test.test_classes.TestWriter import TestWriter

real_frames = \
    [333, 354, 383, 410, 434, 457, 481, 558, 583, 609, 636, 660, 686, 709, 733, 757, 780, 803, 830, 852, 878,
     903, 926, 953, 974, 1004, 1023, 1053, 1079, 1102, 1126, 1197, 1220, 1248, 1273, 1297, 1320, 1346, 1372, 1399,
     1422, 1449, 1474, 1503, 1529, 1558, 1582, 1616, 1637, 1669, 1736, 1760, 1787, 1815, 1838, 1863, 1885, 1916,
     1942, 1964, 1990, 2015, 2038, 2062, 2082, 2109, 2136, 2160, 2184, 2252, 2274, 2303, 2325, 2352, 2375, 2397,
     2417, 2443, 2465, 2487, 2509, 2538, 2563, 2587, 2608, 2634, 2655, 2680, 2698, 2842, 2866, 3546, 3571, 3608,
     3763, 3788, 3934, 3956, 4298, 4322, 4358, 4390, 4413, 4437, 4476, 4599, 4623, 4802, 4833, 4853, 4888, 5057,
     5076, 5103, 5407, 5431, 5463, 5523, 5569, 5741, 5763, 5806, 5851, 6219, 6244, 6279, 6307, 6614, 6636, 6683,
     6707, 6729, 7027, 7049, 7089, 7116, 7467, 7489, 7528, 7562, 7590, 7621, 7648, 8002, 8034, 8055, 8086, 8851,
     8876, 8909, 8935, 8960, 9255, 9276, 9303, 9339, 9662, 9684, 10012, 10041, 10070, 10093, 10135, 10499, 10521,
     10548, 10569, 10641, 10666, 10795, 10819, 10855, 10886, 10912, 11075, 11100, 11228, 11253, 11570, 11592, 11616,
     11650, 11671, 12090, 12117, 12300, 12321, 12363, 12382, 12412, 12445, 12474, 12634, 12904, 12926, 12976, 13011,
     13338, 13360, 13643, 13665, 13711, 13728, 14161, 14185, 14221, 14327, 14352, 14503, 14524, 15029, 15052, 15083,
     15118, 15155, 15187, 15212, 15244, 15281, 15314, 15649, 15669, 15698, 16141, 16177, 16265]


class BounceCalculatorMock(BounceCalculator):
    def __init__(self):
        self.curr_frame = 1
        self.found_frames = []

    def find_bounce(self, history):
        self.curr_frame += 1
        bounced = super(BounceCalculatorMock, self).find_bounce(history)
        if not bounced.is_none():
            self.found_frames.append(self.curr_frame)
        return bounced

    def end_test(self):
        print('\n----- BOUNCE RANKINGS: -----')
        frames = [(321, 530), (552, 1137), (1190, 2194), (2244, 2766), (2834, 2940), (3497, 3655), (3745, 3816),
                  (3888, 4005), (4249, 4511), (4585, 4664), (4751, 4902), (5011, 5134), (5361, 5581), (5694, 5981),
                  (6171, 6353), (6561, 6809), (6982, 7248), (7424, 7709), (7952, 8099), (8235, 8362), (8503, 8577),
                  (8793, 8978), (9206, 9344), (9617, 9761), (9970, 10192), (10461, 10606), (10620, 10687),
                  (10754, 11042),
                  (11056, 11103), (11176, 11304), (11525, 11677), (12076, 12134), (12249, 12715), (12856, 13017),
                  (13285, 13411), (13588, 13759), (14117, 14258), (14314, 14383), (14588, 14587), (14979, 15345),
                  (15602, 15751), (15809, 15819), (15822, 15833), (16060, 16065), (16124, 16220), (16247, 16285)]

        m = lambda x1, x2: list(range(x1, x2 + 1))
        s = lambda t: [item for sublist in t for item in sublist]

        total_set = s(map(lambda x: m(x[0], x[1]), frames))
        TestWriter(total_set, real_frames, self.found_frames, tol1=2, tol2=1).test()