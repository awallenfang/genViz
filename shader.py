from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Shader():
    def __init__(self, file_path):
        self.ready = False

        frag_handle = glCreateShader( GL_FRAGMENT_SHADER )
        vert_handle = glCreateShader( GL_VERTEX_SHADER )

        self.program = glCreateProgram()

        with open("./shaders/default.vert", "r") as source:
            code = source.read()
            glShaderSource(vert_handle, [code], [len(code)])

        self.check_error()

        with open(file_path, "r") as source:
            code = source.read()
            glShaderSource(frag_handle, [code], [len(code)])

        self.check_error()
        
        glCompileShader(vert_handle)

        success = glGetShaderiv( vert_handle, GL_COMPILE_STATUS)

        if not success:
            print(f'Vertex shader compiler error:\n\n{glGetShaderInfoLog(vert_handle)}')
            sys.exit()

        glCompileShader(frag_handle)

        success = glGetShaderiv( frag_handle, GL_COMPILE_STATUS)

        if not success:
            print(f'Fragment shader compiler error:\n\n{glGetShaderInfoLog(frag_handle)}')
            sys.exit()

        glAttachShader(self.program, vert_handle)
        glAttachShader(self.program, frag_handle)

        self.check_error()

        glLinkProgram(self.program)

        self.check_error()

        # success = glGetProgramiv( self.program, GL_LINK_STATUS)

        # if not success:
        #     print(f'Shader linking error:\n\n{glGetProgramInfoLog(self.program)}')
        #     sys.exit()

        self.ready = True

    def bind(self):
        if self.ready:
            glUseProgram(self.program)
        else:
            print("Shader not compiled/linked successfully. Cannot bind")

    def check_error(self):
         err = glGetError()
         if err != GL_NO_ERROR:
              print(f'GLERROR: {gluErrorString(err)}!\n')
