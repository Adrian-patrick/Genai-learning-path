# Agentic Database Query System

## Overview
A multi-agent system using pydantic-ai for intelligent database query planning and execution with feedback loops.

## Architecture

### Agents
1. **Planner Agent**: Breaks down user queries into 3-5 actionable steps
2. **Executor Agent**: Executes steps using database tools with proper error handling
3. **Critic Agent**: Validates executor responses and triggers retries if needed

## Key Improvements

### Security & Error Handling
- **CHANGED**: Bare exception handling replaced with specific exceptions
- **CHANGED**: SELECT-only query validation to prevent accidental modifications
- **CHANGED**: Structured error messages with logging instead of silent failures

### Database Management
- **CHANGED**: Removed persistent global connection; now uses context manager for automatic cleanup
- **CHANGED**: Disabled SQL query echo logging (security/performance)
- **CHANGED**: Added `get_db_connection()` context manager for resource safety

### Retry Mechanism
- **CHANGED**: Implemented actual retry loop (max 3 attempts)
- **CHANGED**: Critic feedback now triggers automatic retries with counter display
- **CHANGED**: Better feedback format with attempt tracking

### Code Quality
- **CHANGED**: Removed duplicate asyncio import
- **CHANGED**: Added structured logging for debugging
- **CHANGED**: Improved docstrings and error messages
- **CHANGED**: Added Field descriptions to CriticOutput model

## How It Works

1. User submits query
2. Planner decomposes into steps
3. Executor runs steps and uses database tool
4. Critic evaluates response
5. If approved: return result
6. If not approved: retry (max 3 times)

## Tested On

- **QUERY**: What did bob purchase and for how much?
- **QUERY**: who has bought mouse and monitor and for how much?
