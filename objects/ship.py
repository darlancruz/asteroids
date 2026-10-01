import glfw
import glm

class Ship:
    ACCEL = 12.0
    FRICTION = 0.985
    ROT_SPEED = 3.5

    def __init__(self):
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

