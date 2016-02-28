# -*- coding: utf-8 -*-

import pygame

from baseState import BaseState

from serialLogNotifier import SerialLogNotifier

from app.trainer.view import SurfaceView

class SandboxState (BaseState):
	
	notifier = None
	surface = None
	workQueue = None
	predictor = None
	font = None
	view = None

	def __init__(self, surface, predictor, workQueue, notifier):
		self.surface = surface
		self.font = pygame.font.Font(None, 36)
		self.predictor = predictor
		self.workQueue = workQueue
		self.notifier = notifier
		self.view = SurfaceView(self.surface)

	def start(self):
		pass
		
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
		
		if isPressed(pygame.K_c):
			self.clear()
			self.view.displayScenario()
			
		self.render()
				
		if isPressed(pygame.K_ESCAPE):
			self.clear()
			setState(0, self)

		return done
	
	def processHit(self, hit):
		(y,x) = self.predictor.predictHit(hit)
		self.view.drawHit(x, y);
		
		logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
		print logReading
		self.notifier.push(logReading)

	
