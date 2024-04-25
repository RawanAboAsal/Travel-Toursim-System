import heapq

class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def add_edge(self, start, end, weight):
        self.vertices.add(start)
        self.vertices.add(end)
        if start not in self.edges:
            self.edges[start] = []
        self.edges[start].append((end, weight))

def dijkstra(graph, start):
    # Initialize distances and the priority queue
    distances = {vertex: float('infinity') for vertex in graph.vertices}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Check if a shorter path has been found
        if current_distance > distances[current_vertex]:
            continue

        # Update distances for neighbors
        for neighbor, weight in graph.edges.get(current_vertex, []):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


co = "Company"
hu = "Hurghada"
sh = "Sharm el Sheikh"
al = "Alexandria"
nc = "North Coast"
go = "El Gouna"
ns = "North Sinai"
lu = "Luxor"
maz = "El Mazarita"
asw = "Aswan"
ps = "Port Said"

# Example usage:
if __name__ == "__main__":
    g = Graph()

    g.add_edge(co, go, 443)
    g.add_edge(go, hu, 32)
    g.add_edge(hu, go, 32)
    g.add_edge(go, co, 445)
    
    g.add_edge(hu, lu, 309)
    g.add_edge(lu, hu, 304)
    
    g.add_edge(co, sh, 502)
    g.add_edge(sh, co, 506)
    g.add_edge(co, ns, 263)
    g.add_edge(ns, co, 263)
    g.add_edge(co, ps, 200)
    g.add_edge(ps, co, 196)
    g.add_edge(ns, ps, 246)
    g.add_edge(ps, ns, 237)
    g.add_edge(ns, sh, 437)
    g.add_edge(sh, ns, 427)
    
    g.add_edge(co, lu, 658)
    g.add_edge(lu, maz, 65)
    g.add_edge(maz, asw, 40)
    g.add_edge(asw, maz, 40)
    g.add_edge(maz, lu, 65)
    g.add_edge(lu, co, 653)
    
    g.add_edge(co, al, 218)
    g.add_edge(al, nc, 64)
    g.add_edge(nc, al, 70)
    g.add_edge(al, co, 219)




    
    try:
        start_vertex = int(input(
        """
        Select the number of the following distination you want to start your trip from:
        1- Company
        2- Hurghada
        3- Sharm el Sheikh
        4- Alex
        5- North Coast
        6- El Gouna
        7- North Sinai
        8- Luxor
        9- El Mazarita
        10- Aswan
        11- Port Said
        
        """))


        if start_vertex in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
            if start_vertex == 1:
                start_dis = "Company"
            elif start_vertex == 2:
                start_dis = "Hurghada"
            elif start_vertex == 3:
                start_dis = "Sharm el Sheikh"
            elif start_vertex == 4:
                start_dis = "Alexandria"
            elif start_vertex == 5:
                start_dis = "North Coast"
            elif start_vertex == 6:
                start_dis = "El Gouna"
            elif start_vertex == 7:
                start_dis = "North Sinai"
            elif start_vertex == 8:
                start_dis = "Luxor"
            elif start_vertex == 9:
                start_dis = "El Mazarita"
            elif start_vertex == 10:
                start_dis = "Aswan"
            elif start_vertex == 11:
                start_dis = "Port Said"

            

            shortest_distances = dijkstra(g, start_dis)

            for vertex, distance in shortest_distances.items():
                if distance != 0:
                    print(f"Shortest distance from {start_dis} to {vertex}: {distance}")
        else:
            print("Sorry, the number you wrote is wrong")
    except ValueError as e:
        print("Invalid input. Please enter a number from the provided options.")
