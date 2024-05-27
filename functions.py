from tkinter import LAST
from math import pi, cos, sin, sqrt
from random import random
from data import *


def create_vertex(left, top, text, canvas):
    canvas.create_text(left, top, text=text+1, font=("Arial", vertex_size))
    canvas.create_oval(left - vertex_size, top - vertex_size, left + vertex_size, top + vertex_size,
                       fill="", outline="red")


def create_vertexes(left, top, size, count, canvas):
    vertexes = [{}] * count
    for i in range(count):
        angle = i * 2 * pi/count
        vertex_left = left + size * sin(angle)
        vertex_top = top - size * cos(angle)
        create_vertex(vertex_left, vertex_top, i, canvas)
        vertex = {
            "left": vertex_left,
            "top": vertex_top,
        }
        vertexes[i] = vertex
        i += 1
    return vertexes


def create_matrix_for_directed_graph(size, k):
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            number = int(random()*2*k)
            matrix[i].append(number)
    return matrix


def create_zero_matrix(size):
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(0)
    return matrix


def create_matrix_for_undirected_graph(matrix_for_directed_graph):
    length = len(matrix_for_directed_graph)
    matrix = create_zero_matrix(length)
    for i in range(length):
        for j in range(length):
            ij = matrix_for_directed_graph[i][j]
            ji = matrix_for_directed_graph[j][i]
            matrix[i][j] = ij if ij else ji
    return matrix


def draw_self_arrow(left, top, i, count_of_vertexes_in_this_graph, canvas):
    main_angle = i / count_of_vertexes_in_this_graph * 2 * pi
    lefter_angle = main_angle + extra_angle_in_self_arrow
    righter_angle = main_angle - extra_angle_in_self_arrow
    first_point_x = left+sin(lefter_angle)*2*vertex_size
    first_point_y = top-cos(lefter_angle)*2*vertex_size
    second_point_x = left+sin(righter_angle)*2*vertex_size
    second_point_y = top-cos(righter_angle)*2*vertex_size
    canvas.create_line(first_point_x, first_point_y, second_point_x, second_point_y)
    canvas.create_line(left + vertex_size*sin(lefter_angle), top - vertex_size*cos(lefter_angle),
                       first_point_x, first_point_y)
    canvas.create_line(second_point_x, second_point_y, left + vertex_size*sin(righter_angle),
                       top - vertex_size*cos(righter_angle), arrow=LAST)


def draw_line(left_i, top_i, left_j, top_j, sin_angle, cos_angle, canvas):
    left_from = left_i - vertex_size * cos_angle
    left_to = left_j + vertex_size * cos_angle
    top_from = top_i + vertex_size * sin_angle
    top_to = top_j - vertex_size * sin_angle
    canvas.create_line(left_from, top_from, left_to, top_to)


def draw_arrow(left_i, top_i, left_j, top_j, sin_angle, cos_angle, canvas):
    left_from = left_i - vertex_size * cos_angle + sin_angle * space_between_edges
    left_to = left_j + vertex_size * cos_angle + sin_angle * space_between_edges
    top_from = top_i + vertex_size * sin_angle + cos_angle * space_between_edges
    top_to = top_j - vertex_size * sin_angle + cos_angle * space_between_edges
    canvas.create_line(left_from, top_from, left_to, top_to, arrow=LAST)


def draw_edges(matrix, vertexes, directed, canvas):
    length = len(matrix)
    for i in range(length):
        for j in range(length if directed else i+1):
            if not matrix[i][j]:
                continue
            if i == j:
                left = vertexes[i]["left"]
                top = vertexes[i]["top"]
                draw_self_arrow(left, top, i, length, canvas)
                continue
            left_i = vertexes[i]["left"]
            left_j = vertexes[j]["left"]
            top_i = vertexes[i]["top"]
            top_j = vertexes[j]["top"]
            dx = left_i - left_j
            dy = top_i - top_j
            line_length = sqrt(dx * dx + dy * dy)
            cos_angle = dx/line_length
            sin_angle = -dy/line_length
            draw_arrow(left_i, top_i, left_j, top_j, sin_angle, cos_angle, canvas) if directed else (
                draw_line(left_i, top_i, left_j, top_j, sin_angle, cos_angle, canvas))


def draw_graph(left, top, size, matrix, directed, canvas):
    length = len(matrix)
    vertexes = create_vertexes(left, top, size, length, canvas)
    draw_edges(matrix, vertexes, directed, canvas)
    return vertexes


def vertexes_analyse(matrix, adder_function):
    length = len(matrix)
    degrees = [0] * length
    for i in range(length):
        for j in range(length):
            degrees[i] += adder_function(matrix, i, j)
    return degrees


def undirected_adder(matrix, i, j):
    if not matrix[i][j]:
        return 0
    if i == j:
        return 2
    return 1


def directed_all_adder(matrix, i, j):
    return matrix[i][j] + matrix[j][i]


def directed_entry_adder(matrix, i, j):
    return matrix[j][i]


