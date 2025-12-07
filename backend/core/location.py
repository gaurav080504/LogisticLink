# location.py

class Location:
    """
    Represents a single delivery stop with a unique ID and geographical coordinates.
    """
    def __init__(self, id: int, lat: float, lon: float):
        # A unique identifier for the stop (e.g., Stop 1, Stop 2)
        self.id = id
        
        # Latitude (e.g., 34.0522)
        self.latitude = lat
        
        # Longitude (e.g., -118.2437)
        self.longitude = lon

    def __repr__(self):
        """A string representation for easy printing/debugging."""
        return f"Location(ID={self.id}, Lat={self.latitude:.4f}, Lon={self.longitude:.4f})"


# --- Test/Example ---
# You can test it by creating a few example locations (e.g., famous landmarks)
if __name__ == '__main__':
    # Coordinates for some well-known places for demonstration
    stop_a = Location(id=1, lat=40.7128, lon=-74.0060) # New York City
    stop_b = Location(id=2, lat=34.0522, lon=-118.2437) # Los Angeles
    
    print(stop_a)
    print(stop_b)