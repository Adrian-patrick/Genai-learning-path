from agents.agent import graph
from agents.agent_io import RequestModel, ResponseModel
from older.prompts import prompt
from langfuse.langchain import CallbackHandler
from langfuse import get_client

langfuse_handler = CallbackHandler()
langfuse = get_client()

system_prompt_v1 = langfuse.get_prompt("system_prompts",version=1)
system_prompt_v2 = langfuse.get_prompt("system_prompts",version=2)

system_prompt = system_prompt_v2.compile()

prompt_v1 = langfuse.get_prompt("test",version=1)
prompt_v2 = langfuse.get_prompt("test",version=2)
prompt_v3 = langfuse.get_prompt("test",version=3)
user_query = prompt_v1.compile()

def main():
    config = {'configurable': {'thread_id': '1'},
              'callbacks': [langfuse_handler]}
    
    

    print(f"system prompt : {system_prompt}")
    print(f"user query : {user_query}")

    while True:

        # user_query = input("user : ")
        # if user_query.lower() == "exit":
        #     print("Exiting...")
        #     break
        try : 
            request_model = RequestModel(query=user_query)
        except Exception as e:
            print(f"Error occurred while structuring user input: {e}")
            break
        state = graph.invoke({"messages": [("system",system_prompt),
                                           ("human",request_model.query)]},config=config)
        #debugging tools
        for msg in state.get('messages', []):
            print(f"Message type: {msg.__class__.__name__}")
            print(f"Content: {msg.content}")  # Add this to see content of every message
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"Tool calls: {msg.tool_calls}")
            if msg.__class__.__name__ == 'ToolMessage':
                print(f"Tool result: {msg.content}")
        

        # Final output section
        last_message = state['messages'][-1]

        try:
            # Convert the string content into your Pydantic object
            parsed_response = ResponseModel.model_validate_json(last_message.content)
            
            # Now you have full object access!
            print(f"\nagent (parsed): {parsed_response.response}\n")
            
        except Exception:
            # If the LLM didn't return JSON (e.g. an error), print raw
            print(f"\nagent (raw): {last_message.content}\n")
        break
        



if __name__ == "__main__":
    main()