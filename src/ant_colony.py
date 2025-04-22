import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import pandas as pd
import random
import time
import math

# Глобальные переменные для хранения вершин и рёбер
vertices = {}
edges = []
current_edge = None
graph_type = "undirected"

DEFAULT_PHEROMONE = 0.1
DEFAULT_PHEROMONE_WEIGHT = 1.0
DEFAULT_LENGTH_WEIGHT = 2.0
DEFAULT_EVAPORATION = 0.5
DEFAULT_ITERATIONS = 100
DEFAULT_ANTS = 10
DEFAULT_Q = 100

def nearest_neighbor_tsp(graph, start_vertex):
    adjacency_list = {}
    for _, row in graph.iterrows():
        v1, v2, length = row['вершина 1'], row['вершина 2'], float(row['длина'])
        if v1 not in adjacency_list:
            adjacency_list[v1] = {}
        if v2 not in adjacency_list:
            adjacency_list[v2] = {}
        adjacency_list[v1][v2] = length
        if graph_type == "undirected":
            adjacency_list[v2][v1] = length

    visited = set()
    path = [start_vertex]
    visited.add(start_vertex)
    total_distance = 0

    current_vertex = start_vertex

    while len(visited) < len(adjacency_list):
        nearest_vertex = None
        nearest_distance = float('inf')

        for neighbor, distance in adjacency_list[current_vertex].items():
            if neighbor not in visited and distance < nearest_distance:
                nearest_vertex = neighbor
                nearest_distance = distance

        if nearest_vertex is None:
            break

        path.append(nearest_vertex)
        visited.add(nearest_vertex)
        total_distance += nearest_distance
        current_vertex = nearest_vertex

    if len(path) == len(adjacency_list) and start_vertex in adjacency_list[current_vertex]:
        path.append(start_vertex)
        total_distance += adjacency_list[current_vertex][start_vertex]
        return path, total_distance
    else:
        return None, None

