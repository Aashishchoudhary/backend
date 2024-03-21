import math

def haversine_distance(reference_lat, reference_lon, lat, lon):
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Convert degrees to radians
    reference_lat = math.radians(reference_lat)
    reference_lon = math.radians(reference_lon)
    lat = math.radians(lat)
    lon = math.radians(lon)

    # Haversine formula
    dlon = lon - reference_lon
    dlat = lat - reference_lat
    a = math.sin(dlat / 2)**2 + math.cos(reference_lat) * math.cos(lat) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance



# Example coordinates: New York City and Los Angeles


def find_nearby_library(reference_lat, reference_lon, coordinates, max_distance_km):
    nearby_coordinates = []

    for lat, lon in coordinates:
        distance = haversine_distance(reference_lat, reference_lon, lat, lon)
        if distance <= max_distance_km:
            nearby_coordinates.append((lat, lon))

    return nearby_coordinates


  
