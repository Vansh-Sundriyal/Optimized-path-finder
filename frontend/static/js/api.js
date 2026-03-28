async function findRoute() {
    if (!selectedVehicle || !source || !destination) {
        alert("Please select source, destination and vehicle");
        return;
    }

    const res = await fetch("/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            source,
            destination,
            vehicle: buildVehiclePayload()
        })
    });

    const data = await res.json();
    if (!data.routes || data.routes.length === 0) return;

    drawAllRoutes(data.routes);

    const r = data.routes[0];

    showStats(
        r.stats.distance_km,
        r.stats.eta_min,
        [r.reason],
        {
            title: "Recommended Route",
            weather: parseWeather(data.weather),
            traffic: r.traffic
        }
    );
}

function buildVehiclePayload() {
    return {
        type: selectedVehicle,
        width: selectedVehicle === "truck" ? 2.5 : 1.8,
        max_speed: selectedVehicle === "walk" ? 5 : 60
    };
}

function parseWeather(w) {
    if (w.rain) return "Rainy";
    if (w.fog) return "Foggy";
    if (w.high_wind) return "Windy";
    return "Clear";
}
