import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pydantic_ai import Agent,RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_graph import BaseNode, Graph, End

load_dotenv()
#defining llm
@dataclass
class State:
    domain: str
    steps : list[str] | None = None
    steps_mapped: dict[str, str] = field(default_factory=dict)
    final_output : str | None = None

azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], provider=azure_provider)
#defining agents
generic_agent = Agent(
    model=model,
    system_prompt="your task is extract the domain from the user query and initialize the domain variable" \
    "leave the other variable alone",
    output_type=State,
    output_retries=3,
    instrument=True
)

planner_agent = Agent(
    model=model,
    system_prompt="""your are an expert planner
    You already have the domain
    Do NOT include steps that are already completed
    you have to create steps to research it not more than three steps
    Output ONLY a list of steps like:
    ["identify domain", "generate topics", "summarize topics"]
    Do NOT include numbering or extra text""",
    output_type=list[str],
    output_retries=3,
    instrument=True
)

executor_agent = Agent(
    model=model,
    system_prompt="""Your job is to follow the instruction and produce the result.

Rules:
- You may use the search_web tool ONLY ONCE if needed
- Do NOT call the tool multiple times
- After getting tool result, produce final answer
- Be concise and complete""",
    output_type=str,
    output_retries=3,
    instrument=True
)

formatter_agent = Agent(
    model=model,
    system_prompt="you job is to use the data in the state and give it in a structured way",
    output_type=str,
    output_retries=3,
    instrument=True
)
#defining nodes
@dataclass
class PlannerNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> 'ExecutorNode':
        print("Planner node started")
        result = await planner_agent.run(f"steps to research the domain {self.state.domain}")
        
        self.state.steps = result.output

        print("Planner node ended")
        return ExecutorNode(state=self.state)

@dataclass
class ExecutorNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> 'FormatterNode':
        print("Executor node started")
        for i, step in enumerate(self.state.steps):
            print(f"Executing step {i}: {step}")
            work = await executor_agent.run(
            f"""
            Domain: {self.state.domain}
            Instruction: {step}

            Stay strictly within the domain.
            """
            )
            self.state.steps_mapped[i] = work.output
            print(f"Output: {work.output}\n")
        print("Executor node ended")
        return FormatterNode(state=self.state)
    
#duckduckgo search tool for executor
from ddgs import DDGS

search_tool = DDGS()

@executor_agent.tool
async def search_web(ctx:RunContext[None],query:str)-> str:
    print("searching...")
    search_results = search_tool.text(query, max_results=5)
    print("search ended")
    return str(search_results)

@dataclass
class FormatterNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> End[State]:
        print("Formatter node started")
        result = await formatter_agent.run(
    f"""
    Domain: {self.state.domain}

    Steps Results:
    {self.state.steps_mapped}

    Create a clean structured summary of this research.
    """
)
        self.state.final_output = result.output

        print("Formatter node ended")
        return End(self.state)
    

#defining graph
graph = Graph(nodes=[PlannerNode, ExecutorNode, FormatterNode])
