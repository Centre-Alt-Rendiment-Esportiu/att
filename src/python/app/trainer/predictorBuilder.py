# -*- coding: utf-8 -*-

import numpy as np

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

# TRAIN_DATA_FILE = "../../data/train_points_20160129_left.txt"
TRAIN_DATA_FILE = "../../data/train_points_20160303_right.txt"


class PredictorBuilder:
    def __init__(self):
        pass

    def buildInstance(self, trainDataFile):
        return self.build_regressor_Classic(trainDataFile)

        # return self.build_regressor_SKLearn(trainDataFile)

    def build_regressor_Classic(self, trainDataFile):
        processor = ATTMatrixHitProcessor()
        regressor = ATTClassicHitRegressor(processor)

        (hits_training_values, Y) = regressor.collect_train_hits_from_file(trainDataFile)
        # print "Train Values: ", np.shape(hits_training_values), np.shape(Y)

        regressor.train(hits_training_values, Y)

        return regressor

    def build_regressor_SKLearn(self, trainDataFile):
        processor = ATTPlainHitProcessor()
        regressor = ATTSkLearnHitRegressor(processor)

        (hits_training_values, Y) = regressor.collect_train_hits_from_file(trainDataFile)
        # print "Train Values: ", np.shape(hits_training_values), np.shape(Y)

        regressor.train(hits_training_values, Y)

        return regressor

    def build_table_predictor(self):
        pass
