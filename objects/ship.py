import glfw
import glm
import moderngl

import numpy as np

from objects.model import Model

class Ship(Model):
    ACCEL = 12.0
    FRICTION = 0.985
    ROT_SPEED = 3.5

    def __init__(self, mesh):
        self.invulnerability_time = 0.0
        self.invulnerability_duration = 2.0

        self.blink_timer = 0.0
        self.visible = True

        super().__init__(mesh)
        

    def handleInput(self, window, dt):
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            self.angle += self.ROT_SPEED * dt
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            self.angle -= self.ROT_SPEED * dt
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            heading = glm.vec2(glm.cos(self.angle), glm.sin(self.angle))
            self.velocity += heading * self.ACCEL * dt

    def make_invulnerable(self):
        self.invulnerability_time = self.invulnerability_duration
        self.blink_timer = 0.0
        self.visible = True

    def update_invulnerability(self, dt):
        if self.invulnerability_time > 0:

            self.invulnerability_time -= dt
            self.blink_timer += dt

            if self.blink_timer >= 0.1:
                self.visible = not self.visible
                self.blink_timer = 0.0

        else:
            self.visible = True


    def reset_position(self):
        self.position = glm.vec2(0.0, 0.0)
        self.velocity = glm.vec2(0.0, 0.0)
        self.angle = 0.0

    def update(self, dt):
        self.velocity *= self.FRICTION
        self.update_invulnerability(dt)

        super().update(dt)

    def draw(self, program, is_dark=False):
        if not self.visible:
            return
        
        super().draw(program, mode=moderngl.TRIANGLE_FAN, is_dark=is_dark)

