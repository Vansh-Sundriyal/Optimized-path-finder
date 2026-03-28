import osmnx as ox
import networkx as nx


class OSMGraph:
    def __init__(self):
        self.graph = None

    def load_from_place(self, place_name: str):
        self.graph = ox.graph_from_place(
            place_name,
            network_type="drive"
        )

    def load_from_bbox(self, north, south, east, west):
        self.graph = ox.graph_from_bbox(
            north, south, east, west,
            network_type="drive"
        )

    def nearest_node(self, lat: float, lon: float) -> int:
        return ox.distance.nearest_nodes(
            self.graph,
            X=lon,
            Y=lat
        )

    def get_node_coords(self, node_id: int):
        node = self.graph.nodes[node_id]
        return node["y"], node["x"]

    def neighbors(self, node_id: int):
        for _, neighbor, edge_data in self.graph.edges(node_id, data=True):
            yield neighbor, edge_data
