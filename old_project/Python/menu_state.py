import serial
import re
from math import fabs
import random as python_random

import pygame

class MenuState:
	font = None

	curOption = 0
	menuOptions = [
		'Projection Surface',
		'Sensor Position',
		'Sensor Matrix',
		'Track Ball']

	def __init__(self, pygame):
		screen = pygame.display.get_surface()

		# Fill background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))

		# Display some text
		self.font = pygame.font.Font(None, 36)

	def update(self, setState, isPressed, pygame):
		screen = pygame.display.get_surface()

		if isPressed(pygame.K_DOWN):
			self.curOption = (self.curOption + 1) % len(self.menuOptions)

		if isPressed(pygame.K_UP):
			self.curOption = (self.curOption + len(self.menuOptions) - 1) % len(self.menuOptions)

		if isPressed(pygame.K_RETURN):
			setState(self.curOption + 1)

		for i in range(len(self.menuOptions)):
			if not(i == self.curOption):
				text = self.font.render(self.menuOptions[i], 1, (80, 80, 80))
			else:
				text = self.font.render(self.menuOptions[i], 1, (0, 0, 0))
			screen.blit(text, (5, 10 + 25 * i))
