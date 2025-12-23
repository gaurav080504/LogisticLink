# backend/core/performance_test.py

import time
import random
from tsp_solver import solve_tsp_brute_force

def generate_random_matrix(n):
    """Generates a random symmetric distance matrix for N cities."""
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = random.uniform(10, 100)
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix

print(f"{'Cities (N)':<12} | {'Time Taken (sec)':<15} | {'Permutations (N-1)!':<20}")
print("-" * 55)

# Test from 4 to 10 cities
for n in range(4, 11):
    matrix = generate_random_matrix(n)
    
    # We only care about the duration here
    _, _, duration = solve_tsp_brute_force(matrix)
    
    # Mathematical permutations: (n-1)! because we fix the first city
    import math
    perms = math.factorial(n-1)
    
    print(f"{n:<12} | {duration:<15.6f} | {perms:<20}")

print("\nObservation: Notice how the time jumps! Imagine if N was 20 or 50...")