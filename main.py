import asyncio
from agents import planner_agent, executor_agent, critic_agent


async def main():

    user_query = input("enter your query: ")

    planner_response = await planner_agent.run(user_query)

    print(f"planner response: {planner_response.output}")

    # CHANGED: Added retry loop with critic feedback
    max_retries = 3
    retry_count = 0
    executor_response = None

    while retry_count < max_retries:
        executor_response = await executor_agent.run(planner_response.output)
        print(
            f"executor response (attempt {retry_count + 1}): {executor_response.output}"
        )

        critic_response = await critic_agent.run(
            # CHANGED: Pass structured context instead of f-string
            f"User query: {user_query}\nExecutor response: {executor_response.output}"
        )

        # CHANGED: Access .output attribute to get CriticOutput model
        critic_output = critic_response.output
        print(
            f"critic agent -> pass_through: {critic_output.pass_through}, reason: {critic_output.reason}"
        )

        # CHANGED: If critic approves, exit loop; otherwise retry
        if critic_output.pass_through:
            print("✓ Critic approved response")
            break
        else:
            retry_count += 1
            if retry_count < max_retries:
                print(f"✗ Retrying (attempt {retry_count + 1}/{max_retries})...")
            else:
                print(f"✗ Max retries ({max_retries}) reached")

    print(f"\nFinal response:\n{executor_response.output}")


if __name__ == "__main__":
    asyncio.run(main())
