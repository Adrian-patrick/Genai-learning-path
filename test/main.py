import asyncio
from agents import State, graph, PlannerNode,domain_identifier_agent #FIX: correct import


async def main():

    user_query = input("user : ") 

    result = await domain_identifier_agent.run(user_query)

    state_instance = State(domain=result.output)

    response = await graph.run(
        start_node=PlannerNode(state=state_instance)
    )

    print(f"\nFinal Output:\n{response.output.final_output}")


if __name__ == '__main__':
    asyncio.run(main())