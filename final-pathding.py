import heapq
import time
import os
import math
from PIL import Image, ImageDraw

def load_dota_map_to_matrix(image_path):
    print(f"Loading map from {image_path}...")
    try:
        img = Image.open(image_path).convert('L')
    except FileNotFoundError:
        print(f"Error: Could not find {image_path}.")
        return None

    width, height = img.size
    dota_grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(1 if img.getpixel((x, y)) > 128 else 0)
        dota_grid.append(row)
    return dota_grid

# FIXED: Octile distance is required for 8-way grid movement to be admissible
def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

# --- A* IMPLEMENTATION (OPTIMIZED) ---
def a_star_search(grid, start, goal):
    height, width = len(grid), len(grid[0])
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    # 8-way movement
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    nodes_explored = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        nodes_explored += 1

        if current == goal:
            break

        for dx, dy in neighbors:
            next_node = (current[0] + dx, current[1] + dy)
            if 0 <= next_node[0] < width and 0 <= next_node[1] < height:
                if grid[next_node[1]][next_node[0]] == 1:
                    # FIXED: Diagonal movement costs sqrt(2), straight costs 1
                    step_cost = math.sqrt(2) if dx != 0 and dy != 0 else 1
                    new_cost = cost_so_far[current] + step_cost

                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + heuristic(goal, next_node)
                        heapq.heappush(frontier, (priority, next_node))
                        came_from[next_node] = current

    if goal not in came_from:
        return None, nodes_explored

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path, nodes_explored

# --- D* LITE FRAMEWORK ---
class DLite:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.height = len(grid)
        self.width = len(grid[0])

        self.g = {}
        self.rhs = {}
        self.U = [] # Priority Queue
        self.km = 0 # Key modifier for dynamic updates
        self.nodes_explored = 0

        # Initialize
        for y in range(self.height):
            for x in range(self.width):
                self.g[(x, y)] = float('inf')
                self.rhs[(x, y)] = float('inf')

        self.rhs[self.goal] = 0
        heapq.heappush(self.U, (self.calculate_key(self.goal), self.goal))

    def calculate_key(self, s):
        min_cost = min(self.g[s], self.rhs[s])
        return (min_cost + heuristic(self.start, s) + self.km, min_cost)

    def get_neighbors(self, u):
        neighbors = []
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in dirs:
            nx, ny = u[0] + dx, u[1] + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] == 1:
                neighbors.append((nx, ny))
        return neighbors

    def cost(self, u, v):
        if self.grid[u[1]][u[0]] == 0 or self.grid[v[1]][v[0]] == 0:
            return float('inf')
        return math.sqrt(2) if u[0] != v[0] and u[1] != v[1] else 1

    def update_vertex(self, u):
        if u != self.goal:
            self.rhs[u] = min([self.cost(u, s) + self.g[s] for s in self.get_neighbors(u)] or [float('inf')])

        # Remove u from queue if it's there
        self.U = [item for item in self.U if item[1] != u]
        heapq.heapify(self.U)

        if self.g[u] != self.rhs[u]:
            heapq.heappush(self.U, (self.calculate_key(u), u))

    def compute_shortest_path(self):
        while self.U and (self.U[0][0] < self.calculate_key(self.start) or self.rhs[self.start] != self.g[self.start]):
            self.nodes_explored += 1
            k_old, u = heapq.heappop(self.U)
            k_new = self.calculate_key(u)

            if k_old < k_new:
                heapq.heappush(self.U, (k_new, u))
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                for s in self.get_neighbors(u):
                    self.update_vertex(s)
            else:
                self.g[u] = float('inf')
                for s in self.get_neighbors(u) + [u]:
                    self.update_vertex(s)

    def extract_path(self):
        curr = self.start
        path = [curr]
        while curr != self.goal:
            neighbors = self.get_neighbors(curr)
            if not neighbors: return None
            # Find the neighbor that minimizes c(curr, s) + g(s)
            curr = min(neighbors, key=lambda s: self.cost(curr, s) + self.g[s])
            path.append(curr)
        return path

def visualize_path_on_map(image_path, path, output_filename):
    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError: return
    draw = ImageDraw.Draw(img)
    if path and len(path) > 1:
        draw.line(path, fill=(255, 0, 0), width=2)
        r = 4
        draw.ellipse((path[0][0]-r, path[0][1]-r, path[0][0]+r, path[0][1]+r), fill=(0, 255, 0)) # Start Green
        draw.ellipse((path[-1][0]-r, path[-1][1]-r, path[-1][0]+r, path[-1][1]+r), fill=(0, 100, 255)) # Goal Blue
    img.save(output_filename)

if __name__ == "__main__":
    # Ensure this points to the directory where your dota-map-coordinates.png is located
    PROJECT_DIR = "./"
    image_file = os.path.join(PROJECT_DIR, "dota-map-coordinates.png")

    navmesh = load_dota_map_to_matrix(image_file)

    if navmesh:
        # Approximate coordinates based on the uploaded image
        start_coord = (200, 195)
        goal_coord = (195, 100)

        print(f"\n--- Running A* Baseline ---")
        start_time = time.perf_counter()
        astar_path, astar_explored = a_star_search(navmesh, start_coord, goal_coord)
        print(f"A* Execution time: {(time.perf_counter() - start_time)*1000:.2f} ms")
        print(f"A* Nodes Explored: {astar_explored}")
        if astar_path: visualize_path_on_map(image_file, astar_path, "astar_result.png")

        print(f"\n--- Running D* Lite Initial Search ---")
        d_lite = DLite(navmesh, start_coord, goal_coord)
        start_time = time.perf_counter()
        d_lite.compute_shortest_path()
        print(f"D* Lite Initial Execution time: {(time.perf_counter() - start_time)*1000:.2f} ms")
        print(f"D* Lite Initial Nodes Explored: {d_lite.nodes_explored}")

        dlite_path = d_lite.extract_path()
        if dlite_path: visualize_path_on_map(image_file, dlite_path, "dlite_initial_result.png")

        # --- Simulate Dynamic Earthshaker Fissure ---
        print(f"\n--- Simulating Earthshaker Fissure Event ---")
        fissure_x, fissure_y = dlite_path[5][0], dlite_path[5][1] # Block the 5th step of the path
        navmesh[fissure_y][fissure_x] = 0
        navmesh[fissure_y][fissure_x+1] = 0

        # A* Recalculation (Full Restart)
        start_time = time.perf_counter()
        _, astar_recalc_explored = a_star_search(navmesh, start_coord, goal_coord)
        print(f"A* Recalculation Time: {(time.perf_counter() - start_time)*1000:.2f} ms (Nodes Explored: {astar_recalc_explored})")

        # D* Lite Local Update
        start_time = time.perf_counter()
        d_lite.km += heuristic(d_lite.start, d_lite.start) # Update Key Modifier
        d_lite.nodes_explored = 0 # Reset counter to measure only the update phase
        d_lite.update_vertex((fissure_x, fissure_y))
        d_lite.update_vertex((fissure_x+1, fissure_y))
        d_lite.compute_shortest_path()
        print(f"D* Lite Local Update Time: {(time.perf_counter() - start_time)*1000:.2f} ms (Nodes Explored: {d_lite.nodes_explored})")

        dlite_new_path = d_lite.extract_path()
        if dlite_new_path: visualize_path_on_map(image_file, dlite_new_path, "dlite_fissure_result.png")
