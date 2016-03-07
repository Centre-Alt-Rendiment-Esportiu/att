# -*- coding: utf-8 -*-

import time
import threading

class ShortServiceProtocol:

	notifier = None
	view = None
	controller = None
	timeoutThread = None
	
	currentState = None
	
	lastHit = None
	currentHit = None
	firstHit = None
	secondHit = None
	thirdHit = None
	
	
	def __init__(self, view, notifier, controller):
		self.view = view
		self.notifier = notifier
		self.controller = controller
		
	def processSate(self, hit):
	
		if self.currentState == None and self.lastHit == None:
			self.currentState = 1
			
		if self.currentState == 1:
			self.controller.clearView()
			self.currentHit = hit
			self.lastHit = None
			self.currentState = 2
		
			self.timeoutThread = ProtocolTimeoutThread(1, self)
			self.timeoutThread.start()
			return
	
		if self.currentState == 2:
			self.timeoutThread.stop()
			self.timeoutThread = None

			self.lastHit = self.currentHit
			self.firstHit = self.lastHit
			self.currentHit = hit
			
			if self.lastHit["side"] <> self.currentHit["side"]:
				self.logHitDeltaInNotifier(hit)
				
				self.currentState = 3
				
				self.timeoutThread = ProtocolTimeoutThread(2, self)
				self.timeoutThread.start()
			else:
				self.controller.clearView()
				self.currentHit = hit
				self.lastHit = None
				self.currentState = 2

				self.timeoutThread = ProtocolTimeoutThread(1, self)
				self.timeoutThread.start()
			
			#self.completedService()
			return
			
		if self.currentState == 3:
			self.timeoutThread.stop()
			self.timeoutThread = None

			self.lastHit = self.currentHit
			self.secondtHit = self.lastHit
			self.currentHit = hit
			
			if self.lastHit["side"] == self.currentHit["side"]:
				self.logHitDeltaInNotifier(hit)
				
				self.currentState = 1
				self.thirdHit = hit
				self.completedService()
			
			return
	
	def getDelta(self, hit):
		if self.lastHit == None:
			return 0
		else:
			return hit["tstamp"] - self.lastHit["tstamp"]
	
	def logHitDeltaInNotifier(self, hit):
		time_delta = self.getDelta(hit)
		self.notifier.push(str(time_delta))
	
	def notify(self):
		time_now = time.time()
		
		time_delta = time_now - self.currentHit["tstamp"]
		self.notifier.push(str(time_delta))
		
		if time_delta > 3 and self.currentState == 2:
			self.timedOutService()
			self.notifier.push("TIMEOUT !!!")
			self.currentState = 1
			self.currentHit = None
			self.lastHit = None
			self.timeoutThread.stop()
			self.timeoutThread = None
			
		if time_delta > 3 and self.currentState == 3:
			self.timedOutService()
			self.notifier.push("TIMEOUT !!!")
			self.currentState = 1
			self.currentHit = None
			self.lastHit = None
			self.timeoutThread.stop()
			self.timeoutThread = None
			
		#if self.lastHit["side"] == self.currentHit["side"] and self.currentState == 3:
		#	pass
						
	def completedService(self):
		"""
		service = {}
		service['first'] = {}
		service['first']['coords'] = self.firstHit['coords']
		service['first']['tstamp'] = self.firstHit['tstamp']
		service['second'] = {}
		service['second']['coords'] = self.secondHit['coords']
		service['second']['tstamp'] = self.secondHit['tstamp']
		service['third'] = {}
		service['third']['coords'] = self.thirdHit['coords']
		service['third']['tstamp'] = self.thirdHit['tstamp']
		self.controller.addServiceEvent(service)
		"""
		pass
	
	def timedOutService(self):
		"""
		service = {}
		service['first'] = {}
		service['first']['coords'] = self.currentHit['coords']
		service['first']['tstamp'] = self.currentHit['tstamp']
		service['second'] = {}
		service['second']['coords'] = ""
		service['second']['tstamp'] = "TIMED_OUT"
		self.controller.addServiceEvent(service)
		"""
		pass
	
	def pause(self):
		if self.timeoutThread != None:
			self.timeoutThread.pause()
	
	def unpause(self):
		if self.timeoutThread != None:
			self.timeoutThread.unpause()

class RallyProtocol:

	notifier = None
	view = None
	controller = None
	timeoutThread = None
	
	currentState = None
	
	currentHit = None
	hitsList = None
	
	
	def __init__(self, view, notifier, controller):
		self.view = view
		self.notifier = notifier
		self.controller = controller
		self.hitsList = []
		
	def processSate(self, hit):
	
		if self.currentState == None and self.hitsList == []:
			self.currentState = 1
			self.controller.clearView()
			
		if self.currentState == 1:
			
			self.currentHit = hit
			self.lastHit = None
			self.currentState = 1
		
			self.hitsList.append(hit)

			self.timeoutThread = ProtocolTimeoutThread(1, self)
			self.timeoutThread.start()
			return
		
		if self.currentState == 2:
			pass
		
	def completedService(self):
		pass
	
	def timedOutService(self):
		pass

	def notify(self):
		time_now = time.time()
		
		if self.currentHit <> None:
			time_delta = time_now - self.currentHit["tstamp"]
			self.notifier.push(str(time_delta))
			
			if time_delta > 3:
				if self.timeoutThread <> None:
					self.timeoutThread.stop()
					self.timeoutThread = None
	
				self.currentState = None
				self.hitsList = []
				self.currentHit = None


class ProtocolTimeoutThread (threading.Thread):
	
	protocol = None
	is_stopped = None
	
	def __init__(self, threadID, protocol):
		threading.Thread.__init__(self)
		self.protocol = protocol
		self.is_stopped = False
	
	def run(self):
	
		while not self.is_stopped:
			time.sleep(0.001)
			self.protocol.notify()
		
	def stop(self):
		self.is_stopped = True

	def pause(self):
		self.is_stopped = True		
	
	def unpause(self):
		self.is_stopped = False
