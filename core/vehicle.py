from typing import Dict


class Vehicle:
    def __init__(
        self,
        vehicle_type: str,
        width: float,
        max_speed: float,
        mileage: Dict[str, float]
    ):
        self.type = vehicle_type        # car, bike, truck
        self.width = width              # meters
        self.max_speed = max_speed      # km/h
        self.mileage = mileage          # road_type -> km per liter
