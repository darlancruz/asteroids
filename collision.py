import glm

def get_axes(vertices):
    axes = []

    for i in range(len(vertices)):
        current = vertices[i]
        next_vertex = vertices[(i + 1) % len(vertices)]

        edge = next_vertex - current

        axis = glm.vec2(-edge.y, edge.x)

        if(glm.length(axis) > 0):
            axis = glm.normalize(axis)
            axes.append(axis)

    return axes

def project_polygon(vertices, axis):
    projections = [glm.dot(vertex, axis) for vertex in vertices]

    return min(projections), max(projections)

def check_collision(vertices_a, vertices_b):
    axes = get_axes(vertices_a) + get_axes(vertices_b)

    for axis in axes:
        min_a, max_a = project_polygon(vertices_a, axis)
        min_b, max_b = project_polygon(vertices_b, axis)

        if max_a < min_b or max_b < min_a:
            return False
        
    return True

def triangulate_fan(vertices):
    triangles = []
    for i in range(1, len(vertices) - 1):
        triangle = [vertices[0], vertices[i], vertices[i + 1]]
        triangles.append(triangle)

    return triangles

def get_asteroid_triangles(asteroid):
    vertices = asteroid.get_world_vertices()
    center = glm.vec2(asteroid.position.x, asteroid.position.y)
    triangles = []

    for i in range(len(vertices)):
        next_i = (i + 1) % len(vertices)
        triangles.append([center, vertices[i], vertices[next_i]])

    return triangles


def get_ship_triangles(ship):
    vertices = ship.get_world_vertices()

    return triangulate_fan(vertices)


def check_ship_asteroid_collision(ship, asteroid):
    ship_triangles = get_ship_triangles(ship)
    asteroid_triangles = get_asteroid_triangles(asteroid)

    for ship_triangle in ship_triangles:
        for asteroid_triangle in asteroid_triangles:
            if check_collision(ship_triangle, asteroid_triangle):
                return True

    return False
