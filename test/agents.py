from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai import Agent
from pydantic_graph import BaseNode, End, Graph
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

# defining azure model
azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    provider=azure_provider
)

# defining required models
@dataclass
class State:
    domain: str
    steps: list[str] | None = None
    steps_mapped: dict[int, str] | None = None  # FIX: int key
    final_output: str | None = None

domain_identifier_prompt = """
You are a domain identifier
you sole job is to identify the domain that the user is talking about and only output the domain to research
"""  # FIX: single step

domain_identifier_agent = Agent(
    model,
    system_prompt=domain_identifier_prompt,
    output_type=str,
    output_retries=1  # FIX: reduced retries
)

planner_prompt = """
You are a planner.
Create EXACTLY ONE step to research the given domain.
Return ONLY a list like:
["step"]
"""  # FIX: single step

planner_agent = Agent(
    model,
    system_prompt=planner_prompt,
    output_type=list[str],
    output_retries=1  # FIX: reduced retries
)

worker_prompt = """
You are a worker.
Follow the instruction exactly.
Stay within the domain.
Give a concise answer.
"""  # FIX: stronger prompt

worker_agent = Agent(
    model,
    system_prompt=worker_prompt,
    output_type=str,
    output_retries=1  # FIX: reduced retries
)

Formatter_prompt = """
You are a formatter.
Use the worker outputs and generate a concise final summary.
"""  # FIX: correct role

Formatter_agent = Agent(
    model,
    system_prompt=Formatter_prompt,
    output_type=str,
    output_retries=1  # FIX
)


# defining node
@dataclass
class PlannerNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> 'ExecutorNode':
        print("Planner is starting..")

        prompt = f"""
the domain is {self.state.domain}
Create steps to research it and keep it short
each step must be short and there MUST be only a MAXIMUM of 5 steps
Return ONLY a list like:
["generate topics","identify key points of the topics","summarize the topics"]
"""  # FIX: used state +  format

        response = await planner_agent.run(prompt)

        self.state.steps = response.output
        print("Planner is ending..")

        return ExecutorNode(state=self.state)


@dataclass
class ExecutorNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> 'FormatterNode':

        if not self.state.steps:  # FIX: safety check
            raise ValueError("No steps generated")

        self.state.steps_mapped = {}

        for i, step in enumerate(self.state.steps):  # FIX: variable name
            print(f"Executor is running step : {i}")

            prompt = f"""you job is to perform the task and stay in the domain and also to be concise
            use the web search tool if required
Domain: {self.state.domain}
Instruction: {step}
"""  # FIX: include domain
            print(prompt)
            print(f"Calling worker for step {i}...")  # FIX: debug
            response = await worker_agent.run(prompt)
            print(f"Worker finished step {i}")  # FIX: debug

            self.state.steps_mapped[i] = response.output

        print("Executor is done")

        return FormatterNode(state=self.state)

#duckduckgo search tool for executor
from ddgs import DDGS

search_tool = DDGS()

@Formatter_agent.tool_plain
async def search_web(query:str)-> str:
    print("searching...")
    search_results = search_tool.text(query, max_results=5)
    print("search ended")
    return str(search_results)

@dataclass
class FormatterNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> End[State]:
        print("Formatter is running")

        prompt = f"""
Domain: {self.state.domain}

Worker outputs:
{self.state.steps_mapped}

Generate a concise summary.
"""  # FIX: better prompt

        response = await Formatter_agent.run(prompt)

        self.state.final_output = response.output

        print("Formatter is done")

        return End(self.state)


graph = Graph(nodes=[PlannerNode, ExecutorNode, FormatterNode])