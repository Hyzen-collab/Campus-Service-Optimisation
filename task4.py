import csv
import math                                                                           
import time

# Load locations from CSV file
def load_locations(file_path):
    locations = {}                                                         #store location IDs as keys and (x, y) coordinates as values
    with open(file_path, mode="r", newline="") as file:                    #Opens the CSV file in read mode 
        reader = csv.DictReader(file)                                      #Reads the CSV file row by row as dictionaries
        for row in reader:                                                 
            locations[row["LocationID"]] = (int(row["X"]), int(row["Y"]))
    return locations

# File path
file_path = "locations.csv"
locations = load_locations(file_path)

# Exit if no locations loaded
if not locations:
    exit()

# Distance calculation
def distance(a, b):                                                #calculate distance between two locations
    x1, y1 = locations[a]
    x2, y2 = locations[b] 
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2), 2)        #Uses Euclidean distance formula to get straight line distance

# ------------------------------------
# Greedy Nearest-Neighbour Algorithm
# ------------------------------------
def greedy_route(start):
    unvisited = list(locations.keys())                              #List of all location IDs
    unvisited.remove(start)                                         #Remove the starting location from unvisited list

    route = [start]                                                 #Stores the route taken (Starts with the initial location)
    total_distance = 0
    current = start

    while unvisited:
        nearest = unvisited[0]                                      #Assumes the first unvisited location is the nearest 
        for loc in unvisited:
            if distance(current, loc) < distance(current, nearest):
                nearest = loc
        total_distance += distance(current, nearest)                #Adds the distance from current to the nearest location to total_distance
        route.append(nearest)                                       #Adds the nearest location to the route
        current = nearest                                           #Updates current to the newly visited location
        unvisited.remove(nearest)                                   #Removes the nearest location from unvisited

    return route, round(total_distance, 2)

# ------------------------------------
# Simple Dijkstra Algorithm 
# ------------------------------------
def dijkstra(start):
    unvisited = list(locations.keys())                              #List of all nodes not yet processed
    distances = {loc: float("inf") for loc in locations}            #Initializes all distances to infinity
    distances[start] = 0                                            #Sets the distance of the starting node to 0

    while unvisited:                                                #Runs until all nodes are processed
        current = unvisited[0]
        for loc in unvisited:
            if distances[loc] < distances[current]:                 #Selects the node with the smallest known distance
                current = loc
        unvisited.remove(current)                                   #Removes the current node from unvisited

        for neighbour in locations:                                               #Iterate through all other locations
            if neighbour != current: 
                new_distance = distances[current] + distance(current, neighbour)  #Total distance from start to neighbour 
                if new_distance < distances[neighbour]:                           #Checks new distance shorter than current shortest distance
                    distances[neighbour] = round(new_distance, 2)                 #Updates distance of that neighbour if shorter path is found
    return distances

# TERMINAL OUTPUT
print("\n********************")
print(" ROUTE OPTIMISATION")
print("***********************")

# Greedy Algorithm
start_time = time.perf_counter()
greedy_path, greedy_dist = greedy_route("L002")                     #The route list in order & total distance 
greedy_time = (time.perf_counter() - start_time) * 1000             #Calculates execution time in milliseconds(current time after algorithm finish)

#Display route, distance and execution time.
print("\nGreedy Nearest-Neighbour Route:")
print(" -> ".join(greedy_path) + " ->")                             #join() string method that concatenates elements of a list into a single string
print("Total Distance: ", greedy_dist)
print("Execution Time: ", round(greedy_time, 3), "ms")

# Dijkstra Algorithm
start_time = time.perf_counter()
dijkstra_dist = dijkstra("L001")
dijkstra_time = (time.perf_counter() - start_time) * 1000

print("\nDijkstra Shortest Distances from L001")
for loc in dijkstra_dist:                                           #Allows embeding variable directly in a string
    print(f"{loc} : {dijkstra_dist[loc]}")                          #Inserts the current locationID & the shortest distance for that location

print("Execution Time: ", round(dijkstra_time, 3), "ms")



