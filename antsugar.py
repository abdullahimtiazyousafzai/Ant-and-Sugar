import tkinter as tk
from tkinter import ttk
import random
import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Vector:
    x: float
    y: float
    
    def add(self, other):
        self.x += other.x
        self.y += other.y
        
    def mult(self, n):
        self.x *= n
        self.y *= n
        
    def heading(self):
        return math.atan2(self.y, self.x)
        
    @staticmethod
    def random2D():
        angle = random.uniform(0, 2 * math.pi)
        return Vector(math.cos(angle), math.sin(angle))
    
    def setMag(self, mag):
        current_mag = math.sqrt(self.x * self.x + self.y * self.y)
        if current_mag != 0:
            self.x = self.x * mag / current_mag
            self.y = self.y * mag / current_mag

class DNA:
    def __init__(self, genes=None):
        self.genes = genes if genes else []
        if not genes:
            for _ in range(LIFESPAN):
                gene = Vector.random2D()
                gene.setMag(MAX_FORCE)
                self.genes.append(gene)
                
    def crossover(self, partner):
        new_genes = []
        mid = random.randint(0, len(self.genes)-1)
        for i in range(len(self.genes)):
            new_genes.append(self.genes[i] if i > mid else partner.genes[i])
        return DNA(new_genes)
    
    def mutation(self):
        for i in range(len(self.genes)):
            if random.random() < MUTATION_RATE:
                self.genes[i] = Vector.random2D()
                self.genes[i].setMag(MAX_FORCE)

class Ant:
    def __init__(self, dna=None):
        self.pos = Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT - 20)  # Adjusted starting position
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.fitness = 0
        self.dna = dna if dna else DNA()
        self.completed = False
        self.crashed = False
        self.completion_time = None
        
    def apply_force(self, force):
        self.acc.add(force)
        
    def update(self, sugar_pos):
        d = math.sqrt((self.pos.x - sugar_pos[0])**2 + (self.pos.y - sugar_pos[1])**2)
        if d < 10 and not self.completed:
            self.completed = True
            self.completion_time = count
            
        if (OX < self.pos.x < OX + OW and 
            OY < self.pos.y < OY + OH):
            self.crashed = True
            
        # Add boundary checking
        if (self.pos.x < 0 or self.pos.x > CANVAS_WIDTH or 
            self.pos.y < 0 or self.pos.y > CANVAS_HEIGHT):
            self.crashed = True
            
        self.apply_force(self.dna.genes[count])
        if not self.completed and not self.crashed:
            self.vel.add(self.acc)
            self.pos.add(self.vel)
            self.acc.mult(0)
            
    def calculate_fitness(self, sugar_pos):
        d = math.sqrt((self.pos.x - sugar_pos[0])**2 + (self.pos.y - sugar_pos[1])**2)
        self.fitness = 1/d
        if self.completed:
            self.fitness *= 10 * (LIFESPAN / (self.completion_time + 1))
        if self.crashed:
            self.fitness /= 10

