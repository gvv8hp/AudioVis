from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math

class Sheet:
    def __init__(self):
        self.verts = [
            [0, .2, 0],
            [1, 1, 0],
            [1, 1, 1],
            [0, 0, 1],
        ]
        self.edges = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
        ]
        self.surfs = [
            [0, 1, 2, 3],
        ]
        self.color = [1,0,1]
    def draw(self):
        glBegin(GL_QUADS)
        x = 0
        for surface in self.surfs:
            glColor3fv(self.color)
            x+=1
            for vertex in surface:
                glVertex3fv(self.verts[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.verts[vertex])
        glEnd()
