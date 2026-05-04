import heapq
import time
import os
from PIL import Image, ImageDraw

def load_dota_map_to_matrix(image_path):
    """Loads the gridnav.png image and converts it to a 2D array."""
    print(f"Loading map from {image_path}...")
    try:
        img = Image.open(image_path).convert('L')
    except FileNotFoundError:
        print(f"Error: Could not find {image_path}. Make sure it is in the same folder!")
        return None

    width, height = img.size
    dota_grid = []

    for y in range(height):
        row = []
        for x in range(width):
            # White pixel (>128) means walkable (1), Black means obstacle (0)
            if img.getpixel((x, y)) > 128:
                row.append(1)
            else:
                row.append(0)
        dota_grid.append(row)

    print(f"Successfully loaded a {width}x{height} grid!")
    return dota_grid

def heuristic(a, b):
    """Calculates Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, goal):
    """
    Standard A* Algorithm.
    grid: 2D array where 1 is walkable, 0 is blocked.
    start, goal: (x, y) tuples.
    """
    height = len(grid)
    width = len(grid[0])

    # Priority queue stores tuples of (f_cost, current_node)
    frontier = []
    heapq.heappush(frontier, (0, start))

    # Dictionary to keep track of where we came from to reconstruct the path
    came_from = {}
    came_from[start] = None

    # Dictionary to track the exact cost from start to a given node (g_cost)
    cost_so_far = {}
    cost_so_far[start] = 0

    # 4-way movement (Up, Down, Left, Right).
    # Add diagonals like (1, 1) if you want 8-way movement.
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    nodes_explored = 0

    while frontier:
        # Get the node with the lowest f_cost
        current_cost, current = heapq.heappop(frontier)
        nodes_explored += 1

        # Early exit if we reached the goal
        if current == goal:
            break

        # Check all valid neighbors
        for dx, dy in neighbors:
            next_node = (current[0] + dx, current[1] + dy)

            # Ensure next_node is within map bounds
            if 0 <= next_node[0] < width and 0 <= next_node[1] < height:
                # Ensure it's not a tree/cliff (must equal 1)
                if grid[next_node[1]][next_node[0]] == 1:

                    # Cost is 1 per step (can adjust for diagonal vs straight)
                    new_cost = cost_so_far[current] + 1

                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + heuristic(goal, next_node)
                        heapq.heappush(frontier, (priority, next_node))
                        came_from[next_node] = current

    # Reconstruct path
    if goal not in came_from:
        return None, nodes_explored # Path not found

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, nodes_explored

    #Vizualizing the path
def visualize_path_on_map(image_path, path, output_filename):
    """
    Takes the original map image, draws the calculated path in red,
    and saves it as a new image file.
    """
    print("Generating visual output...")

    # Open the original image and convert to RGB so we can draw in color
    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print("Error: Could not load the image for drawing.")
        return

    draw = ImageDraw.Draw(img)

    if path and len(path) > 1:
        # Draw the path as a continuous red line (RGB: 255, 0, 0)
        # width=2 makes the line thick enough to easily see
        draw.line(path, fill=(255, 0, 0), width=2)

        # Optional but highly recommended: Draw markers for Start and Goal
        start = path[0]
        goal = path[-1]
        r = 4 # Radius of the marker dot

        # Green dot for Start
        draw.ellipse((start[0]-r, start[1]-r, start[0]+r, start[1]+r), fill=(0, 255, 0))
        # Blue dot for Goal
        draw.ellipse((goal[0]-r, goal[1]-r, goal[0]+r, goal[1]+r), fill=(0, 100, 255))

    # Save the new image
    img.save(output_filename)
    print(f"Success! Map saved as: {output_filename}")

if __name__ == "__main__":
    # Define your main project folder
    PROJECT_DIR = "/home/jefferson/Documents/AoA-project/"

    # Safely join the folder path with the file name
    image_file = os.path.join(PROJECT_DIR, "gridnav.png")

    navmesh = load_dota_map_to_matrix(image_file)

    if navmesh:
        # Coordinates Dire bot line to Radiant top lane
        # gridnav.png is 260*260
        start_coord = (199, 102)
        goal_coord = (200, 200)

        # Hopefully is walkable :/
        if navmesh[start_coord[1]][start_coord[0]] == 0 or navmesh[goal_coord[1]][goal_coord[0]] == 0:
            print("Warning: Start or Goal coordinate is inside a wall. Please pick new coordinates.")
        else:
            print(f"Finding path from {start_coord} to {goal_coord} using A*...")

            start_time = time.perf_counter()
            path, explored_count = a_star_search(navmesh, start_coord, goal_coord)
            end_time = time.perf_counter()

            if path:
                print(f"Path found! Length: {len(path)} steps.")
                print(f"Nodes explored: {explored_count}")
                print(f"Execution time: {end_time - start_time:.5f} seconds")
                output_file = os.path.join(PROJECT_DIR, "astar_result.png")
                visualize_path_on_map(image_file, path, output_file)
                # --- D* LITE LATER ---


            else:
                print("No valid path exists between these coordinates.")
