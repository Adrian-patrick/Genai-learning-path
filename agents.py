from pydantic_ai import Agent,RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from dataclasses import dataclass
import os 
from dotenv import load_dotenv
load_dotenv()

#setting up model(azure)
azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], provider=azure_provider)


#defining agent
from models import Domain
system_prompt = """
You are an expert in topics and summary making
Your task is to use the user query get the domain of the user which you will use to create a list of topics and summary of the domain specified
if the user is found update the source = "TOOL"
if the user is not found fill domain = "NOT FOUND",make source = "LLM" and make rest of the values null
Make sure the topics are as diverse as possible
You should also rate the importance on a scale of 1 to 10 depeneding on how important the topic is in the domain be very critical
for the importance the lower end towards 1 means that the topic is not important in the domian and towards the higher end towards ten means that the topic is very important
DONT always rate highly
Your output must be structured and parseable
RETURN only in the structured format no extra text
"""

agent = Agent(
    model=model,
    system_prompt=system_prompt,
    output_type=Domain,
    output_retries=3
)

#state,tools and dependency  for the agent

#database
@dataclass
class My_db():
    db : dict

#user domain
@agent.tool
def get_domain(ctx:RunContext[My_db],user:str) -> str:
    """ use this tool to get the domain of the user"""
    db_dict = ctx.deps.db
    try:
        user_domain = db_dict[user]
    except Exception:
        return "user not found so return NOT FOUND and follow instructions"
    return user_domain

