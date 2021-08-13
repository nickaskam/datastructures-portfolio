# Course: CS261 - Data Structures
# Student Name: Nick Askam
# Assignment: 6
# Description: Undirected Graph implementation, to add, track, remove edges and vertices. Also, tell if there's a cycle
#               , valid path, and count the connected

import heapq


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        self.adj_list[v] = list()
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u != v:
            # test if the vertex is in the list
            if u not in self.adj_list:
                self.add_vertex(u)

            if v not in self.adj_list:
                self.add_vertex(v)

            # see if the value is already in the list, if not remove
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        # make sure both are in the graph and are connected
        if (v in self.adj_list and u in self.adj_list) and v in self.adj_list[u] and u in self.adj_list[v]:
            # remove the vertex edges
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # remove vertex if in the graph
        if v in self.adj_list:
            for endpoints in self.adj_list:
                if endpoints in self.adj_list[v]:
                    self.remove_edge(v, endpoints)
            self.adj_list.pop(v)

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        heap = []
        for vertices in self.adj_list:
            heapq.heappush(heap, vertices)

        return heap

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_container = []
        # look in each vertex for each connector to add
        for vertex in self.adj_list:
            for element in self.adj_list[vertex]:
                # if it's already been added, do not add
                if (element, vertex) not in edge_container:
                    edge_container.append((vertex, element))
        return edge_container

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        # if the path is empty
        if not path:
            return True

        path_length = path.__len__()
        path_index = 0

        # if the path only has one element
        if path_length == 1:
            if path[0] in self.adj_list:
                return True
            else:
                return False

        while path_index < path_length:
            # if the path is in the list
            if path[path_index] in self.adj_list:
                # set what value should be checked based upon the index
                if path_index != path_length - 1:
                    path_index_check = path_index + 1
                else:
                    path_index_check = 0
                # make sure the next index can be reached
                if path[path_index_check] in self.adj_list[path[path_index]]:
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

        if v_start not in self.adj_list:
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
                # reverse the list
                reverse_list = sorted(self.adj_list[popped_vertex])[::-1]
                # test the next vertices to see if they should be checked next
                for vertex in reverse_list:
                    if vertex not in reachable_vertices:
                        stack.append(vertex)

        return reachable_vertices

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        reachable_vertices = []

        if v_start not in self.adj_list:
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

            # sort to find alphabetically
            sorted_vertices = sorted(self.adj_list[popped_vertex])
            # print("reachable: " + str(reachable_vertices))
            # print("sorted: " + str(sorted_vertices))
            for sibling in sorted_vertices:
                # do processing if the sibling is not in reachable vertices
                if sibling not in reachable_vertices:
                    reachable_vertices.append(sibling)
                    stack.insert(0, sibling)

                # return if at the end of the stack
                if sibling == v_end:
                    return reachable_vertices

        return reachable_vertices

    def count_connected_components(self) -> int:
        """
        Return number of connected components in the graph
        """
        # set the intro values
        connect_components = 0
        total_vertices = self.get_vertices()

        # while there are still vertices left to be counted
        while total_vertices:
            for vertex in total_vertices:
                total_vertices.remove(vertex)
                # if the vertices is in bfs, remove
                for value in self.bfs(vertex):
                    if value in total_vertices:
                        total_vertices.remove(value)
                connect_components += 1

        return connect_components

    def has_cycle(self) -> bool:
        """
        Return True if graph contains a cycle, False otherwise
        """
        available_vertices = self.get_vertices()
        # print(self.get_edges())
        for vertex in available_vertices:
            # set the parent and go digging to find the children
            parent = vertex
            for next_vertex in self.adj_list[vertex]:
                for next_next_vertex in self.adj_list[next_vertex]:
                    if next_next_vertex != parent:
                        found_parent = False
                        dfs_next_next_vertex = self.dfs(next_next_vertex)

                        # look in the dfs and see if a different path was taken to the parent (not reversed)
                        for vertex_in_dfw in dfs_next_next_vertex:
                            if vertex_in_dfw == next_vertex:
                                found_parent = True
                            if vertex_in_dfw == parent and not found_parent:
                                return True

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
