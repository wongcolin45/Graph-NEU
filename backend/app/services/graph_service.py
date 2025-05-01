
from sqlalchemy.orm import Session
from app.repositories.course_repo import CourseRepository
from app.services.course_service import CourseService
import networkx as nx
from collections import defaultdict




class GraphService:

    @staticmethod
    def create_graph(db: Session, root_course):

        G = nx.DiGraph()
        queue = [root_course]

        while queue:

            data = CourseService.get_course_data(db, queue.pop())
            node = data['course'].replace(' ','')

            if node not in G:

                G.add_node(node, data=data)

            # Add Edges
            next_courses = CourseRepository.get_next_courses(db, node)

            for next_node in next_courses:
                data = CourseService.get_course_data(db, next_node)
                if data is None:
                    continue
                course = data['course'].replace(' ','')

                if course not in G:
                    G.add_node(course, data=data)

                G.add_edge(node, course)

                # add to queue
                queue.append(next_node)

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
    def get_longest_layer(layers):
        longest = 0
        for layer in layers:
            if len(layer) > longest:
                longest = layers[layer]
        return longest


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
        horizontal_spacing = 300
        vertical_spacing = 250

        longest_layer = GraphService.get_longest_layer(layers)

        for layer, nodes in layer_to_nodes.items():

            padding = (longest_layer - len(nodes)) / 2 * horizontal_spacing

            for index, node in enumerate(nodes):

                x = index * horizontal_spacing + padding
                y = layer * vertical_spacing
                positions[node] = {"x": x, "y": y}

        # Convert to JSON format
        nodes = []
        edges = []

        for node in G.nodes:
            data = G.nodes[node]['data']
            data['label'] = data['course'] + ': ' + data['name']
            del data['prerequisites']
            attributes = data['attributes']
            attribute_description = ''
            if not attributes:
                attribute_description += 'n/a'
            else:
                for attribute in attributes:
                    attribute_description += attribute + ', '
            data['attributes'] = attribute_description

            nodes.append({
                'id': node,
                'position': positions[node],
                "data": data
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










