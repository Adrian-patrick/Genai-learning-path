import asyncio
from agents import planner_agent, executor_agent, critic_agent


async def main():

    user_query = input("enter your query: ")

    planner_response = await planner_agent.run(user_query)

    print(f"planner response: {planner_response.output}")

    executor_response = await executor_agent.run(planner_response.output)

    print(f"executor response: {executor_response.output}")

    critic_query = f"""
you are a critic agent your job is to return True or False depending on whether you are satified with the workers output
and also must provide reason if it is either.
Note: if you return false for the pass_through variable it will trigger a retry mechanism
user query : {user_query}
executor response : {executor_response.output}
"""
    critic_response = await critic_agent.run(executor_response.output)

    print(
        f"critic agent -> \npass_through: {critic_response.pass_through}\nreason: {critic_response.reason}"
    )


if __name__ == "__main__":
    asyncio.run(main())
