import matplotlib.pyplot as plt
import networkx as nx


class WeightedGraphMixin:
    def __init__(self):
        super().__init__()
        self.edge_weights = {}

    def add_edge(self, vertex1, vertex2, weight=1):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            self.adj_list[vertex1].append(vertex2)
            self.edge_weights[(vertex1, vertex2)] = weight
            if isinstance(self, UndirectedGraph):
                self.adj_list[vertex2].append(vertex1)
                self.edge_weights[(vertex2, vertex1)] = weight
        else:
            raise ValueError("Одна или обе вершины не существуют в графе")

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            self.adj_list[vertex1].remove(vertex2)
            del self.edge_weights[(vertex1, vertex2)]
            if isinstance(self, UndirectedGraph):
                self.adj_list[vertex2].remove(vertex1)
                del self.edge_weights[(vertex2, vertex1)]
        else:
            raise ValueError("Одна или обе вершины не существуют в графе")

    def get_edges(self):
        edges = []
        for (vertex1, vertex2), weight in self.edge_weights.items():
            edges.append((vertex1, vertex2, weight))
        return edges

    def draw_graph(self):
        G = nx.DiGraph() if isinstance(self, DirectedGraph) else nx.Graph()
        for vertex in self.get_vertices():
            G.add_node(vertex)
        for edge in self.get_edges():
            G.add_edge(edge[0], edge[1], weight=edge[2])

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()


class BaseGraph:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def remove_vertex(self, vertex):
        if vertex in self.adj_list:
            for other in self.adj_list:
                if vertex in self.adj_list[other]:
                    self.adj_list[other].remove(vertex)
            del self.adj_list[vertex]
        else:
            raise ValueError("Вершина не существует в графе")

    def get_vertices(self):
        return list(self.adj_list.keys())

    def get_edges(self):
        edges = []
        for vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                edges.append((vertex, neighbor))
        return edges

    def __str__(self):
        result = ""
        for vertex, neighbors in self.adj_list.items():
            result += f"{vertex} -> {', '.join(map(str, neighbors))}\n"
        return result

    def draw_graph(self):
        raise NotImplementedError("Этот метод должен быть реализован в подклассе")


class UndirectedGraph(BaseGraph):
    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            self.adj_list[vertex1].append(vertex2)
            self.adj_list[vertex2].append(vertex1)
        else:
            raise ValueError("Одна или обе вершины не существуют в графе")

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            self.adj_list[vertex1].remove(vertex2)
            self.adj_list[vertex2].remove(vertex1)
        else:
            raise ValueError("Одна или обе вершины не существуют в графе")

    def draw_graph(self):
        G = nx.Graph()
        for vertex in self.get_vertices():
            G.add_node(vertex)
        for edge in self.get_edges():
            if (edge[1], edge[0]) not in G.edges:
                G.add_edge(*edge)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700)
        plt.show()


class DirectedGraph(BaseGraph, ):
    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            self.adj_list[vertex1].append(vertex2)
        else:
            raise ValueError("Одна или обе вершины не существуют в графе")

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            self.adj_list[vertex1].remove(vertex2)
        else:
            raise ValueError("Одна или обе вершины не существуют в графе")

    def draw_graph(self):
        G = nx.DiGraph()
        for vertex in self.get_vertices():
            G.add_node(vertex)
        for edge in self.get_edges():
            G.add_edge(*edge)

        pos = nx.kamada_kawai_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, arrowstyle='-|>',
                arrowsize=20)
        plt.show()


class WeightedUndirectedGraph(WeightedGraphMixin, UndirectedGraph):
    def __init__(self):
        super().__init__()


class WeightedDirectedGraph(WeightedGraphMixin, DirectedGraph):
    def __init__(self):
        super().__init__()


graph = WeightedDirectedGraph()

graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')
graph.add_edge('A', 'B')
graph.add_edge('A', 'C')

graph.add_vertex('D')
graph.add_vertex('F')
graph.add_vertex('G')
graph.add_edge('D', 'F')
graph.add_edge('F', 'G')
graph.add_edge('F', 'C')
graph.add_edge('G', 'C')
graph.add_edge('G', 'A')
graph.add_edge('G', 'B')
graph.add_edge('F', 'D')
graph.add_edge('A', 'G')


print(graph)

graph.draw_graph()
