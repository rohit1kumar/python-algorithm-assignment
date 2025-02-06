from typing import Tuple, List, Set
from ..schemas import TSPInput, TSPOutput


class TSPSolver:
    """
    Solves the Traveling Salesman Problem using exact and approximate methods.
    """

    @staticmethod
    def solve(data: TSPInput) -> TSPOutput:
        """
        Determines whether to use an exact or approximate solution based on the number of cities.
        """
        data.validate_distances()
        city_count = len(data.cities)
        if city_count <= 10:
            return TSPSolver._solve_exact(data)
        else:
            return TSPSolver._solve_approximation(data)

    @staticmethod
    def _solve_exact(data):
        """
        Solves the TSP exactly using dynamic programming with bitmasking.
        """
        city_count = len(data.cities)
        memoization = {}

        def tsp(mask: int, current_city_idx: int) -> Tuple[float, List[str]]:
            """
            Recursive function to find the shortest TSP path using dynamic programming.
            """
            if mask == (1 << city_count) - 1:
                return (
                    data.distances[data.cities[current_city_idx]][data.cities[0]],
                    [data.cities[current_city_idx], data.cities[0]],
                )

            if (mask, current_city_idx) in memoization:
                return memoization[(mask, current_city_idx)]

            min_distance = float("inf")
            best_route = []

            for next_city_idx in range(city_count):
                if (mask & (1 << next_city_idx)) == 0:
                    current_city = data.cities[current_city_idx]
                    next_city = data.cities[next_city_idx]
                    new_mask = mask | (1 << next_city_idx)

                    result = tsp(new_mask, next_city_idx)
                    distance = data.distances[current_city][next_city] + result[0]

                    if distance < min_distance:
                        min_distance = distance
                        best_route = [current_city] + result[1]

            memoization[(mask, current_city_idx)] = (min_distance, best_route)
            return min_distance, best_route

        result = tsp(1, 0)
        return TSPOutput(route=result[1], total_distance=result[0])

    @staticmethod
    def _solve_approximation(data):
        """
        Solves the TSP approximately using a greedy nearest-neighbor heuristic.
        """
        unvisited_cities: Set[str] = set(data.cities[1:])
        route = [data.cities[0]]
        total_distance = 0.0
        current_city = data.cities[0]

        while len(unvisited_cities) > 0:
            next_city = None
            min_distance = float("inf")
            for city in unvisited_cities:
                if data.distances[current_city][city] < min_distance:
                    min_distance = data.distances[current_city][city]
                    next_city = city

            total_distance += min_distance
            route.append(next_city)
            unvisited_cities.remove(next_city)
            current_city = next_city

        total_distance += data.distances[current_city][data.cities[0]]
        route.append(data.cities[0])

        return TSPOutput(route=route, total_distance=total_distance)
