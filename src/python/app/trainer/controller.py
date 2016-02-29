# -*- coding: utf-8 -*-

import abc

import pygame

from app.trainer.view import SurfaceView
from app.trainer.protocol import ShortServiceProtocol

class ATTController:
	__metaclass__ = abc.ABCMeta
	
	#surface = None
	view = None
	
	@abc.abstractmethod
	def start(self):
		pass
	
	@abc.abstractmethod
	def process(self, app, isPressed):
		pass
	
	def clear(self):
		#self.surface.fill((0, 0, 0))
		#self.view.surface.fill((0, 0, 0))
		self.view.clear()
				
	def getX(self, _x):
		return self.view.getX(_x)
	
	def getY(self, _y):
		return self.view.getY(_y)

class MenuController (ATTController):
	
	ID = "MENU"
	
	notifier = None
	workQueue = None
	predictor = None
	font = None
	currentOption = 0
	
	menuOptionsLabels = [{
		"id": "SHORT_SERVICE",
		"label": "Short service",
		"position": 1
	}, {
		"id": "MULTI_BALL",
		"label":"Multiball",
		"position": 2
	}, {
		"id": "POINT_SEQUENCE",
		"label": "Whole point sequence",
		"position": 3
	}, {
		"id": "SAND_BOX",
		"label": "Sandbox",
		"position": 4
	}]
	
	def __init__(self, view, predictor, workQueue, notifier):
		self.view = view		
		self.font = pygame.font.Font(None, 66)
		self.predictor = predictor
		self.workQueue= workQueue
		self.notifier = notifier

	def start(self):
		pass

	def getOptionLabelByPosition(self, position):
		for optionLabel in self.menuOptionsLabels:
			if (position == optionLabel['position']):
				return optionLabel
		pass
	
	def render(self):
		for i in range(len(self.menuOptionsLabels)):
			optionLabel = self.getOptionLabelByPosition(i+1)
			if not(i == self.currentOption):
				text = self.font.render(optionLabel['label'], 1, (100, 100, 100))
			else:
				text = self.font.render(optionLabel['label'], 1, (250, 250, 250))

			self.view.surface.blit(text, (self.getX(30), self.getY(10 + 6 * i)))
			
		self.renderSerialLog()
		pygame.display.flip()
		
	def renderSerialLog(self):
		
		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app):
		done = False
		
		if not self.workQueue.empty():
			hit = self.workQueue.get()
			if hit <> "":		
				(y,x) = self.predictor.predictHit(hit)
				logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
				print logReading
				self.notifier.push(logReading)

		if app.isPressed(pygame.K_DOWN):
			self.currentOption = (self.currentOption + 1) % len(self.menuOptionsLabels)

		if app.isPressed(pygame.K_UP):
			self.currentOption = (self.currentOption + len(self.menuOptionsLabels) - 1) % len(self.menuOptionsLabels)

		self.render()
		
		if app.isPressed(pygame.K_RETURN):
			self.clear()
			
			optionLabel = self.getOptionLabelByPosition(self.currentOption+1)
			controller_id = optionLabel['id']
			app.dispatcher.setController(controller_id)
		
		return done

class ShortServiceController (ATTController):

	ID = "SHORT_SERVICE"
	
	notifier = None	
	workQueue = None
	predictor = None
	font = None
	view = None
	protocol = None
	servicesList = None
	summary = []
	
	state = 0

	def __init__(self, view, predictor, workQueue, notifier):
		self.font = pygame.font.Font(None, 36)
		self.predictor = predictor
		self.workQueue = workQueue
		self.notifier = notifier
		self.view = view
		self.protocol = ShortServiceProtocol(self.view, self.notifier, self)
		
	def start(self):
		self.servicesList = []
		self.summary = []
	
	def render(self):
		self.view.buildScenario()
		self.renderSerialLog()
		self.renderSummary()
		pygame.display.flip()
	
	def renderSerialLog(self):
		
		self.notifier.clear()
		self.notifier.render()
		
	def renderSummary(self):
		if self.state == 1:
			if len(self.summary) > 0:
				
				blue = (0, 0, 70)
				black = (0, 0, 0)
				
				x1 = self.getX(20)
				y1 = self.getY(20)
				x2 = self.getX(70)
				y2 = self.getY(60)
				
				pointlist = [ (x1,y1), (x2,y1), (x2,y2), (x1,y2)]
				pygame.draw.lines(self.view.surface, blue, 1, pointlist, 2)				
				pygame.draw.rect(self.view.surface, black, (x1+1, y1+1, x2-10, y2-10))
				
				myFont = pygame.font.Font(None, 20)
				text = myFont.render(self.summary[0], 1, (70, 70, 70))
				self.view.surface.blit(text, (x1+20, y1+50))
			
	def process(self, app):
		done = False

		if not self.workQueue.empty():
			hit = self.workQueue.get()
			if hit <> "":
				self.processHit(hit)

		self.render()
							
		if app.isPressed(pygame.K_ESCAPE):
			self.clear()
			if self.state == 0:
				self.buildSummary()
				self.state = 1
				app.pressed = []
				app.myThread.pause()
				self.protocol.pause()
			else:
				self.state = 0
				app.myThread.unpause()
				self.protocol.unpause()
				app.dispatcher.setController(MenuController.ID)		
		
		return done
	
	def buildSummary(self):
		print self.servicesList
		
		total = 0
		done = 0
		for service in self.servicesList:
			total += 1
			if service['second'] and service['second']['tstamp'] != "TIMED_OUT":
				done += 1
				
		if total == 0:
			total = 1
		self.summary.append(""+str(float(done/total)*100)+"% done.      Completed="+str(done)+" from Total="+str(total))
		
	def processHit(self, hit):
		(y,x) = self.predictor.predictHit(hit)
		hit['coords'] = (y,x)
		
		logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
		print logReading
		self.notifier.push(logReading)
		
		self.protocol.processSate(hit)
		
		self.view.drawHit(x, y);
		
	def addServiceEvent(self, selfserviceEvent):
		self.servicesList.append(selfserviceEvent)
		
