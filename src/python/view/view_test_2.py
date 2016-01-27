# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 17:40:32 2016

@author: asanso
"""

# An example implementation of the algorithm described at
# http://www.niksula.cs.hut.fi/~hkankaan/Homepages/metaballs.html
#
# The code contains some references to the document above, in form
# ### Formula (x)
# to make clear where each of the formulas is implemented (and what
# it looks like in Python)
#
# Since Python doesn't have an in-built vector type, I used complex
# numbers for coordinates (x is the real part, y is the imaginary part)
#
# Made by Hannu Kankaanpää. Use for whatever you wish.

import math

import pygame
from pygame.locals import *


def main():
    # This is where the execution starts.
    # First initialize the screen.
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    # Then create a couple of balls
    balls = [Ball(350 + 100j, size=3),
             Ball(20  + 200j, size=2),
             Ball(280 + 140j, size=4),
             Ball(400 + 440j, size=3)]

    # And a metaball system (see below for class definition)
    mbs = MetaballSystem(balls, goo=2.0, threshold=0.0004, screen=screen)

    while True:
        # clear screen with black
        screen.fill((0, 0, 0))

        # move ball number 0 according to mouse position
        if pygame.mouse.get_focused():
            balls[0].pos = complex(*pygame.mouse.get_pos())

        # Draw the balls.
        # Try different methods: euler, rungeKutta2 and rungeKutta4
        drawBalls(differentialMethod=rungeKutta2, metaballSystem=mbs,
                  step=20, screen=screen)
        pygame.display.flip()

        # exit when esc is pressed
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return


def drawBalls(differentialMethod, metaballSystem, step, screen):
    mbs = metaballSystem
    balls = mbs.balls

    # First, track the border for all balls and store
    # it to pos0 and edgePos. The latter will move along the border,
    # pos0 stays at the initial coordinates.
    for ball in balls:
        ball.pos0 = mbs.trackTheBorder(ball.pos + 1j)
        ball.edgePos = ball.pos0
        ball.tracking = True

    loopIndex = 0
    while loopIndex < 200:
        loopIndex += 1
        for ball in balls:
            if not ball.tracking:
                continue

            # store the old coordinates
            old_pos = ball.edgePos

            # walk along the tangent, using chosen differential method
            ball.edgePos = differentialMethod(ball.edgePos, step, mbs.calcTangent)

            # correction step towards the border
            ball.edgePos, tmp = mbs.stepOnceTowardsBorder(ball.edgePos)

            pygame.draw.line(screen, (255, 255, 255),
                             (old_pos.real, old_pos.imag),
                             (ball.edgePos.real, ball.edgePos.imag))

            # check if we've gone a full circle or hit some other
            # edge tracker
            for ob in balls:
                if (ob is not ball or loopIndex > 3) and \
                   abs(ob.pos0 - ball.edgePos) < step:
                    ball.tracking = False

        tracking = 0
        for ball in balls:
            if ball.tracking:
                tracking += 1
        if tracking == 0:
            break
											
class Ball:
    """Single metaball."""
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size


class MetaballSystem:
    """A class that manages the metaballs and can calculate
       several useful values from the system.
    """

    def __init__(self, balls, goo, threshold, screen):
        self.balls = balls
        self.goo = goo
        self.threshold = threshold
        self.minSize = min([ball.size for ball in balls])
        self.screen = screen

    def calcForce(self, pos):
        """Return the metaball field's force at point 'pos'."""
        force = 0
        for ball in self.balls:
            ### Formula (1)
            div = abs(ball.pos - pos)**self.goo
            if div != 0: # to prevent division by zero
                force += ball.size / div
            else:
                force += 10000 #"big number"
        return force

    def calcNormal(self, pos):
        """Return a normalized (magnitude = 1) normal at point 'pos'."""
        np = 0j
        for ball in self.balls:
            ### Formula (3)
            div = abs(ball.pos - pos)**(2 + self.goo)
            np += -self.goo * ball.size * (ball.pos - pos) / div
        return np / abs(np)

    def calcTangent(self, pos):
        """Return a normalized (magnitude = 1) tangent at point 'pos'."""
        np = self.calcNormal(pos)
        ### Formula (7)
        return complex(-np.imag, np.real)

    def stepOnceTowardsBorder(self, pos):
        """Step once towards the border of the metaball field, return
           new coordinates and force at old coordinates.
        """
        force = self.calcForce(pos)
        np = self.calcNormal(pos)
        ### Formula (5)
        stepsize = (self.minSize / self.threshold)**(1 / self.goo) - \
                   (self.minSize / force)**(1 / self.goo) + 0.01
        return (pos + np * stepsize, force)

    def trackTheBorder(self, pos):
        """Track the border of the metaball field and return new
           coordinates.
        """
        force = 9999999
        # loop until force is weaker than the desired threshold
        while force > self.threshold:
            pos, force = self.stepOnceTowardsBorder(pos)
            # show a little debug output (i.e. plot yellow pixels)
            sz = self.screen.get_size()
            if 0 <= pos.real < sz[0] and 0 <= pos.imag < sz[1]:
                self.screen.set_at((int(pos.real), int(pos.imag)), (255, 255, 0))
        return pos


def euler(pos, h, func):
    """Euler's method.
       The most simple way to solve differential systems numerically.
    """
    return pos + h * func(pos)


def rungeKutta2(pos, h, func):
    """Runge-Kutta 2 (=mid-point).
       This is only a little more complex than the Euler's method,
       but significantly better.
    """
    return pos + h * func(pos + func(pos) * h / 2)


def rungeKutta4(pos, h, func):
    """Runge-Kutta 4.
       RK4 is quite a bit more complex than RK2. RK2 with a
       small stepsize is often more useful than this.
    """
    t1 = func(pos)
    t2 = func(pos + t1 * h / 2)
    t3 = func(pos + t2 * h / 2)
    t4 = func(pos + t3 * h)
    return pos + (h / 6) * (t1 + 2*t2 + 2*t3 + t4)


if __name__ == '__main__': main()