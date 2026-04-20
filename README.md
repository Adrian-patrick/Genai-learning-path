# Trip Planner App

Minimal FastAPI app for generating travel plans with an agentic planner-worker-formatter flow.

## Agentic Flow

- Planner breaks a travel request into 3 simple steps.
- Worker answers each step and uses web search only when fresh info is needed.
- Formatter turns the step outputs into one clean response.

## Run

```bash
uv run uvicorn main:app --host 127.0.0.1 --port 8000
```

## Endpoints

- `/` - simple frontend
- `/query` - generate a travel plan
- `/history` - recent requests
- `/graph-status` - current graph step