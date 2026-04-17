from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai import Agent
from pydantic_graph import BaseNode,End,Graph
from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

#defining azure model
azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], provider=azure_provider)

#defining required models
@dataclass
class State:
    domain :str
    steps : list[str] | None = None
    steps_mapped : dict[str,str] | None = None
    final_output : str | None = None



planner_prompt ="""
You are a planner
your job is to plan steps to research a given domain
create steps for the worker to research
"""

planner_agent = Agent(model,system_prompt=planner_prompt,output_type=list[str],output_retries=3)

worker_prompt ="""
You are a worker
your job is to follow the steps and stay on topic
"""

worker_agent = Agent(model,system_prompt=worker_prompt,output_type=str,output_retries=3)

Formatter_prompt ="""
You are a planner
your job is to plan steps to research a given domain
create steps for the worker to research
"""

Formatter_agent = Agent(model,system_prompt=Formatter_prompt,output_type=str,output_retries=3)

#defining node
@dataclass
class PlannerNode(BaseNode[State]):
    state:State

    async def run (self,ctx) -> 'ExecutorNode':
        print("Planner is starting..")
        prompt = """
the domain is Artificial Intelligence
your task is to make steps to research it not more than one """

        response = await planner_agent.run(prompt)

        self.state.steps = response.output
        print("Planner is ending..")
        return ExecutorNode(state=self.state)

@dataclass
class ExecutorNode(BaseNode[State]):
    state:State
    
    async def run(self,ctx) -> 'FormatterNode':

        self.state.steps_mapped = {}
    
        for i,steps in enumerate(self.state.steps):
            print(f"Executor is running step : {i}")
            prompt = f"""
your task is to follow the steps and do as it says {steps}"""
            
            response = await worker_agent.run(prompt)

            self.state.steps_mapped[i] = response.output
        
        print("Executor is done")
        return FormatterNode(state=self.state)

@dataclass
class FormatterNode(BaseNode[State]):
    state:State

    async def run (self,ctx) -> 'End[State]':
        print("Formatter is running")
        prompt = f"""
the domain is Artificial Intelligence
your task is to use the workers output {self.state.steps_mapped}
and produce a structured output for the user"""

        response = await Formatter_agent.run(prompt)

        self.state.final_output = response.output
        print("Formatter is done")
        return End(self.state)
    

graph = Graph(nodes=[PlannerNode,ExecutorNode,FormatterNode])