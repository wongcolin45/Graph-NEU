from app.CourseFilter import CourseFilter
from app.services.course_service import CourseService
from collections import defaultdict
import networkx as nx


class GraphService:

    def __init__(self, course_service: CourseService):
        self.course_service = course_service

    async def get_graph(self, course: str, input_filter: CourseFilter):
        G = await self.create_graph(course, input_filter)
        layers = self._get_layers(G)

        layer_to_nodes: dict[int, list[str]] = defaultdict(list)
        for node, layer in layers.items():
            layer_to_nodes[layer].append(node)

        layer_to_nodes = self._reduce_crossings(G, layer_to_nodes, iterations=8)

        positions: dict[str, dict[str, float]] = {}
        horizontal_spacing = 300
        vertical_spacing = 250

        longest_layer_size = self._get_longest_layer(layers)

        for layer, nodes in layer_to_nodes.items():
            padding = (longest_layer_size - len(nodes)) / 2 * horizontal_spacing
            for index, node in enumerate(nodes):
                x = index * horizontal_spacing + padding
                y = layer * vertical_spacing
                positions[node] = {"x": x, "y": y}

        return self._graph_to_json(G, positions)

    async def create_graph(self, root_course: str, input_filter: CourseFilter):
        g = nx.DiGraph()
        queue = [root_course]
        first = True

        while queue:
            current = queue.pop()

            if first:
                data = await self.course_service.get_course_data(current)
                first = False
            else:
                data = await self.course_service.get_course_data(current, course_filter=input_filter)

            if data is None:
                continue

            node = data["course"].replace(" ", "")

            if node not in g:
                g.add_node(node, data=data)

            next_courses = await self.course_service.get_next_courses(node, course_filter=input_filter)

            for next_node in next_courses:
                next_data = await self.course_service.get_course_data(next_node, course_filter=input_filter)
                if next_data is None:
                    continue

                next_code = next_data["course"].replace(" ", "")

                if next_code not in g:
                    g.add_node(next_code, data=next_data)

                g.add_edge(node, next_code)
                queue.append(next_node)

        return g

    def _get_layers(self, graph: nx.DiGraph):
        layers: dict[str, int] = {}
        for node in nx.topological_sort(graph):
            parents = list(graph.predecessors(node))
            if not parents:
                layers[node] = 0
            else:
                layers[node] = 1 + max(layers[p] for p in parents)
        return layers

    def _reduce_crossings(
        self,
        G: nx.DiGraph,
        layer_to_nodes: dict[int, list[str]],
        iterations: int = 8,
    ) -> dict[int, list[str]]:
        layer_ids = sorted(layer_to_nodes.keys())

        for lid in layer_ids:
            layer_to_nodes[lid] = sorted(layer_to_nodes[lid])

        def _barycenter(neighbor_pos: dict[str, int], neighbors: list[str]) -> float | None:
            pts = [neighbor_pos[n] for n in neighbors if n in neighbor_pos]
            if not pts:
                return None
            return sum(pts) / len(pts)

        for _ in range(iterations):
            changed = False

            for idx in range(1, len(layer_ids)):
                prev_layer = layer_ids[idx - 1]
                cur_layer = layer_ids[idx]

                prev_pos = {n: i for i, n in enumerate(layer_to_nodes[prev_layer])}
                old_order = list(layer_to_nodes[cur_layer])

                original_index = {v: i for i, v in enumerate(old_order)}
                scored: list[tuple[float | None, str]] = []

                for v in old_order:
                    parents = list(G.predecessors(v))
                    scored.append((_barycenter(prev_pos, parents), v))

                scored.sort(key=lambda t: (
                    1 if t[0] is None else 0,
                    float("inf") if t[0] is None else t[0],
                    original_index[t[1]],
                ))

                new_order = [v for _, v in scored]
                if new_order != old_order:
                    layer_to_nodes[cur_layer] = new_order
                    changed = True

            for idx in range(len(layer_ids) - 2, -1, -1):
                next_layer = layer_ids[idx + 1]
                cur_layer = layer_ids[idx]

                next_pos = {n: i for i, n in enumerate(layer_to_nodes[next_layer])}
                old_order = list(layer_to_nodes[cur_layer])

                original_index = {v: i for i, v in enumerate(old_order)}
                scored: list[tuple[float | None, str]] = []

                for v in old_order:
                    children = list(G.successors(v))
                    scored.append((_barycenter(next_pos, children), v))

                scored.sort(key=lambda t: (
                    1 if t[0] is None else 0,
                    float("inf") if t[0] is None else t[0],
                    original_index[t[1]],
                ))

                new_order = [v for _, v in scored]
                if new_order != old_order:
                    layer_to_nodes[cur_layer] = new_order
                    changed = True

            if not changed:
                break

        return layer_to_nodes

    def _get_longest_layer(self, layers: dict[str, int]) -> int:
        counts = defaultdict(int)
        for _, layer_idx in layers.items():
            counts[layer_idx] += 1
        return max(counts.values(), default=0)

    def _graph_to_json(self, g: nx.DiGraph, positions: dict[str, dict[str, float]]):
        nodes = []
        edges = []

        for node in g.nodes:
            data = dict(g.nodes[node]["data"])
            data["label"] = f"{data['course']}: {data['name']}"
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

        for source, target in g.edges:
            edges.append({
                "id": f"{source}-{target}",
                "source": source,
                "target": target,
            })

        return {"nodes": nodes, "edges": edges}
