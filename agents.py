import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_graph import BaseNode, Graph, End

load_dotenv()

@dataclass
class State:
    domain: str
    topics: dict[str, str] = field(default_factory=dict)

azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], provider=azure_provider)

topic_agent = Agent(
    model=model,
    system_prompt="your job is to create a list of topics of the domain limit to 2",
    output_type=list[str],
    output_retries=3
)

summarizer_agent = Agent(
    model=model,
    system_prompt="you job is to summarize the topic given",
    output_type=str,
    output_retries=3
)

@dataclass
class TopicNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> 'SummarizerNode':
        print("Topic node started")
        result = await topic_agent.run(f"topics for the domain {self.state.domain}")
        for t in result.output:
            self.state.topics[t] = ""

        print("Topic node ended")
        return SummarizerNode(state=self.state)

@dataclass
class SummarizerNode(BaseNode[State]):
    state: State

    async def run(self, ctx) -> End[State]:
        print("Summarizer node started")
        for topic in self.state.topics:
            summary = await summarizer_agent.run(f"summarize {topic} in under 20 words")
            self.state.topics[topic] = summary.output

        print("Summarizer node ended")
        return End(self.state)

graph = Graph(nodes=[TopicNode, SummarizerNode])
