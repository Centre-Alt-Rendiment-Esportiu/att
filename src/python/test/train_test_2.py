# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/home/asanso/workspace/att-spyder/att/src/python/')

import pygame

import Queue

from hit.serial.serial_port import *
from hit.serial.serial_port_builder import *
from hit.serial.serial_reader import *

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

import numpy as np


def build_regressor_1():
	processor = ATTMatrixHitProcessor()
	regressor = ATTClassicHitRegressor(processor)

	TRAIN_VALUES_FILE_LEFT = "/home/asanso/workspace/att-spyder/att/src/python/data/train_points_20160129_left.txt"	
	(hits_training_values, Y) = regressor.collect_train_hits_from_file(TRAIN_VALUES_FILE_LEFT)
	print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
	
	regressor.train(hits_training_values, Y)

	return regressor
	
def build_regressor_2():
	processor = ATTPlainHitProcessor()
	regressor = ATTSkLearnHitRegressor(processor)
	
	TRAIN_VALUES_FILE_LEFT = "/home/asanso/workspace/att-spyder/att/src/python/data/train_points_20160129_left.txt"	
	(hits_training_values, Y) = regressor.collect_train_hits_from_file(TRAIN_VALUES_FILE_LEFT)
	print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
	
	regressor.train(hits_training_values, Y)
	
	return regressor
	
if __name__ == '__main__':
	
	regressor1 = build_regressor_1()
	regressor2 = build_regressor_2()
	
	hit = "hit: {3190:5 2217:8 4668:4 1913:6 5985:5 0:16 975:6 2932:4 l}"
	print '(6,6)'
	print regressor1.predict(hit)
	print regressor2.predict(hit)