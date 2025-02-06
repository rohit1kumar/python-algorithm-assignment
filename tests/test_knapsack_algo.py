import pytest
from app.schemas import KnapsackInput, KnapsackOutput, Item
from app.services.knapsack_solver import KnapsackSolver


def test_knapsack_basic():
    items = [
        Item(name="Item1", weight=2, value=3),
        Item(name="Item2", weight=3, value=4),
        Item(name="Item3", weight=4, value=5),
    ]
    knapsack_input = KnapsackInput(max_weight=5, items=items)
    result = KnapsackSolver.solve(knapsack_input)

    assert isinstance(result, KnapsackOutput)
    assert result.total_value == 7  # Expected optimal value
    assert set(result.selected_items) == {
        "Item1",
        "Item2",
    }  # Possible optimal selection


def test_knapsack_empty():
    knapsack_input = KnapsackInput(max_weight=5, items=[])
    result = KnapsackSolver.solve(knapsack_input)

    assert isinstance(result, KnapsackOutput)
    assert result.total_value == 0
    assert result.selected_items == []


def test_knapsack_no_fit():
    items = [
        Item(name="HeavyItem", weight=10, value=100),
    ]
    knapsack_input = KnapsackInput(max_weight=5, items=items)
    result = KnapsackSolver.solve(knapsack_input)

    assert isinstance(result, KnapsackOutput)
    assert result.total_value == 0
    assert result.selected_items == []


def test_knapsack_negative_weight():
    items = [
        Item(name="Item1", weight=1, value=1),
    ]
    knapsack_input = KnapsackInput(max_weight=-1, items=items)

    with pytest.raises(ValueError, match="Maximum weight cannot be negative"):
        KnapsackSolver.solve(knapsack_input)


def test_knapsack_fractional_weights():
    items = [
        Item(name="Item1", weight=2.5, value=3),
        Item(name="Item2", weight=1.5, value=2),
    ]
    knapsack_input = KnapsackInput(max_weight=4, items=items)
    result = KnapsackSolver.solve(knapsack_input)

    assert isinstance(result, KnapsackOutput)
    assert result.total_value == 3  # Since fractional weights are floored
    assert result.selected_items == ["Item1"]
