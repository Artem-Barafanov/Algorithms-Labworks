import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import math

class Particle:
    def __init__(self, x_range, y_range):
        self.x = random.uniform(x_range[0], x_range[1])
        self.y = random.uniform(y_range[0], y_range[1])
        
        self.best_value = None
        self.best_x = self.x
        self.best_y = self.y
        
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
    
    def update_best_value(self, value):
        if self.best_value is None or value < self.best_value:
            self.best_value = value
            self.best_x = self.x
            self.best_y = self.y

class Swarm:
    def __init__(self, num_particles, x_range, y_range, c1, c2, k, mod):
        self.global_best_value = None
        self.global_best_x = None
        self.global_best_y = None
        self.mod = mod
        
        self.particles = [Particle(x_range, y_range) for _ in range(num_particles)]
        
        self.c1 = c1
        self.c2 = c2
        
        phi = c1 + c2
        if phi <= 4:
            raise ValueError("Сумма коэффициентов c1 и c2 должна быть больше 4.")
        
        self.chi = (2 * k) / abs(2 - phi - math.sqrt(phi**2 - 4 * phi))
    
    def update_global_best(self):
        for particle in self.particles:
            if self.global_best_value is None or particle.best_value < self.global_best_value:
                self.global_best_value = particle.best_value
                self.global_best_x = particle.best_x
                self.global_best_y = particle.best_y
    
    def update_velocities(self):
        for particle in self.particles:
            r1 = random.random()
            r2 = random.random()
            
            if self.mod == 'canonical':
                particle.vx = self.chi * (particle.vx + 
                                        self.c1 * r1 * (particle.best_x - particle.x) + 
                                        self.c2 * r2 * (self.global_best_x - particle.x))
                
                particle.vy = self.chi * (particle.vy + 
                                        self.c1 * r1 * (particle.best_y - particle.y) + 
                                        self.c2 * r2 * (self.global_best_y - particle.y))

            elif self.mod == 'classic':
                particle.vx = (particle.vx + 
                                        self.c1 * r1 * (particle.best_x - particle.x) + 
                                        self.c2 * r2 * (self.global_best_x - particle.x))
                
                particle.vy = (particle.vy + 
                                        self.c1 * r1 * (particle.best_y - particle.y) + 
                                        self.c2 * r2 * (self.global_best_y - particle.y))

    def update_positions(self):
        for particle in self.particles:
            particle.x += particle.vx
            particle.y += particle.vy
    
    def run_pso(self, objective_function, num_iterations):
        for _ in range(num_iterations):
            for particle in self.particles:
                current_value = objective_function(particle.x, particle.y)
                
                particle.update_best_value(current_value)
            
            self.update_global_best()
            
            self.update_velocities()
            
            self.update_positions()

def inserted(place, num):
    place.delete(0, tk.END)
    place.insert(0, str(num))

def creating():
    global swarm, ax, scatter, canvas_widget

    c1 = float(c1_entry.get())
    c2 = float(c2_entry.get())
    k = float(k_entry.get())
    num_particles = int(num_particles_entry.get())
    mod = mod_var.get()

    swarm = Swarm(num_particles, [-100, 100], [-100, 100], c1, c2, k, mod)

    ax.clear()
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_title("Положение роя")
    scatter = ax.scatter([], [], color='blue', marker='o')
    canvas_widget.get_tk_widget().update_idletasks()
    positions = np.array([[particle.x, particle.y] for particle in swarm.particles])
    scatter.set_offsets(positions)
    canvas_widget.draw()

def make_iterations(n):
    global swarm, ax, scatter, canvas_widget

    it = int(txt4.get())
    txt4.delete(0, tk.END)
    entry_var.set(str(it + n))

    for _ in range(n):
        for particle in swarm.particles:
            current_value = objective_function(particle.x, particle.y)
            
            particle.update_best_value(current_value)
        
        swarm.update_global_best()
        
        swarm.update_velocities()
        
        swarm.update_positions()

    positions = np.array([[particle.x, particle.y] for particle in swarm.particles])
    scatter.set_offsets(positions)
    canvas_widget.draw()
    best_position = (swarm.global_best_x, swarm.global_best_y)
    best_fitness = swarm.global_best_value

    canvas2.delete("all")
    canvas2.create_text(10, 10, anchor="nw", text=f"Лучшее решение: {best_position}\nЗначение функции: {best_fitness}",
                        font=("Arial", 10), fill="black")

root = tk.Tk()
root.title("Роевой интеллект для поиска минимума функции")
root.geometry('1250x800')

left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, sticky="nsew")

left_frame_low = tk.Frame(root)
left_frame_low.grid(row=1, column=0, sticky="nsew")

center_frame = tk.Frame(root)
center_frame.grid(row=0, column=1, sticky="nsew")

center_frame_low = tk.Frame(root)
center_frame_low.grid(row=1, column=1, sticky="nsew")

right_frame = tk.Frame(root)
right_frame.grid(row=0, column=2, sticky="nsew")

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)

lbl = tk.Label(left_frame, text="Предварительные настройки", font=("Arial", 11))
lbl.grid(row=0, column=0, columnspan=2, pady=(10, 0))

