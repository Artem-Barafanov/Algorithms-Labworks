import math
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import pandas as pd
import time
import numpy as np

# Глобальные переменные для хранения вершин и рёбер
vertices = {}
edges = []
current_edge = None
graph_type = "undirected"

def randomized_tsp(graph, start_vertex, randomness=0.5):
    """Рандомизированный алгоритм для нахождения начального решения"""
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
        neighbors = [neighbor for neighbor in adjacency_list[current_vertex].items() if neighbor[0] not in visited]
        
        if not neighbors:
            break

        # С вероятностью randomness выбираем случайного соседа
        if random.random() < randomness:
            nearest_vertex, nearest_distance = random.choice(neighbors)
        else:
            nearest_vertex, nearest_distance = min(neighbors, key=lambda x: x[1])

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

def simulated_annealing_tsp(graph, initial_path, initial_distance, 
                           initial_temp=1000, cooling_rate=0.99, 
                           min_temp=1, iterations_per_temp=100):
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

    if initial_path[0] != initial_path[-1]:
        raise ValueError("Начальный путь должен быть циклом (первая и последняя вершины совпадают)")

    current_path = initial_path.copy()
    current_distance = initial_distance
    best_path = current_path.copy()
    best_distance = current_distance
    
    temp = initial_temp
    
    while temp > min_temp:
        for _ in range(iterations_per_temp):
            new_path = current_path.copy()
            intermediate_vertices = new_path[1:-1]  # Вершины между началом и концом
            
            if len(intermediate_vertices) >= 2:
                operator = random.choice([1, 2, 3])
                
                if operator == 1:  # переворот отрезка
                    i, j = sorted(random.sample(range(1, len(new_path) - 1), 2))
                    new_path[i:j+1] = reversed(new_path[i:j+1])
                
                elif operator == 2:  # Перестановка двух вершин
                    i, j = random.sample(range(1, len(new_path) - 1), 2)
                    new_path[i], new_path[j] = new_path[j], new_path[i]
                
                else:  # Перемещение вершины
                    i = random.randint(1, len(new_path) - 2)
                    j = random.randint(1, len(new_path) - 2)
                    if i != j:
                        vertex = new_path.pop(i)
                        new_path.insert(j, vertex)
            
            if new_path[0] != new_path[-1]:
                new_path[-1] = new_path[0]
            
            new_distance = 0
            valid = True
            for k in range(len(new_path) - 1):
                v1, v2 = new_path[k], new_path[k+1]
                if v2 in adjacency_list[v1]:
                    new_distance += adjacency_list[v1][v2]
                else:
                    valid = False
                    break
            
            if not valid:
                continue
            
            if new_distance < current_distance:
                current_path = new_path
                current_distance = new_distance
                if new_distance < best_distance:
                    best_path = new_path.copy()
                    best_distance = new_distance
            else:
                delta = new_distance - current_distance
                probability = math.exp(-delta / temp)
                if random.random() < probability:
                    current_path = new_path
                    current_distance = new_distance
        
        temp *= cooling_rate
    
    return best_path, best_distance

def very_fast_simulated_annealing_tsp(graph, initial_path, initial_distance, 
                                     initial_temp=1000, min_temp=1, 
                                     iterations_per_temp=100, cooling_factor=1.0):
    """Модификация метода отжига со сверхбыстрым охлаждением (VFSA)"""
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

    if initial_path[0] != initial_path[-1]:
        raise ValueError("Начальный путь должен быть циклом (первая и последняя вершины совпадают)")

    current_path = initial_path.copy()
    current_distance = initial_distance
    best_path = current_path.copy()
    best_distance = current_distance
    
    temp = initial_temp
    iteration = 0
    
    while temp > min_temp:
        for _ in range(iterations_per_temp):
            iteration += 1
            new_path = current_path.copy()
            
            intermediate_vertices = new_path[1:-1]
            
            if len(intermediate_vertices) >= 2:
                operator = random.choice([1, 2, 3])
                
                if operator == 1:
                    i, j = sorted(random.sample(range(1, len(new_path) - 1), 2))
                    new_path[i:j+1] = reversed(new_path[i:j+1])
                elif operator == 2:
                    i, j = random.sample(range(1, len(new_path) - 1), 2)
                    new_path[i], new_path[j] = new_path[j], new_path[i]
                else:
                    i = random.randint(1, len(new_path) - 2)
                    j = random.randint(1, len(new_path) - 2)
                    if i != j:
                        vertex = new_path.pop(i)
                        new_path.insert(j, vertex)
            
            if new_path[0] != new_path[-1]:
                new_path[-1] = new_path[0]
            
            new_distance = 0
            valid = True
            for k in range(len(new_path) - 1):
                v1, v2 = new_path[k], new_path[k+1]
                if v2 in adjacency_list.get(v1, {}):
                    new_distance += adjacency_list[v1][v2]
                else:
                    valid = False
                    break
            
            if not valid:
                continue
            
            if new_distance < current_distance:
                current_path = new_path
                current_distance = new_distance
                if new_distance < best_distance:
                    best_path = new_path.copy()
                    best_distance = new_distance
            else:
                delta = new_distance - current_distance
                probability = math.exp(-delta / temp)
                if random.random() < probability:
                    current_path = new_path
                    current_distance = new_distance
        
        # Сверхбыстрое охлаждение (VFSA)
        temp = initial_temp / (1 + cooling_factor * iteration)
    
    return best_path, best_distance

