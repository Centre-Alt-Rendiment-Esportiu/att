# -*- coding: utf-8 -*-

import Queue

from serial_port import *
from serial_port_builder import *
from serial_reader import *

from hit_processor import *
from hit_train import *

import pygame

def main_f1():
	connected = False
	port = "/dev/ttyACM0"
	baud = 115200
	workQueue = Queue.Queue(10000)
	
	#builder = DummySerialPortBuilder()
	#builder = ATTEmulatedSerialPortBuilder()
	builder = ATTHitsFromFilePort2Builder()
	#builder = ATTArduinoSerialPortBuilder()
	
	processor = ATTHitProcessor2()
	regressor = ATTHitRegressor3(processor)
	#serial_reader = ATTHitsFromFilePort2()
	serial_reader = ATTHitsFromFilePort_TrainPoints()
	
	# ###################################
	# READ
	#
	all_hits_repetitions = []
	for refPoint in range(20):
		
		myThread = ThreadedSerialReader(1, "Thread-1", workQueue, 5, builder, port, baud, serial_reader)
		myThread.start()
		myThread.join()
		
		sensor_repetition_hits = []
		
		while not workQueue.empty():
			
			reading = workQueue.get()
			sensor_repetition_hits.append(reading)
			
		all_hits_repetitions.append(sensor_repetition_hits)
	
	# ###################################
	# Collect hits, parse and apply differences
	#
	hits_training_values = regressor.collect_hits(all_hits_repetitions)
	#print hits_training_values
	print "Train Values: ", shape(hits_training_values)
	
	# ###################################
	# Average repetitions
	#
	averaged_values = regressor.calc_averages(hits_training_values)
	#print averaged_values
	print "Average Diffs: ", shape(averaged_values)
		
	#N_SENSORS = len(averaged_values[0][0])
	
	# ###################################
	# Populate matrices
	#
	Ms = regressor.calc_matrices(averaged_values)
	print "Ms Matrices: ", shape(Ms)
	#print Ms

	# ###################################
	# Ms es matriu de coeficients
	#
	#print shape(Ms)
	
	# ###################################
	# Train
	#
	regressor.calc_coeficients(Ms)
	
	# ###################################
	# Predict
	#

	(x,y) = regressor.predict("hit: {0:17 987:5 2204:6 1205:6 2367:6 1431:5 l}") # (6,6)
	print "Original (6,6), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {252:10 0:6 1067:6 153:5 755:5 766:5 l}") # (18,6)
	print "Original (18,6), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {1835:9 0:48 1226:5 1369:5 993:5 2022:6 l}") # (30,6)
	print "Original (30,6), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {2347:8 1092:5 1445:5 801:5 0:5 1136:5 l}") # (42,42)
	print "Original (42,42), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {1984:10 700:6 2004:6 0:6 2294:5 412:6 l}") # (18,30)
	print "Original (18,30), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {3800:7 867:6 2695:5 2513:5 52:5 0:7 l}") # (30,42)
	print "Original (30,42), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {2057:8 997:8 1008:6 883:5 0:17 2294:5 l}") # (42,18)
	print "Original (42,18), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {2804:5 1090:6 624:5 1433:5 0:6 2667:5 l}") # (54,30)
	print "Original (54,30), Prediccio: ",(x,y)


	(x,y) = regressor.predict("hit: {38:6 247:5 1914:6 0:5 1336:5 484:6 l}") # (12,12)
	print "Original (12,12), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {1616:11 897:11 1498:6 0:7 530:5 541:5 l}") # (24,24)
	print "Original (24,24), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {1648:5 1527:6 4171:5 1681:6 0:5 484:5 l}") # (24,24)
	print "Original (36,24), Prediccio: ",(x,y)
	
def main_f2():
		
	processor = ATTHitProcessor2()
	regressor = ATTHitRegressor4(processor)

	# ###################################
	# Collect hits, parse and apply differences
	#
	(hits_training_values, Y) = regressor.collect_train_hits_from_file("data/train_points_2.txt")
	print "Train Values: ", shape(hits_training_values), shape(Y)
	
	# ###################################
	# Populate matrices
	#
	#Ms = regressor.calc_matrices(hits_training_values)
	#print "Ms Matrices: ", shape(Ms)

	# ###################################
	# Train
	#
	#regressor.calc_coeficients(Ms, Y)
	
	regressor.train(hits_training_values, Y)
	
	# ###################################
	# Predict
	#
	
	(x,y) = regressor.predict("hit: {0:17 987:5 2204:6 1205:6 2367:6 1431:5 l}") # (6,6)
	print "Original (6,6), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {252:10 0:6 1067:6 153:5 755:5 766:5 l}") # (18,6)
	print "Original (18,6), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {1835:9 0:48 1226:5 1369:5 993:5 2022:6 l}") # (30,6)
	print "Original (30,6), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {2347:8 1092:5 1445:5 801:5 0:5 1136:5 l}") # (42,42)
	print "Original (42,42), Prediccio: ",(x,y)
	
	(x,y) = regressor.predict("hit: {1984:10 700:6 2004:6 0:6 2294:5 412:6 l}") # (18,30)
	print "Original (18,30), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {3800:7 867:6 2695:5 2513:5 52:5 0:7 l}") # (30,42)
	print "Original (30,42), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {2057:8 997:8 1008:6 883:5 0:17 2294:5 l}") # (42,18)
	print "Original (42,18), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {2804:5 1090:6 624:5 1433:5 0:6 2667:5 l}") # (54,30)
	print "Original (54,30), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {38:6 247:5 1914:6 0:5 1336:5 484:6 l}") # (12,12)
	print "Original (12,12), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {1616:11 897:11 1498:6 0:7 530:5 541:5 l}") # (24,24)
	print "Original (24,24), Prediccio: ",(x,y)

	(x,y) = regressor.predict("hit: {1648:5 1527:6 4171:5 1681:6 0:5 484:5 l}") # (24,24)
	print "Original (36,24), Prediccio: ",(x,y)
	
		
if __name__ == '__main__':
	
	main_f2()

	










