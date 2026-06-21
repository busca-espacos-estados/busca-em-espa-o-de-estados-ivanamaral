from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        # Busca em profundidade limitada e iterativa usando uma pilha.
        frontier = [initial]             # pilha (LIFO)

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.pop()

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            # Respeita o limite de profundidade: não expande além dele.
            if node.cost >= self.depth_limit:
                continue

            nodes_expanded += 1

            # Evita ciclos no caminho atual (estados já visitados no ramo).
            ancestors = set(node.path())
            for child in node.neighbors():
                if child in ancestors:
                    continue
                nodes_generated += 1
                frontier.append(child)

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
