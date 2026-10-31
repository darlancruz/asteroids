import moderngl

import numpy as np

from objects.hud_element import HUDElement
from objects.mesh import Mesh

class TextRenderer(HUDElement):
    DIGITS = {
        '0': [(-0.3,  0.5,  0.3,  0.5),( 0.3,  0.5,  0.3, -0.5),( 0.3, -0.5, -0.3, -0.5),(-0.3, -0.5, -0.3,  0.5),(-0.3, -0.5,  0.3,  0.5)],
        '1': [(0.0, 0.5, 0.0, -0.5)],
        '2': [(-0.3, 0.5, 0.3, 0.5), (0.3, 0.5, 0.3, 0.0), (0.3, 0.0, -0.3, 0.0), (-0.3, 0.0, -0.3, -0.5), (-0.3, -0.5, 0.3, -0.5)],
        '3': [(-0.3, 0.5, 0.3, 0.5), (0.3, 0.5, 0.3, -0.5), (-0.3, -0.5, 0.3, -0.5), (-0.3, 0.0, 0.3, 0.0)],
        '4': [(-0.3, 0.5, -0.3, 0.0), (-0.3, 0.0, 0.3, 0.0), (0.3, 0.5, 0.3, -0.5)],
        '5': [(0.3, 0.5, -0.3, 0.5), (-0.3, 0.5, -0.3, 0.0), (-0.3, 0.0, 0.3, 0.0), (0.3, 0.0, 0.3, -0.5), (0.3, -0.5, -0.3, -0.5)],
        '6': [((-0.3, 0.5, -0.3, -0.5)), (-0.3, -0.5, 0.3, -0.5), (0.3, -0.5, 0.3, 0.0), (0.3, 0.0, -0.3, 0.0)],
        '7': [(-0.3, 0.5, 0.3, 0.5), (0.3, 0.5, 0.3, -0.5)],
        '8': [(-0.3, 0.5, 0.3, 0.5), (0.3, 0.5, 0.3, -0.5), (0.3, -0.5, -0.3, -0.5), (-0.3, -0.5, -0.3, 0.5), (-0.3, 0.0, 0.3, 0.0)],
        '9': [(-0.3, 0.0, 0.3, 0.0), (0.3, 0.5, -0.3, 0.5), (-0.3, 0.5, -0.3, 0.0), (0.3, 0.5, 0.3, -0.5)]
    }


    def draw_text(self, text, scale=1.0, spacing=0.8, is_dark=False):
        original_x = self.position.x
        
        self.ctx.line_width = 2.0

        for char in str(text):
            if char in self.DIGITS:
                segments = self.DIGITS[char]
                vertices = []
                for seg in segments:
                    vertices.extend([seg[0] * scale, seg[1] * scale])
                    vertices.extend([seg[2] * scale, seg[3] * scale])

                if vertices:
                    mesh = Mesh(self.ctx, self.program, np.array(vertices, dtype="f4"))
                    self.draw_element(mesh, mode=moderngl.LINES, is_dark=is_dark)

            self.position.x += spacing * scale

        self.position.x = original_x