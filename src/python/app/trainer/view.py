# -*- coding: utf-8 -*-

import pygame
import numpy as np

class Ball:
	radius = 15
	position = (250,200)
	color = (255,255,255) 

	def __init__(self):
		pass

class SurfaceView (object):

	surface = None
	
	sensor_coords = np.array ([[5.6, 6.2],
		[30.5, 6.2],
		[55.6, 5.48],
		[17.2, 21.4],
		[46.8, 22.2],
		[6, 38.6],
		[30.5, 38.6],
		[55.6, 38.6]])

	def __init__(self, surface):
		self.surface = surface

	def clearView(self):
		self.surface.fill((0, 0, 0))
	
	# Convert inches to pixel X
	def get_x_conversion(self):
		windowWidth = self.surface.get_size()[0]
		conversion = (windowWidth/2)/54
		return conversion
	
	# Convert inches to pixel Y
	def get_y_conversion(self):
		windowHeight = self.surface.get_size()[1]
		conversion = (windowHeight)/60
		return conversion
	
	# Get X pixels related to percent
	def getX(self, _x):
		#max_x = self.surface.get_size()[0];
		max_x = self.surface.get_size()[0];
		return (max_x/100)*_x
	
	# Get Y pixels related to percent
	def getY(self, _y):
		#max_y = self.surface.get_size()[1];
		max_y = self.surface.get_size()[1];
		return (max_y/100)*_y
	
	def getPercentCoords(self, coords):
		return (self.getX(coords[0]), self.getY(coords[1]))
		
	def drawText(self, text, coords):
		self.surface.blit(text, coords)
		
	def drawBall(self, ball, fill=0):
		pygame.draw.circle(self.surface, ball.color, ball.position, ball.radius, fill)
	
	def drawReferencePoint(self, x, y):
		ball = Ball()
		ball.color = (255, 0, 0)
		ball.radius = 10
		
		translated_x = int(x*self.get_x_conversion())
		translated_y = int(y*self.get_y_conversion())
		ball.position = (translated_x, translated_y)
		
		self.drawBall(ball, 0)
	
	def drawHit(self, x, y, side):
		ball = Ball()
		ball.color = (0, 255, 255)
		ball.radius = 30
		
		offset = 0
		
		if side == 'r':
			offset = 65*self.get_x_conversion()
			#pass
			
		translated_x = int(x*self.get_x_conversion() + offset)
		translated_y = int(y*self.get_y_conversion())
		ball.position = (translated_x, translated_y)
		
		self.drawBall(ball, 0)
		ball.color = (0, 0, 0)
		ball.radius = 25
		self.drawBall(ball, 0)

	def drawConnectedPointsLines(self, hitsList):
		
		new_points = []
		
		i=0
		for structHit in hitsList:
			(x,y) = structHit['coords']
			side = structHit['side']
			i=i+1
			#self.drawHit(x, y, side)
			self.drawHitWithText(x, y, side, str(i))
			
			offset = 0		
			if side == 'r':
				offset = 65*self.get_x_conversion()
				
			translated_x = int(x*self.get_x_conversion() + offset)
			translated_y = int(y*self.get_y_conversion())

			new_pos = (translated_x, translated_y)
			new_points.append(new_pos)
			
		#lines(Surface, color, closed, pointlist, width=1) -> Rect
		
		pygame.draw.lines(self.surface, (150,255,255), 0, new_points,2)
		pygame.display.flip()
	
	def drawLines(self, color, closed, pointlist, width):
		pygame.draw.lines(self.surface, color, closed, pointlist, width)
	
	def drawRect(self, color, pointlist):
		pygame.draw.rect(self.surface, color, pointlist)
	
	def drawHitWithText(self, x, y, side, text):
		self.drawHit(x, y, side)
		
		font = pygame.font.Font(None, 66)
		
		if text <> "":
			text = font.render(text, 1, (255,255,255))
			
			offset = 0		
			if side == 'r':
				offset = 65*self.get_x_conversion()

			xx = int((x * self.get_x_conversion()) + offset)-15
			yy = int(y * self.get_y_conversion())-15
			
			#coords = self.getPercentCoords((x,y))
			coords = (xx,yy)
			self.drawText(text, coords)
	
	def drawSensor(self, x, y):
		ball = Ball()
		ball.color = (0, 0, 255)
		ball.radius = 10
		
		translated_x = int(x*self.get_x_conversion())
		translated_y = int(y*self.get_y_conversion())
		ball.position = (translated_x, translated_y)
		
		self.drawBall(ball, 0)

	def displayReferencePoints(self):
		
		for i in [6,18,30,42,54]:
			for j in [6,18,30,42]:
				self.drawReferencePoint(j, i)

		for i in [6,18,30,42,54]:
			for j in [6,18,30,42]:
				self.drawReferencePoint(j+65, i)

	def displaySensors(self):
		for sensor_coord in self.sensor_coords:
			x = sensor_coord[0]
			y = sensor_coord[1]
			self.drawSensor(y, x)

	def display_box(self, message):
		screen = self.surface
		"Print a message in a box in the middle of the screen"
		fontobject = pygame.font.Font(None,18)
		pygame.draw.rect(screen, (0,0,0),
			((screen.get_width() / 2) - 100,
			(screen.get_height() / 2) - 10,
			200,20), 0)
		pygame.draw.rect(screen, (255,255,255),
			((screen.get_width() / 2) - 102,
			(screen.get_height() / 2) - 12,
			204,24), 1)
		if len(message) != 0:
			screen.blit(fontobject.render(message, 1, (255,255,255)),
					((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
		pygame.display.flip()
		
	def displayTable(self):
	
		tableLineWidth = 1
		
		windowWidth = self.surface.get_size()[0]
		windowHeight = self.surface.get_size()[1]
		
		pygame.draw.line(self.surface, (255,255,255), (tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
		pygame.draw.line(self.surface, (255,255,255), (tableLineWidth/2,windowHeight-1-tableLineWidth/2), (windowWidth-tableLineWidth/2,windowHeight-1-tableLineWidth/2), tableLineWidth) 
		pygame.draw.line(self.surface, (255,255,255), (windowWidth-1-tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-1-tableLineWidth/2,tableLineWidth/2), tableLineWidth) 
		pygame.draw.line(self.surface, (255,255,255), (windowWidth-tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,tableLineWidth/2), tableLineWidth)
		pygame.draw.line(self.surface, (255,255,255), (tableLineWidth/2,windowHeight/2), (windowWidth,windowHeight/2), tableLineWidth)
		pygame.draw.line(self.surface, (255,255,255), (windowWidth/2,tableLineWidth/2), (windowWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 

	def buildScene(self):

		self.displayTable()
		self.displayReferencePoints()
		self.displaySensors()

class LogonView (SurfaceView):
	def __init__(self, surface):
		super(self.__class__, self).__init__(surface)

class MenuView (SurfaceView):
	
	def __init__(self, surface):
		super(self.__class__, self).__init__(surface)
		
	def renderSelectedOption(self, _label, coords):
		color = (250, 250, 250)
		self.renderOption(_label, coords, color)

	def renderUnSelectedOption(self, _label, coords):
		color = (100, 100, 100)
		self.renderOption(_label, coords, color)
	
	def renderOption(self, _label, coords, _color):
		font = pygame.font.Font(None, 66)
		text = font.render(_label, 1, _color)
		coords = self.getPercentCoords(coords)
		self.drawText(text, coords)

class ShortServiceView (SurfaceView):		

	def __init__(self, surface):
		super(ShortServiceView, self).__init__(surface)

	def renderSummary(self, summary):
		blue = (0, 0, 70)
		black = (0, 0, 0)
		
		x1 = self.getX(20)
		y1 = self.getY(20)
		x2 = self.getX(70)
		y2 = self.getY(60)
		
		pointlist = [ (x1,y1), (x2,y1), (x2,y2), (x1,y2)]
		self.drawLines(blue, 1, pointlist, 2)
		#pygame.draw.lines(self.surface, blue, 1, pointlist, 2)
		self.drawRect(black, (x1+1, y1+1, x2-10, y2-10))		
		#pygame.draw.rect(self.surface, black, (x1+1, y1+1, x2-10, y2-10))
		
		myFont = pygame.font.Font(None, 20)
		text = myFont.render(summary[0], 1, (70, 70, 70))
		self.drawText(text, (x1+20, y1+50))

	
class MultiBallView (SurfaceView):		

	def __init__(self, surface):
		super(MultiBallView, self).__init__(surface)

	def drawMessage(self):
		font = pygame.font.Font(None, 36)
		text = font.render("Multi Ball", 1, (250, 250, 250))
		self.drawText(text, self.getPercentCoords((10,10)))

class SandboxView (SurfaceView):		

	def __init__(self, surface):
		super(SandboxView, self).__init__(surface)

class RallyView (SurfaceView):		

	def __init__(self, surface):
		super(RallyView, self).__init__(surface)

	def drawMessage(self):
		font = pygame.font.Font(None, 36)
		text = font.render("Whole point sequence", 1, (250, 250, 250))
		self.drawText(text, self.getPercentCoords((10,10)))
		
class CalibrationView (SurfaceView):

	def __init__(self, surface):
		super(CalibrationView, self).__init__(surface)

