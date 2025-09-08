# Hybrid Genetic Algorithm for the MAX-SAT Problem

This project implements a hybrid genetic algorithm to find approximate solutions for the Maximum Satisfiability (MAX-SAT) problem. The goal is to find a variable assignment that satisfies the maximum possible number of clauses in a given Boolean formula in Conjunctive Normal Form (CNF).

The algorithm combines a standard Genetic Algorithm (GA) with a local search heuristic (bit-flipping) to efficiently explore the solution space and refine promising candidates. This hybrid approach is often referred to as a Memetic Algorithm.

## Features

  * **Genetic Algorithm Core**: Uses core GA principles like selection, crossover, and mutation to evolve a population of potential solutions.
  * **Elitism**: Preserves the best-performing individuals from one generation to the next, ensuring that good solutions are not lost.
  * **Local Search Integration**: The best individuals in each generation are further optimized using a bit-flipping local search algorithm to find nearby, higher-quality solutions.
  * **Weighted Selection**: Parents are chosen for reproduction using a weighted random selection method, where individuals with higher fitness have a greater chance of being selected.
  * **Configurable Parameters**: Key algorithm parameters such as population size, mutation rate, and runtime are easily configurable as constants in the main script.
  * **Problem Loader**: Can read CNF problem instances from an external `CNF.csv` file.

## Requirements

  * Python 3.x
  * NumPy library (`pip install numpy`)

## How to Run

### 1\. Prepare the Input File

The algorithm requires a CNF formula to be provided in a file named `CNF.csv` in the same directory.

  * Each row in the CSV file represents a single **clause**.
  * Each column in a row represents a **literal**.
  * A positive integer `x` corresponds to a variable, and a negative integer `-x` corresponds to its negation.

**Example `CNF.csv` content:**

```csv
5,-12,34
-22,8,-41
1,15,29
```

### 2\. Configure the Algorithm (Optional)

You can modify the constants at the top of the `Improved_Genetic_Algorithm.py` file to tune the algorithm's performance:

```python
NO_OF_VARIABLES = 50      # Must match the variables in your CNF file
POPULATION_SIZE = 20      # Number of individuals in each generation
END_TIME = 45             # Maximum execution time in seconds
MUTATION_RATE = 0.1       # Probability that a new individual will be mutated
POINT_MUTATION_RATE = 0.1 # Probability for each bit to flip during mutation
ELITISM_RATE = 0.60       # Percentage of top individuals to carry to the next generation
LAST_CHANCE = 40000       # Stop if no improvement is seen after this many iterations
```

### 3\. Execute the Script

Run the main solver from your terminal:

```bash
python Improved_Genetic_Algorithm.py
```

### 4\. View the Output

The script will print the results to the console, including the best solution found, its fitness score, and the time taken.

**Example Output:**

```
Number of clauses in CSV file :  175
Best model :  [1, -2, -3, 4, 5, ... , -49, 50]
Fitness value of best model : 99.43
Time taken: 45.01 seconds
```

## How It Works

The project is divided into two main components: the CNF problem handler and the hybrid genetic algorithm solver.

### `CNF_Creator.py`

This module is responsible for handling the CNF formula.

  * The `CNF_Creator` class can be initialized with a specific number of variables.
  * The `ReadCNFfromCSVfile()` method reads the problem instance from `CNF.csv` and loads it into a list of lists format that the solver can use.
  * It also contains methods for generating random 3-CNF sentences, though these are not used by default in the main script.

### `Improved_Genetic_Algorithm.py`

This is the main solver which implements the hybrid genetic algorithm.

1.  **Initialization**: A random initial population of binary strings is created. Each binary string represents a potential solution (a model), where the index corresponds to a variable and the value (0 or 1) corresponds to its truth assignment (False or True).

2.  **Fitness Evaluation**: The fitness of each individual is calculated as the percentage of clauses in the CNF formula that it satisfies. A cache is used to store fitness scores to avoid re-computation for the same individual.

3.  **Evolution Cycle**: The algorithm iterates through generations until a termination condition is met (time limit, 100% fitness, or stalled progress). Each generation involves:

      * **Sorting**: The current population is sorted by fitness in descending order.
      * **Elitism**: A percentage of the fittest individuals (`ELITISM_RATE`) are copied directly to the next generation.
      * **Local Search**: A few of these elite individuals are further refined using the `local_search_bit_flipping` function. This function iteratively flips each bit in the individual and keeps the change if it improves fitness, helping to find local optima quickly.
      * **Selection & Crossover**: For the remainder of the new population, two parents are selected from the sorted list (weighted by fitness). They produce a child using a single-point crossover (`reproduce` function).
      * **Mutation**: The newly created child has a chance (`MUTATION_RATE`) of undergoing mutation, where some of its bits are randomly flipped.

4.  **Termination**: The algorithm stops when the time limit is reached, a perfect solution is found, or if the best fitness score has not improved for a large number of iterations (`LAST_CHANCE`). The best individual found throughout the entire run is returned as the final solution.
