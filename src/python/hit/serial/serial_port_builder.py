# -*- coding: utf-8 -*-

import abc
import serial_port

class SerialPortBuilder:
	__metaclass__ = abc.ABCMeta
		
	@abc.abstractmethod
	def build_serial_port(self, port=None, baud=None):
		pass

class DummySerialPortBuilder (SerialPortBuilder):
	def __init__(self):
		pass

	def build_serial_port(self, port=None, baud=None):
		return serial_port.DummySerialPort(port, baud)
		
class ATTEmulatedSerialPortBuilder (SerialPortBuilder):
	def __init__(self):
		pass

	def build_serial_port(self, port=None, baud=None):
		return serial_port.ATTEmulatedSerialPort(port, baud)

class ATTArduinoSerialPortBuilder (SerialPortBuilder):
	def __init__(self):
		pass

	def build_serial_port(self, port=None, baud=None):
		return serial_port.ATTArduinoSerialPort(port, baud)
		
class ATTHitsFromFilePortBuilder (SerialPortBuilder):
	def __init__(self):
		pass

	def build_serial_port(self, port=None, baud=None):
		return serial_port.ATTHitsFromFilePort(port, baud)

