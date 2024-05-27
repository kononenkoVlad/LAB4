from tkinter import Tk, Canvas
from functions import *
from random import seed

window = Tk()
window.geometry(f'{window_width}x{window_height}')
window.title("Graphs")
window.resizable(False, False)

canvas = Canvas(width=window_width, height=window_height)
canvas.pack()

seed(seed_value)

print("матриця напрямленого графа:")
directed_matrix1 = create_matrix_for_directed_graph(count_of_vertexes, k_1)
for row in directed_matrix1:
    print(row)

print("\nматриця ненапрямленого графа:")
undirected_matrix = create_matrix_for_undirected_graph(directed_matrix1)
for row in undirected_matrix:
    print(row)
print()


def write_degrees(text, degrees):
    print(text)
    for i in range(len(degrees)):
        print(i+1, degrees[i])
    print()


undirected_degrees = get_undirected_degrees(undirected_matrix)
directed_all_degrees = get_directed_all_degrees(directed_matrix1)
directed_entry_degrees = get_directed_entry_degrees(directed_matrix1)
directed_output_degrees = get_directed_output_degrees(directed_matrix1)

write_degrees("степені ненапрямленого графа:", undirected_degrees)
write_degrees("степені напрямленого графа", directed_all_degrees)
write_degrees("напівстепені входу напрямленого графа", directed_entry_degrees)
write_degrees("напівстепені виходу напрямленого графа", directed_output_degrees)

is_regular_undirected = regular_undirected(undirected_degrees)
is_regular_directed = regular_directed(directed_entry_degrees, directed_output_degrees)

if type(is_regular_undirected) is bool:
    print("Ненапрямлений граф не є регулярним")
else:
    print("Ненапрямлений граф є одноріджним. Степінь однорідності: ", is_regular_undirected)

if type(is_regular_directed) is bool:
    print("Напрямлений граф не є регулярним")
else:
    print("Напрямлений граф є одноріджним. Степінь однорідності: ", is_regular_directed)
print()

list_of_isolated_vertices = get_isolated_vertices(directed_matrix1)
list_of_hanging_vertices = get_hanging_vertices(directed_matrix1)


def increment_array(array):
    length = len(array)
    new_array = [0]*length
    for i in range(length):
        new_array[i] = array[i]+1
    return new_array

if not len(list_of_isolated_vertices):
    print("Граф не має ізольованих вершин")
else:
    print("Список ізольованих вершин: ", list_of_isolated_vertices)

if not len(list_of_hanging_vertices):
    print("Граф не має фисячих вершин")
else:
    print("Список висячих вершин: ", list_of_hanging_vertices)

directed_matrix_2 = create_matrix_for_directed_graph(count_of_vertexes, k_2)
print("\nНова матриця напрямленого графа")
for row in directed_matrix_2:
    print(row)

directed_output_degrees_2 = get_directed_output_degrees(directed_matrix_2)
directed_entry_degrees_2 = get_directed_entry_degrees(directed_matrix_2)

write_degrees("\nнапівстепені входу нового напрямленого графа", directed_entry_degrees_2)
write_degrees("напівстепені виходу нового напрямленого графа", directed_output_degrees_2)

paths_2 = find_paths_2(directed_matrix_2)
paths_3 = find_paths_3(directed_matrix_2)
print("Всі шляхи довжиною 2")
for path in paths_2:
    print(path)
print("\nВсі шляхи довжиною 3")
for path in paths_3:
    print(path)

compositions = get_all_compositions(directed_matrix_2)
reachability_matrix = get_reachability_matrix(compositions)
print("\nматриця досяжності")
for row in reachability_matrix:
    print(row)

matrix_of_strong_connectivity = get_matrix_of_strong_connectivity(reachability_matrix)
components_of_strong_connectivity = get_components_of_strong_connectivity(matrix_of_strong_connectivity)
print("\nМатриця сильної зв'язності")
for row in matrix_of_strong_connectivity:
    print(row)
print("\nКомпоненти сильної зв'язнрості")
for row in components_of_strong_connectivity:
    print(increment_array(row))

condensation_matrix = create_condensation_matrix(components_of_strong_connectivity, directed_matrix_2)
print("\nМатриця конденсації")
for row in condensation_matrix:
    print(row)

canvas.create_text(300, 20, text="напрямлений граф", font=("Arial", 20))
canvas.create_text(800, 20, text="ненапрямлений граф", font=("Arial", 20))
draw_graph(300, 250, graph_size, directed_matrix1, True, canvas)
draw_graph(800, 250, graph_size, undirected_matrix, False, canvas)
canvas.create_text(300, 520, text="Другий напрямлений граф", font=("Arial", 20))
canvas.create_text(800, 520, text="Граф конденсації другого графа", font=("Arial", 20))
draw_graph(300, 750, graph_size, directed_matrix_2, True, canvas)
draw_graph(800, 750, graph_size, condensation_matrix, True, canvas)

window.mainloop()
