import serial
from numpy import *
import pygame
# import sys, os

from menu_state 		import MenuState
from projection_state 	import ProjectionCalibrationState
from position_state 	import SensorPositionCalibrationState
from sensor_calibration_state import SensorCalibrationState
from tracking_state 	import TrackingState

# from tkinter import *
# root = Tk()

# root.iconbitmap('favicon/py.ico')
# root.mainloop()

BAUD = 115200
PORT = 2    # PORT = 5 means COM6. FOR WINDOWS
#PORT = '/dev/tty.usbserial-A9005d9p' # FOR MAC
SERIAL_TIMEOUT = .1 # in seconds
arduino_serial = None

positions = array([
	[6, 6],
	[6, 18],
	[6, 30],
	[6, 42],
	[18, 6],
	[18, 18],
	[18, 30],
	[18, 42],
	[30, 6],
	[30, 18],
	[30, 30],
	[30, 42],
	[42, 6],
	[42, 18],
	[42, 30],
	[42, 42],
	[54, 6],
	[54, 18],
	[54, 30],
	[54, 42]])

TABLE_WIDTH = 60
TABLE_HEIGHT = 54
SCREEN_MULITPLIER = 14.6

pressed = None
isButtonUp = True

menu_state 		= None
projection_state = None
position_state 	= None
sensor_state 	= None
tracking_state 	= None
curState = None

screen = None

def open_serial(port, baud):
	""" Initializes the Arduino serial connection """
	arduino_serial = serial.Serial(port, baudrate = baud, timeout = SERIAL_TIMEOUT)
	return arduino_serial

def setState(state):
	global curState, menu_state, projection_state, position_state, sensor_state, tracking_state

	if state == 0:
		curState = menu_state
	elif state == 1:
		curState = projection_state
	elif state == 2:
		curState = position_state
	elif state == 3:
		curState = sensor_state
	elif state == 4:
		curState = tracking_state

def isPressed(key):
	global pressed, isButtonUp
	if pressed[key] and isButtonUp:
		isButtonUp = False
		return True
	return False

def main():
	global pressed, isButtonUp, curState, menu_state, projection_state, position_state, sensor_state, tracking_state

	pygame.init()
	pygame.display.set_caption("Augmented Table Tennis")
	
	# , get_image_file("favicon/ms-icon-70x70.png"))
	screen = pygame.display.set_mode((int(round(2 * 54 * SCREEN_MULITPLIER)), int(round(60 * SCREEN_MULITPLIER))))
	icon = pygame.image.load("asset/favicon.png").convert_alpha()
	pygame.display.set_icon(icon)
	clock = pygame.time.Clock()

	arduino_serial = open_serial(PORT, BAUD)

	menu_state 		= MenuState(pygame)
	projection_state = ProjectionCalibrationState(pygame)
	position_state 	= SensorPositionCalibrationState(pygame)
	sensor_state 	= SensorCalibrationState(arduino_serial, positions, pygame)
	tracking_state 	= TrackingState(arduino_serial, positions, pygame)
	setState(0)

	done = False

	while not done:
		screen.fill((250, 250, 250))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		pressed = pygame.key.get_pressed()
		if not(pressed[pygame.K_UP]) and not(pressed[pygame.K_DOWN]) and not(pressed[pygame.K_RETURN]) and not(pressed[pygame.K_ESCAPE]):
			isButtonUp = True

		curState.update(setState, isPressed, pygame)

		pygame.display.flip()
		clock.tick(60)

if __name__ == '__main__': main()