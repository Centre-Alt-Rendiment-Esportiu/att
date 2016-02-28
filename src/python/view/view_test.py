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
#from pygame.locals import *

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

sensor_coords = np.array ([[5.6, 6.2],
                  [30.5, 6.2],
                  [55.6, 5.48],
                  [17.2, 21.4],
                  [46.8, 22.2],
                  [6, 38.6],
                  [30.5, 38.6],
                  [55.6, 38.6]])
																		
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

def drawBall(ball, window, fill=0):
	pygame.draw.circle(window, ball.color, ball.position, ball.radius, fill)

def drawReferencePoint(x,y,window):
	ball = Ball()
	ball.color = (255, 0, 0)
	ball.radius = 10
	
	translated_x = int(x*x_conversion)
	translated_y = int(y*y_conversion)
	ball.position = (translated_x, translated_y)

	drawBall(ball, window, 0)
	
def drawHit(x,y,window):
	ball = Ball()
	ball.color = (255, 255, 255)
	ball.radius = 30
	
	translated_x = int(x*x_conversion)
	translated_y = int(y*y_conversion)
	ball.position = (translated_x, translated_y)

	drawBall(ball, window, 1)
	
def drawSensor(x, y, window):
	ball = Ball()
	ball.color = (0, 0, 255)
	ball.radius = 10
	
	translated_x = int(x*x_conversion)
	translated_y = int(y*y_conversion)
	ball.position = (translated_x, translated_y)

	drawBall(ball, window, 0)
			
def displayReferencePoints(window):
	for i in [6,18,30,42,54]:
		for j in [6,18,30,42]:
			drawReferencePoint(j, i, window)
			
def displaySensors(window):
	for sensor_coord in sensor_coords:
		x = sensor_coord[0]
		y = sensor_coord[1]
		drawSensor(y, x, window)
		
def displayTable(window, windowWidth, windowHeight):
	
	tableLineWidth = 1

	pygame.draw.line(window,(255,255,255), (tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
	pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight-1-tableLineWidth/2), (windowWidth-tableLineWidth/2,windowHeight-1-tableLineWidth/2), tableLineWidth) 
	pygame.draw.line(window,(255,255,255), (windowWidth-1-tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-1-tableLineWidth/2,tableLineWidth/2), tableLineWidth) 
	pygame.draw.line(window,(255,255,255), (windowWidth-tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,tableLineWidth/2), tableLineWidth)
	pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight/2), (windowWidth,windowHeight/2), tableLineWidth)
	pygame.draw.line(window,(255,255,255), (windowWidth/2,tableLineWidth/2), (windowWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
	
	return window
	
def displayScenario(windowWidth, windowHeight):
	
	#window = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
	window = pygame.display.set_mode((windowWidth, windowHeight))
	
	displayTable(window, windowWidth, windowHeight)
	displayReferencePoints(window)
	displaySensors(window)
	
	return window
	
	
if __name__ == '__main__':
	
	connected = False
	port = "/dev/ttyACM0"
	baud = 115200
	workQueue = Queue.Queue(10)
		
	#builder = DummySerialPortBuilder()
	#builder = ATTEmulatedSerialPortBuilder()
	builder = ATTHitsFromFilePortBuilder()
	#builder = ATTArduinoSerialPortBuilder()
	
	port = HITS_DATA_FILE
	#serial_port = ATTEmulatedSerialPort(port, baud)
	serial_port = ATTHitsFromFilePort(port, baud)
	#serial_port = ATTArduinoSerialPort(port, baud)

	#regressor = build_regressor_SKLearn()
	regressor = build_regressor_Classic()
	
	myThread = ThreadedSerialReader(1, "Thread-1", workQueue, None, builder, port, baud, serial_port, True)
	myThread.start()
		
	pygame.init()
	
	info = pygame.display.Info()
	#windowWidth = info.current_w
	#windowHeight = info.current_h
	windowWidth = 1024
	windowHeight = 768
	
	x_conversion = (windowWidth/2)/48
	y_conversion = (windowHeight)/60
	
	window = displayScenario(windowWidth, windowHeight)
	clock = pygame.time.Clock()

	done = False
	while not done:
		
		if not workQueue.empty():
			hit = workQueue.get()
			if hit <> "":
				print "> "+hit["raw"]				
				(y,x) = regressor.predictHit(hit)				
				drawHit(x, y, window)
						
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				done = True
				
			#if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
			if (event.type == pygame.KEYUP):
				if (event.key == pygame.K_ESCAPE):
					done = True
				if (event.key == pygame.K_c):
					window.fill((0,0,0))
					window = displayScenario(windowWidth, windowHeight)
				if (event.key == pygame.K_r):
					window.fill((0,0,0))
					window = displayScenario(windowWidth, windowHeight)
					serial_port.amIclosed = 1
					serial_port.start()
												
			if event.type == pygame.QUIT:
				done = True
				
		clock.tick(60)
		pygame.display.flip()	
		
	print "Exit..."
	
	myThread.stop()
	pygame.quit()
	#sys.exit()
