from pathlib import Path

import glfw
import moderngl
import glm

import math
import numpy as np
import random

from objects.mesh import Mesh
from objects.ship import Ship
from objects.asteroid import Asteroid
from objects.lifebar import LifeBar
from collision import check_ship_asteroid_collision


class Game:
    LIGHT_THEME = (0.608, 0.737, 0.059, 1.0)
    DARK_THEME = (0.02, 0.02, 0.05, 1.0)

    def __init__(self):
        self.window = None
        self.ctx = None
        self.program = None

        self.ship = None
        self.arr_asteroid = []
        self.life_bar = None

        self.is_dark = True

        self.lives = 3

        self.initialize()

    def initialize(self):
        self.initialize_glfw()
        self.create_window()

        self.ctx = moderngl.create_context()
        self.program = self.setup_shader_program()

        self.setup_projection_matrix()

        self.create_objects()

    def initialize_glfw(self):
        if not glfw.init():
            raise RuntimeError("Falha GLFW.")

    def create_window(self):
        self.window = glfw.create_window(800, 600, "Asteroids", None, None)

        if not self.window:
            raise RuntimeError("Erro ao criar janela.")

        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.handle_key_event)

    def setup_shader_program(self):
        shader_dir = Path(__file__).parent / "shaders"

        return self.ctx.program(
            vertex_shader=(shader_dir / "basic.vert").read_text(),
            fragment_shader=(shader_dir / "basic.frag").read_text()
        )

    def setup_projection_matrix(self):
        projection = glm.ortho(-10.0, 10.0,-7.5, 7.5,-1.0, 1.0)
        self.program["projection"].write(np.array(projection.to_list(), dtype="f4").tobytes())

    def create_ship(self):
        ship_vertices = np.array([0.8, 0.0, -0.4, 0.4, -0.2, 0.0, -0.4, -0.4], dtype="f4")
        mesh = Mesh(self.ctx, self.program, ship_vertices)
        self.ship = Ship(mesh)
        
    def create_asteroid(self, size="G"):
        if size == "G":
            MIN_RADIUS = 0.85
            MAX_RADIUS = 1.15

            MIN_SEGMENT = 8
            MAX_SEGMENT = 12
        elif size == "M":
            MIN_RADIUS = 0.45
            MAX_RADIUS = 0.75
            
            MIN_SEGMENT = 6
            MAX_SEGMENT = 10
        else:
            MIN_RADIUS = 0.25
            MAX_RADIUS = 0.55
                    
            MIN_SEGMENT = 4
            MAX_SEGMENT = 8

        segments = random.randint(MIN_SEGMENT, MAX_SEGMENT)
    
        vertices = []
        base_radius = 1.5
            
        for i in range(segments):
            radius = base_radius * random.uniform(MIN_RADIUS, MAX_RADIUS)
            angle = 2.0 * math.pi * i / segments

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius

            vertices.extend([x, y])

        vertices = np.array(vertices, dtype="f4")
        mesh = Mesh(self.ctx, self.program, vertices)
        asteroid = Asteroid(mesh, size)

        self.arr_asteroid.append(asteroid)

    def create_arr_asteroid(self, size = "G", items = 4):
        for _ in range(items):
            self.create_asteroid(size)

    def create_objects(self):
        self.create_ship()
        self.create_arr_asteroid()
        self.life_bar = LifeBar(self.ctx, self.program)

    def calculate_delta_time(self, last_time):
        current_time = glfw.get_time()
        dt = current_time - last_time

        return current_time, dt

    def handle_input(self, dt):
        self.ship.handleInput(self.window, dt)

    def handle_key_event(self, window, key, scancode, action, mods):
        if key == glfw.KEY_DOWN and action == glfw.PRESS:
            self.is_dark = not self.is_dark

    def handle_collision(self):
        if self.ship.invulnerability_time > 0:
            return
    
        for asteroid in self.arr_asteroid:
            if check_ship_asteroid_collision(self.ship, asteroid):
                self.lose_life()
                self.ship.reset_position()
                break

    def lose_life(self):
        self.lives -= 1
        self.ship.make_invulnerable()

    def update(self, dt):
        self.ship.update(dt)
        for asteroid in self.arr_asteroid:
            asteroid.update(dt)
        self.handle_collision()

    def render(self):
        self.ctx.clear(*(Game.DARK_THEME if self.is_dark else Game.LIGHT_THEME))
        self.ship.draw(self.program, is_dark=self.is_dark)
        self.life_bar.draw(self.lives, self.is_dark)

        for asteroid in self.arr_asteroid:
            asteroid.draw(self.program, self.ctx, is_dark=self.is_dark)

    def run(self):
        last_time = glfw.get_time()

        while not glfw.window_should_close(self.window):
            last_time, dt = self.calculate_delta_time(last_time)

            glfw.poll_events()

            self.handle_input(dt)
            self.update(dt)
            self.render()

            glfw.swap_buffers(self.window)

        self.close()

    def close(self):
        glfw.destroy_window(self.window)
        glfw.terminate()
