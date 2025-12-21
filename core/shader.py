from OpenGL.GL import *
from OpenGL.GL import shaders

class Shader:
    def __init__(self, vertex_path=None, fragment_path=None):
        # 修改点：确保 #version 紧贴着三引号，前面不要有回车
        vertex_src = """#version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aColor;

        out vec3 ourColor;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main() {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
            ourColor = aColor;
        }
        """

        fragment_src = """#version 330 core
        in vec3 ourColor;
        out vec4 FragColor;

        void main() {
            FragColor = vec4(ourColor, 1.0);
        }
        """
        
        # 编译 Shader
        shader_v = shaders.compileShader(vertex_src, GL_VERTEX_SHADER)
        shader_f = shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER)
        self.program = shaders.compileProgram(shader_v, shader_f)

    def use(self):
        glUseProgram(self.program)

    def set_mat4(self, name, mat):
        loc = glGetUniformLocation(self.program, name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, mat)
