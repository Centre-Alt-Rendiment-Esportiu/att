# -*- coding: utf-8 -*-

import sys
import platform

PROJECT_ROOT = ""
if platform.platform().lower().startswith("win"):
	PROJECT_ROOT = "I:/dev/workspaces/python/att-workspace/att/"
else:
	if platform.platform().lower().startswith("linux"):
		PROJECT_ROOT = "/home/asanso/workspace/att-spyder/att/"
		
sys.path.insert(0, PROJECT_ROOT + "/src/python/")

import pygame
from pygame.locals import *

import Queue

from hit.serial.serial_port import *
from hit.serial.serial_port_builder import *
from hit.serial.serial_reader import *

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

import numpy as np

TRAIN_DATA_FILE = "../data/train_points_20160129_left.txt"
HITS_DATA_FILE = "../../arduino/data/train_20160129_left.txt"

def build_regressor_Classic():
	processor = ATTMatrixHitProcessor()
	regressor = ATTClassicHitRegressor(processor)

	(hits_training_values, Y) = regressor.collect_train_hits_from_file(TRAIN_DATA_FILE)
	print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
	
	regressor.train(hits_training_values, Y)

	return regressor
	
def build_regressor_SKLearn():
	processor = ATTPlainHitProcessor()
	regressor = ATTSkLearnHitRegressor(processor)
	
	(hits_training_values, Y) = regressor.collect_train_hits_from_file(TRAIN_DATA_FILE)
	print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
	
	regressor.train(hits_training_values, Y)
	
	return regressor
	
class Ball:
   radius = 15
   position = (250,200)
   color = (255,255,255) 

def drawBall(x,y, window):
	ball = Ball()
	ball.color = (255,0,0)
	ball.radius = 20
	
	translated_x = int(x*x_conversion)
	translated_y = int(y*y_conversion)
	ball.position = (translated_x, translated_y)
	pygame.draw.circle(window, ball.color, ball.position, ball.radius, ball.radius)

			
def displayTable(windowWidth, windowHeight, tableLineWidth, ball):
	window = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
	#window = pygame.display.set_mode((windowWidth, windowHeight))
	    
	pygame.draw.line(window,(255,255,255), (tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
	pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
	pygame.draw.line(window,(255,255,255), (windowWidth-tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-tableLineWidth/2,tableLineWidth/2), tableLineWidth) 
	pygame.draw.line(window,(255,255,255), (windowWidth-tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,tableLineWidth/2), tableLineWidth)
	pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight/2), (windowWidth,windowHeight/2), tableLineWidth)
	pygame.draw.line(window,(255,255,255), (windowWidth/2,tableLineWidth/2), (windowWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
	
	for i in [6,18,30,42,54]:
		for j in [6,18,30,42]:
			drawBall(j,i, window)
			pygame.display.flip()	

	return window

if __name__ == '__main__':
	
	connected = False
	port = "/dev/ttyACM0"
	baud = 115200
	workQueue = Queue.Queue(10000)
		
	#builder = DummySerialPortBuilder()
	#builder = ATTEmulatedSerialPortBuilder()
	#builder = ATTHitsFromFilePortBuilder()
	builder = ATTArduinoSerialPortBuilder()
	
	#port = HITS_DATA_FILE
	#serial_reader = ATTHitsFromFilePort(port, baud)
	serial_reader = ATTArduinoSerialPort(port, baud)

	#regressor = build_regressor_SKLearn()
	regressor = build_regressor_Classic()
	
	myThread = ThreadedSerialReader(1, "Thread-1", workQueue, None, builder, port, baud, serial_reader)
	myThread.start()
		
	ball = Ball()
	
	pygame.init()
	
	info = pygame.display.Info()
	
	windowWidth = info.current_w
	windowHeight = info.current_h
	tableLineWidth = 1
	
	x_conversion = (windowWidth/2)/48
	y_conversion = (windowHeight)/60
	
	window = displayTable(windowWidth, windowHeight, tableLineWidth, ball)
	#clock = pygame.time.Clock()

	done = False
	while not done:	
		if not workQueue.empty():
			reading = workQueue.get()
			if reading <> "":
				#print "> "+reading
				
				(y,x) = regressor.predict(reading)
				
				translated_x = int(x*x_conversion)
				translated_y = int(y*y_conversion)
				
				ball.position = (translated_x, translated_y)
				#print (translated_x, translated_y)
				
				pygame.draw.circle(window, ball.color, ball.position, ball.radius, ball.radius)
		else:
			pass
						
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				done = True
				
			if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
				print event
				print event.key
				if (event.key == pygame.K_ESCAPE):
					done = True
												
			if event.type == pygame.QUIT:
				done = True
		
		pygame.display.flip()	
		#clock.tick(100)
	
	print "Exit..."
	pygame.quit()
	myThread.stop()
	sys.exit()
