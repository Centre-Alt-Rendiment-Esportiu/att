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
		
		self.publisher = None
		#self.publisher = PikaPublisher("my_queue")

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
			
			#time.sleep(0.1)
			
			if (self.serial_port != None and self.serial_port.isOpen()):
				while iterations < self.max_readings or self.max_readings == None:
					
					#time.sleep(0.01)
					
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
			if reading != "":
				
				if self.publisher != None:
					the_reading = reading + "/" + str(time.time())
					self.publisher.publish(the_reading)

				hit = self.processor.parse_hit(reading)
				self.queue.put(hit)
				
				
				
				self.connected = True
				self.write_log("Reading from serial: " + reading)
			else:
				time.sleep(0.1)
				pass
		except:
			self.write_log("Miss!")
			self.serial_port.close()
			self.connected = False
			traceback.print_exc(file=sys.stdout)
			return False
			
		return True

	def write_log(self, str_message):
		print(str_message)
		sys.stdout.flush()
		
	def stop(self):
		self.is_stopped = True
		
	def restart(self):
		self.is_stopped = False

	def pause(self):
		self.is_stopped = True
		
	def unpause(self):
		self.is_stopped = False


import pika

class PikaPublisher(object):
	def __init__(self, queue_name):
		self.queue_name = queue_name
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))

	def publish(self, message):  	
		channel = self.connection.channel()
		
		channel.queue_declare(queue=self.queue_name, durable=True)
		channel.basic_publish(exchange='',
			routing_key=self.queue_name,
			body=message,
			properties=pika.BasicProperties(
				delivery_mode = 2, # make message persistent
			))
		
		channel.close()
		
	def close(self):
		self.connection.close()

