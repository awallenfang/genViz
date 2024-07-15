from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *
import numpy as np
import librosa

from visualizer import Visualizer
from renderer import Renderer

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720


if __name__ == "__main__":
    visualizers = []

    renderer = Renderer(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        

    x = np.linspace(0,400 * np.pi, 2000000)
    # audio = 0.2 * np.sin(x) * (1/(x+0.000000000001))
    # audio += np.sin(2*x)
    # audio += 2*np.sin(8*x)
    # audio += 5*np.sin(100*x)

    audio = np.sin(np.sin(x)*np.pi)

    # Normalize audio
    audio = audio / np.max(audio)

    audio, sr = librosa.load("input.mp3", sr=None)

    vis = Visualizer(audio, 48000, window_height=WINDOW_HEIGHT, window_width=WINDOW_WIDTH, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

    visualizers.append(vis)

    renderer.bind_visualizers(visualizers)

    renderer.render()

