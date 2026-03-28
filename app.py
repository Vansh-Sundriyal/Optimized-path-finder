from flask import Flask, request, jsonify, render_template
import os

from core.router import Router
from core.vehicle import Vehicle
from core.weather import Weather
from core.traffic import Traffic
from core.weather_service import WeatherService

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

router = Router()
router.load_osm_from_place("Dehradun, Uttarakhand, India")

weather_service = WeatherService(
    api_key="dbd281892ba36f06f1abe34f87951589"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/route", methods=["POST"])
def route():
    data = request.json
    s = data["source"]
    d = data["destination"]
    v = data["vehicle"]

    vehicle = Vehicle(v["type"], v["width"], v["max_speed"], {})
    weather_raw = weather_service.get_weather(s["lat"], s["lon"])
    weather = Weather(**weather_raw)
    traffic = Traffic()

    # -------------------------------
    # MAIN ROUTE (shortest distance)
    # -------------------------------
    nodes_main, geo_main, avg_traffic_main = router.find_route(
        s["lat"], s["lon"],
        d["lat"], d["lon"],
        vehicle, weather, traffic,
        1.0, 1.0
    )

    # -------------------------------
    # ALTERNATE ROUTE (penalized)
    # -------------------------------
    penalty_fn = router.penalize_path(nodes_main)

    nodes_alt, geo_alt, avg_traffic_alt = router.find_route(
        s["lat"], s["lon"],
        d["lat"], d["lon"],
        vehicle, weather, traffic,
        1.0, 1.0,
        penalty_fn
    )

    def traffic_color(avg):
        if avg > 0.5:
            return "#ea4335"   
        elif avg > 0.25:
            return "#ff8c00"   
        return "#34a853"       

    def traffic_level(avg):
        if avg > 0.5:
            return "High"
        elif avg > 0.25:
            return "Medium"
        return "Low"

    def build_route(route_id, geo, avg_traffic):
        color = traffic_color(avg_traffic)

        segments = []
        for i in range(len(geo) - 1):
            segments.append({
                "coords": [
                    {"lat": geo[i][0], "lon": geo[i][1]},
                    {"lat": geo[i + 1][0], "lon": geo[i + 1][1]}
                ],
                "color": color
            })

        dist_km = router.compute_distance_km(geo)
        base_min_per_km = {
            "walk": 10,
            "bike": 3,
            "car": 4,
            "truck": 5
        }[vehicle.type]

        eta = round(dist_km * base_min_per_km, 1)

        return {
            "id": route_id,
            "segments": segments,
            "stats": {
                "distance_km": dist_km,
                "eta_min": eta
            },
            "traffic": traffic_level(avg_traffic),
            "reason": (
                "Shortest distance route"
                if route_id == "recommended"
                else "Alternative route"
            )
        }

    routes = [
        build_route("recommended", geo_main, avg_traffic_main),
        build_route("alternative", geo_alt, avg_traffic_alt)
    ]

    # Ensure recommended is first
    routes.sort(key=lambda r: r["id"] != "recommended")

    return jsonify({
        "routes": routes,
        "weather": weather_raw
    })


if __name__ == "__main__":
    app.run(debug=False)