class MultiBallController (ATTController):
	
	ID = "MULTI_BALL"
	
	notifier = None
	workQueue = None
	predictor = None
	font = None
	view = None

	def __init__(self, view, predictor, workQueue, notifier):
		self.font = pygame.font.Font(None, 36)
		self.predictor = predictor
		self.workQueue = workQueue
		self.notifier = notifier
		self.view = view
			
	def start(self):
		pass
	
	def render(self):
		text = self.font.render("Multi Ball", 1, (250, 250, 250))
		self.view.surface.blit(text, (self.getX(10), self.getY(10)))
		
		self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):

		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app):
		done = False

		if not self.workQueue.empty():
			hit = self.workQueue.get()
			if hit <> "":		
				(y,x) = self.predictor.predictHit(hit)
				logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
				print logReading
				self.notifier.push(logReading)

		self.render()

		if app.isPressed(pygame.K_ESCAPE):
			self.clear()
			app.dispatcher.setController(MenuController.ID)
			
		return done

class SandboxController (ATTController):
	
	ID = "SAND_BOX"
	
	notifier = None
	workQueue = None
	predictor = None
	font = None
	view = None

	def __init__(self, view, predictor, workQueue, notifier):
		self.font = pygame.font.Font(None, 36)
		self.predictor = predictor
		self.workQueue = workQueue
		self.notifier = notifier
		self.view = view

	def start(self):
		pass
		
	def render(self):		
		self.view.buildScenario()
		
		self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):
		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app):
		done = False

		if not self.workQueue.empty():
			hit = self.workQueue.get()
			if hit <> "":
				self.processHit(hit)		
		
		if app.isPressed(pygame.K_c):
			self.clear()
			self.view.buildScenario()
			
		self.render()
				
		if app.isPressed(pygame.K_ESCAPE):
			self.clear()
			app.dispatcher.setController(MenuController.ID)

		return done
	
	def processHit(self, hit):
		(y,x) = self.predictor.predictHit(hit)
		self.view.drawHit(x, y);
		
		logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
		print logReading
		self.notifier.push(logReading)

class WholePointSequenceController (ATTController):

	ID = "POINT_SEQUENCE"
	
	notifier = None	
	workQueue = None
	predictor = None
	font = None
	view = None

	def __init__(self, view, predictor, workQueue, notifier):
		self.font = pygame.font.Font(None, 36)
		self.predictor = predictor
		self.workQueue = workQueue
		self.notifier = notifier
		self.view = view

	def start(self):
		pass
	
	def render(self):
		text = self.font.render("Whole point sequence", 1, (250, 250, 250))
		self.view.surface.blit(text, (self.getX(10), self.getY(10)))
		
		self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):
		
		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app):
		done = False

		if not self.workQueue.empty():
			hit = self.workQueue.get()
			if hit <> "":		
				(y,x) = self.predictor.predictHit(hit)
				logReading = "("+"{0:.0f}".format(y)+","+"{0:.0f}".format(x)+") - "+hit["raw"]
				print logReading
				self.notifier.push(logReading)

		self.render()
		
		if app.isPressed(pygame.K_ESCAPE):
			self.clear()
			app.dispatcher.setController(MenuController.ID)

		return done