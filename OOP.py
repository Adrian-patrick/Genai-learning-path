"""
Encapsulation
Classes
Data (state)
Behavior (methods)
Industry example
"""
class LLMClient:
    def __init__(self, model_name: str, temperature: float) -> None:
        self.model_name = model_name
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        # call model here
        return "response"
    
"""
Abstraction
hiding complexity
"""
from abc import ABC, abstractmethod

class BaseLLMClient(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

"""
Inheritance
reusing classes
shared base behaivour
example llm client
"""
class OpenAIClient(BaseLLMClient):
    def generate(self, prompt: str):
        return "OpenAI response"

class AnthropicClient(BaseLLMClient):
    def generate(self, prompt: str):
        return "Anthropic response"
    
"""
Polymorphism
same interface, different behavior
"""
def generate_answer(client: BaseLLMClient, prompt: str):
    return client.generate(prompt)