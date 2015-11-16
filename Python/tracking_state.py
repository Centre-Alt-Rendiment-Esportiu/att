import serial
import re
from math import fabs
import random as python_random

import pygame

class TrackingState:
	font = None

	def __init__(self, arduino_serial, positions, pygame):
		screen = pygame.display.get_surface()

		# Fill background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))

		# Display some text
		self.font = pygame.font.Font(None, 36)

	def update(self, setState, isPressed, pygame):
		screen = pygame.display.get_surface()

		if isPressed(pygame.K_ESCAPE):
			setState(0)

		text = self.font.render("Tracking State...", 1, (0, 0, 0))
		screen.blit(text, (5, 10))
