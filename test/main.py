import asyncio
from agents import State,graph,PlannerNode


async def main():

    user_query = "research AI domain"

    print(f"user : {user_query}")

    state_instance = State(domain=user_query)

    response = await graph.run(start_node=PlannerNode(state=state_instance))

    print(f"response {response.output.final_output}")




if __name__ == '__main__':
    asyncio.run(main())