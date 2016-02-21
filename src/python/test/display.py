import pygame
import random

pygame.init()


tableLineWidth = 4

current_w = pygame.display.Info().current_w
current_h = pygame.display.Info().current_h
heightp=60
widthp = 96
ratioH = current_h/heightp
ratioW = current_w/widthp

#720/96 = 7.5
#480/60 = 8
window = pygame.display.set_mode((current_w,current_h),pygame.FULLSCREEN)

class Ball:
    def __init__(self,radius=8,position=(720/2,480/2),color=(255,255,255)):
        self.radius=radius
        self.position=position
        self.color=color
    

    def setPosition(self,position):
        self.postion = position



def displayTable(windowWidth, windowHeight, tableLineWidth):
    
    pygame.draw.line(window,(255,255,255), (tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
    #pygame.draw.rect(window(255,255,255), (0,0,1096,608))
    pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-tableLineWidth/2,windowHeight-tableLineWidth/2), tableLineWidth) 
    #pygame.draw.line(window,(255,255,255), (2,606), (1094,606), tableLineWidth)    
    pygame.draw.line(window,(255,255,255), (windowWidth-tableLineWidth/2,windowHeight-tableLineWidth/2), (windowWidth-tableLineWidth/2,tableLineWidth/2), tableLineWidth) 
    pygame.draw.line(window,(255,255,255), (windowWidth-tableLineWidth/2,tableLineWidth/2), (tableLineWidth/2,tableLineWidth/2), tableLineWidth)
    pygame.draw.line(window,(255,255,255), (tableLineWidth/2,windowHeight/2), (windowWidth,windowHeight/2), tableLineWidth)
    pygame.draw.line(window,(255,255,255), (windowWidth/2,tableLineWidth/2), (windowWidth/2,windowHeight-tableLineWidth/2), tableLineWidth)
    pygame.display.update()
    
    return
def displayBall(ball):
    pygame.draw.circle(window, ball.color, ball.position, ball.radius, ball.radius)

ball = Ball()
exit = False
while not exit:
    displayTable(current_w, current_h, tableLineWidth)
    displayBall(ball)
    ball.setPosition( (random.randint(0,current_w),random.randint(0,current_w)) )
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
              exit = True