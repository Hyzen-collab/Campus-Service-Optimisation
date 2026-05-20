# Campus Service Management System

A Python-based system for managing and optimising campus service operations
including staff scheduling, route planning, and algorithm performance analysis.

## Project Structure

| File | Description |
|------|-------------|
| `Solution.py` | Greedy-based service scheduler with staff assignment |
| `task4.py` | Route optimisation comparing Greedy vs Dijkstra |
| `import_random.py` | Algorithm benchmarking with graphs |
| `requests.csv` | Campus service requests dataset |
| `staff.csv` | Staff roles and availability |
| `locations.csv` | Campus locations with coordinates |
| `R_DATA (100/200/500).csv` | Simulated datasets for benchmarking |

## Features
- Assigns staff to requests based on service type
- Greedy nearest-neighbour route planning from campus office
- Dijkstra shortest path algorithm comparison
- Bubble Sort vs Merge Sort benchmarking
- Linear Search vs Binary Search benchmarking
- Matplotlib graphs for visual performance comparison

## How to Run

Install dependencies:
pip install matplotlib

Run the scheduler:
python Solution.py

Run route optimisation:
python task4.py

Run algorithm analysis:
python import_random.py

## Requirements
- Python 3.x
- matplotlib
