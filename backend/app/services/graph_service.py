from sqlalchemy.ext.asyncio import AsyncSession

from app.CourseFilter import CourseFilter
from app.repositories.course_repo import CourseRepository
from app.services.course_service import CourseService

import networkx as nx
from collections import defaultdict


class GraphService:

    @staticmethod
    async def create_graph(db: AsyncSession, root_course: str, input_filter: CourseFilter):
        G = nx.DiGraph()
        queue = [root_course]
        first = True

        while queue:
            current = queue.pop()

            # first call ignores filter per your original logic
            if first:
                data = await CourseService.get_course_data(db, current)
                first = False
            else:
                data = await CourseService.get_course_data(db, current, course_filter=input_filter)

            if data is None:
                continue

            node = data["course"].replace(" ", "")

            if node not in G:
                G.add_node(node, data=data)

            # Add Edges
            next_courses = await CourseRepository.get_next_courses(db, node, course_filter=input_filter)

            for next_node in next_courses:
                next_data = await CourseService.get_course_data(db, next_node, course_filter=input_filter)
                if next_data is None:
                    continue

                next_code = next_data["course"].replace(" ", "")

                if next_code not in G:
                    G.add_node(next_code, data=next_data)

                G.add_edge(node, next_code)

                # add to queue
                queue.append(next_node)

        return G

    @staticmethod
    def get_layers(graph: nx.DiGraph):
        layers: dict[str, int] = {}
        for node in nx.topological_sort(graph):
            parents = list(graph.predecessors(node))
            if not parents:
                layers[node] = 0
            else:
                layers[node] = 1 + max(layers[p] for p in parents)
        return layers

    @staticmethod
    def get_longest_layer(layers: dict[str, int]) -> int:
        """
        Return the maximum number of nodes in any layer.
        `layers` maps node -> layer_index, so we count nodes per layer.
        """
        counts = defaultdict(int)
        for _, layer_idx in layers.items():
            counts[layer_idx] += 1
        return max(counts.values(), default=0)

    @staticmethod
    def graph_to_json(G: nx.DiGraph, positions: dict[str, dict[str, float]]):
        # Convert to JSON format
        nodes = []
        edges = []

        for node in G.nodes:
            data = dict(G.nodes[node]["data"])  # copy so we can mutate safely
            data["label"] = f"{data['course']}: {data['name']}"
            # prune large/unused fields for the front-end
            data.pop("prerequisites", None)

            attributes = data.get("attributes") or []
            if not attributes:
                data["attributes"] = "n/a"
            else:
                data["attributes"] = ", ".join(attributes)

            nodes.append({
                "id": node,
                "position": positions[node],
                "data": data,
            })

        for source, target in G.edges:
            edges.append({
                "id": f"{source}-{target}",
                "source": source,
                "target": target,
            })

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    async def get_graph(db: AsyncSession, course: str, input_filter: CourseFilter):
        G = await GraphService.create_graph(db, course, input_filter)
        layers = GraphService.get_layers(G)

        layer_to_nodes: dict[int, list[str]] = defaultdict(list)
        for node, layer in layers.items():
            layer_to_nodes[layer].append(node)

        # calculate positions for each layer
        positions: dict[str, dict[str, float]] = {}
        horizontal_spacing = 300
        vertical_spacing = 250

        longest_layer_size = GraphService.get_longest_layer(layers)

        for layer, nodes in layer_to_nodes.items():
            padding = (longest_layer_size - len(nodes)) / 2 * horizontal_spacing
            for index, node in enumerate(nodes):
                x = index * horizontal_spacing + padding
                y = layer * vertical_spacing
                positions[node] = {"x": x, "y": y}

        return GraphService.graph_to_json(G, positions)
