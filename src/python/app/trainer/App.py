# -*- coding: utf-8 -*-

import sys
import pygame
import traceback
import serialLogNotifier
import Queue

from hit.serial.serial_port import *
from hit.serial.serial_port_builder import *
from hit.serial.serial_reader import *

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

import predictorBuilder
from view import *
from controller import *

class TheApp:
	pressed = None
	isButtonUp = True
	
	predBuilder = None
	predictor = None
	leftPredictor = None
	rightPredictor = None
	workQueue = None
	notifier = None
	surface = None
	myThread = None
	
	dispatcher = None
	
	def __init__(self):
		self.workQueue = Queue.Queue(10)

	def isPressed(self, key):
		if self.pressed[key] and self.isButtonUp:
			self.isButtonUp = False
			return True
		return False
	
	def isAnyPressed(self):
		if len(self.pressed) > 0:
			return True
		return False
	
	def buildScenario(self, windowWidth, windowHeight):
		#self.surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
		self.surface = pygame.display.set_mode((windowWidth, windowHeight))
		
	def buildHitDataSource(self):
		
		self.predictor = TableHitPredictor()		
		
		demo = True
		if demo:
			HITS_DATA_FILE = "../../../arduino/data/hits_reference_points_alltable_20160303.txt"
			#HITS_DATA_FILE = "log/2016_03_03_1820_3_ss.log"
			port = HITS_DATA_FILE
			baud = ""
			serialBuilder = ATTHitsFromFilePortBuilder()			
			serial_port = ATTHitsFromFilePort(port, baud)
		else:
			port = "/dev/ttyACM0"
			baud = 115200
			serialBuilder = ATTArduinoSerialPortBuilder()
			serial_port = ATTArduinoSerialPort(port, baud)
		
		self.myThread = ThreadedSerialReader(1, "Thread-1", self.workQueue, None, serialBuilder, port, baud, serial_port, False)
		self.myThread.start()
		
	def main(self):
		
		pygame.init()
		
		info = pygame.display.Info()
		windowWidth = info.current_w
		windowHeight = info.current_h

		windowWidth = 1280 #1024
		windowHeight = 768 #768

		self.buildHitDataSource()
		
		
		
		self.buildScenario(windowWidth, windowHeight)
		self.notifier = serialLogNotifier.SerialLogNotifier(self.surface, (55,78,100,100))
		
		self.dispatcher = ATTDispatcher(self)
		
		self.dispatcher.buildControllers()
		#self.dispatcher.setController(LogonController.ID)
		self.dispatcher.setController(MenuController.ID)
		
		try:
			done = False
			clock = pygame.time.Clock()
			
			while not done:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						done = True
						break
					
				self.pressed = pygame.key.get_pressed()
				if not(self.pressed[pygame.K_UP]) and not(self.pressed[pygame.K_DOWN]) and not(self.pressed[pygame.K_RETURN]) and not(self.pressed[pygame.K_ESCAPE]):					
					self.isButtonUp = True
		
				done = self.dispatcher.process(self, event)
				
		except Exception:
			print Exception
			traceback.print_exc(file=sys.stdout)
					
		finally:
			print "Thread STOP"
			self.myThread.stop()
			print "Thread STOPPED"
			pygame.quit()
			print "Pygame quit"
			try:
				sys.exit()
				print "SYS exit"
			except Exception:
				print Exception
				traceback.print_exc(file=sys.stdout)
			
			
class ATTDispatcher:
	
	app = None
	
	currentController = None
	controllers = None

	def __init__(self, app):
		self.app = app
		self.controllers = {}
		
	def buildControllers(self):
		
		view = LogonView(self.app.surface)
		controller = LogonController(view)
		self.appendController(controller)
		
		view = MenuView(self.app.surface)
		controller = MenuController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
		
		view = ShortServiceView(self.app.surface)
		controller = ShortServiceController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
		
		view = MultiBallView(self.app.surface)
		controller = MultiBallController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
		
		view = RallyView(self.app.surface)
		controller = RallyController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
		
		view = SandboxView(self.app.surface)
		controller = SandboxController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
	
	def appendController(self, controller):
		self.controllers[controller.ID] = controller
		
	def getController(self, controller_id):
		return self.controllers[controller_id]
	
	def setController(self, controller_id):
		self.currentController = self.getController(controller_id)
		self.currentController.start()
		
	def process(self, app, event):
		return self.currentController.process(app, event)
	
class TableHitPredictor (object):
	leftPredictor = None
	rightPredictor= None
	
	def __init__(self):
		
		predBuilder = predictorBuilder.PredictorBuilder()
		self.leftPredictor = predBuilder.buildInstance("../../data/train_points_20160303_left.txt")
		self.rightPredictor = predBuilder.buildInstance("../../data/train_points_20160303_right.txt")
		
	def predictHit(self, hit):
		side = hit["side"]
		if side == 'l':
			return self.leftPredictor.predictHit(hit)
		else:
			return self.rightPredictor.predictHit(hit)
		
	
if __name__ == '__main__':
	theApp = TheApp()
	theApp.main()