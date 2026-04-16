import asyncio
from agents import State, graph, TopicNode,generic_agent

async def main():

    user_query = input("user query : ")

    response = await generic_agent.run(user_query)

    response_domain = response.output

    print(f"Domain : {response_domain.domain}")
    state_instance = State(domain=response_domain)

    result = await graph.run(TopicNode(state=state_instance))

    print("\n--- Final Topics and Summaries ---")

    for topic, summary in result.output.topics.items():
        print(f"Topic: {topic}\nSummary: {summary}\n")


if __name__ == "__main__":
    asyncio.run(main())
