from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *

import numpy as np
import matplotlib.pyplot as plt
from shader import Shader

class Visualizer():
    def __init__(self, audio_stream: np.array, sample_rate: float, x_origin = 0., y_origin = 0., width = 1920., height= 1080., spectrum_bins = 128, depth=0., shader = None, padding=0.002):
        self.audio_stream = audio_stream
        self.sample_rate = sample_rate
        self.fps = 30.
        self.spectrum_bins = spectrum_bins
        self.z = depth
        self.padding = padding

        if shader == None:
            self.shader = Shader("./shaders/default.frag")
        else:
            self.shader = shader

        self.samples_per_frame = self.sample_rate / self.fps

        self.position = 0.

        self.bins = np.zeros(spectrum_bins)

        verts = self.vertices()

        self.vao = GLuint(0)
        glGenVertexArrays(1, self.vao)
        
        self.vbo = GLuint(0)
        glGenBuffers(1, self.vbo)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER,  verts, GL_STATIC_DRAW)

        glBindVertexArray(self.vao)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, float_size(3), 0)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def set_fps(self, fps: float):
        self.fps = fps
        self.samples_per_frame = self.sample_rate / self.fps

    def set_sample_rate(self, sample_rate: float):
        self.sample_rate = sample_rate
        self.samples_per_frame = self.sample_rate / self.fps

    def tick(self):
        self.position += self.samples_per_frame

    def fill_bins(self):
        # Run fft
        # TODO: Do STFT from the tick function
        # TODO: Convert to dB linear
        complex_fft_data: np.array[complex] = np.fft.fft(self.audio_stream[int(self.position):int(self.position) + int(self.samples_per_frame)])
        fft_magnitude: np.array[float] = np.sqrt(complex_fft_data.real ** 2 + complex_fft_data.imag ** 2)

        # Slice magnitudes into equal bins
        # TODO: Make the bins into their own class with update functions for smoothing
        bin_width = len(fft_magnitude)
        for i in range(0, self.spectrum_bins):
            start = i * bin_width

            self.bins[i] = sum(fft_magnitude[start:start+bin_width])

        # NOTE: Remove this once bins and in dB linear
        factor = max(self.bins)
        for i in range(0, self.spectrum_bins):
            # self.bins[i] /= factor
            self.bins[i] = 1 - (i * (1 / self.spectrum_bins)) ** 2

    def vertices(self):
        vertices = []
        # x and y go from -1 to 1 so the full width is 2
        bin_width = 2 / self.spectrum_bins

        for i in range(0, self.spectrum_bins):
            x = -1 + i * bin_width
            y = -1 + 2 * self.bins[i]

            bar_rect = [
                [x + self.padding, y, self.z], # top left
                [x + self.padding, -1, self.z], # bottom left
                [x - self.padding + bin_width, -1, self.z], # bottom right
                [x + self.padding, y, self.z], # top left
                [x - self.padding + bin_width, -1, self.z], # bottom right
                [x - self.padding + bin_width, y, self.z] # top right
                        ]
            vertices += bar_rect


        return np.array(vertices)
    
    def bind_shader(self, shader: Shader):
        self.shader = shader

    def draw(self):
        self.shader.bind()
        glBegin(GL_TRIANGLES)
        for vert in self.vertices():
            glVertex3f(*vert)
        glEnd()

        # TODO: Figure out vertex arrays later
        # glBindVertexArray(self.vao)
        # glDrawArrays(GL_TRIANGLES, 0, len(self.vertices()))

    

def float_size(n=1):
    return sizeof(ctypes.c_float) * n

