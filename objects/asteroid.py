import glfw
import glm
import moderngl

import random
import math
import numpy as np

class Asteroid:

    COR_NOITE = (0.0,0.0,0.0,0.0)
    CONTORNO_NOITE = (1.0, 1.0, 1.0, 1.0)

    COR_DIA = (0.059, 0.220, 0.059, 1.0)
    CONTORNO_DIA = (0.0,0.0,0.0,0.0)

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

    def wrap_screen(self):
        if self.position.x > 10.0: 
            self.position.x = -10.0

        elif self.position.x < -10.0: 
            self.position.x = 10.0

        if self.position.y > 7.5:
            self.position.y = -7.5

        elif self.position.y < -7.5: 
            self.position.y = 7.5

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_screen()
        
    def render(self, mode=moderngl.TRIANGLES):
        self.mesh.render(mode = mode)

    def draw(self, ctx, program, noite):
        model = glm.translate(glm.mat4(1.0), glm.vec3(self.position.x, self.position.y, 0.0))
        model = glm.rotate(model, self.angle, glm.vec3(0.0, 0.0, 1.0))
        program["model"].write(np.array(model.to_list(), dtype="f4").tobytes())
        
        ctx.line_width = 2.0
       
        program["color"].value = self.COR_NOITE if noite else self.COR_DIA
        self.render(mode = moderngl.LINE_LOOP)
        program["color"].value = self.CONTORNO_NOITE if noite else self.CONTORNO_DIA
        self.render(mode=moderngl.LINE_LOOP)

