from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *
import numpy as np

from visualizer import Visualizer
from renderer import Renderer




if __name__ == "__main__":
    visualizers = []

    renderer = Renderer()
        

    audio = np.zeros(48000)
    vis = Visualizer(audio, 48000)
    visualizers.append(vis)

    renderer.bind_visualizers(visualizers)

    renderer.render()