def add_edge_to_table(v1, v2, length):
    tree.insert("", "end", values=(v1, v2, length, ""))

def on_click(event):
    global current_edge

    for vertex, (x, y) in vertices.items():
        if abs(event.x - x) < 10 and abs(event.y - y) < 10:
            if current_edge is None:
                current_edge = vertex
            else:
                length = simpledialog.askfloat("Длина ребра", f"Введите длину ребра между {current_edge} и {vertex}:")
                if length is not None:
                    edges.append((current_edge, vertex, length))
                    add_edge_to_table(current_edge, vertex, length)
                    current_edge = None
                    draw_input_graph()
            break
    else:
        vertex = f"V{len(vertices) + 1}"
        vertices[vertex] = (event.x, event.y)
        draw_input_graph()

def draw_input_graph():
    input_canvas.delete("all")

    for v1, v2, length in edges:
        x1, y1 = vertices[v1]
        x2, y2 = vertices[v2]
        input_canvas.create_line(x1, y1, x2, y2, width=2, fill="black")
        input_canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{length:.2f}", fill="red")

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

def solve_with_annealing():
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

    try:
        initial_temp = float(entry_initial_temp.get())
        cooling_rate = float(entry_cooling_rate.get())
        min_temp = float(entry_min_temp.get())
        iterations = int(entry_iterations.get())
        max_attempts = int(entry_max_attempts.get())
    except ValueError:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите корректные числовые параметры!")
        return

    # max_attempts попыток
    best_path = None
    best_distance = float('inf')
    execution_time = 0
    
    for attempt in range(1, max_attempts + 1):
        # Находим начальное решение рандомизированным алгоритмом
        start_time = time.time()
        initial_path, initial_distance = randomized_tsp(graph, start_vertex, randomness=0.5)
        end_time = time.time()
        execution_time += end_time - start_time
        
        if initial_path is None:
            continue
            
        start_time = time.time()
        path, distance = simulated_annealing_tsp(
            graph, initial_path, initial_distance,
            initial_temp=initial_temp,
            cooling_rate=cooling_rate,
            min_temp=min_temp,
            iterations_per_temp=iterations
        )
        end_time = time.time()
        execution_time += end_time - start_time
        
        if distance < best_distance:
            best_path = path
            best_distance = distance
        
        if best_path is not None:
            break

    print(f"Время выполнения: {execution_time:.4f} секунд")
    print(f"Попыток: {attempt}")

    if best_path is None:
        messagebox.showwarning("Результат", "Гамильтонов цикл не найден после всех попыток")
        result_path.config(text="")
        result_distance.config(text="")
        draw_output_graph([])
    else:
        result_path.config(text=f"{' -> '.join(best_path)}")
        result_distance.config(text=f"{best_distance:.2f}")
        draw_output_graph(best_path)

