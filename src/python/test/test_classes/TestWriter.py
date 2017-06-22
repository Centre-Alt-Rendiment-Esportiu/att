NUM_FRAMES = 16421

# Class to write test results


class TestWriter:
    def __init__(self, total_set, true, found, tol1=0, tol2=0):
        self.total = len(total_set)
        self.true = true
        self.inv_true = [x for x in total_set if x not in true]
        self.found = found
        self.inv_found = [x for x in total_set if x not in found]
        self.tol1, self.tol2 = tol1, tol2

    def test(self):
        true_positives = 0
        true_found = []
        for fr1 in self.true:
            for fr2 in self.found:
                if fr1-self.tol1 <= fr2 <= fr1+self.tol2:
                    true_positives += 1
                    self.found.remove(fr2)
                    true_found.append(fr1)
                    break
        false_positives = len(self.found)  # After deleting found stuff
        false_negatives = len(self.true) - len(true_found)
        true_negatives = self.total - (false_negatives + false_positives + true_positives)

        print("\t", "TRUE_NEGATIVES: ", true_negatives)
        print("\t", "FALSE_POSITIVES: ", false_positives)
        print("\t", "FALSE_NEGATIVES: ", false_negatives)
        print("\t", "TRUE_POSITIVES: ", true_positives)

        print('')
        accuracy = (true_positives + true_negatives) / self.total
        print("\t", "Accuracy: ", accuracy*100, "%")
        precision = (true_positives / (true_positives + false_positives))
        print("\t", "Precision: ", precision*100, "%")
        true_pos_rate = (true_positives / (true_positives + false_negatives))
        print("\t", "True positive rate: ", true_pos_rate*100, "%")
        false_pos_rate = (false_positives / (false_positives + true_negatives))
        print("\t", "False positive rate: ", false_pos_rate*100, "%")
