let selectedVehicle = null;

function selectVehicle(type, event) {
    selectedVehicle = type;

    document
        .querySelectorAll(".vehicle-options button")
        .forEach(btn => btn.classList.remove("active"));

    event.target.classList.add("active");
}

function showStats(distance, eta, explanation, meta) {
    document.getElementById("routeTitle").innerText = meta.title;
    document.getElementById("distanceText").innerText = distance + " km";
    document.getElementById("etaText").innerText = eta + " min";
    document.getElementById("weatherText").innerText = meta.weather;
    document.getElementById("trafficText").innerText = meta.traffic;

    const list = document.getElementById("explanationList");
    list.innerHTML = "";

    explanation.forEach(t => {
        const li = document.createElement("li");
        li.innerText = "✔ " + t;
        list.appendChild(li);
    });

    document.getElementById("statsPanel").classList.remove("hidden");
}

function resetAll() {
    clearMarkers();
    clearPolylines();

    selectedVehicle = null;

    document
        .querySelectorAll(".vehicle-options button")
        .forEach(btn => btn.classList.remove("active"));

    document.getElementById("statsPanel").classList.add("hidden");
}