lblfunc = tk.Label(left_frame, text="Функция:", font=("Arial", 10))
lblfunc.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

lblfunc2 = tk.Label(left_frame, text="-12*y+4*x**2+4*y**2-4*x*y", font=("Arial", 10))
lblfunc2.grid(row=1, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

lblc1 = tk.Label(left_frame, text="Коэффициент cобственного лучшего значения:", font=("Arial", 10))
lblc1.grid(row=2, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

c1_entry = tk.Entry(left_frame, width=7)
c1_entry.insert(0, "3.0")
c1_entry.grid(row=2, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

lblc2 = tk.Label(left_frame, text="Коэффициент глобального лучшего значения:", font=("Arial", 10))
lblc2.grid(row=3, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

c2_entry = tk.Entry(left_frame, width=7)
c2_entry.insert(0, "2.0")
c2_entry.grid(row=3, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

lblk = tk.Label(left_frame, text="Коэффициент k:", font=("Arial", 10))
lblk.grid(row=4, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

k_entry = tk.Entry(left_frame, width=7)
k_entry.insert(0, "0.72984")
k_entry.grid(row=4, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

lblnum_particles = tk.Label(left_frame, text="Количество частиц:", font=("Arial", 10))
lblnum_particles.grid(row=5, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

num_particles_entry = tk.Spinbox(left_frame, from_=10, to=500, width=5)
num_particles_entry.grid(row=5, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

lblmod = tk.Label(left_frame, text="Режим:", font=("Arial", 10))
lblmod.grid(row=6, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

mod_var = tk.StringVar(value='canonical')
mod_entry = ttk.Combobox(left_frame, textvariable=mod_var, values=['classic', 'canonical'], state='readonly', width=10)
mod_entry.grid(row=6, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

lbl4 = tk.Label(left_frame_low, text="Управление", font=("Arial", 11))
lbl4.grid(row=7, column=0, columnspan=2, pady=(20, 0))

but = tk.Button(left_frame_low, text="Создать частицы", width=42, 
                command=creating,
                bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but.grid(row=8, column=0, columnspan=2, padx=(10, 10), pady=(10, 0))

lbl5 = tk.Label(left_frame_low, text="Количество итераций:", font=("Arial", 10))
lbl5.grid(row=9, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

cntIt = tk.Spinbox(left_frame_low, from_=1, to=5000, width=5)
cntIt.grid(row=9, column=1, padx=(0, 10), pady=(10, 0), sticky="w")

but1 = tk.Button(left_frame_low, text="1", width=8, 
                 command=lambda: inserted(cntIt, 1),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but1.grid(row=10, column=0, padx=(10, 0), pady=(10, 0))

but2 = tk.Button(left_frame_low, text="10", width=8, 
                 command=lambda: inserted(cntIt, 10),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but2.grid(row=10, column=1, padx=(0, 10), pady=(10, 0))

but3 = tk.Button(left_frame_low, text="100", width=8, 
                 command=lambda: inserted(cntIt, 100),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but3.grid(row=11, column=0, padx=(10, 0), pady=(10, 0))

but4 = tk.Button(left_frame_low, text="1000", width=8, 
                 command=lambda: inserted(cntIt, 1000),
                 bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but4.grid(row=11, column=1, padx=(0, 10), pady=(10, 0))

but = tk.Button(left_frame_low, text="Рассчитать", width=42, 
                command=lambda: make_iterations(int(cntIt.get())),
                bg="#DDDDDD", activebackground="#CCCCCC", relief=tk.GROOVE)
but.grid(row=12, column=0, columnspan=2, padx=(10, 10), pady=(10, 0))

lbl5 = tk.Label(left_frame_low, text="Количество выполненных итераций:", font=("Arial", 10))
lbl5.grid(row=13, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

cnt = 0
entry_var = tk.StringVar()
txt4 = tk.Entry(left_frame_low, width=7, textvariable=entry_var, state='disabled', disabledbackground="white", fg="black")
txt4.grid(row=13, column=1, padx=(0, 10), pady=(10, 0), sticky="w")
entry_var.set(str(cnt))

lbl6 = tk.Label(center_frame, text="Результаты", font=("Arial", 11))
lbl6.grid(row=0, column=0, pady=(10, 0))

lbl5 = tk.Label(center_frame, text="Лучшее решение достигается в точке:", font=("Arial", 10))
lbl5.grid(row=1, column=0, padx=(10, 0), pady=(10, 0), sticky="w")

canvas2 = tk.Canvas(center_frame, width=393, height=100, bg="white", borderwidth=1, highlightbackground="#CCCCCC", highlightthickness=2)
canvas2.grid(row=2, column=0, padx=(10, 10), pady=(10, 0))

fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.set_facecolor('white')
ax.tick_params(axis='both', labelsize=8)

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_title("Положение роя")

canvas_widget = FigureCanvasTkAgg(fig, master=center_frame_low)
canvas_widget.get_tk_widget().grid(row=0, column=0, sticky="nsew")

def objective_function(x, y):
    return -12*y + 4*x**2 + 4*y**2 - 4*x*y

root.mainloop()