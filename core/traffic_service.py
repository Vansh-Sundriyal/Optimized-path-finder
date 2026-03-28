import datetime


class TrafficService:
    """
    Returns congestion factor based on
    - time of day
    - road type

    Congestion scale:
    0.0 → free flow
    1.0 → fully congested
    """

    def get_congestion(self, road_type: str) -> float:
        hour = datetime.datetime.now().hour

        # Peak hours (morning & evening)
        is_peak = (8 <= hour <= 10) or (17 <= hour <= 19)

        if is_peak:
            if road_type in ["motorway", "trunk", "highway"]:
                return 0.25
            if road_type in ["primary", "secondary"]:
                return 0.4
            if road_type in ["residential", "service"]:
                return 0.6
        else:
            if road_type in ["motorway", "trunk", "highway"]:
                return 0.1
            if road_type in ["primary", "secondary"]:
                return 0.2
            if road_type in ["residential", "service"]:
                return 0.3

        return 0.2