def solve_with_very_fast_annealing():
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

    try:
        initial_temp = float(entry_initial_temp.get())
        min_temp = float(entry_min_temp.get())
        iterations = int(entry_iterations.get())
        max_attempts = int(entry_max_attempts.get())
        cooling_factor = float(entry_cooling_factor.get())
    except ValueError:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите корректные числовые параметры!")
        return

    # max_attempts попыток
    best_path = None
    best_distance = float('inf')
    execution_time = 0
    
    for attempt in range(1, max_attempts + 1):
        start_time = time.time()
        initial_path, initial_distance = randomized_tsp(graph, start_vertex, randomness=0.5)
        end_time = time.time()
        execution_time += end_time - start_time
        
        if initial_path is None:
            continue
            
        start_time = time.time()
        path, distance = very_fast_simulated_annealing_tsp(
            graph, initial_path, initial_distance,
            initial_temp=initial_temp,
            min_temp=min_temp,
            iterations_per_temp=iterations,
            cooling_factor=cooling_factor
        )
        end_time = time.time()
        execution_time += end_time - start_time
        
        if distance < best_distance:
            best_path = path
            best_distance = distance
        
        if best_path is not None:
            break

    print(f"Время выполнения (сверхбыстрый отжиг): {execution_time:.4f} секунд")
    print(f"Попыток: {attempt}")

    if best_path is None:
        messagebox.showwarning("Результат", "Гамильтонов цикл не найден после всех попыток")
        result_path.config(text="")
        result_distance.config(text="")
        draw_output_graph([])
    else:
        result_path.config(text=f"{' -> '.join(best_path)}")
        result_distance.config(text=f"{best_distance:.2f}")
        draw_output_graph(best_path)

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
        if not all(col in df.columns for col in ["вершина 1", "вершина 2", "длина"]):
            messagebox.showerror("Ошибка", "Файл должен содержать колонки 'вершина 1', 'вершина 2', 'длина'")
            return

        clear_canvas()
        for _, row in df.iterrows():
            v1, v2, length = row['вершина 1'], row['вершина 2'], float(row['длина'])
            if v1 not in vertices:
                vertices[v1] = (random.randint(50, 550), random.randint(50, 250))
            if v2 not in vertices:
                vertices[v2] = (random.randint(50, 550), random.randint(50, 250))
            edges.append((v1, v2, length))
            add_edge_to_table(v1, v2, length)

        draw_input_graph()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

# Создание интерфейса
root = tk.Tk()
root.title("Задача коммивояжера (Метод отжига)")

# Левый фрейм для параметров
left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

label_parameters = ttk.Label(left_frame, text="Параметры метода отжига", font=("Arial", 12))
label_parameters.pack(pady=5)

label_initial_temp = ttk.Label(left_frame, text="Начальная температура:")
label_initial_temp.pack(pady=2)
entry_initial_temp = ttk.Entry(left_frame)
entry_initial_temp.insert(0, "1000")
entry_initial_temp.pack(pady=2)

label_cooling_rate = ttk.Label(left_frame, text="Скорость охлаждения:")
label_cooling_rate.pack(pady=2)
entry_cooling_rate = ttk.Entry(left_frame)
entry_cooling_rate.insert(0, "0.99")
entry_cooling_rate.pack(pady=2)

label_cooling_factor = ttk.Label(left_frame, text="Коэффициент охлаждения (для VFSA):")
label_cooling_factor.pack(pady=2)
entry_cooling_factor = ttk.Entry(left_frame)
entry_cooling_factor.insert(0, "1.0")
entry_cooling_factor.pack(pady=2)

label_min_temp = ttk.Label(left_frame, text="Минимальная температура:")
label_min_temp.pack(pady=2)
entry_min_temp = ttk.Entry(left_frame)
entry_min_temp.insert(0, "1")
entry_min_temp.pack(pady=2)

label_iterations = ttk.Label(left_frame, text="Итераций на температуру:")
label_iterations.pack(pady=2)
entry_iterations = ttk.Entry(left_frame)
entry_iterations.insert(0, "100")
entry_iterations.pack(pady=2)

label_max_attempts = ttk.Label(left_frame, text="Макс. попыток:")
label_max_attempts.pack(pady=2)
entry_max_attempts = ttk.Entry(left_frame)
entry_max_attempts.insert(0, "10")
entry_max_attempts.pack(pady=2)

separator_count = ttk.Separator(left_frame, orient=tk.HORIZONTAL)
separator_count.pack(fill=tk.X, pady=15)

button_solve = ttk.Button(left_frame, text="Рассчитать", command=solve_with_annealing)
button_solve.pack(fill=tk.BOTH, pady=5)

button_solve_vfsa = ttk.Button(left_frame, text="Рассчитать (сверхбыстрый отжиг)", command=solve_with_very_fast_annealing)
button_solve_vfsa.pack(fill=tk.BOTH, pady=5)

label_start = ttk.Label(left_frame, text="Стартовая вершина:")
label_start.pack(pady=7)
entry_start = ttk.Entry(left_frame)
entry_start.pack()

button_load = ttk.Button(left_frame, text="Загрузить граф из файла", command=load_graph_from_file)
button_load.pack(fill=tk.BOTH, pady=5)

separator_left = ttk.Separator(root, orient=tk.VERTICAL)
separator_left.pack(side=tk.LEFT, fill=tk.Y, padx=5)

# Центральный фрейм для графиков
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

tree = ttk.Treeview(right_frame, columns=("вершина 1", "вершина 2", "длина", "феромон"), show="headings")
tree.heading("вершина 1", text="Вершина 1")
tree.heading("вершина 2", text="Вершина 2")
tree.heading("длина", text="Длина")
tree.heading("феромон", text="Феромон")
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

root.mainloop()