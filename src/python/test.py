# -*- coding: utf-8 -*-

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

import numpy as np


# ###################################
# Predict
#

def build_regressor():
	processor = ATTMatrixHitProcessor()
	regressor = ATTClassicHitRegressor(processor)
	
	(hits_training_values, Y) = regressor.collect_train_hits_from_file("test/data/train_points_2.txt")
	print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
	
	regressor.train(hits_training_values, Y)
	
	return regressor
	
def build_Sklearn_Regressor():
	processor = ATTPlainHitProcessor()
	regressor = ATTSkLearnHitRegressor(processor)
	
	(hits_training_values, Y) = regressor.collect_train_hits_from_file("test/data/train_points_2.txt")
	print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
	#print hits_training_values
	regressor.train(hits_training_values, Y)
	
	return regressor
	
def test(model):
	(x,y) = model.predict("hit: {0:17 987:5 2204:6 1205:6 2367:6 1431:5 l}") # (6,6)
	print "Original (6,6), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {252:10 0:6 1067:6 153:5 755:5 766:5 l}") # (18,6)
	print "Original (18,6), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {1835:9 0:48 1226:5 1369:5 993:5 2022:6 l}") # (30,6)
	print "Original (30,6), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {2347:8 1092:5 1445:5 801:5 0:5 1136:5 l}") # (42,42)
	print "Original (42,42), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {1984:10 700:6 2004:6 0:6 2294:5 412:6 l}") # (18,30)
	print "Original (18,30), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {3800:7 867:6 2695:5 2513:5 52:5 0:7 l}") # (30,42)
	print "Original (30,42), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {2057:8 997:8 1008:6 883:5 0:17 2294:5 l}") # (42,18)
	print "Original (42,18), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {2804:5 1090:6 624:5 1433:5 0:6 2667:5 l}") # (54,30)
	print "Original (54,30), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {38:6 247:5 1914:6 0:5 1336:5 484:6 l}") # (12,12)
	print "Original (12,12), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {1616:11 897:11 1498:6 0:7 530:5 541:5 l}") # (24,24)
	print "Original (24,24), Prediccio: ",(x,y)
	
	(x,y) = model.predict("hit: {1648:5 1527:6 4171:5 1681:6 0:5 484:5 l}") # (24,24)
	print "Original (36,24), Prediccio: ",(x,y)

if __name__ == '__main__':
	model = build_regressor()
	#model = build_Sklearn_Regressor()
	test(model)