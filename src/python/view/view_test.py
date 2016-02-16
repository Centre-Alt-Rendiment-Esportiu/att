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

windowWidth = 1024 
windowHeight = 768
tableLineWidth = 4

SCREEN_MULITPLIER = 14.6


TRAIN_DATA_FILE = "../data/train_points_20160129_left.txt"
HITS_DATA_FILE = "../../arduino/data/train_20160129_left.txt"

def build_regressor():
	processor = ATTMatrixHitProcessor()
	regressor = ATTClassicHitRegressor(processor)
	
	(hits_training_values, Y) = regressor.collect_train_hits_from_file(TRAIN_DATA_FILE)
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


def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)
 
    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
 
    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
    return screen

if __name__ == '__main__':
	
	
	connected = False
	port = "/dev/ttyACM0"
	baud = 115200
	workQueue = Queue.Queue(10000)
	
	window = pygame.display.set_mode((windowWidth, windowHeight))
		
	#builder = DummySerialPortBuilder()
	#builder = ATTEmulatedSerialPortBuilder()
	builder = ATTHitsFromFilePortBuilder()
	#builder = ATTArduinoSerialPortBuilder()
	
	processor = ATTMatrixHitProcessor()
	regressor = ATTClassicHitRegressor(processor)
	
	port = HITS_DATA_FILE
	serial_reader = ATTHitsFromFilePort(port, baud)
	#serial_reader = ATTArduinoSerialPort(port, baud)
	
	
 	pygame.init()
	regressor = build_regressor()
	
	myThread = ThreadedSerialReader(1, "Thread-1", workQueue, None, builder, port, baud, serial_reader)
	myThread.start()
		
	ball = Ball()
	
	screen = pygame.display.set_mode((int(round(2 * 54 * SCREEN_MULITPLIER)), int(round(60 * SCREEN_MULITPLIER))))
	
	#toggle_fullscreen()
	
	clock = pygame.time.Clock()

	done = False
	
	#screen.fill((250, 250, 250))
	displayTable(windowWidth, windowHeight, tableLineWidth, ball)
												
	while not done:
		DELAY = 300
		
		if not workQueue.empty():
			reading = workQueue.get()
			if reading <> "":
				print "> "+reading
				DELAY = 50
				
				
				try:
					(y,x) = regressor.predict(reading) # (6,6)
					#ball.position = (int(x*7.5),int(y*8))
					ball.position = (int(x*11),int(y*10))
					print (x,y)
					pygame.draw.circle(window, ball.color, ball.position, ball.radius, ball.radius)
				except:
					pass
				
				pygame.display.update()
		
			
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
		
		pygame.time.delay(DELAY)

		"""	
		pressed = pygame.key.get_pressed()
		if not(pressed[pygame.K_UP]) and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_RETURN]) and not(pressed[pygame.K_ESCAPE]):
			isButtonUp = True
		"""
		
	print "Exit..."
	pygame.quit()	
		
		#pygame.display.flip()
		#clock.tick(60)