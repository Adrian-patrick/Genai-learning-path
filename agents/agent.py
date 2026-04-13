import os
from dotenv import load_dotenv
from langchain.messages import AIMessage
from agents.agent_io import ResponseModel
from langchain_openai import AzureChatOpenAI
from agents.tools import adder, subtractor,web_search
from langchain.agents import create_agent
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict,Annotated
from .tools import tools_list
from pydantic import BaseModel,Field
import operator
load_dotenv()

memory = MemorySaver()

class State(TypedDict):
    messages: Annotated[list,add_messages]
    plan: list[str]
    results: Annotated[list,operator.add]
    current_step: int


#model logic
llm = AzureChatOpenAI(
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"]    
)

#llm_with_tools = llm.bind_tools([adder, subtractor, web_search])

# agent = create_agent(
#     model=llm,
#     tools=[adder, subtractor, web_search],
#     system_prompt="""You are a helpful assistant. 
#     answer only in the specified response format.
#     output should always be valid JSON with no extra text.
#     you should use the tool calls for questions only if it allows you to provide a better answer.

#     examples:
#     User: add 2 and 3
#     calls: adder(a=2, b=3)
#     uses output of adder to answer question
#     Output: {"response": "5"}

#     User: who is elon musk
#     calls: web_search(query="who is elon musk")
#     uses output of web_search to answer question
#     Output: {"response": "Elon Musk is..."}

#     User: Hello, how are you?
#     no tool calls needed
#     Output: {"response": "Hello! I'm doing well, thank you for asking. How can I assist you today?"}
#     """,
#     response_format=ResponseModel
# )

#node building

#planner node
class Plan(BaseModel):
    steps : list[str] = Field(..., description="the steps the agent will take to answer the question")

def planner_node(state:State):
    
    planner_llm = llm.with_structured_output(Plan)
    user_query = state['messages'][-1].content

    result = planner_llm.invoke(f"Always first decide if the query is multi-step. If so, break this task into 3 research steps else it is a single step:{user_query}")

    return {"plan": result.steps,"current_step": 0}

def worker_node(state: State):
    idx = state['current_step']
    task = state['plan'][idx]
    
    # We use the search tool directly for simplicity in the worker
    # If you want the LLM to decide, you'd need a more complex sub-graph
    content = web_search.invoke({"query": task})
    
    return {
        "results": [f"Task {idx+1} result: {content}"], 
        "current_step": idx + 1
    }

def aggregator_node(state: State):
    # Combine results for the final answer
    context = "\n".join(state['results'])
    structured_llm = llm.with_structured_output(ResponseModel)
    
    final_answer = structured_llm.invoke(
    f"Summarize the following research into a CONCISE 3-paragraph report: {context}"
    )
    
    # Return as an AIMessage so main.py can parse it
    return {"messages": [AIMessage(content=final_answer.model_dump_json())]}

def should_continue(state: State):
    if state['current_step'] < len(state['plan']):
        return "worker"
    return "aggregator"

builder = StateGraph(State)

builder.add_node("planner", planner_node)
builder.add_node("worker", worker_node)
builder.add_node("aggregator", aggregator_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "worker")
# The Level 4 Loop
builder.add_conditional_edges(
    "worker",
    should_continue,
    {
        "worker": "worker",      # Loop back to worker
        "aggregator": "aggregator" # Move to final summary
    }
)

builder.add_edge("aggregator", END)

graph = builder.compile(checkpointer=memory)

