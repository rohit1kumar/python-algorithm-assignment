from typing import Tuple, List, Set
from ..schemas import TSPInput, TSPOutput


class TSPSolver:
    @staticmethod
    def solve(data: TSPInput) -> TSPOutput:
        data.validate_distances()
        n = len(data.cities)
        return (
            TSPSolver._solve_exact(data)
            if n <= 10
            else TSPSolver._solve_approximation(data)
        )

    @staticmethod
    def _solve_exact(data: TSPInput) -> TSPOutput:
        n = len(data.cities)
        dp = {}

        def tsp_dp(mask: int, pos: int) -> Tuple[float, List[str]]:
            if mask == (1 << n) - 1:
                return (
                    data.distances[data.cities[pos]][data.cities[0]],
                    [data.cities[pos], data.cities[0]],
                )

            if (mask, pos) in dp:
                return dp[(mask, pos)]

            ans = float("inf")
            best_path = []

            for city_idx in range(n):
                if not mask & (1 << city_idx):
                    curr_city = data.cities[pos]
                    next_city = data.cities[city_idx]
                    new_mask = mask | (1 << city_idx)

                    dist, path = tsp_dp(new_mask, city_idx)
                    total_dist = data.distances[curr_city][next_city] + dist

                    if total_dist < ans:
                        ans = total_dist
                        best_path = [curr_city] + path

            dp[(mask, pos)] = (ans, best_path)
            return ans, best_path

        total_dist, route = tsp_dp(1, 0)
        return TSPOutput(route=route, total_distance=total_dist)

    @staticmethod
    def _solve_approximation(data: TSPInput) -> TSPOutput:
        unvisited: Set[str] = set(data.cities[1:])
        route = [data.cities[0]]
        total_distance = 0.0
        current_city = data.cities[0]

        while unvisited:
            next_city = min(unvisited, key=lambda x: data.distances[current_city][x])
            total_distance += data.distances[current_city][next_city]
            route.append(next_city)
            unvisited.remove(next_city)
            current_city = next_city

        total_distance += data.distances[current_city][data.cities[0]]
        route.append(data.cities[0])

        return TSPOutput(route=route, total_distance=total_distance)
