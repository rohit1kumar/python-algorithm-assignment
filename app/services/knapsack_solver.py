from ..schemas import KnapsackInput, KnapsackOutput


class KnapsackSolver:
    @staticmethod
    def solve(data: KnapsackInput) -> KnapsackOutput:
        if data.max_weight < 0:
            raise ValueError("Maximum weight cannot be negative")

        n = len(data.items)
        W = int(data.max_weight)
        dp = [[0.0 for _ in range(W + 1)] for _ in range(n + 1)]

        # Fill DP table
        for i in range(1, n + 1):
            for w in range(W + 1):
                if data.items[i - 1].weight <= w:
                    dp[i][w] = max(
                        data.items[i - 1].value
                        + dp[i - 1][int(w - data.items[i - 1].weight)],
                        dp[i - 1][w],
                    )
                else:
                    dp[i][w] = dp[i - 1][w]

        # Backtrack to find selected items
        selected_items = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_items.append(data.items[i - 1].name)
                w -= int(data.items[i - 1].weight)

        return KnapsackOutput(selected_items=selected_items[::-1], total_value=dp[n][W])
