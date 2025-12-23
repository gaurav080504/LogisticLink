# backend/core/genetic_algorithm.py

import random
import numpy as np # We'll use numpy for easier math later
from tsp_solver import calculate_total_distance

class GeneticAlgorithm:
    def __init__(self, distance_matrix, population_size=100, mutation_rate=0.01, generations=500):
        self.matrix = distance_matrix
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.num_cities = len(distance_matrix)
        self.population = []

    def create_initial_population(self):
        """Creates a list of random routes."""
        population = []
        for _ in range(self.pop_size):
            # Create a route [0, 1, 2, ...]
            route = list(range(self.num_cities))
            # Shuffle it randomly (keeping city 0 as start)
            other_cities = route[1:]
            random.shuffle(other_cities)
            population.append([route[0]] + other_cities)
        self.population = population
        return population

    def calculate_fitness(self, route):
        """The 'Score' of a route. Higher is better."""
        distance = calculate_total_distance(route, self.matrix)
        # We use 1/distance because GA tries to maximize fitness
        return 1 / distance

# # --- Test --- Before Selection
# if __name__ == '__main__':
#     # 4x4 dummy matrix
#     example_matrix = [
#         [0, 10, 15, 20],
#         [10, 0, 35, 25],
#         [15, 35, 0, 30],
#         [20, 25, 30, 0]
#     ]
    
#     ga = GeneticAlgorithm(example_matrix)
#     pop = ga.create_initial_population()
#     print(f"Created population of {len(pop)} routes.")
#     print(f"Sample route: {pop[0]}")
#     print(f"Fitness of sample: {ga.calculate_fitness(pop[0]):.6f}")


# backend/core/genetic_algorithm.py (Add this inside the GeneticAlgorithm class)

    def selection(self):
        """
        Sorts the current population by fitness and selects the top performers.
        Returns a list of 'parent' routes.
        """
        # Calculate fitness for every route in the population
        # We store them as tuples: (route, fitness_score)
        fitness_results = []
        for route in self.population:
            fitness_results.append((route, self.calculate_fitness(route)))
        
        # Sort by fitness score in descending order (highest fitness first)
        fitness_results.sort(key=lambda x: x[1], reverse=True)
        
        # Keep the best half of the population to act as parents
        # This ensures the 'genes' of the best routes are preserved
        parents = [result[0] for result in fitness_results[:self.pop_size // 2]]
        
        return parents

# # --- Updated Test Block ---
# if __name__ == '__main__':
#     example_matrix = [
#         [0, 10, 15, 20], [10, 0, 35, 25],
#         [15, 35, 0, 30], [20, 25, 30, 0]
#     ]
    
#     ga = GeneticAlgorithm(example_matrix, population_size=10)
#     ga.create_initial_population()
#     parents = ga.selection()
    
#     print(f"Total Population: {len(ga.population)}")
#     print(f"Selected Parents: {len(parents)}")
#     print(f"Best route in this generation: {parents[0]}")




# backend/core/genetic_algorithm.py (Add inside the GeneticAlgorithm class)

    def crossover(self, parent1, parent2):
        """
        Ordered Crossover (OX1): Combines two parents to create a child.
        """
        child = [None] * self.num_cities
        
        # Start at index 1 to keep city 0 (the start/depot) fixed
        start_pos = random.randint(1, self.num_cities - 2)
        end_pos = random.randint(start_pos + 1, self.num_cities - 1)

        # Copy a segment from parent1
        for i in range(start_pos, end_pos):
            child[i] = parent1[i]
        
        # Fill remaining slots from parent2
        child[0] = parent1[0] # Fix the starting city
        
        current_pos = 1
        for city in parent2:
            if city not in child:
                # Find next empty slot in child (skipping city 0)
                while child[current_pos] is not None:
                    current_pos += 1
                child[current_pos] = city
        
        return child

    def breed_population(self, parents):
        """Creates a new generation of children from the selected parents."""
        children = []
        # Keep the top parents (Elitism) - copy them directly to the next generation
        children.extend(parents[:2]) 
        
        # Fill the rest of the population with crossover
        while len(children) < self.pop_size:
            p1 = random.choice(parents)
            p2 = random.choice(parents)
            child = self.crossover(p1, p2)
            children.append(child)
        
        return children
    

# backend/core/genetic_algorithm.py (Add inside the GeneticAlgorithm class)

    def mutate(self, route):
        """
        Randomly swaps two cities in the route based on the mutation rate.
        """
        for i in range(1, self.num_cities): # Start at 1 to keep starting city fixed
            if random.random() < self.mutation_rate:
                # Pick a random index to swap with
                swap_with = random.randint(1, self.num_cities - 1)
                
                # Perform the swap
                route[i], route[swap_with] = route[swap_with], route[i]
        return route

    def mutate_population(self, population):
        """Applies mutation to the entire population."""
        mutated_pop = []
        # We don't mutate the 'Elite' (the very best route) to ensure we don't lose it
        mutated_pop.append(population[0]) 
        
        for i in range(1, len(population)):
            mutated_route = self.mutate(population[i])
            mutated_pop.append(mutated_route)
        
        return mutated_pop
    

# backend/core/genetic_algorithm.py (Add inside the GeneticAlgorithm class)

    def run(self):
        """
        The main loop that evolves the population over several generations.
        """
        self.create_initial_population()
        
        best_route = None
        best_distance = float('inf')

        for gen in range(self.generations):
            # 1. Selection
            parents = self.selection()
            
            # 2. Crossover (Breeding)
            children = self.breed_population(parents)
            
            # 3. Mutation
            self.population = self.mutate_population(children)
            
            # Track the best solution found so far
            current_best_route = self.selection()[0]
            current_best_distance = calculate_total_distance(current_best_route, self.matrix)
            
            if current_best_distance < best_distance:
                best_distance = current_best_distance
                best_route = current_best_route
            
            # Print progress every 100 generations
            if gen % 100 == 0:
                print(f"Generation {gen}: Best Distance = {best_distance:.2f} km")
                
        return best_route, best_distance