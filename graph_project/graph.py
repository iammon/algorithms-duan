import heapq
from collections import deque

# used for displayDirectRoutes()
global_connections = []  

class WeightedGraph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)
        self.adjacency_list[vertex1].append((vertex2, weight))
        self.adjacency_list[vertex2].append((vertex1, weight))  # undirected

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adjacency_list:
            self.adjacency_list[vertex1] = [
                (v, w) for v, w in self.adjacency_list[vertex1] if v != vertex2
            ]
        if vertex2 in self.adjacency_list:
            self.adjacency_list[vertex2] = [
                (v, w) for v, w in self.adjacency_list[vertex2] if v != vertex1
            ]

    def remove_vertex(self, vertex):
        if vertex in self.adjacency_list:
            for adjacent in list(self.adjacency_list[vertex]):
                self.remove_edge(vertex, adjacent[0])
            del self.adjacency_list[vertex]

    def display(self):
        for vertex, edges in self.adjacency_list.items():
            print(f"{vertex}: {edges}")

def A_Project2(airlineDataFileName):
    print(airlineDataFileName, "...")
    graph = WeightedGraph()

    if airlineDataFileName.strip().lower() == "airline1.txt":
        global global_connections
        with open(airlineDataFileName, 'r') as file:
            lines = file.readlines()

        city_count = int(lines[0].strip())
        city_names = {}

        for i in range(city_count):
            city_name = lines[1 + i].strip()
            graph.add_vertex(city_name)
            city_names[i + 1] = city_name

        for line in lines[1 + city_count:]:
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            city1 = city_names[int(parts[0])]
            city2 = city_names[int(parts[1])]
            distance = int(parts[2])
            cost = float(parts[3])
            graph.add_edge(city1, city2, (distance, cost))
            global_connections.append((city1, city2, distance, cost))
        return graph

    # fallback dummy graph
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_vertex("D")
    graph.add_edge("A", "B", (4, 1))
    graph.add_edge("A", "C", (3, 1))
    graph.add_edge("B", "C", (2, 1))
    graph.add_edge("C", "D", (7, 1))
    return graph

def load_graph_from_file(filename):
    graph = WeightedGraph()
    connections = []  # store connections in original direction

    with open(filename, 'r') as file:
        lines = file.readlines()

    city_count = int(lines[0].strip())
    city_names = {}

    for i in range(city_count):
        city_name = lines[1 + i].strip()
        graph.add_vertex(city_name)
        city_names[i + 1] = city_name

    for line in lines[1 + city_count:]:
        parts = line.strip().split()
        if len(parts) != 4:
            continue
        city1_index = int(parts[0])
        city2_index = int(parts[1])
        distance = int(parts[2])
        cost = float(parts[3])

        city1 = city_names[city1_index]
        city2 = city_names[city2_index]

        graph.add_edge(city1, city2, (distance, cost))
        connections.append((city1, city2, distance, cost))  # only one direction

    return graph, connections

def displayDirectRoutes(graph):
    connections = global_connections
    city_count = len(graph.adjacency_list)
    unique_connections = set(tuple(sorted((src, dst))) for src, dst, *_ in connections)
    total_connections = len(unique_connections)
    print(f"There are {city_count} cities and {total_connections} direct connections.\n")
    seen = set()  # used only for total count
    for city in graph.adjacency_list:
        print(f"({city}):")
        printed = False
        for src, dst, distance, cost in connections:
            if city == src:
                print(f"   {src}-{dst}, {distance} miles, ${cost:.2f}")
                printed = True
                seen.add(tuple(sorted((src, dst))))
            elif city == dst:
                print(f"   {dst}-{src}, {distance} miles, ${cost:.2f}")
                printed = True
                seen.add(tuple(sorted((src, dst))))
        if not printed:
            print("   (no direct routes)")
        print()

