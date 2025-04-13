import numpy as np
import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt

# Класс Genetic реализует генетический алгоритм
class Genetic:
    def __init__(self, fitness_function, num_generations, population_size, mut_probab, low, hight, sigma, selection_method):
        self.fitness_function = fitness_function
        self.num_generations = num_generations
        self.population_size = population_size
        self.mut_probab = mut_probab
        self.low = low
        self.hight = hight
        self.sigma = sigma
        self.selection_method = selection_method
        self.population = self.init_population()
        self.fitness_values = self.calculate_fitness()

    def init_population(self):
        population = []
        for _ in range(self.population_size):
            x = random.uniform(self.low, self.hight)
            y = random.uniform(self.low, self.hight)
            population.append([x, y])
        return population

    def calculate_fitness(self):
        fitness_values = []
        for chromo in self.population:
            x, y = chromo
            fitness = self.fitness_function(x, y)
            fitness_values.append(fitness)
        return fitness_values

    def tournament_selection(self, tournament_size):
        tournament = random.sample(range(len(self.population)), tournament_size)
        winner_index = min(tournament, key=lambda i: self.fitness_values[i])
        return self.population[winner_index]

    def crossover(self, parent1, parent2):
        alpha = random.random()
        child1 = [alpha * x1 + (1 - alpha) * x2 for x1, x2 in zip(parent1, parent2)]
        child2 = [(1 - alpha) * x1 + alpha * x2 for x1, x2 in zip(parent1, parent2)]
        return child1, child2

    def gaussian_mutation(self, chromo):
        mutated_chromo = []
        for gene in chromo:
            if random.random() < self.mut_probab:
                mutation = np.random.normal(0, self.sigma)
                mutated_gene = gene + mutation
            else:
                mutated_gene = gene
            mutated_chromo.append(mutated_gene)
        return mutated_chromo

    def run(self):
        generations_data = []
        for generation in range(self.num_generations):
            new_population = []
            if self.selection_method == "elitism":
                elite_size = int(self.population_size * 0.1)
                elite_indices = np.argsort(self.fitness_values)[:elite_size]
                for index in elite_indices:
                    new_population.append(self.population[index])

            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection(tournament_size=2)
                parent2 = self.tournament_selection(tournament_size=2)

                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.gaussian_mutation(child1)
                child2 = self.gaussian_mutation(child2)

                if self.selection_method == "classic":
                    new_population.append(child1)
                    new_population.append(child2)
                elif self.selection_method == "roulette":
                    fitness1 = self.fitness_function(*child1)
                    fitness2 = self.fitness_function(*child2)
                    total_fitness = fitness1 + fitness2
                    if total_fitness > 0:
                        prob1 = fitness1 / total_fitness
                        prob2 = fitness2 / total_fitness
                    else:
                        prob1 = prob2 = 0.5
                    if random.random() < prob1:
                        new_population.append(child1)
                    if random.random() < prob2:
                        new_population.append(child2)
                elif self.selection_method == "elitism":
                    new_population.append(child1)
                    new_population.append(child2)

            self.population = new_population[:self.population_size]
            self.fitness_values = self.calculate_fitness()

            best_fitness = min(self.fitness_values)
            best_index = np.argmin(self.fitness_values)
            best_chromo = self.population[best_index]
            generations_data.append((generation + 1, best_fitness, best_chromo[0], best_chromo[1]))

        return best_chromo, best_fitness, generations_data

def fitness_function(x, y):
    return (-12*y+4*x**2+4*y**2-4*x*y)

def inserted(place, num):
    place.delete(0, tk.END)
    place.insert(0, str(num))

def display_table(data):
    for row in tree.get_children():
        tree.delete(row)
    for row_data in data:
        tree.insert("", "end", values=row_data)

def plot_convergence(data_dict, selected_method):
    plt.clf() 
    if selected_method in data_dict:
        data = data_dict[selected_method]
        generations = [d[0] for d in data]
        fitness_values = [d[1] for d in data]
        plt.plot(generations, fitness_values, label=selected_method)
    plt.xlabel('Поколение')
    plt.ylabel('Лучшее значение функции')
    plt.title('Сходимость генетического алгоритма')
    plt.legend()
    plt.grid(True)
    plt.draw()
    plt.pause(0.01)

def calculate_genetic_algorithm():
    mut_probab = float(ProbMut.get()) / 100.0
    population_size = int(numChrom.get())
    num_generations = int(cntIt.get())
    low = float(minGen.get())
    hight = float(maxGen.get())
    sigma = float(sigmaEntry.get())
    selection_method = selectionVar.get()

    genetic_algorithm = Genetic(fitness_function, num_generations, population_size, mut_probab, low, hight, sigma, selection_method)
    best_chromo, best_fitness, generations_data = genetic_algorithm.run()

    coord_text = f"Координаты точки: ({best_chromo[0]:.4f}, {best_chromo[1]:.4f})"
    fitness_text = f"Функция: {best_fitness:.4f}"

    canvas2.delete("all")
    canvas2.itemconfig(canvas2.create_text(197, 10, text=coord_text, font=("Arial", 10)), tags="result_text_coord")
    canvas2.itemconfig(canvas2.create_text(197, 40, text=fitness_text, font=("Arial", 10)), tags="result_text_fitness")
    display_table(generations_data)

    if not hasattr(calculate_genetic_algorithm, "data_dict"):
        calculate_genetic_algorithm.data_dict = {}
    calculate_genetic_algorithm.data_dict[selection_method] = generations_data

    plot_convergence(calculate_genetic_algorithm.data_dict, selection_method)

