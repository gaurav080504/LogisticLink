# backend/core/tsp_solver.py

import itertools
import time

def calculate_total_distance(route, distance_matrix):
    """Calculates the total distance of a given route (index list)."""
    total = 0
    for i in range(len(route) - 1):
        total += distance_matrix[route[i]][route[i+1]]
    
    # Return to the start (closing the loop)
    total += distance_matrix[route[-1]][route[0]]
    return total

def solve_tsp_brute_force(distance_matrix):
    """
    Solves TSP by checking every possible permutation.
    Warning: Do not use this for more than 10-11 locations!
    """
    num_cities = len(distance_matrix)
    cities = list(range(num_cities))
    
    # We fix the first city to reduce redundant checks (e.g., [0,1,2] is same as [1,2,0])
    start_city = cities[0]
    other_cities = cities[1:]
    
    best_route = None
    min_distance = float('inf')
    
    start_time = time.time()
    
    # Generate all permutations of the remaining cities
    for p in itertools.permutations(other_cities):
        current_route = [start_city] + list(p)
        current_distance = calculate_total_distance(current_route, distance_matrix)
        
        if current_distance < min_distance:
            min_distance = current_distance
            best_route = current_route
            
    end_time = time.time()
    
    return best_route, min_distance, (end_time - start_time)

# --- Test/Example ---
if __name__ == '__main__':
    # Using a dummy 4x4 matrix for testing
    # Matrix[i][j]
    example_matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    
    route, dist, duration = solve_tsp_brute_force(example_matrix)
    print(f"Best Route: {route}")
    print(f"Minimum Distance: {dist}")
    print(f"Time Taken: {duration:.6f} seconds")