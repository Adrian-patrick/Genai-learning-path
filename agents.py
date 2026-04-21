from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_graph import BaseNode, End, Graph
from dataclasses import dataclass, field
from dotenv import load_dotenv
from database import connection
from models import CriticOutput
import asyncio

load_dotenv()
import asyncio
import os
from typing import Callable

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
    """
    print("accessed tool")
    try:
        cur = connection.cursor()
        cur.execute(query=query)
        output = cur.fetchall()
    except:
        print("incorrect syntax")
        return "incorrect syntax"
    print("correct syntax")
    return output


critic_agent = Agent(
    model=model,
    system_prompt="You are a helpful critic"
    "your job is to critique the response from the executor and provide feedback to the planner",
    output_type=CriticOutput,
    output_retries=2,
)
