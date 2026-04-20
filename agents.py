from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_graph import BaseNode, End,Graph
from dataclasses import dataclass, field
from dotenv import load_dotenv
load_dotenv()
import asyncio
import os
from typing import Callable

from ddgs import DDGS

azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], provider=azure_provider)


@dataclass
class State:
    query: str
    steps: list[str] = field(default_factory=list)
    steps_mapped: dict[str, str] = field(default_factory=dict)
    final_output: str = ""
    # Changed: callback used by main/frontend to track exactly which graph step is running.
    progress_hook: Callable[[str], None] | None = None

planner_agent = Agent(
    model,
    system_prompt="""
you are trip planner agent
Decompose queries into exactly 3 actionable steps the worker can answer immediately using general knowledge.

example for "plan a trip to paris for 5 days":
1. Summarize top 5 Paris attractions and best time to visit
2. List 3 hotel recommendations by budget category
3. Outline a sample 5-day itinerary with daily highlights

Rules:
- Always 3 steps exactly
- Make steps direct and answerable from general knowledge
- Avoid meta-steps like "research", "gather", "verify"
- Each step should produce concrete content in one LLM call
- Return only the 3 step strings, no numbering prefix
"""
,
    output_type=list[str],
    output_retries=2
)

worker_agent = Agent(
    model,
    system_prompt="""
you are a travel assistant worker agent
You receive specific travel planning tasks and provide direct, practical answers.

rules:
- Do NOT ask for clarification - make reasonable assumptions and provide content
- Use the provided current_info only when it is included in the prompt
- For current prices, availability, opening hours, weather, or live events, rely on current_info and mention that it was checked recently
- For evergreen travel advice, answer from general knowledge
- Format: bullet points for attractions/hotels, narrative for itineraries
- Keep response under 400 words
- Be specific with recommendations (names, prices ranges, time blocks)
""",
    output_type=str,
    output_retries=1
)


async def fetch_current_info(query: str, max_results: int = 3, timeout_secs: float = 12.0) -> str:
    """Run a short web search for fresh facts like prices or opening hours."""
    safe_max_results = max(1, min(max_results, 5))
    clean_query = query.replace("\x00", " ").strip()
    if not clean_query:
        return ""

    def do_search() -> str:
        try:
            results = list(DDGS().text(clean_query, max_results=safe_max_results))
        except Exception as exc:
            return f"Web search unavailable: {type(exc).__name__}: {str(exc)[:100]}"

        if not results:
            return "No search results found."

        lines = []
        for idx, item in enumerate(results, start=1):
            title = item.get("title", "")
            url = item.get("href", "")
            snippet = item.get("body", "")
            lines.append(f"{idx}. {title}\nURL: {url}\nSnippet: {snippet}")

        return "\n\n".join(lines)

    try:
        return await asyncio.wait_for(asyncio.to_thread(do_search), timeout=timeout_secs)
    except Exception as exc:
        return f"Web search unavailable: {type(exc).__name__}: {str(exc)[:100]}"


def needs_web_search(step: str) -> bool:
    """Heuristic for freshness-sensitive steps that should use web search."""
    keywords = (
        "price",
        "prices",
        "cost",
        "current",
        "latest",
        "updated",
        "today",
        "now",
        "availability",
        "available",
        "opening hours",
        "open now",
        "season",
        "weather",
        "festival",
        "fares",
        "rates",
        "booking",
        "ticket",
    )
    lowered = step.lower()
    return any(keyword in lowered for keyword in keywords)


async def run_agent_with_timeout(agent, prompt: str, timeout_secs: float = 30.0) -> str:
    """Run agent with timeout to prevent hangs."""
    try:
        result = await asyncio.wait_for(agent.run(prompt), timeout=timeout_secs)
        return result.output
    except asyncio.TimeoutError:
        return f"[TIMEOUT after {timeout_secs}s]"
    except Exception as e:
        return f"[ERROR: {type(e).__name__}: {str(e)[:100]}]"

formatter_agent = Agent(
    model,
    system_prompt="""
you are formatter agent
you will be given the original query and the steps with their outputs and you have to format the final output in a presentable way
keep it concise and to the point, do not add unnecessary information
use the information from the steps and their outputs to format the final output, do not add any new information
""",
output_type=str,
output_retries=3
)

@dataclass
class PlannerNode(BaseNode[State]):
    state: State
    # Changed: BaseNode.run must be defined as (self, ctx); earlier order caused ctx/self mix-up and NoneType errors.
    async def run(self, _ctx)-> 'WorkerNode':
        if self.state.progress_hook:
            self.state.progress_hook("planner: started")
        print(f"PlannerNode received query: {self.state.query}")
        # Changed: use Agent.run() and .output because pydantic-ai returns an AgentRunResult.
        steps_result = await planner_agent.run(self.state.query)
        self.state.steps = steps_result.output
        if self.state.progress_hook:
            self.state.progress_hook("planner: completed")
        print(f"PlannerNode generated steps: {self.state.steps}")

        return WorkerNode(state=self.state)
    
@dataclass
class WorkerNode(BaseNode[State]):
    state: State
    # Changed: keep (self, ctx) signature so pydantic-graph can call node.run(ctx) correctly.
    async def run(self, _ctx)-> 'FormatterNode':
        if self.state.progress_hook:
            self.state.progress_hook("worker: started")
        print(f"WorkerNode received steps: {self.state.steps}")

        # Changed: run worker tasks in parallel with timeout protection to prevent hangs.
        async def run_one_step(step: str) -> tuple[str, str]:
            if self.state.progress_hook:
                self.state.progress_hook(f"worker: running step -> {step}")
            current_info = ""
            if needs_web_search(step):
                current_info = await fetch_current_info(step)
            prompt = step if not current_info else f"Step: {step}\n\nCurrent info:\n{current_info}"
            # Use timeout wrapper (60s) to allow LLM inference time
            output_result = await run_agent_with_timeout(worker_agent, prompt, timeout_secs=60.0)
            if self.state.progress_hook:
                self.state.progress_hook(f"worker: completed step -> {step}")
            return step, output_result

        step_results = await asyncio.gather(*(run_one_step(step) for step in self.state.steps))

        # Changed: rebuild mapping from parallel results while preserving step-to-output association.
        self.state.steps_mapped = {step: output for step, output in step_results}
        if self.state.progress_hook:
            self.state.progress_hook("worker: completed")
        print(f"WorkerNode executed steps with outputs: {self.state.steps_mapped}")
        return FormatterNode(state=self.state)

@dataclass
class FormatterNode(BaseNode[State]):
    state: State
    # Changed: same signature fix for terminal node.
    async def run(self, _ctx)-> End[str]:
        if self.state.progress_hook:
            self.state.progress_hook("formatter: started")
        print(f"FormatterNode received steps and outputs: {self.state.steps_mapped}")
        # Changed: pass a string prompt and read .output to avoid passing unsupported tuple input.
        final_output_result = await formatter_agent.run(
            f"Original query: {self.state.query}\nSteps and outputs: {self.state.steps_mapped}"
        )
        self.state.final_output = final_output_result.output
        if self.state.progress_hook:
            self.state.progress_hook("formatter: completed")
        print(f"FormatterNode generated final output: {self.state.final_output}")
        # Changed: End payload must be the final answer string because main reads GraphRunResult.output.
        return End(self.state.final_output)

graph = Graph(nodes = [PlannerNode, WorkerNode, FormatterNode])

