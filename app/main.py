import os
from logging import getLogger
from functools import lru_cache
from fastapi import FastAPI, HTTPException, Depends
from .schemas import TSPInput, TSPOutput, KnapsackInput, KnapsackOutput
from .services.tsp_solver import TSPSolver
from .services.knapsack_solver import KnapsackSolver
from .cache import CacheService

app = FastAPI()
logger = getLogger(__name__)


@lru_cache()
def get_cache():
    return CacheService(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Close Redis connection on shutdown"""
    cache = get_cache()
    await cache.close()


@app.post("/tsp/solve", response_model=TSPOutput)
async def solve_tsp(data: TSPInput, cache: CacheService = Depends(get_cache)):
    """Solve the Problem 1: Traveling Salesman"""
    try:
        # Generate cache key
        cache_key = await cache.get_key("tsp", data.dict())

        # Check cache
        cached_result = await cache.get(cache_key)
        if cached_result:
            return TSPOutput.parse_raw(cached_result)

        # Solve if not in cache
        result = TSPSolver.solve(data)

        # Cache the result
        await cache.set(cache_key, result.json())

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in solving TSP: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/knapsack/solve", response_model=KnapsackOutput)
async def solve_knapsack(data: KnapsackInput, cache: CacheService = Depends(get_cache)):
    """Solve the Problem 2: Knapsack"""
    try:
        # Generate cache key
        cache_key = await cache.get_key("knapsack", data.dict())

        # Check cache
        cached_result = await cache.get(cache_key)
        if cached_result:
            return KnapsackOutput.parse_raw(cached_result)

        # Solve if not in cache
        result = KnapsackSolver.solve(data)

        # Cache the result
        await cache.set(cache_key, result.json())

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in solving Knapsack problem: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
