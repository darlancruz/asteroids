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

FUNDO_DIA = (0.608, 0.737, 0.059, 1.0)
FUNDO_NOITE = (0.02, 0.02, 0.05, 1.0)

noite = True
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

def kill_game(window):
    glfw.destroy_window(window)
    glfw.terminate()

def create_ship(ctx, program):
    ship_vertices = np.array([0.8, 0.0, -0.4, 0.4, -0.2, 0.0, -0.4, -0.4], dtype="f4")
    mesh = Mesh(ctx, program, ship_vertices)
    ship = Ship(mesh)
    return ship

def create_asteroid(ctx, program, size="G"):

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

    vertices.extend([0.0, 0.0])
    base_radius = 1.5

    
    for i in range(segments):
        radius = base_radius * random.uniform(MIN_RADIUS, MAX_RADIUS)
        angle = 2.0 * math.pi * i / segments

        x = math.cos(angle) * radius
        y = math.sin(angle) * radius

        vertices.extend([x, y])

    vertices = np.array(vertices, dtype="f4")
    mesh = Mesh(ctx, program, vertices)
    asteroid = Asteroid(mesh, size)
    return asteroid

def create_arr_asteroid(ctx, program, size = "G", items = 4):
    arr = []

    for _ in range(items):
        asteroid = create_asteroid(ctx, program, size)
        arr.append(asteroid)

    return arr

def calculate_delta_time(last_time):
    current_time = glfw.get_time()
    dt = current_time - last_time

    return current_time, dt

def handle_input(window, dt):
    ship.handleInput(window, dt)

def update(dt, ship, arr_asteroid):
    ship.update(dt)
    for asteroid in arr_asteroid:
        asteroid.update(dt)

def render(ctx, ship, arr_asteroid):
    ctx.clear(*(FUNDO_NOITE if noite else FUNDO_DIA))
    ship.draw(ctx, program, noite)

    for asteroid in arr_asteroid:
        asteroid.draw(ctx, program, noite)

initializate_glfw()
window = generate_window()

ctx = moderngl.create_context()
program = setup_shader_program(ctx)
setup_projection_matrix(program)

ship = create_ship(ctx,program)
arr_asteroid = create_arr_asteroid(ctx, program)
life_bar = LifeBar(ctx, program)

down_pressed = False

last_time = glfw.get_time()
while not glfw.window_should_close(window):
    last_time, dt = calculate_delta_time(last_time)

    glfw.poll_events()

    down = glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS
    if down and not down_pressed:
        noite = not noite

    down_pressed = down

    handle_input(window, dt)
    update(dt, ship, arr_asteroid)
    render(ctx, ship, arr_asteroid)
    life_bar.draw(ctx, program, noite)

    glfw.swap_buffers(window)

kill_game(window)
