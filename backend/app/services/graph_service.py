from sqlalchemy.orm import Session
from app.repositories.course_repo import CourseRepository
import networkx as nx
from collections import defaultdict

class GraphService:

    @staticmethod
    def create_graph(db: Session, root_course):

        G = nx.DiGraph()
        queue = [root_course]

        while queue:


            data = CourseRepository.get_course_data(db, queue.pop())
            node = data['course'].replace(' ','')

            if node not in G:
                name = data['course'] + ': ' + data['name']
                G.add_node(node, name=name)

            # Add Edges
            next_courses = CourseRepository.get_next_courses(db, node)

            for next_node in next_courses:
                data = CourseRepository.get_course_data(db, next_node)
                course = data['course'].replace(' ','')
                name = data['course'] + ': ' + data['name']

                if course not in G:
                    G.add_node(course, name=name)

                G.add_edge(node, course)

        return G

    @staticmethod
    def get_layers(graph: nx.DiGraph):
        layers = {}
        sorted_nodes = nx.topological_sort(graph)

        for node in sorted_nodes:
            parents = list(graph.predecessors(node))
            if not parents:
                layers[node] = 0
                continue
            highest = 0
            for parent in parents:
                highest = max(layers[parent], highest)
            layers[node] = highest + 1
        return layers

    @staticmethod
    def get_graph(db: Session, course):
        G = GraphService.create_graph(db, course)
        layers = GraphService.get_layers(G)

        layer_to_nodes = defaultdict(list)

        # assign nodes to each layer
        for node, layer in layers.items():
            layer_to_nodes[layer].append(node)


        # calculate positions for each layer
        positions = {}
        horizontal_spacing = 200
        vertical_spacing = 150

        for layer, nodes in layer_to_nodes.items():
            for index, node in enumerate(nodes):
                x = index * horizontal_spacing
                y = layer * vertical_spacing
                positions[node] = {"x": x, "y": y}

        nodes = []
        edges = []

        for node in G.nodes:
            nodes.append({
                'id': node,
                'position': positions[node],
                "data": {"label": node}  # or use your course name attribute
            })

        for source, target in G.edges:
            edges.append({
                "id": f"{source}-{target}",
                "source": source,
                "target": target
            })

        return {
            'nodes': nodes,
            'edges': edges
        }










