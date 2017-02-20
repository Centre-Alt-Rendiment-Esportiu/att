# -*- coding: utf-8 -*-

import queue
import time

from serial_port import *
from serial_port_builder import *
from serial_reader import *

connected = False
port = "/dev/ttyACM0"
# port ="COM3"
baud = 115200

# builder = DummySerialPortBuilder()
builder = ATTEmulatedSerialPortBuilder()
# builder = ATTArduinoSerialPortBuilder()

workQueue = queue.Queue(10000)

myThread = ThreadedSerialReader(1, "Thread-1", workQueue, 10, builder, port, baud)
myThread.start()
myThread.join()

myThread = ThreadedSerialReader(2, "Thread-2", workQueue, 1, builder, port, baud)
myThread.start()
myThread.join()

time.sleep(5)

while True:
    time.sleep(0.1)
    myThread.write_log("Wait...")
    if not workQueue.empty():
        reading = workQueue.get()
        myThread.write_log("Reading from queue: " + reading)
