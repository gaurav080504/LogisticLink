# backend/core/main_test.py

import time
from location import Location
from distance_matrix import create_distance_matrix
from genetic_algorithm import GeneticAlgorithm

def run_large_scale_test(num_stops=50):
    print(f"--- LogisticLink: Testing {num_stops} Stops ---")
    
    # 1. Generate 50 random locations (simulating a city area)
    import random
    random.seed(42) # For consistent results
    locations = [
        Location(id=i, lat=random.uniform(18.5, 19.5), lon=random.uniform(72.5, 73.5))
        for i in range(num_stops)
    ]
    
    # 2. Build Distance Matrix
    print("Building Distance Matrix...")
    matrix = create_distance_matrix(locations)
    
    # 3. Initialize GA
    # We'll use 200 population size and 1000 generations
    ga = GeneticAlgorithm(matrix, population_size=200, generations=1000, mutation_rate=0.02)
    
    # 4. Run Optimization
    print("Starting Evolution...")
    start_time = time.time()
    best_route, best_distance = ga.run()
    end_time = time.time()
    
    # 5. Results
    print("\n" + "="*30)
    print(f"Optimization Complete!")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")
    print(f"Best Distance Found: {best_distance:.2f} km")
    print(f"Optimized Route (Stop IDs): {best_route}")
    print("="*30)

if __name__ == '__main__':
    run_large_scale_test(50)