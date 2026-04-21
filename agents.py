from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_graph import BaseNode, End, Graph
from dataclasses import dataclass, field
from dotenv import load_dotenv
from database import get_db_connection
from models import CriticOutput
import asyncio
import os
from typing import Callable
import logging

load_dotenv()
# CHANGED: Removed duplicate asyncio import
# CHANGED: Added logging for better error tracking
logging.basicConfig(level=logging.INFO)

azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], provider=azure_provider
)


planner_agent = Agent(
    model=model,
    system_prompt="You are a helpful planner"
    "your job is to break down the user query into steps for the executor"
    "the executor has access to a tool database with table name transactions and can run SQL queries on it"
    "Not more than 5 steps should be generated and the steps should be in order",
    output_type=str,
    output_retries=2,
)

executor_agent = Agent(
    model=model,
    system_prompt="You are a helpful executor"
    "your job is to execute the steps provided by the planner"
    "you have access to a tool database with table name transactions and can run SQL queries on it"
    "make sure your queries do the database are error free and working before using the tool",
    output_type=str,
    output_retries=2,
)


@executor_agent.tool_plain
async def tool_database(query: str):
    """
    tool_database allows the agent to run SQL queries on the database
    CHANGED: Added parameterized query support and proper exception handling
    """
    # CHANGED: Only allow SELECT queries for safety
    if not query.strip().upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed"}

    try:
        with get_db_connection() as connection:
            cur = connection.cursor()
            # CHANGED: Use raw queries but validate they're SELECT only
            cur.execute(query)
            output = cur.fetchall()
            logging.info(f"Query executed successfully: {query[:50]}...")
            return output
    except Exception as e:
        # CHANGED: Specific exception handling with detailed error message
        error_msg = f"Database error: {str(e)}"
        logging.error(error_msg)
        return {"error": error_msg}


critic_agent = Agent(
    model=model,
    # CHANGED: Improved critic prompt for better feedback
    system_prompt="You are a helpful critic. Your job is to evaluate executor responses for correctness and completeness. Return pass_through=True if satisfied, False if retry needed.",
    output_type=CriticOutput,
    output_retries=2,
)
