# backend/core/clustering.py
from sklearn.cluster import KMeans
import numpy as np

def cluster_locations(locations, num_vehicles):
    """
    Groups locations into 'n' clusters based on geographic coordinates.
    """
    if len(locations) < num_vehicles:
        return [locations] # Not enough stops for all vehicles

    # Extract Lat/Lon for clustering
    coords = np.array([[loc.latitude, loc.longitude] for loc in locations])
    
    # We fix the depot (Stop 0) and cluster the rest
    depot = locations[0]
    other_locations = locations[1:]
    other_coords = coords[1:]

    kmeans = KMeans(n_clusters=num_vehicles, random_state=42, n_init=10)
    labels = kmeans.fit_predict(other_coords)

    clusters = [[] for _ in range(num_vehicles)]
    for idx, label in enumerate(labels):
        clusters[label].append(other_locations[idx])

    # Add the depot to the start of every vehicle's list
    for c in clusters:
        c.insert(0, depot)
        
    return clusters