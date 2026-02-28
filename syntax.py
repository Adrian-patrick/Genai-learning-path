"""
Variable naming
Use descriptive variable names
"""
max_token_length = 10
model_temperature = 0.7

"""
structure of the code
avoid nested loops
"""
condition = True
if condition:
    return
if not condition:
    return

"""
Imports
group imports together
one import per line
blank line between groups of imports
"""
import os
import logging

from fastapi import FastAPI
from pydantic import BaseModel
    
"""
type hints
specifying type of variables in the parameters
and return types of functions
"""
def calculate_total_tokens(user_tokens: int, model_tokens: int) -> int:
    return user_tokens + model_tokens

"""
docstrings/comment
explaining clearly what a function does and code
"""
def validate_prompt(prompt: str) -> bool:
    """
    Validates that the user prompt is not empty and not too long.
    
    Args:
        prompt (str): The input prompt from user.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    return bool(prompt and len(prompt) < 5000)

"""
example of clean code
"""
def validate_model_config(model_name: str, temperature:float , max_tokens: int) -> bool:
    """
    Validates the models configuration
    
    Args: 
    
    model_name (str) : The name of the model to vaildate
    temperature (float) : The temperature value to validate
    max_tokens (int) : The max tokens value to validate
    
    returns:
    
    bool : True if the model configuration is valid else False
    """
    valid_models = ["model_1", "model_n"]
    if model_name not in valid_models:
        raise ValueError(f"Invalid model name: {model_name}. Valid options are: {valid_models}")
    if not (temperature >= 0 and temperature <= 1):
        raise ValueError(f"Temperature must be between 0 and 1. Provided value: {temperature}")
    if max_tokens <= 0:
        raise ValueError(f"Max tokens must be a positive integer. Provided value: {max_tokens}")
    return True


