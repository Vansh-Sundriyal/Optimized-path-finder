import math

def compute_edge_cost(length_m, road_type, vehicle, weather, traffic):
    distance_km = length_m / 1000.0
    if distance_km <= 0:
        return math.inf

    base = {
        "walk": 10,
        "bike": 3,
        "car": 4,
        "truck": 5
    }.get(vehicle.type, 4)

    cost = distance_km * base

    if road_type in ["motorway", "trunk"]:
        cost *= 0.85
    elif road_type in ["residential", "service"]:
        cost *= 1.15

    cost *= (1 + min(traffic.congestion, 0.5))

    if weather.rain:
        cost *= 1.15
    if weather.fog:
        cost *= 1.2

    return cost
