import glm
import moderngl

from objects.model import Model

class Bullet(Model):
    SPEED = 15.0
    MAX_DISTANCE = 15.0

    def __init__(self, mesh, position, direction):
        super().__init__(mesh)

        self.position = glm.vec2(position)
        self.velocity = glm.normalize(direction) * self.SPEED

        self.distance_traveled = 0.0
        self.active = True

    def update(self, dt):

        displacement = self.velocity * dt

        self.position += displacement
        self.distance_traveled += glm.length(displacement)

        if self.distance_traveled >= self.MAX_DISTANCE:
            self.active = False

    def draw(self, program, is_dark=False):

        if not self.active:
            return

        super().draw(
            program,
            mode=moderngl.TRIANGLE_FAN,
            is_dark=is_dark
        )
