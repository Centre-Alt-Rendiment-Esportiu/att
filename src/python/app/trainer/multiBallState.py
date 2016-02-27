# -*- coding: utf-8 -*-

import pygame

from baseState import BaseState

from serialLogNotifier import SerialLogNotifier

from view import Ball
from view import SurfaceView

class MultiBallState (BaseState):
	
	notifier = None
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
			
	def render(self):
		text = self.font.render("Multi Ball", 1, (250, 250, 250))
		self.surface.blit(text, (self.getX(10), self.getY(10)))
		
		self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):

		self.notifier.clear()
		self.notifier.render()
		
	def loop(self, setState, isPressed):
		done = False

		if not self.workQueue.empty():
			reading = self.workQueue.get()
			if reading <> "":		
				(y,x) = self.predictor.predict(reading)
				logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+reading
				print logReading
				self.notifier.push(logReading)

		self.render()

		if isPressed(pygame.K_ESCAPE):
			self.clear()
			setState(0, self)
			
		return done
