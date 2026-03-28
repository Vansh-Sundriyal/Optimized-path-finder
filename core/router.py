import heapq
import math
from typing import Callable

from core.osm_parser import OSMGraph
from core.cost import compute_edge_cost
from core.vehicle import Vehicle
from core.weather import Weather
from core.traffic import Traffic
from core.traffic_service import TrafficService


class Router:
    def __init__(self):
        self.osm = OSMGraph()
        self.traffic_service = TrafficService()
        self.graph_loaded = False

    def load_osm_from_place(self, place_name: str):
        self.osm.load_from_place(place_name)
        self.graph_loaded = True

    # -------------------------------------------------
    # DIJKSTRA: shortest-distance routing
    # -------------------------------------------------
    def find_route(
        self,
        start_lat,
        start_lon,
        goal_lat,
        goal_lon,
        vehicle: Vehicle,
        weather: Weather,
        traffic: Traffic,
        alpha,
        beta,
        edge_penalty_fn: Callable[[int, int], float] | None = None
    ):
        if not self.graph_loaded:
            raise RuntimeError("OSM graph not loaded")

        graph = self.osm.graph
        start = self.osm.nearest_node(start_lat, start_lon)
        goal = self.osm.nearest_node(goal_lat, goal_lon)

        pq = [(0.0, start)]
        dist = {start: 0.0}
        came_from = {}
        traffic_sum = {start: 0.0}
        edge_count = {start: 0}

        while pq:
            cur_dist, u = heapq.heappop(pq)

            if u == goal:
                break

            if cur_dist > dist.get(u, math.inf):
                continue

            for v in graph.successors(u):
                edge_data = graph[u][v][0]

                road_type = edge_data.get("highway", "residential")
                if isinstance(road_type, list):
                    road_type = road_type[0]

                traffic.congestion = self.traffic_service.get_congestion(road_type)

                class _Edge:
                    pass

                edge = _Edge()
                edge.length = edge_data.get("length", 0.0)
                edge.road_type = road_type

                cost = compute_edge_cost(
                    edge_data.get("length", 0.0),
                    road_type,
                    vehicle,
                    weather,
                    traffic
                )

                if edge_penalty_fn:
                    cost *= edge_penalty_fn(u, v)

                new_dist = dist[u] + cost

                if new_dist < dist.get(v, math.inf):
                    dist[v] = new_dist
                    came_from[v] = u
                    traffic_sum[v] = traffic_sum[u] + traffic.congestion
                    edge_count[v] = edge_count[u] + 1
                    heapq.heappush(pq, (new_dist, v))

        if goal not in came_from:
            return [], [], 0.0

        # Reconstruct path
        path_nodes = []
        geo_path = []

        cur = goal
        while cur != start:
            path_nodes.append(cur)
            lat, lon = self.osm.get_node_coords(cur)
            geo_path.append((lat, lon))
            cur = came_from[cur]

        path_nodes.append(start)
        lat, lon = self.osm.get_node_coords(start)
        geo_path.append((lat, lon))

        path_nodes.reverse()
        geo_path.reverse()

        avg_traffic = (
            traffic_sum.get(goal, 0.0) / max(edge_count.get(goal, 1), 1)
        )

        return path_nodes, geo_path, avg_traffic

    # -------------------------------------------------
    def penalize_path(self, node_path, penalty=1.3):
        penalized = set(zip(node_path, node_path[1:]))

        def fn(u, v):
            return penalty if (u, v) in penalized else 1.0

        return fn

    # -------------------------------------------------
    def compute_distance_km(self, geo_path):
        dist = 0.0
        for i in range(len(geo_path) - 1):
            lat1, lon1 = geo_path[i]
            lat2, lon2 = geo_path[i + 1]
            dist += math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 111
        return round(dist, 2)
