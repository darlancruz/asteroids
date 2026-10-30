import glm
import moderngl
import numpy as np

from objects.mesh import Mesh
from objects.model import Model

class LifeBar(Model):

    def __init__(self, ctx, program):
        self.ctx = ctx
        self.program = program

        vertices = np.array([0.0, -0.60, -0.25, -0.40,-0.50, -0.10, -0.55,  0.20,
                             -0.45,  0.45,-0.25,  0.55, 0.00,  0.35, 0.25,  0.55,
                             0.45,  0.45, 0.55,  0.20, 0.50, -0.10, 0.25, -0.40], dtype="f4")

        self.mesh = Mesh(ctx,program,vertices)

    def draw_heart(self, x, y, is_dark=False):
        model = glm.translate(glm.mat4(1.0), glm.vec3(x, y, 0.0))
        model = glm.scale(model, glm.vec3(0.7, 0.7, 1.0))

        self.program["model"].write(np.array(model.to_list(),dtype="f4").tobytes())
        self.ctx.line_width = 2.0

        if is_dark:
            self.program["color"].value = super().DARK_COLOR
        else: 
            self.program["color"].value = super().LIGHT_COLOR

        self.mesh.render( mode=moderngl.TRIANGLE_FAN)

    def draw(self, lives, is_dark=False):
        start_x = -8.8
        y = 6.5
        spacing = 1.4

        for i in range(lives):
            x = start_x + i * spacing
            self.draw_heart(x,y,is_dark)
