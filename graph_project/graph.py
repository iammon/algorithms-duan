import heapq
from collections import deque

class WeightedGraph:
    def __init__(self):
        # Initialize an empty dictionary to represent the adjacency list
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        """Add a weighted edge between two vertices."""
        if vertex1 not in self.adjacency_list:
            self.add_vertex(vertex1)
        if vertex2 not in self.adjacency_list:
            self.add_vertex(vertex2)

        # Add the edge with weight to the adjacency list
        self.adjacency_list[vertex1].append((vertex2, weight))
        self.adjacency_list[vertex2].append((vertex1, weight))  # undirected

    def remove_edge(self, vertex1, vertex2):
        """Remove the edge between two vertices."""
        if vertex1 in self.adjacency_list:
            self.adjacency_list[vertex1] = [
                (v, w) for v, w in self.adjacency_list[vertex1] if v != vertex2
            ]
        if vertex2 in self.adjacency_list:
            self.adjacency_list[vertex2] = [
                (v, w) for v, w in self.adjacency_list[vertex2] if v != vertex1
            ]

    def remove_vertex(self, vertex):
        """Remove a vertex and all its edges."""
        if vertex in self.adjacency_list:
            for adjacent in list(self.adjacency_list[vertex]):
                self.remove_edge(vertex, adjacent[0])
            del self.adjacency_list[vertex]

    def display(self):
        """Print the adjacency list."""
        for vertex, edges in self.adjacency_list.items():
            print(f"{vertex}: {edges}")

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

def displayDirectRoutes(graph, connections):
    city_count = len(graph.adjacency_list)

    # Count unique undirected connections
    unique_connections = set(tuple(sorted((src, dst))) for src, dst, *_ in connections)
    total_connections = len(unique_connections)

    print(f"There are {city_count} cities and {total_connections} direct connections.\n")

    for city in graph.adjacency_list:
        print(f"({city}):")
        for src, dst, distance, cost in connections:
            if city == src or city == dst:
                print(f"   {src}-{dst}, {distance} miles, ${cost:.2f}")
        print()

# display the MST
def displayMSTServiceRoute(graph):
    print("*** MINIMUM SPANNING TREE ***")
    print("(The edges in the MST based on distance):")

    # Step 1: Gather all edges (avoid duplicates in undirected graph)
    edges = set()
    for src in graph.adjacency_list:
        for dst, (distance, cost) in graph.adjacency_list[src]:
            edge = tuple(sorted((src, dst)))
            edges.add((edge[0], edge[1], distance, cost))  # sorted src, dst

    # Step 2: Sort edges by distance (for Kruskal's algorithm)
    sorted_edges = sorted(edges, key=lambda x: x[2])  # sort by distance

    # Step 3: Union-Find setup
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
            return False  # already connected
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        else:
            parent[yroot] = xroot
            if rank[xroot] == rank[yroot]:
                rank[xroot] += 1
        return True

    # Initialize disjoint set
    for city in graph.adjacency_list:
        parent[city] = city
        rank[city] = 0

    # Step 4: Build MST
    mst = []
    for src, dst, distance, cost in sorted_edges:
        if union(src, dst):
            mst.append((src, dst, distance, cost))

    # Step 5: Print MST edges
    for src, dst, distance, cost in mst:
        print(f"{src}-{dst}, {distance} miles, ${cost:.2f}")

    print()

def shortestPath(graph, cost_type, start, end):
    if start not in graph.adjacency_list or end not in graph.adjacency_list:
        print(f"Either {start} or {end} does not exist in the graph.")
        return

    if cost_type == "distance":
        cost_index = 0
        label = "miles"
        title = f"Shortest distance from ({start}) to ({end}):"
    elif cost_type == "price":
        cost_index = 1
        label = "$"
        title = f"Cheapest path from ({start}) to ({end}):"
    elif cost_type == "stops":
        return shortestPathByStops(graph, start, end)
    else:
        print("Invalid cost type.")
        return

    # Dijkstra’s algorithm
    pq = [(0, start, [])]  # (total cost, current city, path)
    visited = set()

    while pq:
        total_cost, current, path = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == end:
            # Print header
            if cost_type == "price":
                print(f"{title} ${total_cost:.2f}.")
            else:
                print(f"{title} {total_cost} {label}.")
            # Print path and cost of each link
            for i in range(len(path) - 1):
                for neighbor, (dist, price) in graph.adjacency_list[path[i]]:
                    if neighbor == path[i+1]:
                        segment_cost = (dist, price)[cost_index]
                        if cost_type == "price":
                            print(f"{path[i]}")
                            print(f"   ...{path[i+1]} : {segment_cost:.2f}")
                        else:
                            print(f"{path[i]}")
                            print(f"   ...{path[i+1]} : {segment_cost}")
                        break
            print()  # Add this blank line for formatting
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
                print(f"{path[i]}")
                print(f"   ...{path[i+1]}")
            print()  # Add this blank line to match formatting
            return

        visited.add(current)
        for neighbor, _ in graph.adjacency_list[current]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    print(f"No path found from {start} to {end}.\n")

def main():
    filename = "airline1.txt"
    graph, connections = load_graph_from_file(filename)
    displayDirectRoutes(graph, connections)
    displayMSTServiceRoute(graph)
    print("Testing shortest path from Akron to Cincinnati:")
    shortestPath(graph, "distance", "Akron", "Cincinnati")
    shortestPath(graph, "price", "Akron", "Cincinnati")
    shortestPath(graph, "stops", "Akron", "Cincinnati")

if __name__ == "__main__":
    main()
