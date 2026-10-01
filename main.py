from pathlib import Path

import glfw
import moderngl
import numpy as np
import glm
from objects.ship import Ship

if not glfw.init():
    raise RuntimeError("Falha GLFW.")

window = glfw.create_window(800, 600, "Asteroids", None, None)
glfw.make_context_current(window)

ctx = moderngl.create_context()
shader_dir = Path(__file__).parent / "shaders"
program = ctx.program(vertex_shader=(shader_dir/"basic.vert").read_text(),
                      fragment_shader=(shader_dir/"basic.frag").read_text())

projection = glm.ortho(-10.0, 10.0, -7.5, 7.5, -1.0, 1.0)
program["projection"].write(np.array(projection.to_list(), dtype="f4").tobytes())

ship_vertices = np.array([0.8, 0.0, -0.4, 0.4, -0.2, 0.0, -0.4, -0.4], dtype="f4")
vao = ctx.simple_vertex_array(program, ctx.buffer(ship_vertices.tobytes()), "in_pos")

dt = 1.0 / 60.0
ship = Ship()

while not glfw.window_should_close(window):
    glfw.poll_events()
   
    ship.handleInput(window, dt)
    ship.update(dt)

    model = glm.translate(glm.mat4(1.0), glm.vec3(ship.position.x, ship.position.y, 0.0))
    model = glm.rotate(model, ship.angle, glm.vec3(0.0, 0.0, 1.0))
    program["model"].write(np.array(model.to_list(), dtype="f4").tobytes())

    ctx.clear(0.02, 0.02, 0.05)
    vao.render(moderngl.LINE_LOOP)
    glfw.swap_buffers(window)

glfw.destroy_window(window)
glfw.terminate()