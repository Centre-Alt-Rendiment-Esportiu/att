# -*- coding: utf-8 -*-

from pyprocessing import *
from random import random

cubies = 20
c = [0]*cubies
quadBG = [[None]*6]*cubies

# Controls cubie's movement
x = [0.0]*cubies
y = [0.0]*cubies
z = [0.0]*cubies
xSpeed = [0.0]*cubies
ySpeed = [0.0]*cubies
zSpeed = [0.0]*cubies

# Controls cubie's rotation
xRot = [0.0]*cubies
yRot = [0.0]*cubies
zRot = [0.0]*cubies

stage = None

# Size of external cube
bounds = 300.0

def setup():
  size(640, 360);
  
  for i in range(0,cubies):
    # Each cube face has a random color component
    quadBG[i][0] = color(0)
    quadBG[i][1] = color(51)
    quadBG[i][2] = color(102)
    quadBG[i][3] = color(153)
    quadBG[i][4] = color(204)
    quadBG[i][5] = color(255)

    # Cubies are randomly sized
    cubieSize = random()*10+5
    c[i] =  Cube(cubieSize, cubieSize, cubieSize)

    # Initialize cubie's position, speed and rotation
    x[i] = 0.0
    y[i] = 0.0
    z[i] = 0.0

    xSpeed[i] = random()*4-2
    ySpeed[i] = random()*4-2
    zSpeed[i] = random()*4-2

    xRot[i] = random()*60+40
    yRot[i] = random()*60+40
    zRot[i] = random()*60+40
  

def draw():
  background(50)
  lights()
  
  # Center in display window
  translate(1024/4, 768/4, -130)
  
  # Outer transparent cube
  noFill()
  
  # Rotate everything, including external large cube
  rotateX(frame.count * 0.001)
  rotateY(frame.count * 0.002)
  rotateZ(frame.count * 0.001)
  stroke(255)
  
  # Draw external large cube
  stage =  Cube(bounds, bounds, bounds);
  stage.create()

  # Move and rotate cubies
  for i in range(0,cubies):
    pushMatrix()
    translate(x[i], y[i], z[i])
    rotateX(frame.count*PI/xRot[i])
    rotateY(frame.count*PI/yRot[i])
    rotateX(frame.count*PI/zRot[i])
    noStroke()
    c[i].create(quadBG[i])
    x[i] += xSpeed[i]
    y[i] += ySpeed[i]
    z[i] += zSpeed[i]
    popMatrix()

    # Draw lines connecting cubbies
    stroke(0)
    if i < cubies-1:
      line(x[i], y[i], z[i], x[i+1], y[i+1], z[i+1])

    # Check wall collisions
    if x[i] > bounds/2 or x[i] < -bounds/2:
      xSpeed[i]*=-1
    
    if y[i] > bounds/2 or y[i] < -bounds/2:
      ySpeed[i]*=-1
    
    if z[i] > bounds/2 or z[i] < -bounds/2:
      zSpeed[i]*=-1
    


# Custom Cube Class

class Cube():
  def __init__(self,w,h,d):
    self.vertices = [0]*24
    self.w = w;
    self.h = h;
    self.d = d;

    # cube composed of 6 quads
    #front
    self.vertices[0] =  PVector(-w/2,-h/2,d/2)
    self.vertices[1] =  PVector(w/2,-h/2,d/2)
    self.vertices[2] =  PVector(w/2,h/2,d/2)
    self.vertices[3] =  PVector(-w/2,h/2,d/2)
    #left
    self.vertices[4] =  PVector(-w/2,-h/2,d/2)
    self.vertices[5] =  PVector(-w/2,-h/2,-d/2)
    self.vertices[6] =  PVector(-w/2,h/2,-d/2)
    self.vertices[7] =  PVector(-w/2,h/2,d/2)
    #right
    self.vertices[8] =  PVector(w/2,-h/2,d/2)
    self.vertices[9] =  PVector(w/2,-h/2,-d/2)
    self.vertices[10] =  PVector(w/2,h/2,-d/2)
    self.vertices[11] =  PVector(w/2,h/2,d/2)
    #back
    self.vertices[12] =  PVector(-w/2,-h/2,-d/2)
    self.vertices[13] =  PVector(w/2,-h/2,-d/2)
    self.vertices[14] =  PVector(w/2,h/2,-d/2)
    self.vertices[15] =  PVector(-w/2,h/2,-d/2)
    #top
    self.vertices[16] =  PVector(-w/2,-h/2,d/2)
    self.vertices[17] =  PVector(-w/2,-h/2,-d/2)
    self.vertices[18] =  PVector(w/2,-h/2,-d/2)
    self.vertices[19] =  PVector(w/2,-h/2,d/2)
    #bottom
    self.vertices[20] =  PVector(-w/2,h/2,d/2)
    self.vertices[21] =  PVector(-w/2,h/2,-d/2)
    self.vertices[22] =  PVector(w/2,h/2,-d/2)
    self.vertices[23] =  PVector(w/2,h/2,d/2)
  
  def create(self,quadBG=None):
    # Draw cube
    for i in range(0,6):
      if quadBG:
          fill(quadBG[i])
      beginShape(QUADS)
      for j in range(0,4):
        vertex(self.vertices[j+4*i].x, self.vertices[j+4*i].y, self.vertices[j+4*i].z)
      endShape()

run()