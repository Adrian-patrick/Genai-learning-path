"""
*args : variable number of positional arguments
**kwargs : variable number of keyword arguments
"""
def example_function(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)
example_function(1, 2, 3, name="Alice", age=30)

"""
Real use case
"""
def call_model(prompt: str, **kwargs):
    temperature = kwargs.get("temperature", 0.7)
    max_tokens = kwargs.get("max_tokens", 500)

    return client.generate(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )

"""
used in wrappers
"""
def wrapper(*args, **kwargs):
    logger.info("Calling function")
    return original_function(*args, **kwargs)

"""
order rule
"""
def func(
    required_param,
    default_param=None,
    *args,
    **kwargs
):

"""
not to use when parameters are known and fixed
"""
def calculate(a: int, b: int) -> int:

"""
parameter override
"""
DEFAULT_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 500
}

def call_model(prompt: str, **kwargs):
    config = {**DEFAULT_CONFIG, **kwargs}
    return client.generate(prompt=prompt, **config)