def ant_colony_tsp(graph, start_vertex=None, use_templates=False):
    try:
        alpha = float(entry_pheromone.get() or DEFAULT_PHEROMONE_WEIGHT)
        beta = float(entry_length.get() or DEFAULT_LENGTH_WEIGHT)
        evaporation = float(entry_evaporation.get() or DEFAULT_EVAPORATION)
        iterations = int(entry_iterations.get() or DEFAULT_ITERATIONS)
        ants_count = int(entry_ants.get() or DEFAULT_ANTS)
        Q = float(entry_q.get() or DEFAULT_Q)
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректные параметры алгоритма")
        return None, None

    adjacency_list = {}
    vertices = set()
    pheromone = {}
    
    for _, row in graph.iterrows():
        v1, v2, length = row['вершина 1'], row['вершина 2'], float(row['длина'])
        initial_pheromone = float(row['феромон']) if 'феромон' in row and row['феромон'] else DEFAULT_PHEROMONE
        vertices.add(v1)
        vertices.add(v2)
        
        if v1 not in adjacency_list:
            adjacency_list[v1] = {}
        if v2 not in adjacency_list:
            adjacency_list[v2] = {}
            
        adjacency_list[v1][v2] = length
        pheromone[(v1, v2)] = initial_pheromone
        
        if graph_type == "undirected":
            adjacency_list[v2][v1] = length
            pheromone[(v2, v1)] = initial_pheromone
    
    vertices = list(vertices)
    best_path = None
    best_length = float('inf')
    
    templates = []
    if use_templates:
        # Создаем несколько шаблонных путей
        for v in vertices[:min(5, len(vertices))]:
            path, length = nearest_neighbor_tsp(graph, v)
            if path and length:
                templates.append((path, length))
    
    for iteration in range(iterations):
        ants_paths = []
        
        for ant in range(ants_count):
            if start_vertex and start_vertex in vertices:
                current_vertex = start_vertex
            else:
                current_vertex = random.choice(vertices)
                
            path = [current_vertex]
            visited = set([current_vertex])
            path_length = 0
            
            while len(visited) < len(vertices):
                possible_transitions = []
                total = 0.0
                
                for neighbor in adjacency_list[current_vertex]:
                    if neighbor not in visited:
                        tau = pheromone.get((current_vertex, neighbor), DEFAULT_PHEROMONE) ** alpha
                        eta = (1.0 / adjacency_list[current_vertex][neighbor]) ** beta
                        weight = tau * eta
                        possible_transitions.append((neighbor, weight))
                        total += weight
                
                if not possible_transitions:
                    break  # нет возможных переходов
                
                if total > 0:
                    probabilities = [(neighbor, weight/total) for neighbor, weight in possible_transitions]
                    probabilities.sort(key=lambda x: -x[1])
                    
                    r = random.random()
                    cumulative = 0.0
                    for neighbor, prob in probabilities:
                        cumulative += prob
                        if r <= cumulative:
                            next_vertex = neighbor
                            break
                    else:
                        next_vertex = probabilities[-1][0]
                else:
                    next_vertex = random.choice([t[0] for t in possible_transitions])
                
                path.append(next_vertex)
                visited.add(next_vertex)
                path_length += adjacency_list[current_vertex][next_vertex]
                current_vertex = next_vertex
            
            if len(path) == len(vertices) and path[0] in adjacency_list[path[-1]]:
                path.append(path[0])
                path_length += adjacency_list[path[-2]][path[-1]]
                ants_paths.append((path, path_length))
                
                if path_length < best_length:
                    best_length = path_length
                    best_path = path.copy()
        
        # Добавляем шаблонные пути (если используется модификация)
        if use_templates and templates:
            ants_paths.extend(templates)
        
        for edge in pheromone:
            pheromone[edge] *= (1.0 - evaporation)
        
        for path, path_length in ants_paths:
            delta_pheromone = Q / path_length
            
            for i in range(len(path)-1):
                edge = (path[i], path[i+1])
                if edge in pheromone:
                    pheromone[edge] += delta_pheromone
        
        if iteration % 10 == 0:
            print(f"Iteration {iteration}: best length = {best_length}")
    
    return best_path, best_length

def add_edge_to_table(v1, v2, length, pheromone=DEFAULT_PHEROMONE):
    tree.insert("", "end", values=(v1, v2, length, pheromone))

def on_click(event):
    global current_edge

    for vertex, (x, y) in vertices.items():
        if abs(event.x - x) < 10 and abs(event.y - y) < 10:  # 10 пикселей
            if current_edge is None:
                current_edge = vertex
            else:
                # Запрашиваем длину ребра
                length = simpledialog.askfloat("Длина ребра", f"Введите длину ребра между {current_edge} и {vertex}:")
                if length is None:
                    return

                # Запрашиваем начальный феромон
                pheromone = simpledialog.askfloat("Феромон ребра", 
                                                 f"Введите начальный феромон для ребра между {current_edge} и {vertex} (по умолчанию {DEFAULT_PHEROMONE}):",
                                                 initialvalue=DEFAULT_PHEROMONE)
                if pheromone is None:
                    pheromone = DEFAULT_PHEROMONE
                
                edges.append((current_edge, vertex, length, pheromone))
                add_edge_to_table(current_edge, vertex, length, pheromone)
                current_edge = None
                draw_input_graph()
            break
    else:
        vertex = f"V{len(vertices) + 1}"
        vertices[vertex] = (event.x, event.y)
        draw_input_graph()

def draw_input_graph():
    input_canvas.delete("all")

    for edge in edges:
        if len(edge) == 3:
            v1, v2, length = edge
            pheromone = DEFAULT_PHEROMONE
        else:
            v1, v2, length, pheromone = edge
            
        x1, y1 = vertices[v1]
        x2, y2 = vertices[v2]
        input_canvas.create_line(x1, y1, x2, y2, width=2, fill="black")
        input_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{length:.2f}", fill="red")
        input_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2 + 15, text=f"φ={pheromone:.2f}", fill="blue")

    for vertex, (x, y) in vertices.items():
        input_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
        input_canvas.create_text(x, y, text=vertex, fill="black")

