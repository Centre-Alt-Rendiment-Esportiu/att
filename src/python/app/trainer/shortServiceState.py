# -*- coding: utf-8 -*-

import pygame

from baseState import BaseState

from serialLogNotifier import SerialLogNotifier

from app.trainer.view import SurfaceView
from protocol import ShortServiceProtocol

class ShortServiceState (BaseState):

	notifier = None	
	workQueue = None
	predictor = None
	font = None
	view = None
	protocol = None
	servicesList = None

	def __init__(self, surface, predictor, workQueue, notifier):
		self.surface = surface
		self.font = pygame.font.Font(None, 36)
		self.predictor = predictor
		self.workQueue = workQueue
		self.notifier = notifier
		self.view = SurfaceView(self.surface)
		self.protocol = ShortServiceProtocol(self.view, self.notifier, self)
		
	def start(self):
		self.servicesList = []
	
	def render(self):
		self.view.displayScenario()
				
		self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):
		
		self.notifier.clear()
		self.notifier.render()
		
	def loop(self, setState, isPressed):
		done = False

		if not self.workQueue.empty():
			hit = self.workQueue.get()
			if hit <> "":
				self.processHit(hit)

		self.render()
				
		if isPressed(pygame.K_ESCAPE):
			print self.servicesList
			self.clear()
			setState(0, self)

		return done
	
	def processHit(self, hit):
		(y,x) = self.predictor.predictHit(hit)
		hit['coords'] = (y,x)
		
		logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
		print logReading
		self.notifier.push(logReading)
		
		self.protocol.processSate(hit)
		
		self.view.drawHit(x, y);
		
		

