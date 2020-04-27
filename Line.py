from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math

class Line:
    def __init__(self, x1, x2, numPoints):
        self.x1 = x1
        self.x2 = x2
        self.numPoints = numPoints
        self.verticies = self.createVerticies()
        self.lines = self.createLines

    def createVerticies(self):
        length = x2 - x1
        spacing = length / (numPoints-1)
        verticies = []
        for i in range(len(numPoints)):
            verticies.append([x1*length*i, 0, 0, 0])
        return verticies
    
    def createLines(self):
        for i in range(len(self.verticies)):
            


    def drawLine(self):
        glBegin(GL_QUADS)
        x = 0
        

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.verts[vertex])
        glEnd()