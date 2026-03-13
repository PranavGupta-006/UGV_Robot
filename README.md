# UGV Path Finding System

A lightweight backend service that simulates autonomous path planning for an Unmanned Ground Vehicle (UGV) in a grid-based environment. The system generates a map with obstacles and computes the shortest navigable route between two points using the A* search algorithm.

The project exposes a REST API via FastAPI, allowing external applications, simulators, or visualization tools to request optimal paths dynamically. A frontend interface built with HTML, CSS, and JavaScript is included for interacting with the system directly in the browser.

---

## Overview

Autonomous ground vehicles must navigate environments containing obstacles while minimizing travel cost. This project implements a grid-based navigation system where:

- The environment is represented as a 2D grid (default 70x70)
- Cells may contain free space or obstacles placed randomly at a configurable density
- The grid is interpreted as an unweighted graph where each step has a cost of 1
- The A* algorithm computes the optimal path between a start and goal position using Manhattan distance as the heuristic

The backend returns the computed route via a REST API, making it suitable for integration with simulators, robotics interfaces, or custom visualization tools.

---

## Features

- Grid-based environment generation with configurable size and obstacle density
- Random obstacle placement to simulate real-world terrain variation
- A* pathfinding on a static grid
- Dynamic A* pathfinding where the grid regenerates on every node expansion
- Manhattan distance heuristic for efficient grid navigation
- REST API built with FastAPI
- Interactive frontend built with HTML, CSS, and JavaScript
- Lightweight and easily deployable with minimal dependencies

---

## Repository Structure

```
UGV_Robot/
│
├── ugv-path-finder/       Frontend interface (HTML, CSS, JavaScript)
├── app.py                 Main FastAPI backend entry point
├── app0.py                Core pathfinding logic and grid generation
├── package.json           Node metadata for frontend tooling
├── package-lock.json
├── .gitignore
└── README.md
```

---

## Algorithm

The environment is modeled as a graph where each grid cell is a node and adjacent cells form edges. All edge weights are uniform (cost of 1 per step).

**Supported movement directions:**

- Up
- Down
- Left
- Right

### A* Search

A* extends Dijkstra's algorithm by adding a heuristic function that estimates the remaining cost to the goal, allowing it to prioritize more promising paths and reach the solution faster.

For each candidate node, A* evaluates:

```
f(n) = g(n) + h(n)
```

Where:

- `g(n)` is the actual cost from the start to node `n`
- `h(n)` is the estimated cost from node `n` to the goal (heuristic)

The heuristic used is **Manhattan distance**, which is admissible and consistent for 4-directional grid movement:

```
h(a, b) = |a.x - b.x| + |a.y - b.y|
```

**Time Complexity:**

```
O((V + E) log V)
```

Where `V` = number of nodes (grid cells) and `E` = number of edges (adjacencies between cells).

### Two Pathfinding Modes

The system exposes two variants of A*:

**Static A* (`/astar`)**

Runs A* on the grid as it was when last generated. The grid remains fixed for the duration of the search. This is the standard mode for finding optimal paths in a known environment.

**Dynamic A* (`/astardynamic`)**

Runs A* but regenerates the entire grid on every node expansion. This simulates a continuously changing environment where obstacles appear and disappear in real time. Because the map changes mid-search, the returned path reflects the state of the grid at the moment the goal was reached, not the original grid. This mode is non-deterministic and is intended for experimentation with dynamic obstacle scenarios.

---

## Configuration

The following parameters are defined at the top of `app.py` and can be modified directly:

| Parameter   | Default | Description                                                     |
|-------------|---------|------------------------------------------------------------------|
| `SIZE`      | `70`    | Width and height of the grid in cells                           |
| `density`   | `0.25`  | Probability (0.0 to 1.0) that any given cell is an obstacle     |

Density can also be updated at runtime without restarting the server using the `/set-density` endpoint.

The start cell `(0, 0)` and goal cell `(69, 69)` are always guaranteed to be free of obstacles regardless of density.

---

## System Requirements

- Python 3.8 or higher
- pip
- A modern web browser (for the frontend)

---

## Installing Python and pip

**macOS**

```bash
# Check if Python is already installed
python3 --version

# Install via Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python

# Verify pip
pip3 --version
```

**Linux (Ubuntu / Debian)**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

