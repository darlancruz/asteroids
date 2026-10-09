import glfw
import glm
import moderngl

import numpy as np

from objects.model import Model

class Ship(Model):
    ACCEL = 12.0
    FRICTION = 0.985
    ROT_SPEED = 3.5

    def handleInput(self, window, dt):
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            self.angle += self.ROT_SPEED * dt
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.angle -= self.ROT_SPEED * dt
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            heading = glm.vec2(glm.cos(self.angle), glm.sin(self.angle))
            self.velocity += heading * self.ACCEL * dt

    def update(self, dt):
        self.velocity *= self.FRICTION
        super().update(dt)

    def draw(self, program, is_dark=False):
        super().draw(program, mode=moderngl.TRIANGLE_FAN, is_dark=is_dark)

