import asyncio
from agents import State, graph, TopicNode

async def main():
    user_query = "Artificial Intelligence"
    state_instance = State(domain=user_query)


    result = await graph.run(TopicNode(state=state_instance))

    print("\n--- Final Topics and Summaries ---")

    for topic, summary in result.output.topics.items():
        print(f"Topic: {topic}\nSummary: {summary}\n")


if __name__ == "__main__":
    asyncio.run(main())
