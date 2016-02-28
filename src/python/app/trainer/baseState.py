# -*- coding: utf-8 -*-

import abc

import pygame

class BaseState:
	__metaclass__ = abc.ABCMeta
	
	surface = None
	
	@abc.abstractmethod
	def loop(self, setState, isPressed):
		pass
	
	def clear(self):
		self.surface.fill((0, 0, 0))
		
		"""
		screen = pygame.display.get_surface()

		# Fill background
		background = pygame.Surface(screen.get_size())
		background = background.convert()
		background.fill((250, 250, 250))
		"""
		
	def getX(self, _x):
		max_x = self.surface.get_size()[0];
		return (max_x/100)*_x
	
	def getY(self, _y):
		max_y = self.surface.get_size()[1];
		return (max_y/100)*_y
