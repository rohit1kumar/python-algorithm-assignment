from ..schemas import KnapsackInput, KnapsackOutput


class KnapsackSolver:
    """
    Solves the 0/1 Knapsack problem using dynamic programming.
    """

    @staticmethod
    def solve(data: KnapsackInput) -> KnapsackOutput:
        """
        Solves the knapsack problem and returns the optimal selection of items.
        """
        if data.max_weight < 0:
            raise ValueError("Maximum weight cannot be negative")

        item_count = len(data.items)
        max_capacity = int(data.max_weight)
        dp_table = []
        for _ in range(item_count + 1):
            dp_table.append([0.0] * (max_capacity + 1))

        for item_idx in range(1, item_count + 1):
            for weight in range(max_capacity + 1):
                current_item = data.items[item_idx - 1]
                if current_item.weight <= weight:
                    dp_table[item_idx][weight] = max(
                        current_item.value
                        + dp_table[item_idx - 1][int(weight - current_item.weight)],
                        dp_table[item_idx - 1][weight],
                    )
                else:
                    dp_table[item_idx][weight] = dp_table[item_idx - 1][weight]

        selected_items = []
        remaining_weight = max_capacity
        for item_idx in range(item_count, 0, -1):
            if (
                dp_table[item_idx][remaining_weight]
                != dp_table[item_idx - 1][remaining_weight]
            ):
                selected_items.append(data.items[item_idx - 1].name)
                remaining_weight -= int(data.items[item_idx - 1].weight)

        return KnapsackOutput(
            selected_items=selected_items[::-1],
            total_value=dp_table[item_count][max_capacity],
        )
