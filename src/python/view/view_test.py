# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/home/asanso/workspace/python/att/src/python/')

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

windowWidth = 1096 
windowHeight = 608
tableLineWidth = 4

SCREEN_MULITPLIER = 14.6

def build_regressor():
	processor = ATTMatrixHitProcessor()
	regressor = ATTClassicHitRegressor(processor)
	
	(hits_training_values, Y) = regressor.collect_train_hits_from_file("/home/asanso/workspace/python/att/src/python/test/data/train_points_2.txt")
	print "Train Values: ", np.shape(hits_training_values), np.shape(Y)
	
	regressor.train(hits_training_values, Y)
	
	return regressor
	
class Ball:
   radius = 8
   position = (250,200)
   color = (255,255,255) 
			
def displayTable(windowWidth, windowHeight, tableLineWidth, ball):
    
    window = pygame.display.set_mode((windowWidth, windowHeight))
    
    pygame.draw.line(window,(255,255,255), (tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
    #pygame.draw.rect(window(255,255,255), (0,0,1096,608))
    pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
    #pygame.draw.line(window,(255,255,255), (2,606), (1094,606), tableLineWidth)    
    pygame.draw.line(window,(255,255,255), (windowWidth-tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-tableLineWidth/2,tableLineWidth/2), tableLineWidth) 
    pygame.draw.line(window,(255,255,255), (windowWidth-tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,tableLineWidth/2), tableLineWidth)
    pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight/2), (windowWidth,windowHeight/2), tableLineWidth)
    pygame.draw.line(window,(255,255,255), (windowWidth/2,tableLineWidth/2), (windowWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
    
    pygame.draw.circle(window, ball.color, ball.position, ball.radius, ball.radius)
    
    pygame.display.update()
				

if __name__ == '__main__':
	
	
	connected = False
	port = "/dev/ttyACM0"
	baud = 115200
	workQueue = Queue.Queue(10000)
	
	window = pygame.display.set_mode((windowWidth, windowHeight))
		
	#builder = DummySerialPortBuilder()
	#builder = ATTEmulatedSerialPortBuilder()
	#builder = ATTHitsFromFilePort2Builder()
	builder = ATTArduinoSerialPortBuilder()
	
	processor = ATTMatrixHitProcessor()
	regressor = ATTClassicHitRegressor(processor)
	#serial_reader = ATTHitsFromFilePort2()
	#serial_reader = ATTHitsFromFilePort_TrainPoints()
	serial_reader = ATTArduinoSerialPort(port, baud)
	
	
 -l	pygame.init()
	regressor = build_regressor()
	
	myThread = ThreadedSerialReader(1, "Thread-1", workQueue, None, builder, port, baud, serial_reader)
	myThread.start()
		
	ball = Ball()
	
	screen = pygame.display.set_mode((int(round(2 * 54 * SCREEN_MULITPLIER)), int(round(60 * SCREEN_MULITPLIER))))
	clock = pygame.time.Clock()

	done = False
	
	screen.fill((250, 250, 250))
	displayTable(windowWidth, windowHeight, tableLineWidth, ball)
												
	while not done:
		
		if not workQueue.empty():
			reading = workQueue.get()
			print "> "+reading
			(y,x) = regressor.predict(reading) # (6,6)
			ball.position = (int(x*7.5),int(y*8))
			print (x,y)
			pygame.draw.circle(window, ball.color, ball.position, ball.radius, ball.radius)
			pygame.display.update()
		
			
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				done = True
				
			if (event.type == pygame.KEYUP) or (event.type == pygame.KEYDOWN):
				print event
				print event.key
				if (event.key == pygame.K_ESCAPE):
					done = True
					
												
			"""
			if event.type == pygame.QUIT:
				done = True
			"""
		"""	
		pressed = pygame.key.get_pressed()
		if not(pressed[pygame.K_UP]) and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_RETURN]) and not(pressed[pygame.K_ESCAPE]):
			isButtonUp = True
		"""
		
	print "Exit..."
	pygame.quit()	
		
		#pygame.display.flip()
		#clock.tick(60)