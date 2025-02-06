from pydantic import BaseModel
from typing import List, Dict


class TSPInput(BaseModel):
    cities: List[str]
    distances: Dict[str, Dict[str, float]]

    def validate_distances(self):
        for city in self.cities:
            if city not in self.distances:
                raise ValueError(f"Missing distance mapping for city {city}")
            for other_city in self.cities:
                if city != other_city and other_city not in self.distances[city]:
                    raise ValueError(
                        f"Missing distance between {city} and {other_city}"
                    )


class TSPOutput(BaseModel):
    route: List[str]
    total_distance: float


class Item(BaseModel):
    name: str
    weight: float
    value: float


class KnapsackInput(BaseModel):
    max_weight: float
    items: List[Item]


class KnapsackOutput(BaseModel):
    selected_items: List[str]
    total_value: float
