class RIPRouter:
    def __init__(self, name):
        self.name = name
        self.routing_table = {}
        self.neighbor_weights = {}

    # Add neighbors with their respective weights (cost)
    def add_neighbor(self, neighbor, weight):
        self.neighbor_weights[neighbor.name] = weight
        self.routing_table[neighbor.name] = {'next_router': neighbor.name, 'hops': weight}

    def update_table(self, neighbor, neighbor_table):
        for dest, hop_count in neighbor_table.items():
            if dest == self.name:  # Skip the route to itself
                continue
            new_hop_count = hop_count + self.neighbor_weights[neighbor]  # Add the cost to the neighbor
            if dest not in self.routing_table or self.routing_table[dest]['hops'] > new_hop_count:
                self.routing_table[dest] = {'next_router': neighbor, 'hops': new_hop_count}

    def send_update(self, neighbors):
        for neighbor in neighbors:
            neighbor.update_table(self.name, {k: v['hops'] for k, v in self.routing_table.items()})

    def print_routing_table(self):
        print(f"Routing Table for {self.name}:")
        for dest, info in self.routing_table.items():
            print(f"  Destination: {dest}, Next Router: {info['next_router']}, Hops: {info['hops']}")


# Create routers
routerA = RIPRouter('A')
routerC = RIPRouter('C')
routerD = RIPRouter('D')

# Add neighbors with weights for the undirected graph
routerA.add_neighbor(routerC, 8)  # A-C has weight 8
routerA.add_neighbor(routerD, 3)  # A-D has weight 3
routerC.add_neighbor(routerA, 8)  # C-A has weight 8
routerC.add_neighbor(routerD, 4)  # C-D has weight 4
routerD.add_neighbor(routerA, 3)  # D-A has weight 3
routerD.add_neighbor(routerC, 4)  # D-C has weight 4

# Perform a few rounds of RIP updates
for i in range(3):
    print(f"Round {i+1}")
    routerA.send_update([routerC, routerD])
    routerC.send_update([routerA, routerD])
    routerD.send_update([routerA, routerC])

    routerA.print_routing_table()
    routerC.print_routing_table()
    routerD.print_routing_table()
    print("----------------------------")
