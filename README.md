# Optimized Path Finder

A smart route planning web app that finds the **best and alternative paths** using real road maps, live weather, and traffic-based cost optimization.

## Features

* Best + alternative route generation
* Real map routing with OpenStreetMap
* Traffic-aware path cost
* Weather-aware route adjustment
* Multiple vehicle modes
  `walk | bike | car | truck`
* Distance and ETA display
* Interactive map UI

## Tech Stack

* Python
* Flask
* OSMnx
* NetworkX
* JavaScript
* Leaflet.js

## Run

```bash
pip install -r requirements.txt
python app.py
```

## Open

```text
http://127.0.0.1:5000
```

## Working

* Loads road graph of Dehradun
* Uses Dijkstra-based optimized routing
* Applies traffic + weather penalties
* Generates recommended and alternative routes

## Core Logic

* `router.py` → routing engine
* `cost.py` → edge cost optimization
* `traffic_service.py` → congestion model
* `weather_service.py` → live weather integration

## Output

* Route on map
* Distance
* ETA
* Traffic level
* Weather status
