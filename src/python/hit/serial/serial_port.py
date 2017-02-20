# -*- coding: utf-8 -*-

import abc

import time
import random
import serial

class SerialPort(metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def start(self):
		pass
	
	@abc.abstractmethod
	def isOpen(self):
		pass
		
	@abc.abstractmethod
	def readline(self, *isFast):
		pass
		
	@abc.abstractmethod
	def close(self):
		pass
	
	@abc.abstractmethod
	def get_port(self):
		return ""
		
	@abc.abstractmethod
	def get_baudrate(self):
		return 0
		
class DummySerialPort (SerialPort):
	def __init__(self, port = None, baud = None):
		pass
	
	def start(self):
		pass
	
	def isOpen(self):
		return True
		
	def close(self):
		pass
		
	def get_port(self):
		return ""
		
	def get_baudrate(self):
		return 0
		
	def readline(self, *isFast):
		if (len(isFast)):
			time_delay = 2*random.random()
			time.sleep(time_delay)
		
		return self.gen_random_line()
		
	def gen_random_line(self):
		return "Hee"
	
class SilentSerialPort (SerialPort):
	def __init__(self, port = None, baud = None):
		pass
	
	def start(self):
		pass
	
	def isOpen(self):
		return True
		
	def close(self):
		pass
		
	def get_port(self):
		return ""
		
	def get_baudrate(self):
		return 0
		
	def readline(self, *isFast):
		return ""
		
	def gen_random_line(self):
		return ""
		
class ATTEmulatedSerialPort (SerialPort):
	def __init__(self, port = None, baud = None):
		pass
	
	def start(self):
		pass
	
	def isOpen(self):
		return True
		
	def close(self):
		pass
		
	def get_port(self):
		return ""
		
	def get_baudrate(self):
		return 0
		
	def readline(self, *isFast):
		if (len(isFast)):
			time_delay = 2*random.random()
			time.sleep(time_delay)

		return self.gen_random_line()
		
	def gen_random_line(self):
		hits = [
			"hit: {1404 1268 0 440 500 1200 81 1 r}", 
			"hit: {0 2080 3824 3132 884 1812 1088 1 r}",
			"hit: {0 2156 13312 2268 964 1988 1172 1 r}",
			"hit: {0 2188 11764 2300 884 1916 1176 1 r}",
			"hit: {0 2080 8744 1076 884 1904 1184 1 r}",
			"hit: {0 2080 3848 3144 884 1896 1172 1 r}",
			"hit: {84 548 5948 1672 0 592 20 1 r}",
			"hit: {84 552 2224 1660 0 588 20 1 r}",
			"hit: {0 572 2332 1604 388 608 44 1 r}",
			"hit: {64 508 2164 1896 428 544 0 1 r}",
			"hit: {68 516 2260 1628 440 556 0 1 r}",
			"hit: {1304 0 1772 1592 112 392 408 1 r}",
			"hit: {1468 0 1768 2312 192 372 388 1 r}",
			"hit: {1456 0 1848 2296 188 464 476 1 r}",
			"hit: {1184 256 9984 1404 0 936 188 1 r}",
			"hit: {1300 0 3600 1608 108 372 388 1 r}",
			"hit: {2916 0 1796 2504 808 632 460 1 r}",
			"hit: {7244 0 1820 11408 816 628 456 1 r}",
			"hit: {1704 0 1992 2528 808 636 464 1 r}",
			"hit: {2908 0 10308 2496 808 636 460 1 r}",
			"hit: {1708 0 1340 3372 808 636 464 1 r}",
			"hit: {0 1712 2428 1832 644 1112 560 1 r}",
			"hit: {0 1292 1752 640 656 1112 560 1 r}",
			"hit: {0 1300 1756 1768 660 1120 576 1 r}",
			"hit: {0 1576 2324 552 212 1056 584 1 r}",
			"hit: {0 1304 1764 1780 216 1124 576 1 r}",
			"hit: {532 920 15992 1380 0 564 284 1 r}",
			"hit: {640 940 1936 1484 0 560 288 1 r}",
			"hit: {720 920 3580 1464 0 560 288 1 r}",
			"hit: {640 932 16380 1316 0 564 288 1 r}",
			"hit: {624 828 5920 1300 0 460 280 1 r}",
			"hit: {916 428 6912 2100 352 556 0 1 r}",
			"hit: {896 704 3260 2064 332 540 0 1 r}",
			"hit: {1004 420 1548 3676 344 648 0 1 r}",
			"hit: {904 800 6992 2016 352 632 0 1 r}",
			"hit: {996 808 7012 2116 348 640 0 1 r}",
			"hit: {1636 0 1104 2928 652 460 568 1 r}",
			"hit: {1692 0 2996 2908 632 544 660 1 r}",
			"hit: {1704 0 1096 2976 624 536 652 1 r}",
			"hit: {1704 0 2932 3056 632 544 664 1 r}",
			"hit: {1720 0 1188 2968 724 636 752 1 r}",
			"hit: {0 976 17052 24 124 620 144 1 r}",
			"hit: {0 1048 3204 576 196 592 212 1 r}",
			"hit: {248 1244 7188 272 0 776 388 1 r}",
			"hit: {796 1208 12816 708 0 728 352 1 r}",
			"hit: {164 1232 7096 88 0 796 404 1 r}",
			"hit: {1440 1260 3144 808 0 824 360 1 r}",
			"hit: {792 1288 1200 816 0 836 460 1 r}",
			"hit: {712 1180 1196 736 0 836 456 1 r}",
			"hit: {780 1172 4736 800 0 820 364 1 r}",
			"hit: {804 1284 1296 828 0 456 472 1 r}"
		]
		return random.choice(hits)
		
class ATTArduinoSerialPort (SerialPort):
	
	port = None
	baud = None
	logFile = None
	
	def __init__(self, port = None, baud = None):
		self.port = port
		self.baud = baud
		self.start()
		self.logFile = open("log/2016_03_03_1820.log","w")
	
	def start(self):
		self.serial_port = serial.Serial(self.port, self.baud)
	
	def isOpen(self):
		return self.serial_port.isOpen()
		
	def close(self):
		self.serial_port.close()
		
	def readline(self, *isFast):
		if (len(isFast)):
			time_delay = 2*random.random()
			time.sleep(time_delay)
			
		line = self.serial_port.readline()
		tstamp = time.time()
		full_line = line.splitlines()[0]+"/"+str(tstamp)+"\n"
		self.logFile.write(full_line)
		self.logFile.flush()
		return line
		
	def get_port(self):
		return self.serial_port.port
		
	def get_baudrate(self):
		return self.serial_port.baudrate
		
class ATTHitsFromFilePort (SerialPort):
	
	port = None
	baud = None
	lines = None
	inner_index = None
	amIclosed = None
	lastTS = None
	
	def __init__(self, port = None, baud = None):
		self.port = port
		self.baud = baud
		self.lines = [line.strip() for line in file(self.port) if line.startswith("hit:")]
		self.inner_index = 0
		self.amIclosed = 0
		self.lastTS = 0
		self.start()
	
	def start(self):
		#self.lines = [line.strip() for line in file(self.port) if line.startswith("hit:")]
		self.inner_index = 0
		self.amIclosed = 0
		
	def isOpen(self):
		return not self.amIclosed
		
	def close(self):
		pass
		
	def get_port(self):
		return ""
		
	def get_baudrate(self):
		return 0
		
	def readline(self, *isFast):
		
		if (len(isFast)):
			#time_delay = random.random()
			time_delay = 0.1
			time.sleep(time_delay)
		
		line = ""
		if self.inner_index < len(self.lines):
			line = self.lines[self.inner_index]
			pieces = line.split("/")
			line = pieces[0]
			if len(pieces)>1:
				delta = float(pieces[1]) - self.lastTS
				print(delta)
				if self.lastTS != float(0):
					time.sleep(delta)
					pass				
					
				self.lastTS = float(pieces[1])
				
			self.inner_index += 1
		else:
			self.amIclosed = 1
		return line








