# -*- coding: utf-8 -*-

import sys
import pygame

import Queue

from hit.serial.serial_port import *
from hit.serial.serial_port_builder import *
from hit.serial.serial_reader import *

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

from serialLogNotifier import SerialLogNotifier

import menuState
import shortServiceState
import multiBallState
import wholePointSequenceState
import sandboxState

import predictorBuilder

pressed = None
isButtonUp = True

currentState = None

menu_state = None
op_1_state = None
op_2_state = None
op_3_state = None
op_4_state = None

predBuilder = None
predictor = None

def setState(state, referer):
	global currentState
	global menu_state
	global op_1_state, op_2_state, op_3_state, op_4_state

	if state == 0:
		currentState = menu_state
	elif state == 1:
		currentState = op_1_state
	elif state == 2:
		currentState = op_2_state
	elif state == 3:
		currentState = op_3_state
	elif state == 4:
		currentState = op_4_state
	
	if referer	!= None:
		referer.clear()

def isPressed(key):
	global pressed, isButtonUp
	if pressed[key] and isButtonUp:
		isButtonUp = False
		return True
	return False

def displayScenario(windowWidth, windowHeight):
	#surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
	surface = pygame.display.set_mode((windowWidth, windowHeight))
	#surface.fill((250, 250, 250))
	return surface
	
def main():
	global pressed, isButtonUp, currentState, menu_state, op_1_state, op_2_state, op_3_state, op_4_state

	predBuilder = predictorBuilder.PredictorBuilder()
	predictor = predBuilder.buildInstance()
	
	workQueue = Queue.Queue(10)
	
	port = "/dev/ttyACM0"
	HITS_DATA_FILE = "../../../arduino/data/train_20160129_left.txt"
	port = HITS_DATA_FILE
	baud = 115200
	
	serialBuilder = ATTHitsFromFilePortBuilder()
	serial_port = ATTHitsFromFilePort(port, baud)
	
	myThread = ThreadedSerialReader(1, "Thread-1", workQueue, None, serialBuilder, port, baud, serial_port)
	myThread.start()

	pygame.init()
	
	#info = pygame.display.Info()
	#windowWidth = info.current_w
	#windowHeight = info.current_h
	windowWidth = 1280 #1024
	windowHeight = 768 #768
	
	surface = displayScenario(windowWidth, windowHeight)
	notifier = SerialLogNotifier(surface, (55,80,98,102))
	
	menu_state = menuState.MenuState(surface, predictor, workQueue, notifier)
	op_1_state = shortServiceState.ShortServiceState(surface, predictor, workQueue, notifier)
	op_2_state = multiBallState.MultiBallState(surface, predictor, workQueue, notifier);
	op_3_state = wholePointSequenceState.WholePointSequenceState(surface, predictor, workQueue, notifier)
	op_4_state = sandboxState.SandboxState(surface, predictor, workQueue, notifier)
	
	setState(0, None)
	
	try:
		done = False
		clock = pygame.time.Clock()
		
		while not done:
			#surface.fill((0, 0, 0))
				
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				
			pressed = pygame.key.get_pressed()
			if not(pressed[pygame.K_UP]) and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_RETURN]) and not(pressed[pygame.K_ESCAPE]):					
				isButtonUp = True
	
			currentState.loop(setState, isPressed)
			
			pygame.display.flip()
			clock.tick(60)
			
	except Exception:
		print Exception
				
	finally:
		myThread.stop()
		pygame.quit()
		sys.exit()

if __name__ == '__main__': main()