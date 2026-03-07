# backend/server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import time

# Importing our custom modules
from core.location import Location
from core.distance_matrix import create_distance_matrix, get_osrm_distance_matrix
from core.genetic_algorithm import GeneticAlgorithm
from core.clustering import cluster_locations 

app = Flask(__name__)
CORS(app) # Allows the HTML frontend to communicate with this Python API

@app.route('/solve', methods=['POST'])
def solve_tsp():
    data = request.json
    
    # 1. Get data from frontend (locations list and number of vehicles)
    locations_data = data.get('locations', [])
    num_vehicles = int(data.get('vehicles', 1))
    
    # Safety check: We need enough points to form a route
    if len(locations_data) < 3:
        return jsonify({"error": "Need at least 3 locations"}), 400

    # 2. Convert the incoming JSON into Python "Location" objects
    # This now includes the 'priority' flag (True/False) from your right-clicks
    locations = [
        Location(loc['id'], loc['lat'], loc['lon'], loc.get('priority', False)) 
        for loc in locations_data
    ]

    # 3. SPLIT stops between vehicles using Clustering
    # This groups stops that are geographically close to each other
    print(f"Clustering {len(locations)} stops for {num_vehicles} vehicles...")
    clusters = cluster_locations(locations, num_vehicles)
    
    final_results = []
    
    # 4. Loop through each cluster and find the best route for that specific vehicle
    for cluster in clusters:
        if len(cluster) < 2: 
            continue # Skip if a vehicle has no stops assigned

        # --- DISTANCE LOGIC: Try Road distances (OSRM) first, then Crow-fly (Haversine) ---
        print(f"Fetching road distances for cluster of size {len(cluster)}...")
        matrix = get_osrm_distance_matrix(cluster)
        
        if matrix is None:
            # This is your Haversine fallback if OSRM is offline or fails
            print("OSRM failed or offline. Falling back to Haversine (Straight-line) distances.")
            matrix = create_distance_matrix(cluster)
        
        # 5. Run the Genetic Algorithm (The "Brain")
        # We track the time it takes to see how efficient the GA is
        start_ga = time.time()
        ga = GeneticAlgorithm(matrix, cluster, population_size=100, generations=500)
        best_route_indices, best_dist = ga.run()
        end_ga = time.time()

        # 6. Prepare the result for this specific vehicle
        # We map the cluster's internal index back to the original Marker ID
        final_results.append({
            "route_indices": [cluster[i].id for i in best_route_indices],
            "distance": round(best_dist, 2), # Distance in km
            "ga_time_ms": round((end_ga - start_ga) * 1000, 2) # Time in milliseconds
        })

    # 7. Return the final data back to the JavaScript frontend
    return jsonify({
        "vehicles": final_results,
        "total_vehicles_used": len(final_results)
    })

if __name__ == '__main__':
    # Running on Port 5000
    app.run(debug=True, port=5000)