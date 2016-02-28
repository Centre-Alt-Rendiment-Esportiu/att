# -*- coding: utf-8 -*-

import pygame

from baseState import BaseState

from serialLogNotifier import SerialLogNotifier

class MenuState (BaseState):
	
	notifier = None
	workQueue = None
	predictor = None
	font = None
	currentOption = 0
	
	menuOptionsLabels = [
		"Short service",
		"Multiball",
		"Whole point sequence",
		"Sandbox"
	]
	
	def __init__(self, surface, predictor, workQueue, notifier):
		self.surface = surface		
		self.font = pygame.font.Font(None, 66)
		self.predictor = predictor
		self.workQueue= workQueue
		self.notifier = notifier

	def render(self):
		for i in range(len(self.menuOptionsLabels)):
			if not(i == self.currentOption):
				text = self.font.render(self.menuOptionsLabels[i], 1, (100, 100, 100))
			else:
				text = self.font.render(self.menuOptionsLabels[i], 1, (250, 250, 250))
				
			self.surface.blit(text, (self.getX(30), self.getY(10 + 6 * i)))
			
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
				(y,x) = self.predictor.predictHit(hit)
				logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
				print logReading
				self.notifier.push(logReading)

		if isPressed(pygame.K_DOWN):
			self.currentOption = (self.currentOption + 1) % len(self.menuOptionsLabels)

		if isPressed(pygame.K_UP):
			self.currentOption = (self.currentOption + len(self.menuOptionsLabels) - 1) % len(self.menuOptionsLabels)

		self.render()
		
		if isPressed(pygame.K_RETURN):
			self.surface.fill((0, 0, 0))
			self.clear()
			setState(self.currentOption + 1, self)
			
		
		
		return done
