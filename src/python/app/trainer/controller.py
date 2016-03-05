# -*- coding: utf-8 -*-

import abc

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

from session_manager import SessionManager
from protocol import ShortServiceProtocol



import time

class ATTController:
	__metaclass__ = abc.ABCMeta
	
	#surface = None
	view = None
	
	@abc.abstractmethod
	def start(self):
		pass
	
	@abc.abstractmethod
	def process(self, app, event):
		pass
	
	def clear(self):
		self.view.clear()

class LogonController (ATTController):
	
	ID = "LOGON"
	
	def __init__(self, view):
		self.view = view
	
	def start(self):
		pass
	
	def render(self):
		pygame.display.flip()
		
	def get_key(self):
		while 1:
			event = pygame.event.poll()
			if event.type == pygame.KEYDOWN:
				return event.key
		else:
			pass
	
	def display_box(self, message):
		screen = self.view.surface
		"Print a message in a box in the middle of the screen"
		fontobject = pygame.font.Font(None,18)
		pygame.draw.rect(screen, (0,0,0),
			((screen.get_width() / 2) - 100,
			(screen.get_height() / 2) - 10,
			200,20), 0)
		pygame.draw.rect(screen, (255,255,255),
			((screen.get_width() / 2) - 102,
			(screen.get_height() / 2) - 12,
			204,24), 1)
		if len(message) != 0:
			screen.blit(fontobject.render(message, 1, (255,255,255)),
					((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
		pygame.display.flip()
	
	def ask(self, question):
		screen = self.view.surface
		"ask(screen, question) -> answer"
		pygame.font.init()
		current_string = []
		self.display_box(question + ": " + string.join(current_string,""))
		while 1:
			inkey = self.get_key()
			if inkey == K_BACKSPACE:
				current_string = current_string[0:-1]
			elif inkey == K_RETURN:
				break
			elif inkey == K_MINUS:
				current_string.append("_")
			elif inkey <= 127:
				current_string.append(chr(inkey))
				self.display_box(question + ": " + string.join(current_string,""))
		return string.join(current_string,"")

	def process(self, app, event):
		done = False

		credentials = self.ask("Name")
		pieces = credentials.split(",")
		if len(pieces) == 2:
			username = pieces[0]
			password = pieces[1]
			
			sm = SessionManager()
			if sm.validateCredentials(username, password):
				app.pressed = []
				app.isButtonUp = False
				self.clear()
				
				#app.buildHitDataSource()
				#self.myThread = ThreadedSerialReader(1, "Thread-1", self.workQueue, None, serialBuilder, port, baud, serial_port, False)
				#self.myThread.start()

				app.dispatcher.setController(MenuController.ID)
			else:
				time.sleep(0.1)
		
		return done
	
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
			percentCoords = (30, 10+6*i)
			
			if not(i == self.currentOption):
				self.view.renderUnSelectedOption(optionLabel['label'], percentCoords)
			else:
				self.view.renderSelectedOption(optionLabel['label'], percentCoords)
			
		self.renderSerialLog()
		pygame.display.flip()
		
	def renderSerialLog(self):
		
		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app, event):
		done = False
		
		if app.isPressed(pygame.K_ESCAPE):
			return True
			
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
		#self.renderSerialLog()
		self.renderSummary()
		pygame.display.flip()
	
	def renderSerialLog(self):
		
		self.notifier.clear()
		self.notifier.render()
		
	def renderSummary(self):
		if self.state == 1:
			if len(self.summary) > 0:
				self.view.renderSummary(self.summary)
			
	def process(self, app, event):
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
		
		self.view.drawHit(x, y, hit["side"])
		
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
		self.view.drawMessage()
		self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):

		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app, event):
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
		
		#self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):
		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app, event):
		done = False
		
		if not self.workQueue.empty():
			hit = self.workQueue.get()
			if hit <> "":
				self.processHit(hit)		
		
		if app.isPressed(pygame.K_c):
			self.clear()
			self.view.buildScenario()

		if event.type == pygame.MOUSEMOTION:
			#print event.pos
			pass
			
		self.render()
				
		if app.isPressed(pygame.K_ESCAPE):
			self.clear()
			app.dispatcher.setController(MenuController.ID)

		return done
	
	def processHit(self, hit):
		(y,x) = self.predictor.predictHit(hit)
		#print hit
		self.view.drawHit(x, y, hit["side"]);
		
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
		self.view.drawMessage()
		self.renderSerialLog()
		pygame.display.flip()
	
	def renderSerialLog(self):
		
		self.notifier.clear()
		self.notifier.render()
		
	def process(self, app, event):
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
