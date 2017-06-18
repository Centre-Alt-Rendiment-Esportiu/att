class TestWriter:
    def __init__(self, real, found, tol1=0, tol2=0):
        self.real = real
        self.found = found
        self.tol1, self.tol2 = tol1, tol2

    def test(self):
        print(self.found)
        num_real = len(self.real)
        num_found = len(self.found)

        hits = 0
        for fr1 in self.real:
            for fr2 in self.found:
                if fr1-self.tol1 <= fr2 <= fr1+self.tol2:
                    hits += 1
                    self.found.remove(fr2)
                    break

        false_negatives = num_real - hits
        false_positives = num_found - hits
        total_errors = false_negatives + false_positives

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
