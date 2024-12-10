import heapq

class OSPFRouter:
    def __init__(self, name, links):
        self.name = name
        self.links = links  # Links is a dictionary of neighbors with cost

    def dijkstra(self, network):
        distances = {router: float('inf') for router in network}
        distances[self.name] = 0
        priority_queue = [(0, self.name)]
        previous_nodes = {router: None for router in network}

        while priority_queue:
            current_distance, current_router = heapq.heappop(priority_queue)

            # If we find a larger distance in the queue, we skip processing
            if current_distance > distances[current_router]:
                continue

            for neighbor, weight in network[current_router].links.items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_router
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, previous_nodes

    def print_shortest_paths(self, distances, previous_nodes):
        print(f"Shortest paths from {self.name}:")
        for dest, distance in distances.items():
            if distance < float('inf'):
                path = []
                current = dest
                while current is not None:
                    path.insert(0, current)
                    current = previous_nodes[current]
                print(f"  To {dest}: Distance {distance}, Path: {' -> '.join(path)}")
            else:
                print(f"  To {dest}: unreachable")


# Create the network as a graph based on the image
network = {
    'u': OSPFRouter('u', {'v': 2, 'x': 1}),
    'v': OSPFRouter('v', {'u': 2, 'w': 3, 'x': 2}),
    'w': OSPFRouter('w', {'v': 3, 'y': 1, 'z': 5}),
    'x': OSPFRouter('x', {'u': 1, 'v': 2, 'y': 1}),
    'y': OSPFRouter('y', {'x': 1, 'w': 1, 'z': 2}),
    'z': OSPFRouter('z', {'w': 5, 'y': 2}),
}

# Each router runs Dijkstra's algorithm
for router_name, router in network.items():
    distances, previous_nodes = router.dijkstra(network)
    router.print_shortest_paths(distances, previous_nodes)
    print("----------------------------")
