# -*- coding: utf-8 -*-

import time
import threading

class ShortServiceProtocol:

	notifier = None
	view = None
	state = None
	currentState = None
	lastHit = None
	currentHit = None
	timeoutThread = None
	
	def __init__(self, view, notifier, state):
		self.view = view
		self.notifier = notifier
		self.state = state
	
	def processSate(self, hit):
	
		if self.currentState == None and self.lastHit == None:
			self.currentState = 1
			
		if self.currentState == 1:
			self.state.clear()
			self.currentHit = hit
			self.lastHit = None
			self.currentState = 2
								
			self.timeoutThread = ProtocolTimeoutThread(1, self)
			self.timeoutThread.start()
			return
	
		if self.currentState == 2:
			self.lastHit = self.currentHit
			self.currentHit = hit
			
			time_delta = hit["tstamp"] - self.lastHit["tstamp"]
			self.notifier.push(str(time_delta))
			self.currentState = 1
			
			self.timeoutThread.stop()
			self.timeoutThread = None
								
			self.completedService()
			
			return
	
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
						
	def completedService(self):					
		service = {}
		service['first'] = {}
		service['first']['coords'] = self.lastHit['coords']
		service['first']['tstamp'] = self.lastHit['tstamp']
		service['second'] = {}
		service['second']['coords'] = self.currentHit['coords']
		service['second']['tstamp'] = self.currentHit['tstamp']
		self.state.addServiceEvent(service)
	
	def timedOutService(self):
		service = {}
		service['first'] = {}
		service['first']['coords'] = self.currentHit['coords']
		service['first']['tstamp'] = self.currentHit['tstamp']
		service['second'] = {}
		service['second']['coords'] = ""
		service['second']['tstamp'] = "TIMED_OUT"
		self.state.addServiceEvent(service)
		
	def pause(self):
		if self.timeoutThread != None:
			self.timeoutThread.pause()
	
	def unpause(self):
		if self.timeoutThread != None:
			self.timeoutThread.unpause()

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
