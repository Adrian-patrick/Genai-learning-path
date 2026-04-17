import asyncio
from test.agents import State, graph, PlannerNode,generic_agent
import os
from dotenv import load_dotenv
load_dotenv()

from langfuse import get_client
 
langfuse = get_client()

from pydantic_ai.agent import Agent

# Initialize Pydantic AI instrumentation
Agent.instrument_all()

async def main():

    #user_query = input("user query : ")

    user_query = "research about Artificial Intelligence"
    print(f"user query : {user_query}")
    
    response = await generic_agent.run(user_query)

    response_domain = response.output

    print(f"Domain : {response_domain.domain}")
    state_instance = State(domain=response_domain.domain)

    result = await graph.run(PlannerNode(state=state_instance))
    final_result = result.output.final_output
    # steps_dict = result.output.steps

    # for key in steps_dict:
    #     #print(f"step {key} : {steps_dict[key]}")
    #     print(key)

    print(f"Final output : {final_result}")


if __name__ == "__main__":
    asyncio.run(main())