def draw_output_graph(path):
    output_canvas.delete("all")

    for i in range(len(path) - 1):
        v1, v2 = path[i], path[i + 1]
        x1, y1 = vertices[v1]
        x2, y2 = vertices[v2]
        output_canvas.create_line(x1, y1, x2, y2, width=2, fill="green")

    for vertex, (x, y) in vertices.items():
        output_canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")
        output_canvas.create_text(x, y, text=vertex, fill="black")

def solve_tsp():
    edges_table = []
    for item in tree.get_children():
        edge = tree.item(item, "values")
        edges_table.append(edge)

    if not edges_table:
        messagebox.showwarning("Ошибка", "Добавьте хотя бы одно ребро!")
        return

    graph = pd.DataFrame(edges_table, columns=["вершина 1", "вершина 2", "длина", "феромон"])

    start_vertex = entry_start.get().strip()
    if not start_vertex:
        messagebox.showwarning("Ошибка", "Введите стартовую вершину!")
        return

    all_vertices = set(graph['вершина 1']).union(set(graph['вершина 2']))
    if start_vertex not in all_vertices:
        messagebox.showwarning("Ошибка", f"Стартовая вершина '{start_vertex}' не найдена в графе!")
        return

    start_time = time.time()
    path, total_distance = ant_colony_tsp(graph, start_vertex)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения муравьиного алгоритма: {execution_time:.4f} секунд")

    if path is None:
        messagebox.showwarning("Результат", "Гамильтонов цикл не найден")
        result_path.config(text="")
        result_distance.config(text="")
        draw_output_graph([])
    else:
        result_path.config(text=f"{' -> '.join(path)}")
        result_distance.config(text=f"{total_distance:.2f}")
        draw_output_graph(path)

def solve_tsp_with_templates():
    edges_table = []
    for item in tree.get_children():
        edge = tree.item(item, "values")
        edges_table.append(edge)

    if not edges_table:
        messagebox.showwarning("Ошибка", "Добавьте хотя бы одно ребро!")
        return

    graph = pd.DataFrame(edges_table, columns=["вершина 1", "вершина 2", "длина", "феромон"])

    start_vertex = entry_start.get().strip()
    if not start_vertex:
        messagebox.showwarning("Ошибка", "Введите стартовую вершину!")
        return

    all_vertices = set(graph['вершина 1']).union(set(graph['вершина 2']))
    if start_vertex not in all_vertices:
        messagebox.showwarning("Ошибка", f"Стартовая вершина '{start_vertex}' не найдена в графе!")
        return

    start_time = time.time()
    path, total_distance = ant_colony_tsp(graph, start_vertex, use_templates=True)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения муравьиного алгоритма с шаблонами: {execution_time:.4f} секунд")

    if path is None:
        messagebox.showwarning("Результат", "Гамильтонов цикл не найден")
        result_path.config(text="")
        result_distance.config(text="")
        draw_output_graph([])
    else:
        result_path.config(text=f"{' -> '.join(path)}")
        result_distance.config(text=f"{total_distance:.2f}")
        draw_output_graph(path)

def clear_canvas():
    global vertices, edges, current_edge
    vertices = {}
    edges = []
    current_edge = None
    input_canvas.delete("all")
    output_canvas.delete("all")
    tree.delete(*tree.get_children())
    result_path.config(text="")
    result_distance.config(text="")
    draw_input_graph()
    draw_output_graph([])

def set_graph_type(type):
    global graph_type
    graph_type = type
    messagebox.showinfo("Тип графа", f"Тип графа изменён на {'неориентированный' if type == 'undirected' else 'ориентированный'}")