class Population:
    def __init__(self):
        self.pop_size = POPULATION_SIZE
        self.ants = [Ant() for _ in range(self.pop_size)]
        self.pool = []
        self.best_fitness = 0
        self.avg_fitness = 0
        self.success_rate = 0
        
    def evaluate(self, sugar_pos):
        max_fit = 0
        total_fit = 0
        completed_count = 0
        
        for ant in self.ants:
            ant.calculate_fitness(sugar_pos)
            max_fit = max(max_fit, ant.fitness)
            total_fit += ant.fitness
            if ant.completed:
                completed_count += 1
                
        self.best_fitness = max_fit
        self.avg_fitness = total_fit / len(self.ants)
        self.success_rate = (completed_count / len(self.ants)) * 100
            
        for ant in self.ants:
            ant.fitness /= max_fit
            
        self.pool = []
        for ant in self.ants:
            n = int(ant.fitness * 100)
            self.pool.extend([ant] * n)
            
    def selection(self):
        new_ants = []
        for _ in range(len(self.ants)):
            parent_a = random.choice(self.pool).dna
            parent_b = random.choice(self.pool).dna
            child = parent_a.crossover(parent_b)
            child.mutation()
            new_ants.append(Ant(child))
        self.ants = new_ants

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Ant Colony Genetic Algorithm Simulator")
        self.configure(bg='#2b2b2b')
        
        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create canvas
        self.canvas = tk.Canvas(main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, 
                              bg='#1e1e1e', highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="5")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Add buttons
        self.running = True
        self.start_stop_btn = ttk.Button(control_frame, text="Pause", 
                                       command=self.toggle_simulation)
        self.start_stop_btn.grid(row=0, column=0, padx=5)
        
        self.reset_btn = ttk.Button(control_frame, text="Reset", 
                                  command=self.reset_simulation)
        self.reset_btn.grid(row=0, column=1, padx=5)
        
        # Stats panel
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="5")
        stats_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.gen_label = ttk.Label(stats_frame, text="Generation: 1")
        self.gen_label.grid(row=0, column=0, padx=5)
        
        self.fitness_label = ttk.Label(stats_frame, text="Best Fitness: 0.0")
        self.fitness_label.grid(row=0, column=1, padx=5)
        
        self.success_label = ttk.Label(stats_frame, text="Success Rate: 0%")
        self.success_label.grid(row=0, column=2, padx=5)
        
        # Initialize simulation
        self.population = Population()
        self.generation_count = 1
        self.sugar_pos = (CANVAS_WIDTH/2, 50)
        
        # Bind mouse events for moving sugar
        self.canvas.bind("<B1-Motion>", self.move_sugar)
        
        # Start simulation
        self.after(33, self.update)
        
    def move_sugar(self, event):
        self.sugar_pos = (event.x, event.y)
        
    def toggle_simulation(self):
        self.running = not self.running
        self.start_stop_btn.configure(text="Resume" if not self.running else "Pause")
        
    def reset_simulation(self):
        self.population = Population()
        self.generation_count = 1
        global count
        count = 0
        
    def update(self):
        global count
        self.canvas.delete("all")
        
        if self.running:
            # Draw obstacle with gradient
            self.canvas.create_rectangle(OX, OY, OX+OW, OY+OH, 
                                      fill='#404040', outline='#606060')
            
            # Draw sugar with glow effect
            self.canvas.create_oval(self.sugar_pos[0]-12, self.sugar_pos[1]-12,
                                  self.sugar_pos[0]+12, self.sugar_pos[1]+12,
                                  fill='#3c3c3c', outline='#606060')
            self.canvas.create_oval(self.sugar_pos[0]-8, self.sugar_pos[1]-8,
                                  self.sugar_pos[0]+8, self.sugar_pos[1]+8,
                                  fill='#ffffff', outline='#ffffff')
            
            # Update and draw ants with color based on status
            for ant in self.population.ants:
                ant.update(self.sugar_pos)
                color = '#ff0000' if ant.crashed else '#00ff00' if ant.completed else '#ffffff'
                
                # Draw ant with direction indicator
                angle = ant.vel.heading()
                cx, cy = ant.pos.x, ant.pos.y
                r = 4  # radius
                
                # Ant body
                self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color, outline=color)
                
                # Direction indicator
                if not ant.crashed and not ant.completed:
                    end_x = cx + math.cos(angle) * (r + 2)
                    end_y = cy + math.sin(angle) * (r + 2)
                    self.canvas.create_line(cx, cy, end_x, end_y, fill=color, width=2)
            
            # Update stats
            self.gen_label.configure(text=f"Generation: {self.generation_count}")
            self.fitness_label.configure(text=f"Best Fitness: {self.population.best_fitness:.2f}")
            self.success_label.configure(text=f"Success Rate: {self.population.success_rate:.1f}%")
            
            # Progress bar
            progress = (count / LIFESPAN) * CANVAS_WIDTH
            self.canvas.create_rectangle(0, CANVAS_HEIGHT-5, progress, CANVAS_HEIGHT,
                                      fill='#404040', outline='')
            
            count += 1
            if count >= LIFESPAN:
                self.population.evaluate(self.sugar_pos)
                self.population.selection()
                self.generation_count += 1
                count = 0
        
        self.after(33, self.update)

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
LIFESPAN = 300
MAX_FORCE = 0.3
MUTATION_RATE = 0.01
POPULATION_SIZE = 100
OX = 200  # Obstacle X
OY = 300  # Obstacle Y
OW = 400  # Obstacle Width
OH = 20   # Obstacle Height

# Global variables
count = 0

if __name__ == "__main__":
    app = Application()
    
    # Configure style
    style = ttk.Style()
    style.configure("TButton", padding=5)
    style.configure("TLabelFrame", padding=5)
    
    app.mainloop()