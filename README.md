# Ant Colony Genetic Algorithm Simulator

This project demonstrates a simulation of ants evolving through a genetic algorithm to find the shortest path to a food source (sugar) while avoiding obstacles. It is implemented using Python's `tkinter` for graphical visualization.

## Features

- **Genetic Algorithm**: Simulates evolution with selection, crossover, and mutation processes.
- **Interactive Visualization**: Includes a canvas where ants' movements and progress are displayed in real-time.
- **Dynamic Control**: Pause, resume, and reset the simulation using intuitive buttons.
- **Obstacle Handling**: Ants avoid predefined obstacles on the canvas.
- **Real-Time Stats**: Displays generation count, best fitness, and success rate.

## How It Works

### Key Components

1. **Vector Class**: 
   - Provides essential vector operations like addition, scaling, and random 2D vector generation.
   - Used to represent ants' position, velocity, and acceleration.

2. **DNA Class**:
   - Represents the genetic blueprint of an ant.
   - Contains an array of forces (`Vector` objects) for each time step in a lifespan.

3. **Ant Class**:
   - Simulates the movement of an ant.
   - Calculates fitness based on the distance to the sugar and whether the ant successfully reaches the target or crashes.

4. **Population Class**:
   - Maintains a collection of ants.
   - Handles evaluation of fitness, selection, and the creation of the next generation.

5. **Application Class**:
   - Manages the GUI using `tkinter`.
   - Displays ants, obstacles, sugar, and simulation stats on the canvas.

### Simulation Dynamics

- Ants are randomly initialized with DNA that guides their movement.
- Over successive generations:
  - Fitness is evaluated based on proximity to the sugar and success in reaching it.
  - New generations are created through genetic operations:
    - **Selection**: Fitter ants are more likely to contribute to offspring.
    - **Crossover**: Combines DNA from two parents to create new ants.
    - **Mutation**: Introduces random changes in DNA to maintain diversity.

- The simulation runs for a fixed lifespan before moving to the next generation.

## Installation

1. Ensure you have Python 3 installed.
2. Install any missing dependencies:
   ```bash
   pip install tkinter
