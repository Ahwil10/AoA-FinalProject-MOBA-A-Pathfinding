# AoA-FinalProject-MOBA-A-Pathfinding

# Dynamic Graph Pathfinding in MOBA Environments

This repository contains the Python implementations and empirical data for a comparative analysis between the **A* (A-Star)** search algorithm and the dynamic **D* Lite** algorithm. 

This project was developed for the *Analysis of Algorithms* course at Yachay Tech University.

## 📌 Project Overview
Static pathfinding algorithms suffer from massive computational overhead when a graph's topology changes mid-execution. This project models the dynamic environments of Multiplayer Online Battle Arenas (MOBAs) like *Dota 2*. 

We extracted a discrete 12x12 micro-grid from the Source 2 Navigation Mesh to test how both algorithms respond to a simulated sudden terrain blockage (e.g., an Earthshaker Fissure).

## 🚀 Repository Structure
* `/src/`: Contains the native Python 3 implementations of A* and D* Lite.
* `/data/`: Contains the `gridnav.png` NavMesh extraction and the boolean matrix configurations.
* `/report/`: Contains the LaTeX source code (`.tex`, `.bib`, and images) for the formal 12-page TICEC-2026 formatted academic report.
* `/visualizations/`: Contains the output images of the pathfinding routes (`astar_result.png`).

## 🛠️ How to Run
1. Ensure you have Python 3 installed.
2. Install the required image processing library:
   `pip install Pillow`
3. Run the baseline pathfinder:
   `python src/devilesk-path-finding.py`

## 👨‍💻 Author
**Jefferson Daniel Lamiña Valencia**  
School of Mathematical and Computer Sciences, Yachay Tech University.
