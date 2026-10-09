import glfw
import glm
import moderngl

import random
import math
import numpy as np

from objects.model import Model

class Asteroid(Model):

    def __init__(self, mesh, size):
        self.mesh = mesh

        x,y = self.generate_initial_position()
        self.position = glm.vec2(x,y)

        self.angle =  math.radians(random.randint(1, 360))

        if(size == "G"):
            speed = 1.5
        elif(size == "M"):
            speed = 3
        else:
            speed = 6

        self.velocity = glm.vec2(math.cos(self.angle), math.sin(self.angle)) * speed

    def generate_initial_position(self):
        x_limit = 10
        y_limit = 7

        rand_number = random.randint(1, 2)
        if(rand_number > 1):
            x = random.randint(-x_limit, x_limit)
            if(x==10 or x==-10):
                y = random.randint(-y_limit, y_limit)
            else:
                y = random.choice([7,-7])
            return x,y

        y = random.randint(-y_limit, y_limit)
        if(y==7 or y==-7):
            x = random.randint(-x_limit, x_limit)
        else:
             x = random.choice([10,-10])
        
        return x,y
        
    def draw(self, program, ctx, is_dark=False):
        ctx.line_width = 2.0
        super().draw(program, mode=moderngl.LINE_LOOP, is_dark=is_dark)

