import moderngl

class Mesh():
    def __init__(self, ctx, program, vertices):
           self.vbo = ctx.buffer(vertices.tobytes())
           self.vao = ctx.simple_vertex_array(program, self.vbo, "in_pos")

    def render(self, mode=moderngl.TRIANGLES):
        self.vao.render(mode= mode)
          