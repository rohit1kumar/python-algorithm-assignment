# Python Algorithm Assignment

## Tech Stack

- FastAPI
- Redis
- Docker

## Setup and Run

1. Clone the repository & move to the dir:
   ```bash
   git clone https://github.com/rohit1kumar/python-algorithm-assignment.git
   cd python-algorithm-assignment
   ```
2. Use docker to run the application
   ```bash
   docker-compose up --build
   ```
3. Access the application at http://localhost:8000

4. API Docs are available at http://localhost:8000/docs

## Unit Tests

To run the unit tests, use the following command:

```bash
pytest -v # make sure you have pytest installed
```

## TODO's completed

- [x] Implement the API using FastAPI
- [x] Implement the Unit Tests using pytest
- [x] Implement the Docker Compose
- [x] Implement the Cache using Redis

## API endpoints

`POST /tsp/solve`

body:

```json
{
	"cities": ["A", "B", "C", "D"],
	"distances": {
		"A": {
			"B": 10,
			"C": 15,
			"D": 20
		},
		"B": {
			"A": 10,
			"C": 35,
			"D": 25
		},
		"C": {
			"A": 15,
			"B": 35,
			"D": 30
		},
		"D": {
			"A": 20,
			"B": 25,
			"C": 30
		}
	}
}
```

`POST /knapsack/solve`

body:

```json
{
	"max_weight": 60,
	"items": [
		{
			"name": "Laptop",
			"weight": 10,
			"value": 60
		},
		{
			"name": "Phone",
			"weight": 20,
			"value": 100
		},
		{
			"name": "Tablet",
			"weight": 30,
			"value": 120
		}
	]
}
```
