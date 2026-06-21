import heapq
import itertools
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma das distâncias de cada peça até sua posição-alvo.

        É admissível (nunca superestima) porque cada movimento reposiciona uma única
        peça em exatamente uma casa adjacente.
        """
        # Posição-alvo de cada valor no estado objetivo.
        goal_pos = {value: index for index, value in enumerate(GOAL_STATE)}

        distance = 0
        for index, value in enumerate(state.tiles):
            if value == 0:  # o espaço vazio não conta
                continue
            row, col = divmod(index, 3)
            goal_row, goal_col = divmod(goal_pos[value], 3)
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        counter = itertools.count()      # desempate estável na fila de prioridade
        start_f = self.heuristic(initial)
        frontier = [(start_f, next(counter), initial)]
        # Melhor custo g conhecido para cada estado já alcançado.
        best_cost = {initial: 0}

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)

            # Entrada obsoleta: já encontramos um caminho melhor para este estado.
            if node.cost > best_cost.get(node, node.cost):
                continue

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            nodes_expanded += 1

            for child in node.neighbors():
                if child.cost < best_cost.get(child, float("inf")):
                    best_cost[child] = child.cost
                    nodes_generated += 1
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, next(counter), child))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
