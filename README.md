# Expense Tracker api

```
I will be coding a expense tracker api with proper coding principles:

1. Cohesion & SRP (Single Responsibility Principle)
Ask yourself: "Can I describe this class's purpose in one sentence without using 'and'?"

2. Encapsulation & Abstraction
Ask yourself: "If I change this internal implementation, will client code break?"

3. Loose Coupling & Modularity
Ask yourself: "Can I test this component without instantiating half my system?"

4. Reusability & Extensibility
Ask yourself: "Can I add new functionality without editing existing code?"

5. Portability
Ask yourself: "Will this work on Linux, Windows, and Mac?"

6. Defensibility
Ask yourself: "What's the worst that could happen with bad input?"

7. Maintainability & Testability
Ask yourself: "Can I write a unit test for this without mocking 5 things?"

8. Simplicity (KISS, DRY, YAGNI)
Ask yourself:
"Am I making this more complex than it needs to be?"
"Have I written this exact logic elsewhere?"
"Will I really need this feature?"
```

## Architecture

The project follows a simple layered design so each part has one job and stays easy to test.

Request flow:

`main.py` -> `api/expense_routes.py` -> `services/expense_service.py` -> `repositories/expense_repository.py` -> `models/expense.py` -> SQLite database

Layer responsibilities:

`main.py`
Starts the FastAPI app, creates tables, seeds dummy data, and includes the routes.

`api/expense_routes.py`
Handles HTTP requests, query parameters, path parameters, and response codes.

`services/expense_service.py`
Contains business rules and coordinates the repository calls.

`repositories/expense_repository.py`
Handles database queries and persistence only.

`models/expense.py`
Defines the SQLAlchemy ORM table and the shared expense category enums.

`schemas/expense_schema.py`
Defines request and response validation with Pydantic.

`database/database.py`
Creates the engine, session factory, base class, and database dependencies.

`utils/seed_data.py`
Adds dummy expenses on startup when the table is empty.

### Design Notes

The app is intentionally minimal and uses SQLite so it can run locally without extra setup.
Expense categories are stored as an enum to keep values consistent across the API, service, and database layers.
The `GET /expenses` endpoint supports category filtering, optional pagination, and an `All` option for returning every expense.