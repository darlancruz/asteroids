from pathlib import Path

import glfw
import moderngl
import glm

import math
import numpy as np
import random

from objects.mesh import Mesh
from objects.model import Model
from objects.ship import Ship
from objects.asteroid import Asteroid
from objects.lifebar import LifeBar
from objects.pause_icon import PauseIcon
from objects.text_renderer import TextRenderer

from collision import check_ship_asteroid_collision, check_bullet_asteroid_collision


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
        self.arr_bullets = []

        self.is_dark = True
        self.is_stated = False
        self.is_paused = False

        self.lives = 3
        self.score = 0
        self.current_wave = 0

        self.vsync_enabled = True
        self.frame_count = 0
        self.fps_timer = 0.0
        self.current_fps = 0.0

        self.key_actions = {
            glfw.KEY_DOWN: self.toggle_dark_mode,
            glfw.KEY_ENTER: self.handle_enter,
            glfw.KEY_SPACE: self.handle_shoot,
            glfw.KEY_V: self.toggle_vsync,
            glfw.KEY_BACKSPACE: self.handle_restart,
        }

        self.initialize()

    def initialize(self):
        self.initialize_glfw()
        self.create_window()

        self.ctx = moderngl.create_context()
        self.program = self.setup_shader_program()

        self.setup_projection_matrix()

        self.create_meshs()
        self.create_objects()

    def restart_game(self):
        self.lives = 3
        self.score = 0
        self.is_paused = False
        self.arr_bullets.clear()
        self.arr_asteroid.clear()
        self.create_objects()

    def initialize_glfw(self):
        if not glfw.init():
            raise RuntimeError("Falha GLFW.")

    def create_window(self):
        self.window = glfw.create_window(800, 600, "Asteroids", None, None)

        if not self.window:
            raise RuntimeError("Erro ao criar janela.")

        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.swap_interval(1)
        glfw.set_window_size_callback(self.window, self.resize_callback)

    def resize_callback(self, window, width, height):
        self.update_projection(width, height)

    def setup_shader_program(self):
        shader_dir = Path(__file__).parent / "shaders"

        return self.ctx.program(
            vertex_shader=(shader_dir / "basic.vert").read_text(),
            fragment_shader=(shader_dir / "basic.frag").read_text(),
        )

    def setup_projection_matrix(self):
        width, height = glfw.get_window_size(self.window)
        self.update_projection(width, height)

    def update_projection(self, width, height):
        if height == 0:
            height = 1

        self.ctx.viewport = (0, 0, width, height)

        half_height = 7.5
        aspect = width / height
        half_width = half_height * aspect

        Model.SCREEN_WIDTH = half_width

        projection = glm.ortho(
            -half_width, half_width, -half_height, half_height, -1.0, 1.0
        )
        self.program["projection"].write(
            np.array(projection.to_list(), dtype="f4").tobytes()
        )

    def create_ship(self):
        self.ship = Ship(self.ship_mesh)

    def create_meshs(self):
        self.ship_mesh = self.create_ship_mesh()
        self.bullet_mesh = self.create_bullet_mesh()

    def create_ship_mesh(self):
        ship_vertices = np.array(
            [0.8, 0.0, -0.4, 0.4, -0.2, 0.0, -0.4, -0.4], dtype="f4"
        )
        return Mesh(self.ctx, self.program, ship_vertices)

    def create_bullet_mesh(self):
        vertices = np.array([0.12, 0.0, 0.0, 0.12, -0.12, 0.0, 0.0, -0.12], dtype="f4")
        return Mesh(self.ctx, self.program, vertices)

    def create_asteroid(self, size="G", position=None, velocity=None):
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
        asteroid = Asteroid(mesh, size, radius, position, velocity)

        self.arr_asteroid.append(asteroid)

    def create_arr_asteroid(self, size="G", items=4):
        for _ in range(items):
            self.create_asteroid(size)

    def split_asteroid(self, asteroid):
        new_size = asteroid.split()

        if new_size is None:
            return

        direction = glm.normalize(asteroid.velocity)
        perpendicular = glm.vec2(-direction.y, direction.x)
        speed = glm.length(asteroid.velocity) * 2

        velocity_a = perpendicular * speed
        velocity_b = -perpendicular * speed

        self.create_asteroid(new_size, asteroid.position, velocity_a)
        self.create_asteroid(new_size, asteroid.position, velocity_b)

    def create_objects(self):
        self.create_ship()
        self.create_arr_asteroid()

        self.life_bar = LifeBar(self.ctx, self.program)
        self.pause_icon = PauseIcon(self.ctx, self.program)

        self.score_renderer = TextRenderer(self.ctx, self.program, position=(6.8, 6.5))
        self.main_text_renderer = TextRenderer(
            self.ctx, self.program, position=(0.0, 1.0)
        )
        self.secondary_text_renderer = TextRenderer(
            self.ctx, self.program, position=(0.0, -1.0)
        )

    def calculate_delta_time(self, last_time):
        current_time = glfw.get_time()
        dt = current_time - last_time

        if dt > 0.1:
            dt = 0.1

        return current_time, dt

    def handle_input(self, dt):
        self.ship.handleInput(self.window, dt)

    def key_callback(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.on_key_action(key)

    def on_key_action(self, key):
        action = self.key_actions.get(key)
        if action:
            action()

    def toggle_dark_mode(self):
        self.is_dark = not self.is_dark

    def handle_enter(self):
        if not self.is_stated:
            self.is_stated = True
            self.restart_game()
        elif self.lives > 0:
            self.is_paused = not self.is_paused

    def handle_shoot(self):
        if self.is_stated and not self.is_paused and self.lives > 0:
            bullet = self.ship.shoot(self.bullet_mesh)
            self.arr_bullets.append(bullet)

    def toggle_vsync(self):
        self.vsync_enabled = not self.vsync_enabled
        glfw.swap_interval(1 if self.vsync_enabled else 0)

    def handle_restart(self):
        if self.is_stated:
            self.restart_game()

    def handle_collision(self):
        if self.ship.invulnerability_time > 0:
            return

        for asteroid in self.arr_asteroid:
            if check_ship_asteroid_collision(self.ship, asteroid):
                self.lose_life()
                self.ship.reset_position()
                break

    def handle_bullet_collision(self):
        for bullet in self.arr_bullets:
            for asteroid in self.arr_asteroid:
                if check_bullet_asteroid_collision(bullet, asteroid):
                    bullet.active = False
                    self.split_asteroid(asteroid)
                    self.update_score(asteroid.size)
                    self.arr_asteroid.remove(asteroid)
                    break

    def lose_life(self):
        self.lives -= 1
        self.ship.make_invulnerable()

    def spawn_asteroids(self):
        if len(self.arr_asteroid) < 2:
            self.current_wave += 1
            num_large = min(2 + self.current_wave, 8)
            self.create_arr_asteroid("G", num_large)

    def update_score(self, asteroid_size):
        if asteroid_size == "G":
            self.score += 20
        elif asteroid_size == "M":
            self.score += 50
        else:
            self.score += 100

    def update_fps_counter(self, dt):
        self.frame_count += 1
        self.fps_timer += dt

        if self.fps_timer >= 0.5:
            self.current_fps = self.frame_count / self.fps_timer
            self.frame_count = 0
            self.fps_timer = 0.0

            vsync_status = "ON" if self.vsync_enabled else "OFF"
            title = f"Asteroids | FPS: {self.current_fps:.1f} | VSync: {vsync_status}"
            glfw.set_window_title(self.window, title)

    def update(self, dt):
        self.update_fps_counter(dt)
        self.ship.update(dt)
        for asteroid in self.arr_asteroid:
            asteroid.update(dt)
        for bullet in self.arr_bullets:
            bullet.update(dt)

        self.handle_bullet_collision()
        self.arr_bullets = [bullet for bullet in self.arr_bullets if bullet.active]

        self.handle_collision()
        self.spawn_asteroids()

    def render(self):
        self.ctx.clear(*(Game.DARK_THEME if self.is_dark else Game.LIGHT_THEME))

        if self.is_stated:
            if self.lives > 0:
                self.ship.draw(self.program, is_dark=self.is_dark)

            self.life_bar.draw(self.lives, self.is_dark)
            self.score_renderer.draw_text(
                f"{self.score:04d}", scale=0.8, is_dark=self.is_dark
            )

        for asteroid in self.arr_asteroid:
            asteroid.draw(self.program, self.ctx, is_dark=self.is_dark)
        for bullet in self.arr_bullets:
            bullet.draw(self.program, is_dark=self.is_dark)

        if self.is_paused:
            self.pause_icon.draw(is_dark=self.is_dark)

        if self.lives <= 0 and self.is_stated:
            self.main_text_renderer.draw_text(
                "FIM DE JOGO", scale=1.5, is_dark=self.is_dark, centered=True
            )
            self.secondary_text_renderer.draw_text(
                "APERTE BACKSPACE PARA REINICIAR",
                scale=0.5,
                is_dark=self.is_dark,
                centered=True,
            )

        if not self.is_stated:
            self.main_text_renderer.draw_text(
                "ASTEROID", scale=1.5, is_dark=self.is_dark, centered=True
            )
            self.secondary_text_renderer.draw_text(
                "APERTE ENTER PARA INICIAR",
                scale=0.5,
                is_dark=self.is_dark,
                centered=True,
            )

    def run(self):
        last_time = glfw.get_time()

        while not glfw.window_should_close(self.window):
            last_time, dt = self.calculate_delta_time(last_time)

            glfw.poll_events()

            if not self.is_paused:
                self.handle_input(dt)
                self.update(dt)

            self.render()

            glfw.swap_buffers(self.window)

        self.close()

    def close(self):
        glfw.destroy_window(self.window)
        glfw.terminate()
