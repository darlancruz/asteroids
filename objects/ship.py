import glfw
import glm
import moderngl

import numpy as np

class Ship:
    ACCEL = 12.0
    FRICTION = 0.985
    ROT_SPEED = 3.5

    COR_NOITE = (0.0,0.0,0.0,0.0)
    CONTORNO_NOITE = (1.0, 1.0, 1.0, 1.0)

    COR_DIA = (0.608, 0.737, 0.059, 1.0)
    CONTORNO_DIA = (0.0,0.0,0.0,0.0)

    def __init__(self, mesh):
        self.mesh = mesh
        self.position = glm.vec2(0.0, 0.0)
        self.velocity = glm.vec2(0.0, 0.0)
        self.angle = 0.0

    def handleInput(self, window, dt):
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            self.angle += self.ROT_SPEED * dt
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.angle -= self.ROT_SPEED * dt
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            heading = glm.vec2(glm.cos(self.angle), glm.sin(self.angle))
            self.velocity += heading * self.ACCEL * dt

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
        self.velocity *= self.FRICTION
        self.wrap_screen()

    def render(self, mode=moderngl.TRIANGLES):
        self.mesh.render(mode = mode)

    def draw(self, ctx, program, noite):
        model = glm.translate(glm.mat4(1.0), glm.vec3(self.position.x, self.position.y, 0.0))
        model = glm.rotate(model, self.angle, glm.vec3(0.0, 0.0, 1.0))
        program["model"].write(np.array(model.to_list(), dtype="f4").tobytes())
        
        ctx.line_width = 2.0
        program["color"].value = self.COR_NOITE if noite else self.COR_DIA
        self.render(mode = moderngl.TRIANGLE_FAN)
        program["color"].value = self.CONTORNO_NOITE if noite else self.CONTORNO_DIA
        self.render(mode=moderngl.LINE_LOOP)

