import csv
import math

# CSV LOADER
def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:  #opens the CSV file and ensures it is closed automatically after reading
        return list(csv.DictReader(f))

# LOAD DATA FILES
requests = load_csv("requests.csv")
staff = load_csv("staff.csv")
locations = load_csv("locations.csv")


# PRIORITY RANKING (Dictionary that converts text priority -> numeric value)
priority_rank = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

# LOCATION DICTIONARY
location_map = {}
for loc in locations:                            #Loops through each row in the locations file
    location_map[loc["LocationID"]] = {          #Access current dictionary corresponding to the key
        "x": float(loc["X"]),
        "y": float(loc["Y"])                     #Stores X and Y coordinates as floats
    }

# STAFF ASSIGNMENT (Map service type to staff IDs)
staff_by_role = {}
for s in staff:                                  #s->Variable representing the current staff member
    role = s["Role"]                             #Extracts the staff member’s role from CSV
    if role not in staff_by_role:                #Prevents overwriting previous entries for the same role
        staff_by_role[role] = []                 #Store all staff IDs for that role                
    staff_by_role[role].append(s["StaffID"])     #Adds the current staff member’s ID to the list corresponding to their role


#Function to assign staff based on service type
def get_staff_id(service_type):
    # Return first available staff ID or 'NotAvailable' if none
    return staff_by_role.get(service_type, ["NotAvailable"])[0]


# DISTANCE FUNCTION (calculate distance between two points)
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)              #Uses Euclidean distance formula (Calculates straight-line distance between two coordinates)

# SORT REQUESTS BY PRIORITY (Takes one argument r (each element of requests)/ r["Priority"]->Accesses the "Priority" column of the current request
requests.sort(key=lambda r: priority_rank.get(r["Priority"], 99))      #modifies the original list & converts each request’s priority to a numeric value for sorting

# GREEDY ROUTE CONSTRUCTION (FROM OFFICE L001)
office_location = "L001"                           #storing the starting point of the route
current_position = office_location
visited = [office_location]                        #keeps the travel path

current_x = location_map[office_location]["x"]     #Retrieves the x-coordinate of the starting location from location_map
current_y = location_map[office_location]["y"]     

total_distance = 0

# FINAL OUTPUT
print("\n=============== FINAL SCHEDULE ===============\n")

for req in requests:                               #Processes each service request one by one
    target = req["LocationID"]                     #Extract LocationID of current request

    if target not in location_map:
        print(f"Request {req['RequestID']} location {target} not found!")   #Uses f-strings to print a formatted error message
        continue                                                            #Skip rest of the loop for this request and moves to next request

    tx = location_map[target]["x"]
    ty = location_map[target]["y"]                              #Gets target coordinates

    step_distance = distance((current_x, current_y), (tx, ty))  #Calculates distance from current location
    total_distance += step_distance

    visited.append(target)                          #Adds location to travel path

    staff_id = get_staff_id(req["ServiceType"])     #Assigns staff based on service type

    print(f"Task ID        : {req['RequestID']}")
    print(f"Assigned Staff : {staff_id}")
    print(f"Target Point   : {target}")
    print(f"Travel Path    : {' -> '.join(visited)}")            #Joins all elements in the visited list with " -> " to show the travel path
    print(f"Distance Used  : {round(total_distance, 2)} units")
    print("============================================")

    current_x, current_y = tx, ty                   
    current_position = target                       #Moves the current position to the target location for the next iteration
    



