# -*- coding: utf-8 -*-

import importlib
from astropy.modeling import powerlaws

"""
MyPort = getattr(importlib.import_module("hit.serial.serial_port"), "DummySerialPort")
MyPort = getattr(importlib.import_module("hit.serial.serial_port"), "ATTEmulatedSerialPort")
MyPort = getattr(importlib.import_module("hit.serial.serial_port"), "ATTHitsFromFilePort")

instance = MyPort()
print instance.readline(1)
"""

class Container:
	
	def __init__(self):
		pass
	
	@staticmethod
	def getClass(package, className):
		return getattr(importlib.import_module(package), className)
		
	@staticmethod
	def getInstance(package, className, *args):
		myClass = Container.getClass(package, className)
		return myClass(*args)


myPackage = "hit.serial.serial_port"
myClassName = "ATTEmulatedSerialPort"
port = "../../../arduino/data/rally_demo_2.txt"
baud = ""

instance = Container.getInstance(myPackage, myClassName, port, baud)
print(instance.readline())
print(instance.readline())
print(instance.readline())
print(instance.readline())
print(instance.readline())
print(instance.readline())
print(instance.readline())
print(instance.readline())
