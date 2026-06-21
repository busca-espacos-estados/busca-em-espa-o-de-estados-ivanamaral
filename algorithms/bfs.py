from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        # Teste de objetivo na geração (BFS): verificamos o nó ao ser gerado.
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_generated=1, max_frontier_size=1)

        frontier = deque([initial])
        in_frontier = {initial}          # acompanha o conteúdo da fronteira para evitar duplicatas
        explored: set[State] = set()

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            node = frontier.popleft()
            in_frontier.discard(node)
            explored.add(node)
            nodes_expanded += 1

            for child in node.neighbors():
                if child in explored or child in in_frontier:
                    continue
                nodes_generated += 1
                if child.is_goal:
                    return SearchResult(
                        solution=child,
                        nodes_expanded=nodes_expanded,
                        nodes_generated=nodes_generated,
                        max_frontier_size=max_frontier_size,
                        depth=child.cost,
                    )
                frontier.append(child)
                in_frontier.add(child)

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
