const map = L.map("map").setView([30.3165, 78.0322], 13);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
}).addTo(map);

const greenIcon = new L.Icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/green-dot.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32]
});

const redIcon = new L.Icon({
    iconUrl: "https://maps.google.com/mapfiles/ms/icons/red-dot.png",
    iconSize: [32, 32],
    iconAnchor: [16, 32]
});

let source = null;
let destination = null;
let markers = [];
let polylines = [];
let activeRouteId = "recommended";

map.on("click", function (e) {
    if (!source) {
        source = { lat: e.latlng.lat, lon: e.latlng.lng };
        markers.push(L.marker(e.latlng, { icon: greenIcon }).addTo(map));
    } else if (!destination) {
        destination = { lat: e.latlng.lat, lon: e.latlng.lng };
        markers.push(L.marker(e.latlng, { icon: redIcon }).addTo(map));
    }
});

function drawAllRoutes(routes) {
    clearPolylines();

    routes.forEach(route => {
        const isActive = route.id === activeRouteId;

        route.segments.forEach(seg => {
            const line = L.polyline(
                seg.coords.map(p => [p.lat, p.lon]),
                {
                    color: seg.color,
                    weight: isActive ? 8 : 5,
                    opacity: isActive ? 1.0 : 0.55,
                    dashArray: route.id === "alternative" ? "8 6" : null
                }
            ).addTo(map);

            line.on("click", () => {
                activeRouteId = route.id;
                drawAllRoutes(routes);
            });

            polylines.push(line);
        });
    });
}

function clearPolylines() {
    polylines.forEach(p => map.removeLayer(p));
    polylines = [];
}

function clearMarkers() {
    markers.forEach(m => map.removeLayer(m));
    markers = [];
    source = null;
    destination = null;
}