# display the MST
def displayMSTServiceRoute(graph):
    print("*** MINIMUM SPANNING TREE ***")
    print("(The edges in the MST based on distance):")
    edges = set()
    for src in graph.adjacency_list:
        for dst, (distance, cost) in graph.adjacency_list[src]:
            edge = tuple(sorted((src, dst)))
            edges.add((edge[0], edge[1], distance, cost))
    sorted_edges = sorted(edges, key=lambda x: x[2])

    parent = {}
    rank = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        xroot = find(x)
        yroot = find(y)
        if xroot == yroot:
            return False
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        else:
            parent[yroot] = xroot
            if rank[xroot] == rank[yroot]:
                rank[xroot] += 1
        return True

    for city in graph.adjacency_list:
        parent[city] = city
        rank[city] = 0

    mst = []
    for src, dst, distance, cost in sorted_edges:
        if union(src, dst):
            mst.append((src, dst, distance, cost))

    for src, dst, distance, cost in mst:
        print(f"{src}-{dst}, {distance} miles, ${cost:.2f}")
    print()

def shortestPath(graph, cost_type, start, end):
    cost_type = cost_type.lower()
    if "distance" in cost_type:
        cost_index = 0
        label = "miles"
        title = f"Shortest distance from ({start}) to ({end}):"
    elif "price" in cost_type:
        cost_index = 1
        label = "$"
        title = f"Cheapest path from ({start}) to ({end}):"
    elif "stop" in cost_type:
        return shortestPathByStops(graph, start, end)
    else:
        print("Invalid cost type.")
        return

    pq = [(0, start, [])]
    visited = set()

    while pq:
        total_cost, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == end:
            if cost_index == 1:
                print(f"{title} ${total_cost:.2f}.")
            else:
                print(f"{title} {total_cost} {label}.")
            for i in range(len(path) - 1):
                for neighbor, (dist, price) in graph.adjacency_list[path[i]]:
                    if neighbor == path[i + 1]:
                        val = (dist, price)[cost_index]
                        if cost_index == 1:
                            print(f"{path[i]}\n   ...{path[i+1]} : {val:.2f}")
                        else:
                            print(f"{path[i]}\n   ...{path[i+1]} : {val}")
                        break
            print()
            return

        for neighbor, (dist, price) in graph.adjacency_list[current]:
            if neighbor not in visited:
                cost = (dist, price)[cost_index]
                heapq.heappush(pq, (total_cost + cost, neighbor, path))

    print(f"No path found from {start} to {end}.\n")

def shortestPathByStops(graph, start, end):
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == end:
            print(f"Path with least stops from ({start}) to ({end}): {len(path) - 1} stops.")
            for i in range(len(path) - 1):
                print(f"{path[i]}\n   ...{path[i+1]}")
            print()
            return

        visited.add(current)
        for neighbor, _ in graph.adjacency_list[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    print(f"No path found from {start} to {end}.\n")

def allAffordableTrips(graph, budget):
    print(f"All trips under budget ${budget:.2f} (Note: paths're duplicated & reversible):\n")
    numTrips = 0

    def dfs(current, start, visited, path, total_cost):
        nonlocal numTrips
        visited.add(current)
        for neighbor, (dist, price) in graph.adjacency_list[current]:
            if neighbor not in visited:
                new_cost = total_cost + price
                if new_cost <= budget:
                    print(f"({start}):")
                    print(f"...{current}-{neighbor}, {dist} miles, ${price:.2f}")
                    print(f"   Total cost: ${new_cost:.2f}.\n")
                    numTrips += 1
                    dfs(neighbor, start, visited.copy(), path + [neighbor], new_cost)

    for city in graph.adjacency_list:
        dfs(city, city, set(), [city], 0.0)

    print(f"With the budget, a total {numTrips} trips available.\n")


def main():
    # this is what we will use to grade your project 2

    # create an object for the airline network
    fileName = "airline1.txt"
    graph = A_Project2(fileName)

    print("\n... testing your implementation of Part I ...")
    displayDirectRoutes(graph)
    displayMSTServiceRoute(graph)

    print("\n... testing your implementation of Part II ...")
    cityA = "Akron"
    cityB = "Cincinnati"
    shortestPath(graph, "based on the distance", cityA, cityB)
    shortestPath(graph, "based on the price", cityA, cityB)
    shortestPath(graph, "based on the stops", cityA, cityB)

    print("\n... testing your implementation of Part III ...")
    allAffordableTrips(graph, 250)


if __name__ == "__main__":
    main()
