from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *

import numpy as np
from shader import Shader

class Visualizer():
    def __init__(self, audio_stream: np.array, sample_rate: float, x_origin = 0., y_origin = 0., width = 1920., height= 1080., spectrum_bins = 64, depth=0., shader = None):
        self.audio_stream = audio_stream
        self.sample_rate = sample_rate
        self.fps = 30.
        self.spectrum_bins = spectrum_bins
        self.z = depth

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
        complex_fft_data: np.array[complex] = np.fft.fft(self.audio_stream[int(self.position):int(self.position) + int(self.samples_per_frame)])
        fft_magnitude: np.array[float] = np.sqrt(complex_fft_data.real ** 2 + complex_fft_data.imag ** 2)

    def vertices(self):
        vertices = np.array([
            [-1.,-1.,self.z],
            [-1.,1.,self.z],
            [1.,1.,self.z],
            [-1.,-1.,self.z],
            [1.,1.,self.z],
            [1.,-1.,self.z],
        ])
        return vertices
    
    def bind_shader(self, shader: Shader):
        self.shader = shader

    def draw(self):
        self.shader.bind()
        glBegin(GL_POLYGON)
        for vert in self.vertices():
            glVertex3f(*vert)
        glEnd()

        # TODO: Figure out vertex arrays later
        # glBindVertexArray(self.vao)
        # glDrawArrays(GL_TRIANGLES, 0, len(self.vertices()))

    

def float_size(n=1):
    return sizeof(ctypes.c_float) * n