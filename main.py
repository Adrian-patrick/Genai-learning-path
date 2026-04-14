from agents import graph
from langfuse.langchain import CallbackHandler
from langfuse import get_client

langfuse = get_client()



langfuse_handler = CallbackHandler()

config = {"thread_id":"1","callbacks":[langfuse_handler]}

user_query = langfuse.get_prompt("multi-agent").compile()

def main():
    
    print(f"user : {user_query}")

    response = graph.invoke({"messages": [{"role": "user", "content": user_query}]},config=config)

    print(f"agent : {response["messages"][-1].content}")


if __name__ == "__main__":
    main()