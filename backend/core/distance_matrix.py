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

# --- Test/Example ---
if __name__ == '__main__':
    # Define sample locations (e.g., London and Paris)
    london = Location(id=1, lat=51.5074, lon=0.1278)
    paris = Location(id=2, lat=48.8566, lon=2.3522)
    
    dist = calculate_haversine_distance(london, paris)
    # Expected distance is approx. 344 km (or 214 miles)
    print(f"Distance between London and Paris: {dist:.2f} km")