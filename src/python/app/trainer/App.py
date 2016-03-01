# -*- coding: utf-8 -*-

import sys

import platform
from pip._vendor.cachecontrol import controller

PROJECT_ROOT = ""
if platform.platform().lower().startswith("win"):
	PROJECT_ROOT = "I:/dev/workspaces/python/att-workspace/att/"
else:
	if platform.platform().lower().startswith("linux"):
		PROJECT_ROOT = "/home/asanso/workspace/att-spyder/att/"
		
sys.path.insert(0, PROJECT_ROOT + "/src/python/")

import pygame
import traceback

import Queue

from hit.serial.serial_port import *
from hit.serial.serial_port_builder import *
from hit.serial.serial_reader import *

from hit.process.processor import ATTMatrixHitProcessor
from hit.process.processor import ATTPlainHitProcessor
from hit.train.regressor import ATTClassicHitRegressor
from hit.train.regressor import ATTSkLearnHitRegressor

from app.trainer.serialLogNotifier import SerialLogNotifier

from app.trainer.controller import MenuController
from app.trainer.controller import ShortServiceController
from app.trainer.controller import MultiBallController
from app.trainer.controller import SandboxController
from app.trainer.controller import WholePointSequenceController

import predictorBuilder

from app.trainer.view import SurfaceView
from app.trainer.view import MenuView
from app.trainer.view import ShortServiceView
from app.trainer.view import MultiBallView
from app.trainer.view import SandboxView
from app.trainer.view import WholePointSequenceView

class TheApp:
	pressed = None
	isButtonUp = True
	
	predBuilder = None
	predictor = None
	workQueue = None
	notifier = None
	surface = None
	myThread = None
	
	dispatcher = None
	
	def __init__(self):
		pass

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
		#surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
		self.surface = pygame.display.set_mode((windowWidth, windowHeight))
		
	def buildHitDataSource(self):
		predBuilder = predictorBuilder.PredictorBuilder()
		self.predictor = predBuilder.buildInstance()
		
		self.workQueue = Queue.Queue(10)
		
		port = "/dev/ttyACM0"
		HITS_DATA_FILE = "../../../arduino/data/train_20160129_left.txt"
		port = HITS_DATA_FILE
		baud = 115200
		
		serialBuilder = ATTHitsFromFilePortBuilder()
		serial_port = ATTHitsFromFilePort(port, baud)
		
		self.myThread = ThreadedSerialReader(1, "Thread-1", self.workQueue, None, serialBuilder, port, baud, serial_port, False)
		self.myThread.start()
		
	def main(self):

		windowWidth = 1280 #1024
		windowHeight = 768 #768

		self.buildHitDataSource()
		
		pygame.init()
		
		self.buildScenario(windowWidth, windowHeight)
		self.notifier = SerialLogNotifier(self.surface, (55,78,100,100))
		
		self.dispatcher = ATTDispatcher(self)
		
		self.dispatcher.buildControllers()
		self.dispatcher.setController(MenuController.ID)
		
		try:
			done = False
			clock = pygame.time.Clock()
			
			while not done:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						done = True
					
				self.pressed = pygame.key.get_pressed()
				if not(self.pressed[pygame.K_UP]) and not(self.pressed[pygame.K_DOWN]) and not(self.pressed[pygame.K_RETURN]) and not(self.pressed[pygame.K_ESCAPE]):					
					self.isButtonUp = True
		
				self.dispatcher.process(self)
				
				pygame.display.flip()
				clock.tick(60)
				
		except Exception:
			print Exception
			traceback.print_exc(file=sys.stdout)
					
		finally:
			self.myThread.stop()
			pygame.quit()
			sys.exit()
			
			
class ATTDispatcher:
	
	app = None
	
	currentController = None
	controllers = None

	def __init__(self, app):
		self.app = app
		self.controllers = {}
		
	def buildControllers(self):
		view = MenuView(self.app.surface)
		controller = MenuController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
		
		view = ShortServiceView(self.app.surface)
		controller = ShortServiceController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
		
		view = MultiBallView(self.app.surface)
		controller = MultiBallController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
		self.appendController(controller)
		
		view = WholePointSequenceView(self.app.surface)
		controller = WholePointSequenceController(view, self.app.predictor, self.app.workQueue, self.app.notifier)
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
		
	def process(self, app):
		self.currentController.process(app)
	
	
if __name__ == '__main__':
	theApp = TheApp()
	theApp.main()