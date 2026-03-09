import random
import heapq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SIZE = 70
density = 0.25
grid = None


def generate_grid():
    global grid

    grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    for i in range(SIZE):
        for j in range(SIZE):
            if random.random() < density:
                grid[i][j] = 1

    grid[0][0] = 0
    grid[69][69] = 0

    return grid


def astar(grid, start, goal):

    SIZE = len(grid)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    def heuristic(a,b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    open_set = []
    heapq.heappush(open_set,(0,start))

    came_from = {}
    g_score = {start:0}

    while open_set:

        current = heapq.heappop(open_set)[1]

        if current == goal:

            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()
            return path

        x,y = current

        for dx,dy in moves:

            nx = x + dx
            ny = y + dy
            neighbor = (nx,ny)

            if not (0 <= nx < SIZE and 0 <= ny < SIZE):
                continue

            if grid[nx][ny] == 1:
                continue

            tentative = g_score[current] + 1

            if neighbor not in g_score or tentative < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = tentative

                f = tentative + heuristic(neighbor,goal)

                heapq.heappush(open_set,(f,neighbor))

    return None


def parse_node(node: str):
    try:
        x, y = map(int, node.replace(" ", "").split(","))
        return (x, y)
    except:
        return None


@app.post("/set-density")
def set_density(value: float):

    global density

    if not 0 <= value <= 1:
        return {"error": "density must be between 0 and 1"}

    density = value

    return {"density": density}


@app.post("/generate-grid")
def create_grid():
    grid = generate_grid()
    return {"grid": grid}


@app.get("/grid")
def get_grid():
    if grid is None:
        return {"grid": []}
    return {"grid": grid}


@app.get("/astar")
def run_astar(start: str, goal: str):

    if grid is None:
        return {"error": "grid not generated yet"}

    start_node = parse_node(start)
    goal_node = parse_node(goal)

    if start_node is None or goal_node is None:
        return {"error": "invalid start or goal format"}

    path = astar(grid, start_node, goal_node)

    if path is None:
        return {"message": "No path found"}

    return {
        "path": path,
        "distance": len(path) - 1
    }