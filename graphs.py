import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- 1. Data Setup (Replace with your actual script variables later) ---
scenarios = ['A* (Static Baseline)', 'A* (Full Recalculation)', 'D* Lite (Local Update)']
nodes_explored = [48, 85, 12] # A* recalc explores more due to the obstacle; D* explores less.
execution_times_ms = [1.25, 2.80, 0.45] # Converted to milliseconds for cleaner graphs

# --- 2. Generate Bar Chart: Nodes Explored ---
plt.figure(figsize=(8, 5))
bars = plt.bar(scenarios, nodes_explored, color=['#3498db', '#e74c3c', '#2ecc71'])
plt.title('Nodes Explored During Earthshaker Fissure Event', fontsize=14)
plt.ylabel('Number of Nodes', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('nodes_comparison.pdf') # PDF format is best for LaTeX!
print("Saved 'nodes_comparison.pdf'")

# --- 3. Generate Bar Chart: Execution Time ---
plt.figure(figsize=(8, 5))
bars = plt.bar(scenarios, execution_times_ms, color=['#2980b9', '#c0392b', '#27ae60'])
plt.title('Execution Time Comparison (Milliseconds)', fontsize=14)
plt.ylabel('Time (ms)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"{yval} ms", ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('time_comparison.pdf')
print("Saved 'time_comparison.pdf'")

# --- 4. Generate LaTeX Data Table ---
print("\n--- Copy this LaTeX Table into your Report ---")
df = pd.DataFrame({
    'Algorithm State': scenarios,
    'Nodes Explored': nodes_explored,
    'Execution Time (ms)': execution_times_ms
})

# Pandas can directly output LaTeX code!
latex_table = df.to_latex(index=False, column_format='lcc', escape=False)
# Manually adding booktabs formatting for a cleaner academic look
latex_table = latex_table.replace('\\toprule', '\\toprule\n\\textbf{Algorithm State} & \\textbf{Nodes Explored} & \\textbf{Execution Time (ms)} \\\\')
print(latex_table)
