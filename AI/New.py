import queue
import math

# Manhattan distance heuristic
def heuristic(current_node, goal_node):
    current_pos = location[current_node]
    goal_pos = location[goal_node]
    return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])

# Calculate the Euclidean distance between two nodes
def euclidean_distance(node1, node2):
    pos1 = location[node1]
    pos2 = location[node2]
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# Best-First Search implementation
def best_first_search(graph, start, goal):
    open_list = queue.PriorityQueue()
    open_list.put((0, start))

    came_from = {start: None}
    closed_list = set()

    iteration_states = []

    while not open_list.empty():
        priority, current = open_list.get()

        # Capture successors with distances
        successors = []
        for neighbor in graph[current]:
            if neighbor not in closed_list:
                distance = heuristic(neighbor, goal)
                successors.append((neighbor, distance))

        # Save the current state including successors
        open_list_contents = list(open_list.queue)
        iteration_states.append({
            'current_node': current,
            'open_list': open_list_contents,
            'closed_list': list(closed_list),
            'successors': successors
        })

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, list(closed_list), iteration_states

        closed_list.add(current)

        for neighbor, distance in successors:
            if neighbor not in closed_list:
                open_list.put((distance, neighbor))
                if neighbor not in came_from:
                    came_from[neighbor] = current

    return None, list(closed_list), iteration_states

# Graph and location data
graph = {
    "A": ["B", "E"],
    "B": ["K", "C", "E"],
    "C": ["D", "F"],
    "D": ["I"],
    "E": ["L"],
    "F": ["J", "K"],
    "G": [],
    "I": ["J"],
    "J": ["G"],
    "K": ["G"],
    "L": ["E", "K"]
}

location = {
    "A": [1, 1],
    "B": [1, 4],
    "C": [2, 5],
    "D": [3, 7],
    "E": [3, 2],
    "F": [5, 5],
    "G": [8, 5],
    "I": [4, 8],
    "J": [6, 7],
    "K": [7, 3],
    "L": [6, 1]
}

start = "D"
goal = "G"

# Running the search algorithm
path, closed_list, iteration_states = best_first_search(graph, start, goal)

# Calculate total distance traveled along the path
total_distance = 0
if path:
    for i in range(len(path) - 1):
        total_distance += euclidean_distance(path[i], path[i + 1])

# Output the results
print("Path:", path)
print("Final Closed List:", closed_list)
print("Total Distance Traveled:", total_distance)
print("\nIteration States:")

for i, state in enumerate(iteration_states):
    print()
    print(f"Iteration {i + 1}:")
    print("  Current Node:", state['current_node'])
    print("  Open List:", state['open_list'])
    print("  Closed List:", state['closed_list'])
    print("  Successors:", state['successors'])
    print()
