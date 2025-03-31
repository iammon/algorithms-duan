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
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Step 1: Number of cities
    city_count = int(lines[0].strip())

    # Step 2: City names
    city_names = {}
    for i in range(city_count):
        city_name = lines[1 + i].strip()
        graph.add_vertex(city_name)
        city_names[i + 1] = city_name  # 1-based indexing

    # Step 3: Routes
    for line in lines[1 + city_count:]:
        parts = line.strip().split()
        if len(parts) != 4:
            continue  # skip malformed lines
        city1_index = int(parts[0])
        city2_index = int(parts[1])
        distance = int(parts[2])
        cost = float(parts[3])

        city1 = city_names[city1_index]
        city2 = city_names[city2_index]

        graph.add_edge(city1, city2, (distance, cost))

    return graph

def displayDirectRoutes(graph):
    city_count = len(graph.adjacency_list)

    # Count total undirected unique edges
    seen_edges = set()
    for city, neighbors in graph.adjacency_list.items():
        for neighbor, _ in neighbors:
            edge = tuple(sorted((city, neighbor)))
            seen_edges.add(edge)
    total_connections = len(seen_edges)

    print(f"There are {city_count} cities and {total_connections} direct connections.\n")

    for city in sorted(graph.adjacency_list.keys()):
        print(f"({city}):")
        for neighbor, (distance, cost) in graph.adjacency_list[city]:
            print(f"   {city}-{neighbor}, {distance} miles, ${cost:.2f}")
        print()

def main():
    filename = "airline1.txt"  # Replace with your actual file path if needed
    graph = load_graph_from_file(filename)
    displayDirectRoutes(graph)


if __name__ == "__main__":
    main()
