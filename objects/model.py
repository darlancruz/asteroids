import glfw
import glm
import moderngl

import numpy as np

class Model:
    SCREEN_WIDTH = 10  
    SCREEN_HEIGHT = 7.5

    DARK_COLOR= (1.0, 1.0, 1.0, 1.0)
    LIGHT_COLOR = (0.0,0.0,0.0,0.0)

    def __init__(self, mesh):
        self.mesh = mesh
        self.position = glm.vec2(0.0, 0.0)
        self.velocity = glm.vec2(0.0, 0.0)
        self.angle = 0.0

    def wrap_screen(self):
        if self.position.x > self.SCREEN_WIDTH: 
            self.position.x = -self.SCREEN_WIDTH

        elif self.position.x < -self.SCREEN_WIDTH: 
            self.position.x = self.SCREEN_WIDTH

        if self.position.y > self.SCREEN_HEIGHT:
            self.position.y = -self.SCREEN_HEIGHT

        elif self.position.y < -self.SCREEN_HEIGHT: 
            self.position.y = self.SCREEN_HEIGHT

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_screen()

    def render(self, mode=moderngl.TRIANGLES):
        self.mesh.render(mode = mode)

    def draw(self, program, mode=moderngl.TRIANGLES, is_dark=False):
        model = glm.translate(glm.mat4(1.0), glm.vec3(self.position.x, self.position.y, 0.0))
        model = glm.rotate(model, self.angle, glm.vec3(0.0, 0.0, 1.0))
        program["model"].write(np.array(model.to_list(), dtype="f4").tobytes())

        program["color"].value = self.DARK_COLOR if is_dark else self.LIGHT_COLOR
        self.render(mode=mode)