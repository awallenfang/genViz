import numpy as np
import cv2

from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *

class Renderer():
    def __init__(self, width=500, height=500, bg_color=(0.,1.,0.), fps=30.):
        self.width = width
        self.height = height
        self.clear_col = bg_color
        self.fps = fps
        self.visualizers = []

        self.init_camera()
        self.glut_init()

        self.is_done = False

        fourcc = cv2.VideoWriter.fourcc('X','V','I','D')
        print(self.width, self.height)
        self.video_writer: cv2.VideoWriter = cv2.VideoWriter('output.avi', fourcc, self.fps, (self.height, self.width))


    

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
        glutInitWindowSize(self.width, self.height)
        self.window = glutCreateWindow("test")

    def display_callback(self):
        # clear all pixels
        glClear (GL_COLOR_BUFFER_BIT)

        for vis in self.visualizers:
            self.is_done = vis.tick()
            vis.draw()

        if not self.is_done:
            self.read_frame()
        else:
            self.video_writer.release()

        glutSwapBuffers(self.window)

    def render(self):
        glutDisplayFunc(self.display_callback)
        glutIdleFunc(self.display_callback)
        glutMainLoop()
        
    def read_frame(self):        
        out = glReadPixels(0,0,self.width, self.height, format=GL_RGB, type=GL_UNSIGNED_SHORT)
                
        self.video_writer.write(out)