def directed_output_adder(matrix, i, j):
    return matrix[i][j]


def get_undirected_degrees(matrix):
    return vertexes_analyse(matrix, undirected_adder)


def get_directed_all_degrees(matrix):
    return vertexes_analyse(matrix, directed_all_adder)


def get_directed_entry_degrees(matrix):
    return vertexes_analyse(matrix, directed_entry_adder)


def get_directed_output_degrees(matrix):
    return vertexes_analyse(matrix, directed_output_adder)


def regular_undirected(degrees):
    length = len(degrees)
    for i in range(length-1):
        if degrees[i] != degrees[length-1]:
            return False
    return degrees[length-1]


def regular_directed(degrees_entry, degrees_output):
    length = len(degrees_entry)
    for i in range(length-1):
        if degrees_entry[i] != degrees_entry[length-1]:
            return False
        if degrees_output[i] != degrees_output[length-1]:
            return False
    return degrees_output[length] + degrees_entry[length-1]


def get_isolated_vertices(matrix):
    length = len(matrix)
    list_of_isolated = []
    for i in range(length):
        is_isolated = True
        for j in range(length):
            if i == j:
                continue
            if matrix[i][j] or matrix[j][i]:
                is_isolated = False
                break
        if is_isolated:
            list_of_isolated.append(i)
    return list_of_isolated


def get_hanging_vertices(matrix):
    length = len(matrix)
    list_of_hanging = []
    for i in range(length):
        count_of_connections = 0
        for j in range(length):
            if i == j:
                continue
            if matrix[i][j] or matrix[j][i]:
                count_of_connections += 1
        if count_of_connections == 1:
            list_of_hanging.append(i)
    return list_of_hanging


def get_all_compositions(matrix):
    length = len(matrix)
    compositions = [matrix]
    for k in range(length):
        if k == 0:
            continue
        compositions.append(create_zero_matrix(length))
        for l in range(length):
            for i in range(length):
                for j in range(length):
                    compositions[k][i][j] = compositions[k][i][j] or\
                        (compositions[0][i][l] and compositions[k-1][l][j])
    return compositions


def find_paths_2(matrix_1):
    paths = []
    length = len(matrix_1)
    for i_1 in range(length):
        for i_2 in range(length):
            for i_3 in range(length):
                if matrix_1[i_1][i_2] and matrix_1[i_2][i_3]:
                    if i_1 == i_2 and i_2 == i_3:
                        continue
                    paths.append([i_1+1, i_2+1, i_3+1])
    return paths


def find_paths_3(matrix_1):
    paths = []
    length = len(matrix_1)
    for i_1 in range(length):
        for i_2 in range(length):
            for i_3 in range(length):
                for i_4 in range(length):
                    if matrix_1[i_1][i_2] and matrix_1[i_2][i_3] and matrix_1[i_3][i_4]:
                        if (i_1 == i_2 and i_2 == i_3) or (i_2 == i_3 and i_3 == i_4) or (i_1 == i_3 and i_2 == i_4):
                            continue
                        paths.append([i_1+1, i_2+1, i_3+1, i_4+1])
    return paths


def get_reachability_matrix(compositions):
    matrix_length = len(compositions[0])
    reachability_matrix = create_zero_matrix(matrix_length)
    for k in range(len(compositions)):
        for i in range(matrix_length):
            for j in range(matrix_length):
                if compositions[k][i][j]:
                    reachability_matrix[i][j] = 1
    for i in range(matrix_length):
        reachability_matrix[i][i] = 1
    return reachability_matrix


def get_matrix_of_strong_connectivity(reachability_matrix):
    length = len(reachability_matrix)
    new_matrix = create_zero_matrix(length)
    for i in range(length):
        for j in range(length):
            new_matrix[i][j] = 1 if (reachability_matrix[i][j] and reachability_matrix[j][i]) else 0
    return new_matrix


def get_components_of_strong_connectivity(matrix_of_strong_connectivity):
    components = []
    length = len(matrix_of_strong_connectivity)
    for row in range(length):
        same_component_number = False
        for k in range(len(components)):
            same_components = True
            component = components[k]["component"]
            for cell in range(len(component)):
                if component[cell] != matrix_of_strong_connectivity[row][cell]:
                    same_components = False
                    break

            if same_components:
                same_component_number = k
                break
        if type(same_component_number) is not bool:
            components[same_component_number]["rows"].append(row)
        else:
            components.append({
                "component": matrix_of_strong_connectivity[row],
                "rows": [row],
            })

    result = []
    for component in components:
        result.append(component["rows"])
    return result


def create_condensation_matrix(components, matrix):
    components_length = len(components)
    new_matrix = create_zero_matrix(components_length)
    for first_component in range(components_length):
        for second_component in range(components_length):
            if first_component == second_component:
                continue
            for first_vertex in components[first_component]:
                for second_vertex in components[second_component]:
                    if matrix[first_vertex][second_vertex]:
                        new_matrix[first_component][second_component] = 1
                        break
    return new_matrix
