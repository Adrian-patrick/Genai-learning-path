from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from models import ResponseModel
from dotenv import load_dotenv

load_dotenv()
import os

azure_provider = AzureProvider(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

model = OpenAIChatModel(
    os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], provider=azure_provider
)

system_prompt = """
your an email intent classification agent
your job is to understand the email using the text given to you and classify it
you will classify it in 4 categories spam,important,promotion,general
you will aslo give a short reason on how you classified it and why
"""
agent = Agent(
    model, system_prompt=system_prompt, output_retries=3, output_type=ResponseModel
)
