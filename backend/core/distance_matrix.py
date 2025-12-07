# backend/core/distance_matrix.py

import math
from location import Location  # Import the Location class you just created

# Radius of the Earth in kilometers. Use 3958.8 for miles.
R = 6371.0 

def calculate_haversine_distance(loc1: Location, loc2: Location) -> float:
    """
    Calculates the great-circle distance between two points 
    on the Earth using the Haversine formula.
    """
    # 1. Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(loc1.latitude)
    lon1_rad = math.radians(loc1.longitude)
    lat2_rad = math.radians(loc2.latitude)
    lon2_rad = math.radians(loc2.longitude)

    # 2. Calculate the difference in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # 3. Apply the Haversine formula (a = sin²(Δφ/2) + cos φ₁ ⋅ cos φ₂ ⋅ sin²(Δλ/2))
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    
    # 4. Calculate the central angle (c = 2 * atan2(√a, √(1−a)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 5. Calculate the distance
    distance = R * c
    
    return distance



# ... (Existing imports and calculate_haversine_distance function above) ...

def create_distance_matrix(locations: list[Location]) -> list[list[float]]:
    """
    Generates a 2D list (Adjacency Matrix) where M[i][j] is the distance 
    between Location i and Location j using the Haversine formula.
    """
    num_locations = len(locations)
    # Initialize the matrix with zeros
    matrix = [[0.0] * num_locations for _ in range(num_locations)]

    # Calculate distances for the upper triangular part (i < j)
    # and mirror them to the lower part for efficiency
    for i in range(num_locations):
        for j in range(i + 1, num_locations):
            loc_i = locations[i]
            loc_j = locations[j]
            
            # Calculate distance using the function from Step 1.2
            dist = calculate_haversine_distance(loc_i, loc_j)
            
            # Since Haversine is symmetric, set both M[i][j] and M[j][i]
            matrix[i][j] = dist
            matrix[j][i] = dist
            
    return matrix

# --- Test/Example ---
# Add this updated test block to the end of distance_matrix.py
if __name__ == '__main__':
    # 3 Example Locations (London, Paris, Berlin)
    london = Location(id=0, lat=51.5074, lon=0.1278)
    paris = Location(id=1, lat=48.8566, lon=2.3522)
    berlin = Location(id=2, lat=52.5200, lon=13.4050)
    
    cities = [london, paris, berlin]
    
    dist_matrix = create_distance_matrix(cities)

    print("\n--- 3-City Distance Matrix (in km) ---")
    for row in dist_matrix:
        print([f"{d:.2f}" for d in row])
        
    print("\nVerification:")
    # Distance from London (0) to Paris (1)
    print(f"London to Paris (Matrix[0][1]): {dist_matrix[0][1]:.2f} km") 
    # Distance from Paris (1) to Berlin (2)
    print(f"Paris to Berlin (Matrix[1][2]): {dist_matrix[1][2]:.2f} km")