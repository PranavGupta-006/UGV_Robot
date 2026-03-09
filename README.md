# UGV Path Finding Algorithm

A lightweight backend service that simulates path planning for an **Unmanned Ground Vehicle (UGV)** in a grid-based environment. The system generates a map with obstacles and computes the shortest path between two points using graph search algorithms.

The project exposes a REST API using **FastAPI**, allowing external applications or visualizers to request optimal paths dynamically.

---

## Overview

Autonomous ground vehicles must navigate environments containing obstacles while minimizing travel cost. This project implements a grid-based navigation system where:

* The environment is represented as a **2D grid**
* Cells may contain **free space or obstacles**
* The grid is interpreted as a **graph**
* The algorithm computes the **optimal path** between a start and goal position

The service returns the computed route via an API, making it suitable for integration with simulators, robotics interfaces, or visualization tools.

---

## Features

* Grid-based environment generation
* Random obstacle placement
* Graph-based path computation
* REST API interface using FastAPI
* Lightweight and easily deployable
* Designed for experimentation with pathfinding algorithms

---

## Project Structure

```
.
├── main.py          # FastAPI server and pathfinding logic
├── data.csv         # Optional graph dataset (if used)
├── requirements.txt # Python dependencies
└── README.md
```

---

## Pathfinding Approach

The environment is modeled as a **graph** where:

* Each grid cell is a node
* Adjacent cells form edges
* Edge weights represent movement cost

Typical movement directions include:

* Up
* Down
* Left
* Right

The algorithm maintains a **priority queue** and repeatedly expands the lowest-cost node until the destination is reached.

Common algorithms suitable for this framework include:

* Dijkstra's Algorithm
* A* Search
* Breadth-First Search (for uniform cost)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ugv-pathfinding.git
cd ugv-pathfinding
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Server

Start the FastAPI server using:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive API documentation:

```
http://127.0.0.1:8000/docs
```

---

## API Example

### Request

```
GET /path?start_x=0&start_y=0&end_x=20&end_y=30
```

### Response

```json
{
  "path": [[0,0],[0,1],[1,1],[2,1],...],
  "distance": 52
}
```

---

## Configuration

Important parameters that control the environment:

| Parameter     | Description                        |
| ------------- | ---------------------------------- |
| `SIZE`        | Size of the grid                   |
| `density`     | Probability of obstacles appearing |
| movement cost | Weight assigned to each step       |

These can be modified directly in the source code to simulate different terrains.

---

## Use Cases

This project can be extended for:

* Robotics navigation simulations
* Autonomous vehicle research
* Algorithm benchmarking
* Path planning visualization
* AI search algorithm experimentation

---

## Possible Improvements

Future extensions may include:

* A* heuristic optimization
* Diagonal movement
* Dynamic obstacle updates
* Real-time map streaming
* Frontend visualization using React or Three.js
* Integration with robotics simulators (ROS / Gazebo)

---

## Technologies Used

* Python
* FastAPI
* NumPy
* Heap-based priority queues
* Graph search algorithms

---

## License

This project is intended for educational and research purposes.
