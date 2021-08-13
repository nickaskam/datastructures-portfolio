# Course: CS261 - Data Structures
# Student Name: Nick Askam
# Assignment: 6
# Description: Directed Graph that has implementation to add, get the edges, find if it has a cycle, dfs, bfs, etc

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        add a vertex to the graph
        """
        index = self.v_count
        v = index - 1
        self.adj_matrix.append([0] * (index + 1))
        while v >= 0:
            self.adj_matrix[v].append(0)
            v -= 1
        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add an edge to the graph
        """
        # add in the source and destination to the weight
        if self.v_count > src != dst < self.v_count:
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove an edge from the graph
        """
        if self.v_count > src >= 0 and self.v_count > dst >= 0 and self.adj_matrix[src][dst] != 0:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Get the vertices on the graph
        """
        vertices = []
        index_value = 0
        for _ in self.adj_matrix:
            vertices.append(index_value)
            index_value += 1
        return vertices

    def get_edges(self) -> []:
        """
        Get the edges on the graph
        """
        edges_in_graph = []
        source_index = 0

        # go through each list to find the values
        for source in self.adj_matrix:
            destination_index = 0
            for destination in source:
                if destination != 0:
                    edges_in_graph.append((source_index, destination_index, destination))
                destination_index += 1
            source_index += 1

        return edges_in_graph

    def is_valid_path(self, path: []) -> bool:
        """
        Find out if the path that is given is valid
        """
        # if the path is empty
        if not path:
            return True

        path_length = path.__len__()
        path_index = 0

        # if the path only has one element
        if path_length == 1:
            if path[0] in self.get_vertices():
                return True
            else:
                return False

        while path_index < path_length - 1:
            # if the path is in the list
            if path[path_index] in self.get_vertices():
                # change the path index check
                path_index_check = path_index + 1
                # see if it equals 0
                if self.adj_matrix[path[path_index]][path[path_index_check]] > 0:
                    path_index += 1
                else:
                    return False
            else:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        reachable_vertices = []

        if v_start not in self.get_vertices():
            return reachable_vertices

        stack = [v_start]

        # as long as the stack is not empty
        while stack.__len__() > 0:
            popped_vertex = stack.pop()
            # if the popped vertex is not in the current reachable vertices
            if popped_vertex not in reachable_vertices:
                reachable_vertices.append(popped_vertex)

                if popped_vertex == v_end:
                    return reachable_vertices

                # set the index to start looking at the end of the list and then go backwards
                vertex_index = len(self.get_vertices()) - 1
                for _ in self.adj_matrix[popped_vertex]:
                    # if the path length is not 0, add to the stack
                    if self.adj_matrix[popped_vertex][vertex_index] != 0:
                        stack.append(vertex_index)
                    vertex_index -= 1

        return reachable_vertices

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        reachable_vertices = []

        if v_start not in self.get_vertices():
            return reachable_vertices

        # set the stack constants
        stack = [v_start]
        reachable_vertices.append(v_start)

        # as long as the stack is not empty
        while stack.__len__() > 0:
            # pop the last element
            popped_vertex = stack.pop()
            # return if at the end of the stack
            if popped_vertex == v_end:
                return reachable_vertices

            vertex_index = 0
            for _ in self.adj_matrix[popped_vertex]:
                # do processing if the sibling is not in reachable vertices and the index is filled
                if self.adj_matrix[popped_vertex][vertex_index] != 0 and vertex_index not in reachable_vertices:
                    reachable_vertices.append(vertex_index)
                    stack.insert(0, vertex_index)

                # return if at the end of the stack
                if vertex_index == v_end:
                    return reachable_vertices

                vertex_index += 1

        return reachable_vertices

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        available_vertices = self.get_vertices()
        for vertex in available_vertices:
            # set the parent and go digging to find the children
            parent = vertex
            vertex_index = 0
            for _ in self.adj_matrix[vertex]:
                # if there is a connector, find the vertex then perform dfs. if parent is in dfs, return True
                if self.adj_matrix[vertex][vertex_index] != 0:
                    dfs = self.dfs(vertex_index)
                    if parent in dfs:
                        return True
                vertex_index += 1

        return False

    def dijkstra(self, src: int) -> []:
        """
        Find the shortest path between two points
        """
        # set the initial matrix
        distance = []
        for _ in self.get_vertices():
            distance.append(0)

        # create visited and priority queue
        visited = [src]
        priority_queue = [src]

        while priority_queue.__len__() > 0:
            priority_queue_value = priority_queue.pop()
            priority_queue_dist = distance[priority_queue_value]
            visited.append(priority_queue_value)

            # find the next set of values to test
            next_set = []
            next_set_index = 0

            for _ in self.adj_matrix[priority_queue_value]:
                if self.adj_matrix[priority_queue_value][next_set_index] != 0:
                    next_set.append(next_set_index)
                next_set_index += 1

            saved_distance = priority_queue_dist
            # test each value to the point in the graph
            for vertex in next_set:
                # make sure distance is reset at each iteration
                priority_queue_dist = saved_distance
                # set the new distance
                new_distance = priority_queue_dist + self.adj_matrix[priority_queue_value][vertex]
                if distance[vertex] == 0 or distance[vertex] > new_distance:
                    distance[vertex] = new_distance
                    priority_queue.append(vertex)

        # make values inf if they do not exist and replace 0
        mapping_key = 0
        for _ in distance:
            if mapping_key != src and distance[mapping_key] == 0:
                distance[mapping_key] = float('inf')
            elif mapping_key == src:
                distance[mapping_key] = 0
            mapping_key += 1

        return distance


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
