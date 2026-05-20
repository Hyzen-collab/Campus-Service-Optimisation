import csv
import time
import matplotlib.pyplot as plt              #Used to draw graphs for time, memory, and operations

# PRIORITY MAPPING
priority_value = {
    "High": 1,
    "Medium": 2,
    "Low": 3
}

# CLEAN PRIORITY VALUE
def clean_priority(value):                   #Ensures priority values are consistent and valid
    parts = value.strip().split()            
    for p in parts:
        if p in priority_value:
            return p
    return "Low"                             #Default case if no valid priority is found, it assumes Low

# LOAD CSV DATA
def load_data(path):
    with open(path, newline='', encoding='utf-8') as file:        #ensures the file is automatically closed & avoids encoding problems
        data = list(csv.DictReader(file))                         #Converts it into a list of rows & reads each row as a dictionary
        for row in data:
            row["Priority"] = clean_priority(row["Priority"])     #Access the priority colum
        return data

# SORTING ALGORITHMS
def bubble_sort(data):
    arr = data[:]                      #Creates a copy of the list
    ops = 0                            
    n = len(arr)                       #Number of elements (stores the dataset size to control loop execution)

    for i in range(n):
        for j in range(0, n - i - 1):  #Each pass pushes the largest element to the end (-1 prevents index out of range error (arr[j+1]))
            ops += 1                   
            if priority_value[arr[j]["Priority"]] > priority_value[arr[j + 1]["Priority"]]:    #Compares numeric priority values (Higher number = lower priority)
                arr[j], arr[j + 1] = arr[j + 1], arr[j]                                        #Swaps elements if they are in the wrong order

    return ops                         #operation count (not sorted list)

def merge_sort(data):
    ops = 0

    def sort(arr):                     #Used to implement recursion
        nonlocal ops                   #Allows modifying ops defined outside this function
        if len(arr) <= 1:              #Base condition to terminate recursion (A list with 0 or 1 element already sorted)
            return arr                 

        mid = len(arr) // 2            #The list is divided into two halves
        left = sort(arr[:mid])         #The left half is recursively sorted
        right = sort(arr[mid:])        

        result = []                    #Temporary list is used to merge sorted halves
        i = j = 0                      #Pointers that track the current position in left and right sublists during merging

        while i < len(left) and j < len(right):             #The loop continues while both left and right lists still have elements to compare
            ops += 1
            if priority_value[left[i]["Priority"]] <= priority_value[right[j]["Priority"]]:     #Compares priorities
                result.append(left[i])
                i += 1                                      
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])                            #Add remaining elements (because they are already sort)
        return result 

    sort(data[:])                                           #Sorts copy of data
    return ops                                              #Returns operation count

# SEARCHING ALGORITHMS
def linear_search(data, target):
    ops = 0
    for item in data:                                       #Loops through entire list
        ops += 1                                            #Each check is an operation
        if item["RequestID"] == target:                     #Checks whether the current element matches the search target
            break
    return ops

def binary_search(data, target):
    ops = 0
    low, high = 0, len(data) - 1                            #Search range

    while low <= high:                                      #Continue until range collapses
        ops += 1
        mid = (low + high) // 2                             #The middle element is selected to divide the search space
        if data[mid]["RequestID"] == target:                #If middle element matches the target the search ends
            break
        elif data[mid]["RequestID"] < target:               #If the target is greater search continues in the right half         
            low = mid + 1                                   
        else:
            high = mid - 1                                  

    return ops

# CSV FILES & PATH
files = {
    100: "R_DATA (100).csv",
    200: "R_DATA (200).csv",
    500: "R_DATA (500).csv"
}

sizes = [100, 200, 500]                                        #List of integers (Used for loops & X axis graphs)

bubble_time, bubble_mem, bubble_ops = [], [], []
merge_time, merge_mem, merge_ops = [], [], []
linear_time, linear_mem, linear_ops = [], [], []
binary_time, binary_mem, binary_ops = [], [], []               #Three empty list for Execution time/Memory usage/Num of comparisons

