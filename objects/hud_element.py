import glm
import moderngl

import numpy as np


class HUDElement:
    DARK_COLOR = (1.0, 1.0, 1.0, 1.0)
    LIGHT_COLOR = (0.0, 0.0, 0.0, 0.0)

    def __init__(self, ctx, program, position):
        self.ctx = ctx
        self.program = program
        self.position = glm.vec2(position)

    def draw_element(self, mesh, mode=moderngl.TRIANGLES, is_dark=False, scale=1.0):
        model = glm.translate(
            glm.mat4(1.0), glm.vec3(self.position.x, self.position.y, 0.0)
        )
        if scale != 1.0:
            model = glm.scale(model, glm.vec3(scale, scale, 1.0))

        self.program["model"].write(np.array(model.to_list(), dtype="f4").tobytes())
        self.program["color"].value = self.DARK_COLOR if is_dark else self.LIGHT_COLOR
        mesh.render(mode=mode)
