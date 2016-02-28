# -*- coding: utf-8 -*-

import pygame
from baseState import BaseState

class SerialLogNotifier(BaseState):

    font = None
    surface = None
    notifications = []
    TOP = 0
    LIMIT = 10
    area = None
    
    def __init__(self, surface, area):
        self.surface = surface
        self.area = area
        self.font = None
        
        for i in range(self.LIMIT):
            self.notifications.append("")

    def start(self):
        pass
        
    def render(self):
        blue = (0, 0, 70)
        
        x1 = self.getX(self.area[0])
        y1 = self.getY(self.area[1])
        x2 = self.getX(self.area[2])
        y2 = self.getY(self.area[3])
        #pygame.draw.rect(self.surface, blue, (x1, y1, x2, y2))
        
        pointlist = [ (x1,y1), (x2,y1), (x2,y2), (x1,y2)]
        pygame.draw.lines(self.surface, blue, 1, pointlist, 2)
        
        myFont = pygame.font.Font(None, 20)
        i=0
        for notification in self.notifications:
            text = myFont.render(notification, 1, (70, 70, 70))
            
            x1 = self.getX(self.area[0]+1)
            y1 = self.getY(self.area[1] + 2 * i + 1)
            self.surface.blit(text, (x1, y1))
            i=i+1
    
    def clear(self):
        black = (0, 0, 0)
        
        x1 = self.getX(self.area[0])
        y1 = self.getY(self.area[1])
        x2 = self.getX(self.area[2])
        y2 = self.getY(self.area[3])
        pygame.draw.rect(self.surface, black, (x1, y1, x2, y2))
        
    def loop(self, setState, isPressed):
        pass
    
    def push(self, line):
        if (self.TOP >= self.LIMIT):
            self.rotate(1)
            self.TOP = self.LIMIT-1
            self.notifications[self.TOP] = line
            self.TOP = self.TOP + 1
        else:
            self.notifications[self.TOP] = line
            self.TOP = self.TOP + 1
            
    def rotate(self, num):        
        for index in range(0, self.LIMIT-1):
            self.notifications[index] = self.notifications[index+1]
        self.notifications[self.LIMIT-1] = ""
        


