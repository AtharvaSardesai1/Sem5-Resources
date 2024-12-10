import math
import heapq

graph = {"A": ["B", "E"], "B": ["K", "C", "E"], "C": ["D", "F"], "D": ["I"], "E": ["L"], "F": ["J", "K"], "G": [], "I": ["J"], "J": ["G"], "K": ["G"], "L": ["E", "K"]}
location = {"A": [1, 1], "B": [1, 4], "C": [2, 5], "D": [3, 7], "E": [3, 2], "F": [3, 5], "G": [8, 5], "I": [4, 8], "J": [6, 7], "K": [7, 3], "L": [6, 1]}

goal = "G"
goal_location = location[goal]

manhattan = {}
euclidean = {}
maximum = {}
for node in graph:
    manhattan[node] = abs(location[node][0] - goal_location[0]) + abs(location[node][1] - goal_location[1])
    euclidean[node] = math.sqrt((location[node][0] - goal_location[0]) ** 2 + (location[node][1] - goal_location[1]) ** 2)
    maximum[node] = max(abs(location[node][0] - goal_location[0]), abs(location[node][1] - goal_location[1]))

def print_openlist(openlist):
    print("Openlist:", [(node, h_score) for h_score, node in openlist])

def print_closedlist(closedlist):
    print("Closedlist:", closedlist)

def print_successors(graph, current, closedlist):
    successors = [neighbour for neighbour in graph[current] if neighbour not in closedlist]
    print("Successors of", current, ":", successors)

def print_path(parents, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = parents.get(current)
    path.reverse()
    print("Path:", " -> ".join(path))
    return path

def best_first_search(graph, start, goal, heuristic):
    openlist = []
    closedlist = set()
    parents = {start: None}
    heapq.heappush(openlist, (heuristic[start], start))
    
    while openlist: 
        print("\nCurrent State:")
        print_openlist(openlist)
        print_closedlist(closedlist)
        
        h_score, current = heapq.heappop(openlist)
        
        if current == goal:
            print(f"Goal {goal} reached using Best-First Search with the selected heuristic.")
            path = print_path(parents, start, goal)
            return
        
        closedlist.add(current)
        print(f"Visiting {current}, h(n) = {h_score}")
        
        print_successors(graph, current, closedlist)
        
        for neighbour in graph[current]:
            if neighbour in closedlist:
                continue
            
            if neighbour not in [n for _, n in openlist]:
                parents[neighbour] = current
                heapq.heappush(openlist, (heuristic[neighbour], neighbour))
                
    print(f"Goal {goal} not reachable using Best-First Search.")

print("Best-First Search with Manhattan Distance:")
best_first_search(graph, "A", goal, manhattan)
print("--------------------------------------------------")
print("Best-First Search with Euclidean Distance:")
best_first_search(graph, "A", goal, euclidean)
print("--------------------------------------------------")
print("Best-First Search with Maximum Distance:")
best_first_search(graph, "A", goal, maximum)
