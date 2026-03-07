# backend/server.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from core.location import Location
from core.distance_matrix import create_distance_matrix, get_osrm_distance_matrix
from core.genetic_algorithm import GeneticAlgorithm

app = Flask(__name__)
CORS(app) # This allows your React/HTML frontend to talk to this API

@app.route('/solve', methods=['POST'])
def solve_tsp():
    data = request.json
    # Expected data: { "locations": [{"id": 0, "lat": 12.3, "lon": 45.6}, ...] }
    
    locations_data = data.get('locations', [])
    if len(locations_data) < 3:
        return jsonify({"error": "Need at least 3 locations"}), 400

    # 1. Convert JSON back into Location objects
    locations = [Location(loc['id'], loc['lat'], loc['lon']) for loc in locations_data]

    # --- NEW LOGIC: Try OSRM first, fallback to Haversine ---
    print("Fetching road distances from OSRM...")
    matrix = get_osrm_distance_matrix(locations)
    
    if matrix is None:
        print("OSRM failed. Using Haversine distances.")
        matrix = create_distance_matrix(locations)
    # -------------------------------------------------------

    # 3. Run GA (Lower generations for faster web response)
    ga = GeneticAlgorithm(matrix,locations, population_size=100, generations=500)
    best_route_indices, best_distance = ga.run()

    # 4. Return the result
    return jsonify({
        "route_indices": best_route_indices,
        "distance": round(best_distance, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)