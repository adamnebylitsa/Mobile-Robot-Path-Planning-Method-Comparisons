# Enhanced Rapidly-exploring Random Trees (RRT) Planner Comparisions for Robotic Navigation

## Overview
This project aims to improve the performance of the standard RRT planner by altering various aspects of the algorithm. Key enhancements include the implementation of bidirectional search trees, a goal-biased sampling method, and a breadth-first search algorithm for node expansion. These modifications were tested in five different simulated environments, comparing their performance against the baseline RRT method.

## Features
- **Bidirectional Search Trees**: Implementation of trees growing simultaneously from start and end points to enhance connection possibilities and reduce pathfinding time.
- **Local Sampling Heuristic**: Optimizes the sampling process by focusing on promising areas of the environment, thereby increasing efficiency in reaching the target.
- **Breadth-First Search for Node Expansion**: Utilizes a breadth-first strategy to ensure broader coverage and potentially more optimal paths. Specifically, instead of seeking the nearest point in a traditional sense, this modification involves a BFS starting from the start position. The first node found with a clear path to the new position is deemed the "nearest" for expansion purposes. This approach aims to create paths with fewer nodes and potentially shorter distances, maintaining time efficiency.

## Environments
The simulations are run in environments created from text files, which define obstacles and boundaries within a grid. Each environment is converted into an occupancy grid, where each cell represents a potential space for navigation.

## Data and Reports 
For a more detailed analysis, including the comparative analysis of each method:
- [Project Report](https://docs.google.com/document/d/1uXCafIOUeDR7brnZ9s860canGNX_OtaCnkBKx8aKYig/edit?usp=sharing)
- [Performance Data Spreadsheet](https://docs.google.com/spreadsheets/d/1saFGm9w6gioqPoT8-3PXdp0LcrFLO6N5tdtV-hdf-JE/edit?usp=sharing)

## Citing
"RRT-Connect : An Efficient Approach to Single-Query Path Planning" by Kuffner (https://ieeexplore.ieee.org/document/844730)
