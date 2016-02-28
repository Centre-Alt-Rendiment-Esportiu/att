# -*- coding: utf-8 -*-

import numpy as np

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

TRAIN_DATA_FILE = "../../data/train_points_20160129_left.txt"
HITS_DATA_FILE = "../../arduino/data/train_20160129_left.txt"

class PredictorBuilder:
	def __init__(self):
		pass
	
	def buildInstance(self):
		return self.build_regressor_Classic()

	def build_regressor_Classic(self):
		processor = ATTMatrixHitProcessor()
		regressor = ATTClassicHitRegressor(processor)
	
		(hits_training_values, Y) = regressor.collect_train_hits_from_file(TRAIN_DATA_FILE)
		#print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
		
		regressor.train(hits_training_values, Y)
	
		return regressor
		
	def build_regressor_SKLearn(self):
		processor = ATTPlainHitProcessor()
		regressor = ATTSkLearnHitRegressor(processor)
		
		(hits_training_values, Y) = regressor.collect_train_hits_from_file(TRAIN_DATA_FILE)
		#print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
		
		regressor.train(hits_training_values, Y)
		
		return regressor