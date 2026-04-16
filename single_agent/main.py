import asyncio
from agents import agent
from agents import My_db

async def main():

    my_db = My_db(db={"A":"Artifical Intelligence","B":"Machine learning"})

    user_query = "user is A"
    print(f"user : {user_query}")
    response = await agent.run(user_query,deps=my_db)
    domain_data = response.output

    print(f"=== DOMAIN ===")
    print(domain_data.domain)

    print(f"=== SOURCE ===")
    print(domain_data.source)

    print(f"=== OVERALL SUMMARY ===")
    print(domain_data.overall_summary)

    print(f"\n=== DETAILED TOPICS ({len(domain_data.topics)}) ===")
    for index, topic in enumerate(domain_data.topics, 1):
        print(f"\nTopic {index}: {topic.title}")
        print(f"Importance: {topic.importance}/10")
        print(f"Summary: {topic.summary}")

    



if __name__=="__main__":
    asyncio.run(main())