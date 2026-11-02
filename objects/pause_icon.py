import moderngl

import numpy as np

from objects.mesh import Mesh
from objects.hud_element import HUDElement


class PauseIcon(HUDElement):
    def __init__(self, ctx, program):
        super().__init__(ctx, program, position=(8.7, 5.5))

        vertices = np.array(
            [
                -0.28,
                0.35,
                -0.04,
                0.35,
                -0.04,
                -0.35,
                -0.28,
                0.35,
                -0.04,
                -0.35,
                -0.28,
                -0.35,
                0.04,
                0.35,
                0.28,
                0.35,
                0.28,
                -0.35,
                0.04,
                0.35,
                0.28,
                -0.35,
                0.04,
                -0.35,
            ],
            dtype="f4",
        )

        self.mesh = Mesh(ctx, program, vertices)

    def draw(self, is_dark=False):
        self.draw_element(self.mesh, mode=moderngl.TRIANGLES, is_dark=is_dark)