def load_graph_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        df = pd.read_csv(file_path)
        required_columns = ["вершина 1", "вершина 2", "длина"]
        if not all(col in df.columns for col in required_columns):
            messagebox.showerror("Ошибка", f"Файл должен содержать колонки: {', '.join(required_columns)}")
            return

        clear_canvas()
        for _, row in df.iterrows():
            v1, v2, length = row['вершина 1'], row['вершина 2'], float(row['длина'])
            pheromone = float(row['феромон']) if 'феромон' in row and pd.notna(row['феромон']) else DEFAULT_PHEROMONE
            
            if v1 not in vertices:
                vertices[v1] = (random.randint(50, 550), random.randint(50, 250))
            if v2 not in vertices:
                vertices[v2] = (random.randint(50, 550), random.randint(50, 250))
            edges.append((v1, v2, length, pheromone))
            add_edge_to_table(v1, v2, length, pheromone)

        draw_input_graph()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

root = tk.Tk()
root.title("Задача коммивояжера (Муравьиный алгоритм)")

# Левый фрейм для параметров и кнопок
left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

label_parameters = ttk.Label(left_frame, text="Параметры алгоритма", font=("Arial", 12))
label_parameters.pack(pady=5)

label_pheromone = ttk.Label(left_frame, text="Вес феромона (α):")
label_pheromone.pack(pady=2)
entry_pheromone = ttk.Entry(left_frame)
entry_pheromone.insert(0, str(DEFAULT_PHEROMONE_WEIGHT))
entry_pheromone.pack(pady=2)

label_length = ttk.Label(left_frame, text="Вес длины (β):")
label_length.pack(pady=2)
entry_length = ttk.Entry(left_frame)
entry_length.insert(0, str(DEFAULT_LENGTH_WEIGHT))
entry_length.pack(pady=2)

label_evaporation = ttk.Label(left_frame, text="Испарение феромона:")
label_evaporation.pack(pady=2)
entry_evaporation = ttk.Entry(left_frame)
entry_evaporation.insert(0, str(DEFAULT_EVAPORATION))
entry_evaporation.pack(pady=2)

label_iterations = ttk.Label(left_frame, text="Кол-во итераций:")
label_iterations.pack(pady=2)
entry_iterations = ttk.Entry(left_frame)
entry_iterations.insert(0, str(DEFAULT_ITERATIONS))
entry_iterations.pack(pady=2)

label_ants = ttk.Label(left_frame, text="Кол-во муравьев:")
label_ants.pack(pady=2)
entry_ants = ttk.Entry(left_frame)
entry_ants.insert(0, str(DEFAULT_ANTS))
entry_ants.pack(pady=2)

label_q = ttk.Label(left_frame, text="Количество феромона (Q):")
label_q.pack(pady=2)
entry_q = ttk.Entry(left_frame)
entry_q.insert(0, str(DEFAULT_Q))
entry_q.pack(pady=2)

separator_count = ttk.Separator(left_frame, orient=tk.HORIZONTAL)
separator_count.pack(fill=tk.X, pady=10)

button_solve = ttk.Button(left_frame, text="Муравьиный алгоритм", command=solve_tsp)
button_solve.pack(fill=tk.BOTH, pady=5)

button_solve_templates = ttk.Button(left_frame, text="С шаблонами", command=solve_tsp_with_templates)
button_solve_templates.pack(fill=tk.BOTH, pady=5)

label_start = ttk.Label(left_frame, text="Стартовая вершина:")
label_start.pack(pady=5)
entry_start = ttk.Entry(left_frame)
entry_start.pack()

button_load = ttk.Button(left_frame, text="Загрузить граф из файла", command=load_graph_from_file)
button_load.pack(fill=tk.BOTH, pady=5)

separator_left = ttk.Separator(root, orient=tk.VERTICAL)
separator_left.pack(side=tk.LEFT, fill=tk.Y, padx=5)

# Центральный фрейм для холстов
center_frame = ttk.Frame(root)
center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

