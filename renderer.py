import numpy as np

from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *

class Renderer():
    def __init__(self, width=1920, height=1080, bg_color=(0.,1.,0.), fps=30.):
        self.width = width
        self.height = height
        self.clear_col = bg_color
        self.fps = fps
        self.visualizers = []

        self.init_camera()
        self.glut_init()

    

    def init_camera(self):
        """
        With this the coordinate space of the elements is [0,1] for x and y, and [-1,1] for z
        """
        # select clearing color
        glClearColor (0.0, 1.0, 0.0, 0.0)

        # initialize viewing values
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)

    def bind_visualizers(self, visualizers):
        self.visualizers = visualizers

    def glut_init(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowSize(1920, 1080)
        self.window = glutCreateWindow("test")

    def display_callback(self):
        # clear all pixels
        glClear (GL_COLOR_BUFFER_BIT)

        for vis in self.visualizers:
            vis.draw()

        glutSwapBuffers(self.window)

    def render(self):
        # self.init_glut()
        glutDisplayFunc(self.display_callback)
        glutMainLoop()
        
    