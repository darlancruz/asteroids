from pathlib import Path

import glfw
import moderngl
import glm

import math
import numpy as np

from mesh import Mesh
from objects.ship import Ship
from objects.asteroid import Asteroid


def initializate_glfw():
    if not glfw.init():
        raise RuntimeError("Falha GLFW.")

def generate_window():
    window = glfw.create_window(800, 600, "Asteroids", None, None)
    if not window:
     raise RuntimeError("Erro ao criar Janela")
    glfw.make_context_current(window)
    return window

def setup_shader_program(ctx):
    shader_dir = Path(__file__).parent / "shaders"
    program = ctx.program(vertex_shader=(shader_dir/"basic.vert").read_text(),
                      fragment_shader=(shader_dir/"basic.frag").read_text())
    return program

def setup_projection_matrix(program):
    projection = glm.ortho(-10.0, 10.0, -7.5, 7.5, -1.0, 1.0)
    program["projection"].write(np.array(projection.to_list(), dtype="f4").tobytes())

def kill_game():
    glfw.destroy_window(window)
    glfw.terminate()

def create_ship(ctx, program):
    ship_vertices = np.array([0.8, 0.0, -0.4, 0.4, -0.2, 0.0, -0.4, -0.4], dtype="f4")
    mesh = Mesh(ctx, program, ship_vertices)
    ship = Ship(mesh)
    return ship

def create_asteroid(ctx, program):
    segments = 100
    vertices = []

    vertices.extend([0.0, 0.0])

    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments

        x = math.cos(angle) * 0.5
        y = math.sin(angle) * 0.5

        vertices.extend([x, y])

    vertices = np.array(vertices, dtype="f4")
    mesh = Mesh(ctx, program, vertices)
    asteroid = Asteroid(mesh)
    return asteroid


initializate_glfw()
window = generate_window()

ctx = moderngl.create_context()
program = setup_shader_program(ctx)
setup_projection_matrix(program)

ship = create_ship(ctx,program)
asteroid = create_asteroid(ctx, program)

dt = 1.0 / 60.0
while not glfw.window_should_close(window):
    glfw.poll_events()
   
    ship.handleInput(window, dt)
    ship.update(dt)
    asteroid.update(dt)

    ctx.clear(0.02, 0.02, 0.05)

    model = glm.translate(glm.mat4(1.0), glm.vec3(ship.position.x, ship.position.y, 0.0))
    model = glm.rotate(model, ship.angle, glm.vec3(0.0, 0.0, 1.0))
    program["model"].write(np.array(model.to_list(), dtype="f4").tobytes())

    ctx.line_width = 2.0
    program["color"].value = (0.0,0.0,0.0,0.0)
    ship.render(mode = moderngl.TRIANGLES)
    program["color"].value = (1.0, 1.0, 1.0, 1.0)
    ship.render(mode=moderngl.LINE_LOOP)

    model = glm.translate(glm.mat4(1.0), glm.vec3(asteroid.position.x, asteroid.position.y, 0.0))
    model = glm.rotate(model, asteroid.angle, glm.vec3(0.0, 0.0, 1.0))
    program["model"].write(np.array(model.to_list(), dtype="f4").tobytes())

    ctx.line_width = 2.0
    program["color"].value = (0.0,0.0,0.0,0.0)
    asteroid.render(mode = moderngl.TRIANGLE_FAN)
    program["color"].value = (1.0, 1.0, 1.0, 1.0)
    asteroid.render(mode=moderngl.LINE_LOOP)

    glfw.swap_buffers(window)

kill_game()
