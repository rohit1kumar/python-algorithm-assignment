from fastapi import FastAPI, HTTPException
from .schemas import TSPInput, TSPOutput, KnapsackInput, KnapsackOutput
from .services.tsp_solver import TSPSolver
from logging import getLogger

app = FastAPI()
logger = getLogger(__name__)


@app.post("/tsp/solve", response_model=TSPOutput)
async def solve_tsp(data: TSPInput):
    """Solve the Problem 1: Traveling Salesman"""
    try:
        return TSPSolver.solve(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in solving TSP: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/knapsack/solve", response_model=KnapsackOutput)
async def solve_knapsack(data: KnapsackInput):
    """Solve the Problem 2: Knapsack"""
    try:
        pass
    except Exception as e:
        logger.error(f"Error in solving TSP: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
