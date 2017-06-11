from test.classes.ball_detector.BounceCalculator import BounceCalculator

bounce1 = [333, 354, 383, 410, 434, 457, 481, 558, 583, 609, 636, 660, 686, 709, 733, 757, 780, 803, 830, 852, 878,
           903, 926, 953, 974, 1003, 1023, 1053, 1079, 1102, 1126, 1197, 1220, 1248, 1273, 1297, 1320, 1346, 1372,
           1399, 1422, 1449, 1474, 1503, 1529, 1558, 1582, 1616, 1637, 1669, 1760, 1787, 1815, 1838, 1863, 1885, 1916,
           1942, 1964, 1990, 2015, 2038, 2062, 2082, 2018, 2038, 2062, 2082, 2108, 2136, 2160, 2184, 2252, 2274, 2303,
           2325, 2352, 2374, 2397, 2417, 2443, 2465, 2487, 2509, 2538, 2563, 2586, 2608, 2634, 2655, 2680, 2698, 2841,
           2865]
bounce2 = [3546, 3571, 3608, 3763, 3787, 3934, 3956, 4298, 4322, 4358, 4390, 4413, 4437, 4476, 4599, 4622, 4802, 4833,
           4853, 4888, 5056, 5076, 5103, 5405, 5431, 5462, 5523, 5569, 5740, 5762, 5806, 5851]
bounce3 = [6219, 6243, 6279, 6307, 6614, 6636, 6683, 6707, 6729, 7027, 7049, 7089, 7115, 7466, 7489, 7527, 7561, 7589,
           7620, 7648, 8001, 8033, 8054, 8085, 8851, 8876, 8909, 8935, 8959]
bounce4 = [9254, 9276, 9303, 9339, 9662, 9684, 10012, 10041, 10070, 10093, 10135, 10499, 10521, 10548, 10569, 10640,
           10666, 10795, 10819, 10855, 10886, 10912, 10936, 10956, 11075, 11000, 11228, 11253, 11570, 11592, 11616,
           11650, 11671]

bounce_frames = [bounce1, bounce2, bounce3, bounce4]


class BounceCalculatorMock(BounceCalculator):
    def __init__(self):
        self.curr_frame = 1
        self.found_frames = []

    def find_bounce(self, history):
        self.curr_frame += 1
        bounced = super(BounceCalculatorMock, self).find_bounce(history)
        if self.curr_frame % 3000 == 0:
            i = int(self.curr_frame / 3000)
            self.test(i)
            if i-1 == len(bounce_frames)-1:
                print('\n----- GLOBAL RANKINGS: -----')
                self.test(-1)
                exit(0)
        if not bounced.is_none():
            self.found_frames.append(self.curr_frame)
        return bounced

    def test(self, i):
        if i == -1:
            tmp = [item for sublist in bounce_frames for item in sublist] # Flatten
            x1, x2 = 0, float('inf')
        else:
            tmp = bounce_frames[i-1].copy()
            x1, x2 = (i-1)*3000, i*3000

        num_real = len(tmp)
        sliced_found = list(filter(lambda x: x1 <= x < x2, self.found_frames))
        num_found = len(sliced_found)

        hits = 0
        for fr1 in sliced_found:
            for fr2 in tmp:
                if fr2-2 <= fr1 <= fr2+2:
                    hits += 1
                    tmp.remove(fr2)
                    break

        false_negatives = num_real - hits
        false_positives = num_found - hits
        total_errors = false_negatives + false_positives

        print("\n", "Test results of frames", str(x1), "to", str(x2))

        print("\t", "HITS: ", hits)
        print("\t", "FALSE_NEGATIVES (MISSES): ", false_negatives)
        print("\t", "FALSE_POSITIVES: ", false_positives)

        print('')
        print("\t", "TOTAL TO FIND: ", num_real)
        print("\t", "TOTAL ERRORS (includes both types): ", total_errors)

        print('')
        print("\t", "HIT RATE: ", hits * 100 / num_real, "%")
        print("\t", "MISS RATE:", false_negatives * 100 / num_real, "%")
        print("\t", "FALSE POSITIVE RATE: ", false_positives * 100 / total_errors, "%")
        print("\t", "FALSE NEGATIVE RATE: ", false_negatives * 100 / total_errors, "%")
