import glm
import moderngl

import random
import math

from objects.model import Model

class Asteroid(Model):
    WRAP_MARGIN = 2

    def __init__(self, mesh, size, radius, position = None, velocity=None):
        super().__init__(mesh)
        self.mesh = mesh
        self.size = size
        self.radius = radius

        if(position):
            self.position = glm.vec2(position)
        else:
            x, y = self.generate_initial_position()
            self.position = glm.vec2(x, y)

        if velocity:
            self.velocity = glm.vec2(velocity)
        else:
            if size == "G":
                speed = 1.5
            elif size == "M":
                speed = 3.0
            else:
                speed = 6.0

            angle_to_center = math.atan2(-self.position.y, -self.position.x)
            spread = math.radians(random.randint(-60, 60))
            self.angle = angle_to_center + spread

            self.velocity = glm.vec2(math.cos(self.angle), math.sin(self.angle)) * speed

    def generate_initial_position(self):
        x_limit = 10.0
        y_limit = 7.5
             
        bound_x = x_limit + self.WRAP_MARGIN + 5
        bound_y = y_limit + self.WRAP_MARGIN

        side = random.choice(['left', 'right', 'bottom', 'top'])

        if side == 'left':
            x = -bound_x
            y = random.uniform(-bound_y, bound_y)
        elif side == 'right':
            x = bound_x
            y = random.uniform(-bound_y, bound_y)
        elif side == 'bottom':
            x = random.uniform(-bound_x, bound_x)
            y = -bound_y
        else:  
            x = random.uniform(-bound_x, bound_x)
            y = bound_y

        return x, y

    def wrap_screen(self):
        bound_x = self.SCREEN_WIDTH + self.WRAP_MARGIN
        bound_y = self.SCREEN_HEIGHT + self.WRAP_MARGIN

        if self.position.x > bound_x: 
            self.position.x = -bound_x
        elif self.position.x < -bound_x: 
            self.position.x = bound_x

        if self.position.y > bound_y:
            self.position.y = -bound_y
        elif self.position.y < -bound_y: 
            self.position.y = bound_y

    def split(self):
        if self.size == "G":
            return "M"

        elif self.size == "M":
            return "P"

        return None
        
    def draw(self, program, ctx, is_dark=False):
        ctx.line_width = 2.0
        super().draw(program, mode=moderngl.LINE_LOOP, is_dark=is_dark)