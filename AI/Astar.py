import math
import heapq

graph = {"A" : ["B", "E"], "B" : ["K", "C", "E"], "C" : ["D", "F"], "D" : ["I"], "E" : ["L"], "F" : ["J", "K"], "G" : [], "I" : ["J"], "J" :["G"], "K" : ["G"], "L" :["E", "K"]}
location = {"A" : [1,1], "B" : [1,4], "C" : [2,5], "D" : [3,7], "E" : [3,2], "F" : [3,5], "G" : [8,5], "I" : [4,8], "J" : [6,7], "K" : [7,3], "L" : [6,1]}

goal = "G"
goal_location = location[goal]

manhattan = {}
euclidean = {}
maximum = {}
for node in graph:
    manhattan[node] = abs(location[node][0] - goal_location[0]) + abs(location[node][1] - goal_location[1])
    euclidean[node] = math.sqrt((location[node][0] - goal_location[0])**2 + (location[node][1] - goal_location[1])**2)
    maximum[node] = max(abs(location[node][0] - goal_location[0]), abs(location[node][1] - goal_location[1]))

def print_openlist(openlist):
    print("Openlist:", [(node, f_score) for f_score, node in openlist])

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

def calculate_path_cost(path, g_scores):
    # The cost of the path is the g_score of the goal node
    return g_scores[path[-1]]

def astar_manhattan(graph, start, goal):
    openlist = []
    closedlist = set()
    parents = {start: None}
    g_scores = {start: 0}
    heapq.heappush(openlist, (manhattan[start], start))  
    
    while openlist:
        print("\nCurrent State:")
        print_openlist(openlist)
        print_closedlist(closedlist)
        
        f_score, current = heapq.heappop(openlist)
        
        if current == goal:
            print(f"Goal {goal} reached using A* with Manhattan Distance.")
            path = print_path(parents, start, goal)
            cost = calculate_path_cost(path, g_scores)
            print(f"Total path cost: {cost}")
            return
        
        closedlist.add(current)
        print(f"Visiting {current}, f(n) = {f_score}")
        
        print_successors(graph, current, closedlist)
        
        for neighbour in graph[current]:
            if neighbour in closedlist:
                continue
            
            tentative_g_score = g_scores[current] + 1
            
            if neighbour not in [n for _, n in openlist]:
                parents[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_score = g_scores[neighbour] + manhattan[neighbour]
                heapq.heappush(openlist, (f_score, neighbour))
            elif tentative_g_score < g_scores.get(neighbour, float('inf')):
                parents[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_score = g_scores[neighbour] + manhattan[neighbour]
                heapq.heappush(openlist, (f_score, neighbour))
                
    print(f"Goal {goal} not reachable using A* with Manhattan Distance.")

def astar_euclidean(graph, start, goal):
    openlist = []
    closedlist = set()
    parents = {start: None}
    g_scores = {start: 0} 
    heapq.heappush(openlist, (euclidean[start], start)) 
    
    while openlist:
        print("\nCurrent State:")
        print_openlist(openlist)
        print_closedlist(closedlist)
        
        f_score, current = heapq.heappop(openlist)
        
        if current == goal:
            print(f"Goal {goal} reached using A* with Euclidean Distance.")
            path = print_path(parents, start, goal)
            cost = calculate_path_cost(path, g_scores)
            print(f"Total path cost: {cost}")
            return
        
        closedlist.add(current)
        print(f"Visiting {current}, f(n) = {f_score}")
        
        print_successors(graph, current, closedlist)
        
        for neighbour in graph[current]:
            if neighbour in closedlist:
                continue
            
            tentative_g_score = g_scores[current] + 1
            
            if neighbour not in [n for _, n in openlist]:
                parents[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_score = g_scores[neighbour] + euclidean[neighbour]
                heapq.heappush(openlist, (f_score, neighbour))
            elif tentative_g_score < g_scores.get(neighbour, float('inf')):
                parents[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_score = g_scores[neighbour] + euclidean[neighbour]
                heapq.heappush(openlist, (f_score, neighbour))
                
    print(f"Goal {goal} not reachable using A* with Euclidean Distance.")

def astar_maximum(graph, start, goal):
    openlist = []
    closedlist = set()
    parents = {start: None}
    g_scores = {start: 0}
    heapq.heappush(openlist, (maximum[start], start)) 
    
    while openlist:
        print("\nCurrent State:")
        print_openlist(openlist)
        print_closedlist(closedlist)
        
        f_score, current = heapq.heappop(openlist)
        
        if current == goal:
            print(f"Goal {goal} reached using A* with Maximum Distance.")
            path = print_path(parents, start, goal)
            cost = calculate_path_cost(path, g_scores)
            print(f"Total path cost: {cost}")
            return
        
        closedlist.add(current)
        print(f"Visiting {current}, f(n) = {f_score}")
        
        print_successors(graph, current, closedlist)
        
        for neighbour in graph[current]:
            if neighbour in closedlist:
                continue
            
            tentative_g_score = g_scores[current] + 1
            
            if neighbour not in [n for _, n in openlist]:
                parents[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_score = g_scores[neighbour] + maximum[neighbour]
                heapq.heappush(openlist, (f_score, neighbour))
            elif tentative_g_score < g_scores.get(neighbour, float('inf')):
                parents[neighbour] = current
                g_scores[neighbour] = tentative_g_score
                f_score = g_scores[neighbour] + maximum[neighbour]
                heapq.heappush(openlist, (f_score, neighbour))
                
    print(f"Goal {goal} not reachable using A* with Maximum Distance.")

print("A* Search with Manhattan Distance:")
astar_manhattan(graph, "A", goal)
print("--------------------------------------------------")
print("A* Search with Euclidean Distance:")
astar_euclidean(graph, "A", goal)
print("--------------------------------------------------")
print("A* Search with Maximum Distance:")
astar_maximum(graph, "A", goal)