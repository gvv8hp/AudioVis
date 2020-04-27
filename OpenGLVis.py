import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math

# Input imports
import pyaudio
import numpy as np
import time

import SpectrumPlotter
import VisStream
import Cube
import Sheet

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class Camera:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def setPosition(self, x, y, z):
        dx = x-self.x
        dy = y-self.y
        dz = z-self.z
        glTranslatef(-dx, -dy, -dz)
        self.x+=dx
        self.y+=dy
        self.z+=dz
    def move(self, x, y, z):
        self.x+=x
        self.y+=y
        self.z+=z
        glTranslate(-x, -y, -z)
      

def main():
    pygame.init()
    windowScale = 1
    display = (int(1920*windowScale), int(1080*windowScale))
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(25, (display[0]/display[1]), 0.0, 50.0)
    # glTranslatef(0, 0.0, -5)
    cam = Camera()
    cam.setPosition(0, 0, 10)
    glRotatef(0, 0, 0, 0)

    myStream = VisStream.VisStream(rate=48000*2, chunkSize=2**11)
    cube = Cube.Cube()
    # sheet = Sheet.Sheet()

    while True:
        glRotatef(myStream.getDynamicRotation(.0001,50, 150), 3, 1, 1)
        # glRotatef(1, 1, 0, 0)
        # cam.setPosition(0, 0, -1*myStream.getDynamicRotation(5, 15, 150))
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        
        cube.setSideColors(myStream.getSideColors())
        
        cube.draw()
        # sheet.draw()
        cs = myStream.getDynamicRotation(1,1.5,100)
        cube.scaleCorner(scalars=[cs,cs,cs,cs,cs,cs,cs,cs])
        
        pygame.display.flip()
        pygame.time.wait(10)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                myStream.endStream()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    myStream.plotStream()
                if event.key == pygame.K_r:
                    myStream.reset()
                if event.key == pygame.K_p:
                    gluPerspective(myStream.getDynamicRotation(45,90,150), (display[0]/display[1]), 0.0, 50.0)
                if event.key == pygame.K_DOWN:
                    cam.move(0, -1, 0)
                if event.key == pygame.K_UP:
                    cam.move(0, 1, 0)
                if event.key == pygame.K_LEFT:
                    cam.move(-1, 0, 0)
                if event.key == pygame.K_RIGHT:
                    cam.move(1, 0, 0)



main()