label_input_graph = ttk.Label(center_frame, text="Входной граф", font=("Arial", 12))
label_input_graph.pack(pady=5)

graph_type_frame = ttk.Frame(center_frame)
graph_type_frame.pack(pady=5)

graph_type_var = tk.StringVar(value="undirected")
radio_undirected = ttk.Radiobutton(graph_type_frame, text="Неориентированный", variable=graph_type_var, value="undirected", command=lambda: set_graph_type("undirected"))
radio_undirected.pack(side=tk.LEFT, padx=5)
radio_directed = ttk.Radiobutton(graph_type_frame, text="Ориентированный", variable=graph_type_var, value="directed", command=lambda: set_graph_type("directed"))
radio_directed.pack(side=tk.LEFT, padx=5)

input_canvas = tk.Canvas(center_frame, width=600, height=300, bg="white")
input_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

label_output_graph = ttk.Label(center_frame, text="Выходной граф", font=("Arial", 12))
label_output_graph.pack(pady=2)

output_canvas = tk.Canvas(center_frame, width=600, height=300, bg="white")
output_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

control_frame = ttk.Frame(center_frame)
control_frame.pack(fill=tk.X, padx=10, pady=10)

button_clear = ttk.Button(control_frame, text="Очистить", command=clear_canvas)
button_clear.pack(fill=tk.BOTH, padx=5)

input_canvas.bind("<Button-1>", on_click)

separator_right = ttk.Separator(root, orient=tk.VERTICAL)
separator_right.pack(side=tk.LEFT, fill=tk.Y, padx=5)

# Правый фрейм для таблицы и результатов
right_frame = ttk.Frame(root, width=300)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

label_edges = ttk.Label(right_frame, text="Ребра", font=("Arial", 12))
label_edges.pack(pady=5)

style = ttk.Style()
style.layout("my.Treeview", [
    ("Treeview.field", {"sticky": "nswe", "border": "1", "children": [
        ("Treeview.padding", {"sticky": "nswe", "children": [
            ("Treeview.treearea", {"sticky": "nswe"})
        ]})
    ]})
])
style.configure("my.Treeview", font=("Arial", 10), rowheight=25, borderwidth=1, relief="solid")
style.configure("my.Treeview.Heading", font=("Arial", 10, "bold"), background="gray")
style.map("my.Treeview", background=[("selected", "#347083")])

tree = ttk.Treeview(right_frame, columns=("вершина 1", "вершина 2", "длина", "феромон"), show="headings", style="my.Treeview")
tree.heading("вершина 1", text="Вершина 1")
tree.heading("вершина 2", text="Вершина 2")
tree.heading("длина", text="Длина")
tree.heading("феромон", text="Феромон")
tree.column("вершина 1", width=110, anchor="center")
tree.column("вершина 2", width=110, anchor="center")
tree.column("длина", width=110, anchor="center")
tree.column("феромон", width=110, anchor="center")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

separator_results_top = ttk.Separator(right_frame, orient=tk.HORIZONTAL)
separator_results_top.pack(fill=tk.X, pady=10)

result_frame = ttk.Frame(right_frame)
result_frame.pack(fill=tk.BOTH, padx=10, pady=10)

label_path = ttk.Label(result_frame, text="Полученный путь:", font=("Arial", 12))
label_path.grid(row=0, column=0, padx=5, pady=5, sticky="w")
result_path = ttk.Label(result_frame, text="", font=("Arial", 12), wraplength=400)
result_path.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_distance = ttk.Label(result_frame, text="Длина пути:", font=("Arial", 12))
label_distance.grid(row=1, column=0, padx=5, pady=5, sticky="w")
result_distance = ttk.Label(result_frame, text="", font=("Arial", 12))
result_distance.grid(row=1, column=1, padx=5, pady=5, sticky="w")

separator_results_bottom = ttk.Separator(right_frame, orient=tk.HORIZONTAL)
separator_results_bottom.pack(fill=tk.X, pady=10)

root.mainloop()