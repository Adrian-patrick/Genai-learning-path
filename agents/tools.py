from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

search = DuckDuckGoSearchResults()


@tool
def adder(a: int, b: int) -> int:
    """Always use this tool to add two numbers together."""
    return a + b

@tool
def subtractor(a: int, b: int) -> int:
    """Always use this tool to subtract the second number from the first."""
    return a - b    

@tool
def web_search(query:str) -> str:
    """Always use this tool to answer any questions that are not mathematical in nature."""
    search_results = search.invoke(query)
    return search_results

tools_list = [adder, subtractor, web_search]