root = tk.Tk()
root.title("Генетический алгоритм для поиска минимума функции")
root.geometry('800x450')

left_frame = tk.Frame(root, width=400, height=450)
left_frame.grid(row=0, column=0, sticky="nsew")

right_frame = tk.Frame(root, width=400, height=450)
right_frame.grid(row=0, column=1, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

tk.Label(left_frame, text="Предварительные настройки", font=("Arial", 11)).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(left_frame, text="Функция:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
tk.Label(left_frame, text="-12y+4x^2+4y^2-4xy", font=("Arial", 10)).grid(row=1, column=1, sticky="w", padx=10, pady=5)

tk.Label(left_frame, text="Вероятность мутации, %:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
ProbMut = tk.Entry(left_frame, width=7)
ProbMut.insert(0, "20")
ProbMut.grid(row=2, column=1, sticky="w", padx=10, pady=5)

tk.Label(left_frame, text="Количество хромосом:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
numChrom = tk.Entry(left_frame, width=7)
numChrom.insert(0, "50")
numChrom.grid(row=3, column=1, sticky="w", padx=10, pady=5)

tk.Label(left_frame, text="Минимальное значение гена:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
minGen = tk.Entry(left_frame, width=7)
minGen.insert(0, "-50")
minGen.grid(row=4, column=1, sticky="w", padx=10, pady=5)

tk.Label(left_frame, text="Максимальное значение гена:", font=("Arial", 10)).grid(row=5, column=0, sticky="w", padx=10, pady=5)
maxGen = tk.Entry(left_frame, width=7)
maxGen.insert(0, "50")
maxGen.grid(row=5, column=1, sticky="w", padx=10, pady=5)

tk.Label(left_frame, text="Стандартное отклонение мутации:", font=("Arial", 10)).grid(row=6, column=0, sticky="w", padx=10, pady=5)
sigmaEntry = tk.Entry(left_frame, width=7)
sigmaEntry.insert(0, "0.5")
sigmaEntry.grid(row=6, column=1, sticky="w", padx=10, pady=5)

tk.Label(left_frame, text="Управление", font=("Arial", 11)).grid(row=7, column=0, columnspan=2, pady=10)

tk.Label(left_frame, text="Количество поколений:", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=10, pady=5)
cntIt = tk.Spinbox(left_frame, from_=1, to=5000, width=5)
cntIt.grid(row=8, column=1, sticky="w", padx=10, pady=5)

tk.Button(left_frame, text="1", width=8, command=lambda: inserted(cntIt, 1), bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE).grid(row=9, column=0, padx=10, pady=5)
tk.Button(left_frame, text="10", width=8, command=lambda: inserted(cntIt, 10), bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE).grid(row=9, column=1, padx=10, pady=5)
tk.Button(left_frame, text="100", width=8, command=lambda: inserted(cntIt, 100), bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE).grid(row=10, column=0, padx=10, pady=5)
tk.Button(left_frame, text="1000", width=8, command=lambda: inserted(cntIt, 1000), bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE).grid(row=10, column=1, padx=10, pady=5)

selectionVar = tk.StringVar(value="classic")
tk.Label(left_frame, text="Метод отбора:", font=("Arial", 10)).grid(row=11, column=0, sticky="w", padx=10, pady=5)
selection_method_menu = tk.OptionMenu(left_frame, selectionVar, "classic", "roulette", "elitism")
selection_method_menu.grid(row=11, column=1, sticky="w", padx=10, pady=5)

tk.Button(left_frame, text="Рассчитать", width=42, command=calculate_genetic_algorithm, bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE).grid(row=12, column=0, columnspan=2, padx=10, pady=10)

tk.Label(right_frame, text="Результаты", font=("Arial", 11)).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(right_frame, text="Лучшее решение достигается в точке:", font=("Arial", 10)).grid(row=1, column=0, columnspan=2, padx=10, pady=5)

canvas2 = tk.Canvas(right_frame, width=393, height=50, bg="white", borderwidth=1, highlightbackground="#CCCCCC", highlightthickness=2)
canvas2.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

frame_tree = ttk.Frame(right_frame, borderwidth=2, relief="groove")
frame_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

columns = ("Номер", "Результат", "Ген 1", "Ген 2")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=10)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10))
style.configure("Treeview", font=("Arial", 9), rowheight=25)
style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(expand=True, fill="both")

plt.ion()

root.mainloop()