python3 --version
pip3 --version
```

**Windows**

Download Python from [python.org/downloads](https://www.python.org/downloads/) and run the installer.

Important: Enable the option **Add Python to PATH** during installation.

```cmd
python --version
pip --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/PranavGupta-006/UGV_Robot.git
cd UGV_Robot
```

Create and activate a Python virtual environment:

```bash
# Create the environment
python3 -m venv venv

# Activate on macOS / Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

Install backend dependencies:

```bash
pip install fastapi uvicorn
```

---

## Running the Backend

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation (auto-generated by FastAPI):

```
http://127.0.0.1:8000/docs
```

---

## Running the Frontend

Open the `ugv-path-finder` directory and serve it with a local HTTP server:

```bash
cd ugv-path-finder

# Using Python's built-in HTTP server
python3 -m http.server 8080
```

Then open:

```
http://localhost:8080
```

The frontend communicates with the FastAPI backend to request path computations and display results.

---

## API Reference

### Generate a Grid

Generates a new random grid and stores it in memory. Must be called before running any pathfinding endpoint.

```
POST /generate-grid
```

**Response:**

```json
{
  "grid": [[0, 1, 0, ...], ...]
}
```

---

### Get the Current Grid

Returns the grid currently stored in memory.

```
GET /grid
```

**Response:**

```json
{
  "grid": [[0, 1, 0, ...], ...]
}
```

Returns an empty grid if no grid has been generated yet.

---

### Set Obstacle Density

Updates the density value used when generating future grids. Does not regenerate the current grid.

```
POST /set-density?value={density}
```

**Query Parameters:**

| Parameter | Type  | Description                                  |
|-----------|-------|----------------------------------------------|
| `value`   | float | Obstacle probability between 0.0 and 1.0     |

**Example:**

```
POST /set-density?value=0.3
```

**Response:**

```json
{
  "density": 0.3
}
```

---

### Run Static A*

Runs A* on the current stored grid. The grid does not change during the search.

```
GET /astar?start={x,y}&goal={x,y}
```

**Query Parameters:**

| Parameter | Type   | Description                              |
|-----------|--------|------------------------------------------|
| `start`   | string | Start cell as `"x,y"` (e.g. `"0,0"`)    |
| `goal`    | string | Goal cell as `"x,y"` (e.g. `"69,69"`)   |

**Example Request:**

```
GET /astar?start=0,0&goal=69,69
```

**Example Response:**

```json
{
  "path": [[0,0],[0,1],[1,1],[2,1]],
  "distance": 3
}
```

If no path exists:

```json
{
  "message": "No path found"
}
```

---

### Run Dynamic A*

Runs A* with the grid regenerating on every node expansion. Simulates a continuously changing obstacle environment.

```
GET /astardynamic?start={x,y}&goal={x,y}
```

**Query Parameters:**

| Parameter | Type   | Description                              |
|-----------|--------|------------------------------------------|
| `start`   | string | Start cell as `"x,y"` (e.g. `"0,0"`)    |
| `goal`    | string | Goal cell as `"x,y"` (e.g. `"69,69"`)   |

**Example Request:**

```
GET /astardynamic?start=0,0&goal=69,69
```

Response format is identical to `/astar`. Results are non-deterministic due to mid-search grid regeneration.

---

## Example Workflow

1. Start the FastAPI backend server
2. Call `POST /generate-grid` to create the obstacle map
3. Optionally call `GET /grid` to inspect the generated map
4. Call `GET /astar` or `GET /astardynamic` with start and goal coordinates
5. The backend runs A* and returns the path and step count
6. Open the frontend to interact with the system visually

---

## Use Cases

- Autonomous ground vehicle navigation simulations
- Robotics path planning research and prototyping
- Dynamic obstacle environment experimentation
- Graph search algorithm benchmarking and comparison
- Educational demonstrations of A* and heuristic search

---

## Future Improvements

- Diagonal movement support with adjusted cost (square root of 2)
- Weighted terrain cells for non-uniform movement costs
- Real-time map streaming via WebSockets
- Persistent grid state across requests without manual regeneration
- Interactive grid visualization with React or Three.js
- Integration with robotics simulators such as ROS or Gazebo
- Exportable path data for use in external simulations
- Benchmarking mode to compare static vs dynamic A* performance

---

## Technologies Used

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python, FastAPI, Uvicorn            |
| Algorithm | A* Search, Manhattan heuristic, heapq |
| Frontend  | HTML, CSS, JavaScript               |
| API       | REST (JSON responses)               |

---

## License

This project is intended for educational and research purposes.
