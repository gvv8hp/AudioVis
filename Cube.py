from OpenGL.GL import *
from OpenGL.GLU import *

import random
import math


class Cube:
    def __init__(self):
        self.verticies = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1),
        )

        self.edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7),
        )

        self.surfaces = (
            (0, 1, 2, 3),
            (3, 2, 7, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (4, 0, 3, 6),
        )

        self.sideColors = (
            (1,0,0),
            (0,1,0),
            (0,0,1),
            (0,0,0),
            (1,1,1),
            (0,1,1),
            (1,0,0),
            (0,1,0),
            (0,0,1),
            (0,0,0),
            (1,1,1),
            (0,1,1),
        )

    def draw(self):
        glBegin(GL_QUADS)
        x = 0
        for surface in self.surfaces:
            glColor3fv(self.sideColors[x])
            x+=1
            for vertex in surface:
                glVertex3fv(self.verticies[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.verticies[vertex])
        glEnd()

    def setSideColors(self, sideColors):
        self.sideColors = sideColors

    def scaleCorner(self, scalars=[0, 0, 0, 0, 0, 0, 0, 0]):
        verts = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1),
        )
        vertList = []
        for vert in verts:
            vertList.append(list(vert))
        for i in range(len(vertList)):
            for j in range(len(vertList[i])):
                vertList[i][j] = vertList[i][j]*scalars[i]
        tupleList = []
        for vert in vertList:
            tupleList.append(tuple(vert))
        cornerTuples = tuple(tupleList)
        self.verticies = cornerTuples

        
        