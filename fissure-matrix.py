import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 12x12 Micro-grid (1=Walkable, 0=Wall, 2=Path, 3=Fissure)
grid_before = np.array([
    [0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 2, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 1, 1, 0, 0, 0, 0, 0], # Choke point
    [0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 0, 0]
])

# Deep copy and add the Earthshaker Fissure (Value 3) at Row 8
grid_after = np.copy(grid_before)
grid_after[8][4] = 3
grid_after[8][5] = 3
grid_after[8][6] = 3
# Remove the old path passing through the fissure
grid_after[8][4] = 3
grid_after[7][4] = 1
grid_after[6][4] = 1

# Define colors: 0:Black (Wall), 1:White (Floor), 2:Blue (Path), 3:Orange (Fissure)
cmap = mcolors.ListedColormap(['black', 'white', '#3498db', '#e67e22'])
bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

def plot_matrix(matrix, title, filename):
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(matrix, cmap=cmap, norm=norm)

    # Draw gridlines
    for x in range(12):
        for y in range(12):
            ax.axhline(y-0.5, color='gray', linewidth=0.5)
            ax.axvline(x-0.5, color='gray', linewidth=0.5)

    # Mark Start (S) and Goal (G)
    ax.text(5, 11, 'S', va='center', ha='center', color='green', fontweight='bold', fontsize=16)
    ax.text(2, 0, 'G', va='center', ha='center', color='red', fontweight='bold', fontsize=16)

    plt.title(title, pad=20, fontsize=14)
    plt.xticks([]) # Hide axis ticks
    plt.yticks([])
    plt.savefig(filename, bbox_inches='tight')
    print(f"Saved '{filename}'")

plot_matrix(grid_before, "A* Optimal Path (Before Fissure)", "matrix_before.pdf")
plot_matrix(grid_after, "Earthshaker Fissure Blocks the Path", "matrix_after.pdf")