# MAIN TESTING LOOP
for size in sizes:
    dataset = load_data(files[size])

    # ---------------- Bubble Sort ----------------
    start = time.perf_counter()                                 #Measure execution time
    ops = bubble_sort(dataset)                                  #Count the number of comparisons & Returns that count
    bubble_time.append((time.perf_counter() - start) * 1000)    #Convert to milliseconds & store
    bubble_ops.append(ops)                                      #Store the number of comparisons made by Bubble Sort
    bubble_mem.append(1)     # O(1) space

    # ---------------- Merge Sort -----------------
    start = time.perf_counter()
    ops = merge_sort(dataset)
    merge_time.append((time.perf_counter() - start) * 1000)
    merge_ops.append(ops)
    merge_mem.append(size)   # O(n) space

    # --------- Prepare data for searching --------
    sorted_data = sorted(dataset, key=lambda x: x["RequestID"])  #Creates a new sorted list
    target = sorted_data[-1]["RequestID"]                        #Selects last element & store (Represents worst-case scenario)

    # ---------------- Linear Search --------------
    start = time.perf_counter()
    linear_ops.append(linear_search(sorted_data, target))        #Check elements one by one/Count num of comparisons
    linear_time.append((time.perf_counter() - start) * 1000)
    linear_mem.append(size)  # O(n) access-based memory (linear access-based memory usage for different dataset sizes)

    # ---------------- Binary Search --------------
    start = time.perf_counter()
    binary_ops.append(binary_search(sorted_data, target))        #Repeatedly halves the search space/Count num of comparisons
    binary_time.append((time.perf_counter() - start) * 1000)
    binary_mem.append(1)     # O(1) space

# TERMINAL OUTPUT (As a text)
print("\nALGORITHM PERFORMANCE SUMMARY\n")

for i, size in enumerate(sizes):                                          #Access the dataset size & its corresponding index
    print(f"Data Size: {size}")                                           #Clearly labels which dataset results are being shown
    print("-" * 60)                                                       #Visual separation
    print(f"{'Algorithm':<15}{'Time(ms)':>10}{'Ops':>10}{'Memory':>15}")  #Visual alignment width
    print("-" * 60)

    print(f"{'Bubble Sort':<15}{bubble_time[i]:>10.3f}{bubble_ops[i]:>10}{bubble_mem[i]:>15}")    #Alignment & decimal places
    print(f"{'Merge Sort':<15}{merge_time[i]:>10.3f}{merge_ops[i]:>10}{merge_mem[i]:>15}")
    print(f"{'Linear Search':<15}{linear_time[i]:>10.3f}{linear_ops[i]:>10}{linear_mem[i]:>15}")
    print(f"{'Binary Search':<15}{binary_time[i]:>10.3f}{binary_ops[i]:>10}{binary_mem[i]:>15}")
    print()

# GRAPH FUNCTION
def show_graph(x, y1, y2, l1, l2, title, y_label):                         #designed to plot and compare two datasets on the same graph
    plt.figure()                                                           #Creates a new blank graph(Prevents overlapping with previous plots)
    plt.plot(x, y1, marker='o', label=l1)                                  #Plots y1 against x
    plt.plot(x, y2, marker='o', label=l2)
    plt.xlabel("Number of Records")
    plt.ylabel(y_label)                                                    #Uses dynamic label(represent time, memory or operations)
    plt.title(title)                                                       #Sets the graph title
    plt.legend()                                                           #Displays labels for both lines(to identify algorithms)
    plt.grid(True)                                                         #Grid lines are enabled for better visualization
    plt.show()
    plt.close()                                                            #This closes the figure to release resource(prevents overlapping plots in future calls)

# VISUALIZATION (6 GRAPHS)

# Sorting Graphs
show_graph(sizes, bubble_time, merge_time,                                 
           "Bubble Sort", "Merge Sort",                                    #X-axis: sizes->number of records                         
           "Sorting Execution Time", "Time (ms)")                          #Y-axis: execution time in milliseconds

show_graph(sizes, bubble_mem, merge_mem,
           "Bubble Sort", "Merge Sort",
           "Sorting Memory Usage", "Memory Units")

show_graph(sizes, bubble_ops, merge_ops,
           "Bubble Sort", "Merge Sort",
           "Sorting Operations", "Comparisons")

# Searching Graphs
show_graph(sizes, linear_time, binary_time,
           "Linear Search", "Binary Search",
           "Searching Execution Time", "Time (ms)")

show_graph(sizes, linear_mem, binary_mem,
           "Linear Search", "Binary Search",
           "Searching Memory Usage", "Memory Units")

show_graph(sizes, linear_ops, binary_ops,
           "Linear Search", "Binary Search",
           "Searching Operations", "Comparisons")


