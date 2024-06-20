from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *
import numpy as np

from visualizer import Visualizer
from renderer import Renderer




if __name__ == "__main__":
    visualizers = []

    renderer = Renderer()
        

    x = np.linspace(0,400 * np.pi, 20000)
    audio = np.sin(x)
    audio += np.sin(2*x)
    audio += np.sin(8*x)

    vis = Visualizer(audio, 48000)
    visualizers.append(vis)
    vis.fill_bins()

    renderer.bind_visualizers(visualizers)

    renderer.render()