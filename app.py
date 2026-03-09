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

grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

for i in range(SIZE):
    for j in range(SIZE):
        if random.random() < density:
            grid[i][j] = 1

grid[0][0] = 0
grid[69][69] = 0


def astar(grid, start, goal):

    SIZE = len(grid)

    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}

    g_score = {start: 0}

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

        x, y = current

        for dx, dy in moves:

            nx = x + dx
            ny = y + dy
            neighbor = (nx, ny)

            if not (0 <= nx < SIZE and 0 <= ny < SIZE):
                continue

            if grid[nx][ny] == 1:
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, goal)

                heapq.heappush(open_set, (f_score, neighbor))

    return None


def parse_node(node: str):
    x, y = map(int, node.replace(" ", "").split(","))
    return (x, y)


@app.get("/astar")
def run_astar(start: str, goal: str):

    start_node = parse_node(start)
    goal_node = parse_node(goal)

    path = astar(grid, start_node, goal_node)

    if path is None:
        return {
            "start": start_node,
            "goal": goal_node,
            "path": None,
            "distance": None,
            "message": "No path found"
        }

    return {
        "start": start_node,
        "goal": goal_node,
        "path": path,
        "distance": len(path)
    }