from OpenGL.GLUT import *
from OpenGL.GL import *
# from OpenGL.GLU import *

import numpy as np
import matplotlib.pyplot as plt
from shader import Shader

from bin import Bin
from visualizers.base_bar_visualizer import BaseBarVisualizer

class VerticalBarVisualizer(BaseBarVisualizer):
    def __init__(self, audio_stream: np.array, sample_rate: float, x_origin = 0., y_origin = 0., window_width = 500, window_height = 500, width = 500, height= 500, spectrum_bins = 128, depth=0., shader = None, padding=0.002):
        """
        Init a Vertical Bar Visualizer. This is the classical style of a visualizer with vertical bars being arranged side by side.
        The audio_stream that should be displayed, as well as the sample_rate have to be delivered. 
        """
        self.audio_stream = audio_stream
        self.sample_rate = sample_rate
        self.fps = 30.
        self.spectrum_bins = spectrum_bins
        self.z = depth
        self.padding = padding
        
        self.window_width = window_width
        self.window_height = window_height
        self.width = width / window_width
        self.height = height / window_height
        self.set_width(width)
        self.set_height(height)
        self.set_position(x_origin, y_origin)
        
        self.finished = False

        self.vbo = glGenBuffers(1)
        self.vertex_amt = 0
        self.idx_amt = 0


        if shader == None:
            self.shader = Shader("./shaders/default.frag")
        else:
            self.shader = shader

        self.samples_per_frame = self.sample_rate / self.fps

        self.fft_size = 0
        i = 0
        # Choose the smallest power of two that can incapsulate all frames for a fast fft and free smoothing
        while self.fft_size < self.samples_per_frame:
            self.fft_size = 2**i
            i+=1

        self.fft_window = hann_window(self.fft_size)
        self.transport_pos = 0.

        self.bins = [Bin(0) for i in range(0,spectrum_bins)]

        self.transform = np.identity(4)
        self.build_transform_matrix()

        verts = self.build_vertices()

        self.vao = glGenVertexArrays(1)
        
        
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)


        self.fill_bins()

        print(f'Initialized Visualizer using audio stream with {len(audio_stream)} samples and {self.fps} FPS resulting in {self.samples_per_frame} samples/frame. \nUsing a fft buffer size of {self.fft_size} samples. \nWith a sample rate of {self.sample_rate} its duration is {len(self.audio_stream) / self.sample_rate} seconds')

    def set_fps(self, fps: float):
        
        self.fps = fps
        self.samples_per_frame = self.sample_rate / self.fps

    def set_sample_rate(self, sample_rate: float):
        self.sample_rate = sample_rate
        self.samples_per_frame = self.sample_rate / self.fps

    def tick(self):
        """
        Tick a frame in the audio data.
        """
        if self.finished:
            return
        
        self.transport_pos += self.samples_per_frame
        if self.transport_pos >= len(self.audio_stream) - self.samples_per_frame:
            self.finished = True
        self.fill_bins()

    def fill_bins(self):
        """
        Fill the bins with the data that is at the current transport position
        """
        # Run fft and pad remaining space with 0s
        data_slice = np.zeros(int(self.fft_size))
        if self.transport_pos + self.samples_per_frame > len(self.audio_stream):
            data_slice[:len(self.audio_stream) - int(self.transport_pos)] = self.audio_stream[int(self.transport_pos):]
        else:
            data_slice[:int(self.samples_per_frame)] = self.audio_stream[int(self.transport_pos):int(self.transport_pos) + int(self.samples_per_frame)]
        
        # Map into [0,1]
        data_slice += (data_slice + 1.) / 2
        data_slice = np.clip(data_slice, 0, 1)
        data_slice /= self.fft_size / 2

        data_slice *= self.fft_window
        # Due to the mirrored nature we just need half the output
        complex_fft_data: np.array[complex] = np.fft.fft(data_slice)[:len(data_slice) // 2 + 1]
        fft_magnitude: np.array[float] = complex_fft_data.real ** 2 + complex_fft_data.imag ** 2

        # Convert the magnitudes to dB
        fft_magnitude = 10 * np.log10(fft_magnitude + 0.000000000001)
        fft_magnitude[fft_magnitude < -90.] = -90.

        # Slice magnitudes into equal bins
        bin_width = len(fft_magnitude) // self.spectrum_bins #len(fft_magnitude) // self.spectrum_bins
        for i in range(0, self.spectrum_bins):
            start = i * bin_width
            bin_sum = sum(fft_magnitude[start:start+bin_width]) / bin_width

            self.bins[i].update(bin_sum) 
            # self.bins[i].update(i / self.spectrum_bins)

    def build_vertices(self):
        """
        Construct the vertex arrays from the spectrum bins
        """
        vertices = []
        indices = []
        # x and y go from -1 to 1 so the full width is 2
        bin_width = 2 / self.spectrum_bins

        for i in range(0, self.spectrum_bins):
            x = -1 + i * bin_width
            y = -1 + 2 * self.bins[i].linear_val()

            bar_rect_vert = [
                [x + self.padding, y, self.z], # top left
                [x + self.padding, -1, self.z], # bottom left
                [x - self.padding + bin_width, -1, self.z], # bottom right
                [x + self.padding, y, self.z], # top left
                [x - self.padding + bin_width, -1, self.z], # bottom right
                [x - self.padding + bin_width, y, self.z] # top right
                        ]
            
            base_idx = i*4
            bar_rect_idx = [
                base_idx + 0,base_idx + 2,base_idx + 3,
                base_idx + 0,base_idx + 3,base_idx + 1
            ]
            vertices += bar_rect_vert
            indices += bar_rect_idx


        self.vertex_amt = len(vertices)
        self.idx_amt = len(indices)

        return (np.array(vertices), np.array(indices))
    
    def bind_shader(self, shader: Shader):
        self.shader = shader

    def draw(self):
        """
        Draw this visualizer into the currently active ramebuffer
        """
        self.shader.bind()
        # TODO: Bind transformation matrix
        transform_location = glGetUniformLocation(self.shader.program, 'transform')
        pos_location = glGetUniformLocation(self.shader.program, 'pos')


        glUniformMatrix4fv(transform_location,1,False,self.transform)
        glUniform2fv(pos_location, 1, [self.x + self.origin_offset_x, self.y + self.origin_offset_y])
        glBegin(GL_TRIANGLES)
        for vert, idx in self.build_vertices():
            glVertex3f(vert)
        glEnd()
        
        # TODO: Figure out vertex arrays later
        # glBindVertexArray(self.vao)
        # glDrawArrays(GL_TRIANGLES, 0, len(self.vertices()))

    def set_position(self, x, y):
        # Set the position and normalize it
        self.x = 2 * (x / self.window_width)
        self.y = 2 * ((y / self.window_height) * -1)

    def set_width(self, width):
        # Normalize the width and set the offset to the space that is lost through the scaling
        self.width = width / self.window_width
        self.origin_offset_x = -(1 - self.width)
        self.build_transform_matrix()

    def set_height(self, height):
        # Normalize the height and set the offset to the space that is lost through the scaling
        self.height = height / self.window_height
        self.origin_offset_y = (1 - self.height)
        self.build_transform_matrix()

    def build_transform_matrix(self):
        """
        Build the scale transformation matrix
        """
        self.transform =  np.array([[self.width, 0, 0, 0],
                                   [0,self.height, 0, 0],
                                   [0,0,1,0],
                                   [0,0,0,1]])
    

def float_size(n=1):
    return sizeof(ctypes.c_float) * n

def hann_window(size) -> np.array:
    x = np.arange(0, size)
    window = np.sin(np.pi * x / size) ** 2
    return window