# -*- coding: utf-8 -*-

import threading
import time
import sys

from hit.process.processor import ATTMatrixHitProcessor

import traceback

class ThreadedSerialReader (threading.Thread):
	def __init__(self, threadID, name, queue, max_readings, serial_port_builder, port, baud, CustomSerial=None, isFast=True):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.queue = queue
		self.connected = False
		self.max_readings = max_readings
		self.serial_port_builder = serial_port_builder
		self.port = port
		self.baudrate = baud
		self.custom_serial = CustomSerial 
		self.is_stopped = False
		self.build_serial()
		self.processor = ATTMatrixHitProcessor()
		self.isFast = isFast

	def build_serial(self):
		if self.custom_serial != None:
			self.serial_port = self.custom_serial
		else:
			self.serial_port = self.serial_port_builder.build_serial_port(self.port, self.baudrate)

	def run(self):
		self.write_log("Starting " + self.name)
		
		time.sleep(5)
		
		iterations = 0
		while not self.connected and not self.is_stopped:
			
			time.sleep(0.1)
			
			if (self.serial_port != None and self.serial_port.isOpen()):
				while iterations < self.max_readings or self.max_readings == None:
					if self.read_and_enqueue() == True:
						iterations = iterations + 1
					else:
						break
			else:
				time.sleep(0.1)
				try:
					self.serial_port = self.build_serial()
				except Exception:
					self.write_log("Error: Check the serial connection or cable, please.")

		self.write_log("Exiting " + self.name)
		
	def read_and_enqueue(self):
		
		try:
			if self.isFast:
				reading = self.serial_port.readline()
			else:
				reading = self.serial_port.readline(1)
			if reading <> "":
				hit = self.processor.parse_hit(reading)
				self.queue.put(hit)
				self.connected = True
				self.write_log("Reading from serial: " + reading)
			else:
				time.sleep(0.1)
		except:
			self.write_log("Miss!")
			self.serial_port.close()
			self.connected = False
			traceback.print_exc(file=sys.stdout)
			return False
			
		
		#reading = self.serial_port.readline()
		#self.queue.put(reading)
		
		return True

	def write_log(self, str_message):
		print str_message
		sys.stdout.flush()
		#time.sleep(0.1)
		pass
		
	def stop(self):
		self.is_stopped = True
		
	def restart(self):
		self.is_stopped = False

	def pause(self):
		self.is_stopped = True
		
	def unpause(self):
		self.is_stopped = False

