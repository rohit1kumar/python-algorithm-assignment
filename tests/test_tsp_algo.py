import pytest
from app.schemas import TSPInput
from app.services.tsp_solver import TSPSolver


@pytest.fixture
def small_tsp_input():
    return TSPInput(
        cities=["A", "B", "C"],
        distances={
            "A": {"B": 10, "C": 15},
            "B": {"A": 10, "C": 20},
            "C": {"A": 15, "B": 20},
        },
    )


def test_small_tsp(small_tsp_input):
    """Test TSP with small number of cities (exact solution)"""
    result = TSPSolver.solve(small_tsp_input)
    assert len(result.route) == 4  # Start + intermediate cities + return
    assert result.route[0] == result.route[-1]  # Returns to start
    assert set(result.route[:-1]) == set(small_tsp_input.cities)


@pytest.mark.parametrize("num_cities", [11, 15, 20])
def test_large_tsp(num_cities):
    """Test TSP with large number of cities (approximation solution)"""
    cities = [str(i) for i in range(num_cities)]
    distances = {
        city: {other: 10 if city != other else 0 for other in cities} for city in cities
    }
    data = TSPInput(cities=cities, distances=distances)
    result = TSPSolver.solve(data)

    assert len(result.route) == len(cities) + 1
    assert result.route[0] == result.route[-1]
    assert set(result.route[:-1]) == set(cities)
    assert result.total_distance > 0


def test_invalid_distances():
    """Test TSP with invalid distance matrix"""
    data = TSPInput(
        cities=["A", "B"],
        distances={
            "A": {"B": 10},
            # Missing distances for B
        },
    )
    with pytest.raises(ValueError):
        TSPSolver.solve(data)


def test_single_city_tsp():
    """Test TSP with single city"""
    data = TSPInput(cities=["A"], distances={"A": {"A": 0}})
    result = TSPSolver.solve(data)
    assert result.route == ["A", "A"]
    assert result.total_distance == 0


@pytest.mark.parametrize(
    "distances,expected_length",
    [
        (
            {
                "A": {"B": 10, "C": 15},
                "B": {"A": 5, "C": 20},
                "C": {"A": 15, "B": 10},
            },
            4,
        ),
        (
            {
                "A": {"B": 1, "C": 10},
                "B": {"A": 10, "C": 1},
                "C": {"A": 1, "B": 10},
            },
            4,
        ),
    ],
)
def test_asymmetric_distances_tsp(distances, expected_length):
    """Test TSP with asymmetric distances"""
    data = TSPInput(cities=["A", "B", "C"], distances=distances)
    result = TSPSolver.solve(data)
    assert len(result.route) == expected_length
    assert result.route[0] == result.route[-1]
